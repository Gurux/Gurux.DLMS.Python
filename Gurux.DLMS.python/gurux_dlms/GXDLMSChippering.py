#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename: $HeadURL$
#
#  Version: $Revision$,
#                   $Date$
#                   $Author$
#
#  Copyright (c) Gurux Ltd
#
# ---------------------------------------------------------------------------
#
#   DESCRIPTION
#
#  This file is a part of Gurux Device Framework.
#
#  Gurux Device Framework is Open Source software; you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http://www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http://www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
from .enums.Security import Security
from .GXByteBuffer import GXByteBuffer
from .CountType import CountType
from .objects.enums.SecuritySuite import SecuritySuite
from .GXDLMSChipperingStream import GXDLMSChipperingStream
from .internal._GXCommon import _GXCommon
from .enums.Command import Command

#pylint: disable=too-many-instance-attributes,too-many-public-methods
class GXDLMSChippering:

    #
    #      * Get nonse from frame counter and system title.
    #      * @param invocationCounter Invocation counter.
    #      * @param systemTitle System title.
    #      * @return Generated nonse.
    #
    @classmethod
    def getNonse(cls, invocationCounter, systemTitle):
        nonce = bytearray(12)
        nonce[0:7] = systemTitle
        nonce[8] = ((invocationCounter >> 24) & 0xFF)
        nonce[9] = ((invocationCounter >> 16) & 0xFF)
        nonce[10] = ((invocationCounter >> 8) & 0xFF)
        nonce[11] = (invocationCounter & 0xFF)
        return nonce

    @classmethod
    def encryptAesGcm(cls, p, plainText):
        p.countTag = None
        data = GXByteBuffer()
        if p.type_ == CountType.PACKET:
            data.setUInt8(p.security)
        tmp = bytearray(4)
        invocationCounter = 0
        if p.securitySuite == SecuritySuite.AES_GCM_128:
            invocationCounter = p.invocationCounter
        tmp[0] = ((invocationCounter >> 24) & 0xFF)
        tmp[1] = ((invocationCounter >> 16) & 0xFF)
        tmp[2] = ((invocationCounter >> 8) & 0xFF)
        tmp[3] = (invocationCounter & 0xFF)
        aad = cls.getAuthenticatedData(p, plainText)
        iv = cls.getNonse(invocationCounter, p.systemTitle)
        gcm = GXDLMSChipperingStream(p.security, True, p.blockCipherKey, aad, iv, None)
        #  Encrypt the secret message
        if p.security != Security.AUTHENTICATION:
            gcm.write(plainText)
        ciphertext = gcm.flushFinalBlock()
        if p.security == Security.AUTHENTICATION:
            if p.type_ == CountType.PACKET:
                data.set(tmp)
            if (p.type_ & CountType.DATA) != 0:
                data.set(plainText)
            if (p.type_ & CountType.TAG) != 0:
                p.countTag = gcm.tag
                data.set(p.countTag)
        elif p.security == Security.ENCRYPTION:
            if p.type_ == CountType.PACKET:
                data.set(tmp)
            data.set(ciphertext)
        elif p.security == Security.AUTHENTICATION_ENCRYPTION:
            if p.type_ == CountType.PACKET:
                data.set(tmp)
            if (p.type_ & CountType.DATA) != 0:
                data.set(ciphertext)
            if (p.type_ & CountType.TAG) != 0:
                p.countTag = gcm.tag
                data.set(p.countTag)
        else:
            raise ValueError("security")
        if p.type_ == CountType.PACKET:
            tmp2 = GXByteBuffer(10 + len(data))
            tmp2.setUInt8(p.tag)
            if p.tag == Command.GENERAL_GLO_CIPHERING or p.tag == Command.GENERAL_DED_CIPHERING or p.tag == Command.DATA_NOTIFICATION:
                if not p.ignoreSystemTitle:
                    _GXCommon.setObjectCount(len(p.systemTitle), tmp2)
                    tmp2.set(p.systemTitle)
                else:
                    tmp2.SetUInt8(0)
            _GXCommon.setObjectCount(len(data), tmp2)
            tmp2.set(data, 0, len(data))
            data = tmp2
        crypted = data.array()
        return crypted

    @classmethod
    def getAuthenticatedData(cls, p, plainText):
        data = GXByteBuffer()
        sc = p.security | p.securitySuite
        if p.security == Security.AUTHENTICATION:
            data.setUInt8(sc)
            data.set(p.authenticationKey)
            data.set(plainText)
        elif p.security == Security.AUTHENTICATION_ENCRYPTION:
            data.setUInt8(sc)
            data.set(p.authenticationKey)
            if p.securitySuite != SecuritySuite.AES_GCM_128:
                #  transaction-id
                transactionId = GXByteBuffer()
                transactionId.setUInt64(p.invocationCounter)
                data.setUInt8(8)
                data.set(transactionId)
                #  originator-system-title
                _GXCommon.setObjectCount(len(p.systemTitle), data)
                data.set(p.systemTitle)
                #  recipient-system-title
                _GXCommon.setObjectCount(len(p.recipientSystemTitle), data)
                data.set(p.recipientSystemTitle)
                #  date-time not present
                data.setUInt8(0)
                #  other-information not present
                data.setUInt8(0)
        elif p.security == Security.ENCRYPTION:
            data.set(p.authenticationKey)
        return data.array()

    #
    #      * Decrypt data.
    #      *
    #      * @param c
    #      * Cipher settings.
    #      * @param p
    #      * GMAC Parameter.
    #      * @return Encrypted data.
    #
    @classmethod
    def decryptAesGcm(cls, p, data):
        # pylint: disable=too-many-locals
        if not data or len(data) - data.position < 2:
            raise ValueError("cryptedData")
        tmp = []
        len_ = 0
        cmd = data.getUInt8()
        if cmd in (Command.GENERAL_GLO_CIPHERING, Command.GENERAL_DED_CIPHERING):
            len_ = _GXCommon.getObjectCount(data)
            title = bytearray(len_)
            data.get(title)
            p.systemTitle = title
            if p.xml and p.xml.comments:
                p.xml.appendComment(_GXCommon.systemTitleToString(0, p.systemTitle))
        elif cmd in (Command.GENERAL_CIPHERING, Command.GLO_INITIATE_REQUEST, Command.GLO_INITIATE_RESPONSE, Command.GLO_READ_REQUEST, Command.GLO_READ_RESPONSE, \
            Command.GLO_WRITE_REQUEST, Command.GLO_WRITE_RESPONSE, Command.GLO_GET_REQUEST, Command.GLO_GET_RESPONSE, Command.GLO_SET_REQUEST, \
            Command.GLO_SET_RESPONSE, Command.GLO_METHOD_REQUEST, Command.GLO_METHOD_RESPONSE, Command.GLO_EVENT_NOTIFICATION,\
            Command.DED_GET_REQUEST, Command.DED_GET_RESPONSE, Command.DED_SET_REQUEST, Command.DED_SET_RESPONSE, Command.DED_METHOD_REQUEST,\
            Command.DED_METHOD_RESPONSE, Command.DED_EVENT_NOTIFICATION, Command.DED_READ_REQUEST, Command.DED_READ_RESPONSE, Command.DED_WRITE_REQUEST, \
            Command.DED_WRITE_RESPONSE, Command.GLO_CONFIRMED_SERVICE_ERROR, Command.DED_CONFIRMED_SERVICE_ERROR):
            pass
        else:
            raise ValueError("cryptedData")
        value = 0
        transactionId = 0
        if cmd == Command.GENERAL_CIPHERING:
            len_ = _GXCommon.getObjectCount(data)
            tmp = bytearray(len_)
            data.get(tmp)
            t = GXByteBuffer(tmp)
            transactionId = t.getInt64()
            len_ = _GXCommon.getObjectCount(data)
            tmp = bytearray(len_)
            data.get(tmp)
            p.setSystemTitle(tmp)
            len_ = _GXCommon.getObjectCount(data)
            tmp = bytearray(len_)
            data.get(tmp)
            p.setRecipientSystemTitle(tmp)
            #  Get date time.
            len_ = _GXCommon.getObjectCount(data)
            if len_ != 0:
                tmp = bytearray(len_)
                data.get(tmp)
                p.dateTime = tmp
            #  other-information
            len_ = data.getUInt8()
            if len_ != 0:
                tmp = bytearray(len_)
                data.get(tmp)
                p.otherInformation = tmp
            #  KeyInfo OPTIONAL
            len_ = data.getUInt8()
            #  AgreedKey CHOICE tag.
            data.getUInt8()
            #  key-parameters
            len_ = data.getUInt8()
            value = data.getUInt8()
            p.setKeyParameters(value)
            if value == 1:
                #  KeyAgreement.ONE_PASS_DIFFIE_HELLMAN
                #  key-ciphered-data
                len_ = _GXCommon.getObjectCount(data)
                tmp = bytearray(len_)
                data.get(tmp)
                p.keyCipheredData = tmp
            elif value == 2:
                #  KeyAgreement.STATIC_UNIFIED_MODEL
                len_ = _GXCommon.getObjectCount(data)
                if len_ != 0:
                    raise ValueError("Invalid key parameters")
            else:
                raise ValueError("key-parameters")
        len_ = _GXCommon.getObjectCount(data)
        p.cipheredContent = data.remaining()
        sc = data.getUInt8()
        security = sc & 0x30
        ss = sc & 0x3
        if ss != SecuritySuite.AES_GCM_128:
            raise ValueError("Decrypt failed. Invalid security suite.")
        p.security = security
        invocationCounter = data.getUInt32()
        p.invocationCounter = invocationCounter
        tag = bytearray(12)
        encryptedData = None
        if security == Security.AUTHENTICATION:
            len_ = len(data) - data.position() - 12
            encryptedData = bytearray(len_)
            data.get(encryptedData)
            data.get(tag)
            #  Check tag.
            cls.encryptAesGcm(p, encryptedData)
            if not GXDLMSChipperingStream.tagsEquals(tag, p.countTag):
                if transactionId != 0:
                    p.setInvocationCounter(transactionId)
                if not p.xml:
                    raise ValueError("Decrypt failed. Invalid tag.")
                p.xml.appendComment("Decrypt failed. Invalid tag.")
            return encryptedData
        ciphertext = None
        if security == Security.ENCRYPTION:
            len_ = len(data) - data.position
            ciphertext = bytearray(len_)
            data.get(ciphertext)
        elif security == Security.AUTHENTICATION_ENCRYPTION:
            len_ = len(data) - data.position - 12
            ciphertext = bytearray(len_)
            data.get(ciphertext)
            data.get(tag)
        aad = cls.getAuthenticatedData(p, ciphertext)
        iv = cls.getNonse(invocationCounter, p.systemTitle)
        gcm = GXDLMSChipperingStream(security, True, p.blockCipherKey, aad, iv, tag)
        gcm.write(ciphertext)
        if transactionId != 0:
            p.setInvocationCounter(transactionId)
        return gcm.flushFinalBlock()

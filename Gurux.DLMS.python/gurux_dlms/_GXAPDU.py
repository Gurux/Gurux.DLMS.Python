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
from __future__ import print_function
from .enums import BerType, PduType, Authentication, Command, AssociationResult, SourceDiagnostic, Service
from .ConfirmedServiceError import ConfirmedServiceError
from .GXDLMSConfirmedServiceError import GXDLMSConfirmedServiceError
from .internal._GXCommon import _GXCommon
from .GXByteBuffer import GXByteBuffer
from .GXDLMSException import GXDLMSException
from .TranslatorTags import TranslatorTags
from .TranslatorOutputType import TranslatorOutputType
from .TranslatorSimpleTags import TranslatorSimpleTags
from .TranslatorGeneralTags import TranslatorGeneralTags
from .ServiceError import ServiceError
from .TranslatorStandardTags import TranslatorStandardTags
from .enums.Security import Security
from .AesGcmParameter import AesGcmParameter
from .GXCiphering import GXCiphering

#
# The services to access the attributes and methods of COSEM objects are
# determined on DLMS/COSEM Application layer.  The services are carried by
# Application Protocol Data Units (APDUs).
# <p />
# In DLMS/COSEM the meter is primarily a server, and the controlling system
# is
# a client.  Also unsolicited (received without a request) messages are
# available.
# pylint: disable=too-many-public-methods
class _GXAPDU:
    #
    # Retrieves the string that indicates the level of authentication, if any.
    #
    @classmethod
    def getAuthenticationString(cls, settings, data, ignoreAcse):
        if settings.authentication != Authentication.NONE or \
            (not ignoreAcse and settings.cipher and settings.cipher.security != Security.NONE):
            #  Add sender ACSE-requirements field component.
            data.setUInt8(BerType.CONTEXT | PduType.SENDER_ACSE_REQUIREMENTS)
            data.setUInt8(2)
            data.setUInt8(BerType.BIT_STRING | BerType.OCTET_STRING)
            data.setUInt8(0x80)
            data.setUInt8(BerType.CONTEXT | PduType.MECHANISM_NAME)
            #  Len
            data.setUInt8(7)
            #  OBJECT IDENTIFIER
            p = [int(0x60), int(0x85), int(0x74), 0x05, 0x08, 0x02, settings.authentication]
            data.set(p)
        #  If authentication is used.
        if settings.authentication != Authentication.NONE:
            #  Add Calling authentication information.
            len_ = 0
            callingAuthenticationValue = None
            if settings.authentication == Authentication.LOW:
                if settings.password:
                    callingAuthenticationValue = settings.password
            else:
                callingAuthenticationValue = settings.ctoSChallenge
            #  0xAC
            data.setUInt8(BerType.CONTEXT | BerType.CONSTRUCTED | PduType.CALLING_AUTHENTICATION_VALUE)
            #  Len
            len_ = len(callingAuthenticationValue)
            data.setUInt8((2 + len_))
            #  Add authentication information.
            data.setUInt8(BerType.CONTEXT)
            #  Len.
            data.setUInt8(len_)
            if len_ != 0:
                data.set(callingAuthenticationValue)

    #
    # Code application context name.
    #
    # @param settings
    #            DLMS settings.
    # @param data
    #            Byte buffer where data is saved.
    # @param cipher
    #            Is ciphering settings.
    #
    @classmethod
    def generateApplicationContextName(cls, settings, data, cipher):
        #  ProtocolVersion
        if settings.protocolVersion:
            len_ = len(settings.protocolVersion)
            data.setUInt8(BerType.CONTEXT | PduType.PROTOCOL_VERSION)
            data.setUInt8(2)
            data.setUInt8(8 - len_)
            _GXCommon.setBitString(data, settings.protocolVersion, False)
        #  Application context name tag
        data.setUInt8((BerType.CONTEXT | BerType.CONSTRUCTED | PduType.APPLICATION_CONTEXT_NAME))
        #  Len
        data.setUInt8(0x09)
        data.setUInt8(BerType.OBJECT_IDENTIFIER)
        #  Len
        data.setUInt8(0x07)
        ciphered = cipher and cipher.isCiphered()
        data.setUInt8(0x60)
        data.setUInt8(0x85)
        data.setUInt8(0x74)
        data.setUInt8(0x5)
        data.setUInt8(0x8)
        data.setUInt8(0x1)
        if settings.getUseLogicalNameReferencing():
            if ciphered:
                data.setUInt8(3)
            else:
                data.setUInt8(1)
        else:
            if ciphered:
                data.setUInt8(4)
            else:
                data.setUInt8(2)

        #  Add system title.
        if not settings.isServer and (ciphered or settings.authentication == Authentication.HIGH_GMAC) or settings.authentication == Authentication.HIGH_ECDSA:
            if len(cipher.systemTitle) != 8:
                raise ValueError("SystemTitle")
            #  Add calling-AP-title
            data.setUInt8((BerType.CONTEXT | BerType.CONSTRUCTED | PduType.CALLING_AP_TITLE))
            #  LEN
            data.setUInt8(2 + len(cipher.systemTitle))
            data.setUInt8(BerType.OCTET_STRING)
            #  LEN
            data.setUInt8(len(cipher.systemTitle))
            data.set(cipher.systemTitle)
        #  Add CallingAEInvocationId.
        if not settings.isServer and settings.userId != -1:
            data.setUInt8(BerType.CONTEXT | BerType.CONSTRUCTED | PduType.CALLING_AE_INVOCATION_ID)
            #  LEN
            data.setUInt8(3)
            data.setUInt8(BerType.INTEGER)
            #  LEN
            data.setUInt8(1)
            data.setUInt8(settings.userId)

    # Reserved for internal use.
    @classmethod
    def getConformanceToArray(cls, data):
        ret = _GXCommon.swapBits(data.getUInt8())
        ret |= _GXCommon.swapBits(data.getUInt8()) << 8
        ret |= _GXCommon.swapBits(data.getUInt8()) << 16
        return ret

    # Reserved for internal use.
    @classmethod
    def setConformanceToArray(cls, value, data):
        data.setUInt8(_GXCommon.swapBits(int(value) & 0xFF))
        data.setUInt8(_GXCommon.swapBits((int(value) >> 8) & 0xFF))
        data.setUInt8(_GXCommon.swapBits((int(value) >> 16) & 0xFF))

    #
    # Generate User information initiate request.
    #
    # @param settings
    #            DLMS settings.
    # @param cipher
    # @param data
    #
    @classmethod
    def getInitiateRequest(cls, settings, data):
        #  Tag for xDLMS-Initiate request
        data.setUInt8(Command.INITIATE_REQUEST)
        #  Usage field for the response allowed component.
        #  Usage field for dedicated-key component.
        if not settings.cipher or settings.cipher.security == Security.NONE or not settings.cipher.dedicatedKey:
            #  Not used
            data.setUInt8(0x00)
        else:
            data.setUInt8(1)
            _GXCommon.setObjectCount(len(settings.cipher.dedicatedKey), data)
            data.set(settings.cipher.dedicatedKey)
        #  encoding of the response-allowed component (BOOLEAN DEFAULT TRUE)
        #  usage flag (FALSE, default value TRUE conveyed)
        data.setUInt8(0)
        #  Usage field of the proposed-quality-of-service component.  Not used
        if settings.qualityOfService == 0:
            data.setUInt8(0x00)
        else:
            data.setUInt8(0x01)
            data.setUInt8(settings.qualityOfService)

        data.setUInt8(settings.dlmsVersion)
        #  Tag for conformance block
        data.setUInt8(0x5F)
        data.setUInt8(0x1F)
        #  length of the conformance block
        data.setUInt8(0x04)
        #  encoding the number of unused bits in the bit string
        data.setUInt8(0x00)
        cls.setConformanceToArray(settings.proposedConformance, data)
        data.setUInt16(settings.maxPduSize)

    #
    # Generate user information.
    #
    # @param settings
    #            DLMS settings.
    # @param cipher
    # @param data
    #            Generated user information.
    #
    @classmethod
    def generateUserInformation(cls, settings, cipher, encryptedData, data):
        data.setUInt8(BerType.CONTEXT | BerType.CONSTRUCTED | PduType.USER_INFORMATION)
        if not cipher or not cipher.isCiphered():
            #  Length for AARQ user field
            data.setUInt8(0x10)
            #  Coding the choice for user-information (Octet STRING, universal)
            data.setUInt8(BerType.OCTET_STRING)
            #  Length
            data.setUInt8(0)
            offset = len(data)
            cls.getInitiateRequest(settings, data)
            data.setUInt8(len(data) - offset, offset - 1)
        else:
            if encryptedData:
                #  Length for AARQ user field
                data.setUInt8(int((4 + len(encryptedData))))
                #  Tag
                data.setUInt8(BerType.OCTET_STRING)
                data.setUInt8(int((2 + len(encryptedData))))
                #  Coding the choice for user-information (Octet STRING,
                #  universal)
                data.setUInt8(int(Command.GLO_INITIATE_REQUEST))
                data.setUInt8(len(encryptedData))
                data.set(encryptedData)
            else:
                tmp = GXByteBuffer()
                cls.getInitiateRequest(settings, tmp)
                p = AesGcmParameter(Command.GLO_INITIATE_REQUEST, cipher.systemTitle, cipher.blockCipherKey, cipher.authenticationKey)
                p.security = cipher.security
                p.invocationCounter = cipher.invocationCounter
                crypted = GXCiphering.encrypt(p, tmp.array())
                #  Length for AARQ user field
                data.setUInt8(2 + len(crypted))
                #  Coding the choice for user-information (Octet string,
                #  universal)
                data.setUInt8(BerType.OCTET_STRING)
                data.setUInt8(len(crypted))
                data.set(crypted)

    #
    # Generates Aarq.
    #
    @classmethod
    def generateAarq(cls, settings, cipher, encryptedData, data):
        #  AARQ APDU Tag
        data.setUInt8(BerType.APPLICATION | BerType.CONSTRUCTED)
        #  Length is updated later.
        offset = len(data)
        data.setUInt8(0)
        # /////////////////////////////////////////
        #  Add Application context name.
        cls.generateApplicationContextName(settings, data, cipher)
        cls.getAuthenticationString(settings, data, encryptedData)
        cls.generateUserInformation(settings, cipher, encryptedData, data)
        data.setUInt8((len(data) - offset - 1), offset)

    # pylint: disable=unused-variable
    @classmethod
    def getConformance(cls, value, xml):
        tmp = 1
        if xml.outputType == TranslatorOutputType.SIMPLE_XML:
            for it in range(0, 24):
                if (tmp & value) != 0:
                    xml.appendLine(TranslatorGeneralTags.CONFORMANCE_BIT, "Name", TranslatorSimpleTags.conformancetoString(tmp))
                tmp = tmp << 1
        else:
            for it in range(0, 24):
                if (tmp & value) != 0:
                    xml.append(TranslatorStandardTags.conformancetoString(tmp) + " ")
                tmp = tmp << 1

    #
    # Parse User Information from PDU.
    #
    @classmethod
    def parseUserInformation(cls, settings, cipher, data, xml):
        len_ = data.getUInt8()
        if len(data) - data.position < len_:
            if xml is None:
                raise ValueError("Not enough data.")
            xml.appendComment("Error: Invalid data size.")
        #  Encoding the choice for user information
        tag = data.getUInt8()
        if tag != 0x4:
            raise ValueError("Invalid tag.")
        len_ = data.getUInt8()
        if len(data) - data.position < len_:
            if not xml:
                raise ValueError("Not enough data.")
            xml.appendComment("Error: Invalid data size.")
        if xml and xml.outputType == TranslatorOutputType.STANDARD_XML:
            xml.appendLine(TranslatorGeneralTags.USER_INFORMATION, None, data.toHex(False, data.position, len_))
            data.position = data.position + len_
            return
        _GXAPDU.parseInitiate(False, settings, cipher, data, xml)

    # pylint: disable=too-many-arguments,too-many-locals,unused-argument
    @classmethod
    def parse(cls, initiateRequest, settings, cipher, data, xml, tag2):
        len_ = 0
        tmp2 = GXByteBuffer()
        tmp2.setUInt8(0)
        response = tag2 == Command.INITIATE_RESPONSE
        if response:
            if xml:
                #  <InitiateResponse>
                xml.appendStartTag(Command.INITIATE_RESPONSE)
            #  Optional usage field of the negotiated quality of service
            #  component
            tag = data.getUInt8()
            if tag != 0:
                len_ = data.getUInt8()
                data.position = data.position + len_
                if len_ == 0 and xml and xml.outputType == TranslatorOutputType.SIMPLE_XML:
                    #  NegotiatedQualityOfService
                    xml.appendLine(TranslatorGeneralTags.NEGOTIATED_QUALITY_OF_SERVICE, "Value", "00")
        elif tag2 == Command.INITIATE_REQUEST:
            if xml:
                xml.appendStartTag(Command.INITIATE_REQUEST)
            #  Optional usage field of the negotiated quality of service
            #  component
            tag = data.getUInt8()
            if tag != 0:
                len_ = data.getUInt8()
                tmp = bytearray(len_)
                data.get(tmp)
                if settings.cipher:
                    settings.cipher.setDedicatedKey(tmp)
                if xml:
                    xml.appendLine(TranslatorGeneralTags.DEDICATED_KEY, None, GXByteBuffer.hex(tmp, False))
            elif settings.cipher:
                settings.cipher.dedicatedKey = None
            #  Optional usage field of the negotiated quality of service
            #  component
            tag = data.getUInt8()
            if tag != 0:
                len_ = data.getUInt8()
                if xml and (initiateRequest or xml.outputType == TranslatorOutputType.SIMPLE_XML):
                    xml.appendLine(TranslatorGeneralTags.PROPOSED_QUALITY_OF_SERVICE, None, str(len_))
            else:
                if xml and xml.outputType == TranslatorOutputType.STANDARD_XML:
                    xml.appendLine(TranslatorTags.RESPONSE_ALLOWED, None, "true")
            #  Optional usage field of the proposed quality of service
            #  component
            tag = data.getUInt8()
            #  Skip if used.
            if tag != 0:
                len_ = data.getUInt8()
                data.position = data.position + len_
        elif tag2 == Command.CONFIRMED_SERVICE_ERROR:
            if xml:
                xml.appendStartTag(Command.CONFIRMED_SERVICE_ERROR)
                if xml.outputType == TranslatorOutputType.STANDARD_XML:
                    data.getUInt8()
                    xml.appendStartTag(TranslatorTags.INITIATE_ERROR)
                    type_ = ServiceError(data.getUInt8())
                    str_ = TranslatorStandardTags.serviceErrorToString(type_)
                    value = TranslatorStandardTags.getServiceErrorValue(type_, int(data.getUInt8()))
                    xml.appendLine("x:" + str_, None, value)
                    xml.appendEndTag(TranslatorTags.INITIATE_ERROR)
                else:
                    xml.appendLine(TranslatorTags.SERVICE, "Value", xml.integerToHex(data.getUInt8(), 2))
                    type_ = ServiceError(data.getUInt8())
                    xml.appendStartTag(TranslatorTags.SERVICE_ERROR)
                    xml.appendLine(TranslatorSimpleTags.serviceErrorToString(type_), "Value", TranslatorSimpleTags.getServiceErrorValue(type_, int(data.getUInt8())))
                    xml.appendEndTag(TranslatorTags.SERVICE_ERROR)
                xml.appendEndTag(Command.CONFIRMED_SERVICE_ERROR)
                return
            raise GXDLMSConfirmedServiceError(ConfirmedServiceError(data.getUInt8()), ServiceError(data.getUInt8()), data.getUInt8())
        else:
            if xml:
                xml.appendComment("Error: Failed to descypt data.")
                data.position = len(data)
                return
            raise ValueError("Invalid tag.")
        #  Get DLMS version number.
        if not response:
            settings.dlmsVersion = data.getUInt8()
            if settings.dlmsVersion != 6:
                if not settings.isServer:
                    raise ValueError("Invalid DLMS version number.")
            #  ProposedDlmsVersionNumber
            if xml and (initiateRequest or xml.outputType == TranslatorOutputType.SIMPLE_XML):
                xml.appendLine(TranslatorGeneralTags.PROPOSED_DLMS_VERSION_NUMBER, "Value", xml.integerToHex(settings.dlmsVersion, 2))
        else:
            if data.getUInt8() != 6:
                raise ValueError("Invalid DLMS version number.")
            if xml and (initiateRequest or xml.outputType == TranslatorOutputType.SIMPLE_XML):
                xml.appendLine(TranslatorGeneralTags.NEGOTIATED_DLMS_VERSION_NUMBER, "Value", xml.integerToHex(settings.dlmsVersion, 2))
        #  Tag for conformance block
        tag = data.getUInt8()
        if tag != 0x5F:
            raise ValueError("Invalid tag.")
        #  Old Way...
        if data.getUInt8(data.position) == 0x1F:
            data.getUInt8()
        len_ = data.getUInt8()
        #  The number of unused bits in the bit string.
        tag = data.getUInt8()
        v = cls.getConformanceToArray(data)
        if settings.isServer:
            settings.negotiatedConformance = v & settings.proposedConformance
            if xml:
                xml.appendStartTag(TranslatorGeneralTags.PROPOSED_CONFORMANCE)
                cls.getConformance(v, xml)
        else:
            if xml:
                xml.appendStartTag(TranslatorGeneralTags.NEGOTIATED_CONFORMANCE)
                cls.getConformance(v, xml)
            settings.negotiatedConformance = v
        if not response:
            #  Proposed max PDU size.
            pdu = data.getUInt16()
            settings.maxPduSize = pdu
            if xml:
                #  ProposedConformance closing
                if xml.outputType == TranslatorOutputType.SIMPLE_XML:
                    xml.appendEndTag(TranslatorGeneralTags.PROPOSED_CONFORMANCE)
                elif initiateRequest:
                    xml.append(TranslatorGeneralTags.PROPOSED_CONFORMANCE, False)
                #  ProposedMaxPduSize
                xml.appendLine(TranslatorGeneralTags.PROPOSED_MAX_PDU_SIZE, "Value", xml.integerToHex(pdu, 4))
            #  If client asks too high PDU.
            if pdu > settings.maxServerPDUSize:
                settings.setMaxPduSize = settings.maxServerPDUSize
        else:
            pdu = data.getUInt16()
            if xml is None and pdu < 64:
                raise GXDLMSConfirmedServiceError(ConfirmedServiceError.INITIATE_ERROR, ServiceError.SERVICE, Service.PDU_SIZE)
            #  Max PDU size.
            settings.maxPduSize = pdu
            if xml:
                #  NegotiatedConformance closing
                if xml.outputType == TranslatorOutputType.SIMPLE_XML:
                    xml.appendEndTag(TranslatorGeneralTags.NEGOTIATED_CONFORMANCE)
                elif initiateRequest:
                    xml.append(TranslatorGeneralTags.NEGOTIATED_CONFORMANCE, False)
                #  NegotiatedMaxPduSize
                xml.appendLine(TranslatorGeneralTags.NEGOTIATED_MAX_PDU_SIZE, "Value", xml.integerToHex(settings.maxPduSize, 4))
        if response:
            #  VAA Name
            tag = data.getUInt16()
            if xml:
                if initiateRequest or xml.outputType == TranslatorOutputType.SIMPLE_XML:
                    xml.appendLine(TranslatorGeneralTags.VAA_NAME, "Value", xml.integerToHex(tag, 4))
            if tag == 0x0007:
                if initiateRequest:
                    settings.setUseLogicalNameReferencing(True)
                else:
                    #  If LN
                    if not settings.getUseLogicalNameReferencing() and xml is None:
                        raise ValueError("Invalid VAA.")
            elif tag == 0xFA00:
                #  If SN
                if initiateRequest:
                    settings.setUseLogicalNameReferencing(False)
                else:
                    if settings.getUseLogicalNameReferencing():
                        raise ValueError("Invalid VAA.")
            else:
                #  Unknown VAA.
                raise ValueError("Invalid VAA.")
            if xml:
                #  <InitiateResponse>
                xml.appendEndTag(Command.INITIATE_RESPONSE)
        elif xml:
            xml.appendEndTag(Command.INITIATE_REQUEST)

    #pylint: disable=too-many-function-args, broad-except, too-many-arguments,
    #too-many-locals
    @classmethod
    def parseInitiate(cls, initiateRequest, settings, cipher, data, xml):
        #  Tag for xDLMS-Initate.response
        tag = data.getUInt8()
        originalPos = 0
        if tag in (Command.GLO_INITIATE_RESPONSE, Command.GLO_INITIATE_REQUEST,
                   Command.GENERAL_GLO_CIPHERING, Command.GENERAL_DED_CIPHERING):
            if xml:
                originalPos = data.position
                if tag in (Command.GENERAL_GLO_CIPHERING, Command.GENERAL_DED_CIPHERING):
                    cnt = _GXCommon.getObjectCount(data)
                    st = bytearray(cnt)
                    data.get(st)
                else:
                    st = settings.sourceSystemTitle
                cnt = _GXCommon.getObjectCount(data)
                encrypted = bytearray(cnt)
                data.get(encrypted)
                if cipher and xml.comments:
                    pos = xml.getXmlLength()
                    try:
                        data.position = originalPos - 1
                        p = AesGcmParameter(settings.sourceSystemTitle, settings.cipher.blockCipherKey, settings.cipher.authenticationKey)
                        p.xml = (xml)
                        tmp = GXCiphering.decrypt(settings.cipher, p, data)
                        data.clear()
                        data.set(tmp)
                        cipher.setSecurity(p.security)
                        tag1 = data.getUInt8()
                        xml.startComment("Decrypted data:")
                        xml.appendLine("Security: " + p.security)
                        xml.appendLine("Invocation Counter: " + p.invocationCounter)
                        cls.parse(initiateRequest, settings, cipher, data, xml, tag1)
                        xml.endComment()
                    except Exception:
                        #  It's OK if this fails.
                        xml.setXmlLength(pos)
                xml.appendLine(tag, None, GXByteBuffer.hex(encrypted, False))
                return
            data.position = data.position - 1
            p = AesGcmParameter(0, settings.sourceSystemTitle, settings.cipher.blockCipherKey, settings.cipher.authenticationKey)
            tmp = GXCiphering.decrypt(settings.cipher, p, data)
            data.size = 0
            data.set(tmp)
            cipher.security = p.security
            cipher.securitySuite = p.securitySuite
            tag = data.getUInt8()
        _GXAPDU.parse(initiateRequest, settings, cipher, data, xml, tag)

    #
    # Parse application context name.
    #
    # @param settings
    #            DLMS settings.
    # @param buff
    #            Received data.
    #
    #pylint: disable=too-many-boolean-expressions, too-many-return-statements
    @classmethod
    def parseApplicationContextName(cls, settings, buff, xml):
        #Get length.
        len_ = buff.getUInt8()
        if len(buff) - buff.position < len_:
            raise ValueError("Encoding failed. Not enough data.")
        if buff.getUInt8() != 0x6:
            raise ValueError("Encoding failed. Not an Object ID.")
        if settings.isServer and settings.cipher:
            settings.cipher.setSecurity(Security.NONE)
        #  Object ID length.
        len_ = buff.getUInt8()
        tmp = bytearray(len_)
        buff.get(tmp)
        if tmp[0] != 0x60 or tmp[1] != 0x85 or tmp[2] != 0x74 or tmp[3] != 0x5 or tmp[4] != 0x8 or tmp[5] != 0x1:
            if xml:
                xml.appendLine(TranslatorGeneralTags.APPLICATION_CONTEXT_NAME, "Value", "UNKNOWN")
                return True
            raise Exception("Encoding failed. Invalid Application context name.")
        name = tmp[6]
        if xml:
            if name == 1:
                if xml.outputType == TranslatorOutputType.SIMPLE_XML:
                    xml.appendLine(TranslatorGeneralTags.APPLICATION_CONTEXT_NAME, "Value", "LN")
                else:
                    xml.appendLine(TranslatorGeneralTags.APPLICATION_CONTEXT_NAME, None, "1")
                settings.setUseLogicalNameReferencing(True)
            elif name == 3:
                if xml.outputType == TranslatorOutputType.SIMPLE_XML:
                    xml.appendLine(TranslatorGeneralTags.APPLICATION_CONTEXT_NAME, "Value", "LN_WITH_CIPHERING")
                else:
                    xml.appendLine(TranslatorGeneralTags.APPLICATION_CONTEXT_NAME, None, "3")
                settings.setUseLogicalNameReferencing(True)
            elif name == 2:
                if xml.outputType == TranslatorOutputType.SIMPLE_XML:
                    xml.appendLine(TranslatorGeneralTags.APPLICATION_CONTEXT_NAME, "Value", "SN")
                else:
                    xml.appendLine(TranslatorGeneralTags.APPLICATION_CONTEXT_NAME, None, "2")
                settings.setUseLogicalNameReferencing(False)
            elif name == 4:
                if xml.outputType == TranslatorOutputType.SIMPLE_XML:
                    xml.appendLine(TranslatorGeneralTags.APPLICATION_CONTEXT_NAME, "Value", "SN_WITH_CIPHERING")
                else:
                    xml.appendLine(TranslatorGeneralTags.APPLICATION_CONTEXT_NAME, None, "4")
                settings.setUseLogicalNameReferencing(False)
            else:
                return False
            return True
        if settings.getUseLogicalNameReferencing():
            if name == 1:
                return True
            #  If ciphering is used.
            return name == 3
        if name == 2:
            return True
        #  If ciphering is used.
        return name == 4

    @classmethod
    def validateAare(cls, settings, buff):
        tag = buff.getUInt8()
        if settings.isServer:
            if tag != (BerType.APPLICATION | BerType.CONSTRUCTED | PduType.PROTOCOL_VERSION):
                raise ValueError("Invalid tag.")
        else:
            if tag != (BerType.APPLICATION | BerType.CONSTRUCTED | PduType.APPLICATION_CONTEXT_NAME):
                raise ValueError("Invalid tag.")

    #
    # Parse APDU.
    #
    @classmethod
    def parsePDU(cls, settings, cipher, buff, xml):
        #  Get AARE tag and length
        cls.validateAare(settings, buff)
        len_ = _GXCommon.getObjectCount(buff)
        size = len(buff) - buff.position
        if len_ > size:
            if xml is None:
                raise ValueError("Not enough data.")
            xml.appendComment("Error: Invalid data size.")
        #  Opening tags
        if xml:
            if settings.isServer:
                xml.appendStartTag(Command.AARQ)
            else:
                xml.appendStartTag(Command.AARE)
        ret = _GXAPDU.parsePDU2(settings, cipher, buff, xml)
        #  Closing tags
        if xml:
            if settings.isServer:
                xml.appendEndTag(Command.AARQ)
            else:
                xml.appendEndTag(Command.AARE)
        return ret

    @classmethod
    def parseProtocolVersion(cls, settings, buff, xml):
        #  Get count.
        buff.getUInt8()
        unusedBits = buff.getUInt8()
        value = buff.getUInt8()
        sb = _GXCommon.toBitString(value, 8 - unusedBits)
        settings.protocolVersion = sb
        if xml:
            xml.appendLine(TranslatorTags.PROTOCOL_VERSION, "Value", settings.protocolVersion)

    #
    # Parse APDU.
    #pylint: disable=broad-except
    @classmethod
    def parsePDU2(cls, settings, cipher, buff, xml):
        resultComponent = AssociationResult.ACCEPTED
        resultDiagnosticValue = SourceDiagnostic.NONE
        len_ = 0
        tag = 0
        while buff.position < len(buff):
            tag = buff.getUInt8()
            if tag == BerType.CONTEXT | BerType.CONSTRUCTED | PduType.APPLICATION_CONTEXT_NAME:
                if not cls.parseApplicationContextName(settings, buff, xml):
                    raise GXDLMSException(AssociationResult.PERMANENT_REJECTED, SourceDiagnostic.NOT_SUPPORTED)
            elif tag == BerType.CONTEXT | BerType.CONSTRUCTED | PduType.CALLED_AP_TITLE:
                #  0xA2
                #  Get length.
                if buff.getUInt8() != 3:
                    raise ValueError("Invalid tag.")
                if settings.isServer:
                    #  Choice for result (INTEGER, universal)
                    if buff.getUInt8() != BerType.OCTET_STRING:
                        raise ValueError("Invalid tag.")
                    len_ = buff.getUInt8()
                    tmp = bytearray(len_)
                    buff.get(tmp)
                    try:
                        settings.sourceSystemTitle = tmp
                    except Exception as ex:
                        if xml is None:
                            raise ex
                    if xml:
                        #  RespondingAPTitle
                        if xml.comments:
                            xml.appendComment(_GXCommon.systemTitleToString(settings.standard, settings.sourceSystemTitle))
                        xml.appendLine(TranslatorTags.CALLED_AP_TITLE, "Value", GXByteBuffer.hex(tmp, False))
                else:
                    #  Choice for result (INTEGER, universal)
                    if buff.getUInt8() != BerType.INTEGER:
                        raise ValueError("Invalid tag.")
                    #  Get length.
                    if buff.getUInt8() != 1:
                        raise ValueError("Invalid tag.")
                    resultComponent = buff.getUInt8()
                    if xml:
                        if resultComponent != AssociationResult.ACCEPTED:
                            xml.appendComment(resultComponent.__str__())
                        xml.appendLine(TranslatorGeneralTags.ASSOCIATION_RESULT, "Value", xml.integerToHex(resultComponent, 2))
                        xml.appendStartTag(TranslatorGeneralTags.RESULT_SOURCE_DIAGNOSTIC)
            elif tag == BerType.CONTEXT | BerType.CONSTRUCTED | PduType.CALLED_AE_QUALIFIER:
                #  0xA3
                resultDiagnosticValue = _GXAPDU.parseSourceDiagnostic(settings, buff, xml)
            elif tag == BerType.CONTEXT | BerType.CONSTRUCTED | PduType.CALLED_AP_INVOCATION_ID:
                #  0xA4
                _GXAPDU.parseResult(settings, buff, xml)
            elif tag == BerType.CONTEXT | BerType.CONSTRUCTED | PduType.CALLING_AP_TITLE:
                #  0xA6
                len_ = buff.getUInt8()
                tag = buff.getUInt8()
                len_ = buff.getUInt8()
                tmp = bytearray(len_)
                buff.get(tmp)
                try:
                    settings.setSourceSystemTitle(tmp)
                except Exception as ex:
                    if xml is None:
                        raise ex
                _GXAPDU.appendClientSystemTitleToXml(settings, xml)
            elif tag == BerType.CONTEXT | BerType.CONSTRUCTED | PduType.SENDER_ACSE_REQUIREMENTS:
                #  0xAA
                len_ = buff.getUInt8()
                tag = buff.getUInt8()
                len_ = buff.getUInt8()
                tmp = bytearray(len_)
                buff.get(tmp)
                settings.setStoCChallenge(tmp)
                _GXAPDU.appendServerSystemTitleToXml(settings, xml, tag)
            elif tag == BerType.CONTEXT | BerType.CONSTRUCTED | PduType.CALLING_AE_INVOCATION_ID:
                #  0xA9
                len_ = buff.getUInt8()
                tag = buff.getUInt8()
                len_ = buff.getUInt8()
                settings.userId = buff.getUInt8()
                if xml:
                    #  CallingAPTitle
                    xml.appendLine(TranslatorGeneralTags.CALLING_AE_INVOCATION_ID, "Value", xml.integerToHex(settings.userId, 2))
            elif tag == BerType.CONTEXT | BerType.CONSTRUCTED | PduType.CALLED_AE_INVOCATION_ID:
                #  0xA5
                len_ = buff.getUInt8()
                tag = buff.getUInt8()
                len_ = buff.getUInt8()
                settings.userId = buff.getUInt8()
                if xml:
                    #  CallingAPTitle
                    xml.appendLine(TranslatorGeneralTags.CALLED_AE_INVOCATION_ID, "Value", xml.integerToHex(settings.getUserId(), 2))
            elif tag == BerType.CONTEXT | BerType.CONSTRUCTED | 7:
                #  0xA7
                len_ = buff.getUInt8()
                tag = buff.getUInt8()
                len_ = buff.getUInt8()
                settings.userId = buff.getUInt8()
                if xml:
                    #  CallingAPTitle
                    xml.appendLine(TranslatorGeneralTags.RESPONDING_AE_INVOCATION_ID, "Value", xml.integerToHex(settings.userId, 2))
            elif tag == BerType.CONTEXT | BerType.CONSTRUCTED | PduType.CALLING_AP_INVOCATION_ID:
                #  0xA8
                if buff.getUInt8() != 3:
                    raise ValueError("Invalid tag.")
                if buff.getUInt8() != 2:
                    raise ValueError("Invalid length.")
                if buff.getUInt8() != 1:
                    raise ValueError("Invalid tag length.")
                #  Get value.
                len_ = buff.getUInt8()
                if xml:
                    #  CallingApInvocationId
                    xml.appendLine(TranslatorTags.CALLING_AP_INVOCATION_ID, "Value", xml.integerToHex(len_, 2))
            elif tag in (BerType.CONTEXT | PduType.SENDER_ACSE_REQUIREMENTS, BerType.CONTEXT | PduType.CALLING_AP_INVOCATION_ID):
                #  0x88
                #  Get sender ACSE-requirements field component.
                if buff.getUInt8() != 2:
                    raise ValueError("Invalid tag.")
                if buff.getUInt8() != BerType.OBJECT_DESCRIPTOR:
                    raise ValueError("Invalid tag.")
                #  Get only value because client application is
                #  sending system title with LOW authentication.
                buff.getUInt8()
                if xml:
                    xml.appendLine(tag, "Value", "1")
            elif tag in (BerType.CONTEXT | PduType.MECHANISM_NAME, BerType.CONTEXT | PduType.CALLING_AE_INVOCATION_ID):
                #  0x89
                _GXAPDU.updateAuthentication(settings, buff)
                if xml:
                    if xml.outputType == TranslatorOutputType.SIMPLE_XML:
                        str_ = Authentication.toString(settings.authentication)
                        xml.appendLine(tag, "Value", str_)
                    else:
                        xml.appendLine(tag, "Value", str(settings.authentication))
            elif tag == BerType.CONTEXT | BerType.CONSTRUCTED | PduType.CALLING_AUTHENTICATION_VALUE:
                #  0xAC
                _GXAPDU.updatePassword(settings, buff, xml)
            elif tag == BerType.CONTEXT | BerType.CONSTRUCTED | PduType.USER_INFORMATION:
                #  0xBE
                #  Check result component.  Some meters are returning invalid
                #  user-information if connection failed.
                if xml is None and resultComponent != AssociationResult.ACCEPTED and resultDiagnosticValue != SourceDiagnostic.NONE:
                    raise GXDLMSException(resultComponent, resultDiagnosticValue)
                try:
                    _GXAPDU.parseUserInformation(settings, cipher, buff, xml)
                except Exception:
                    if xml is None:
                        raise GXDLMSException(AssociationResult.PERMANENT_REJECTED, SourceDiagnostic.NO_REASON_GIVEN)
            elif tag == BerType.CONTEXT:
                #  0x80
                cls.parseProtocolVersion(settings, buff, xml)
            else:
                #  Unknown tags.
                print("Unknown tag: " + str(tag) + ".")
                if buff.position < len(buff):
                    len_ = buff.getUInt8()
                    buff.position = buff.position + len_
        #  All meters don't send user-information if connection is failed.
        #  For this reason result component is check again.
        if xml is None and resultComponent != AssociationResult.ACCEPTED and resultDiagnosticValue != SourceDiagnostic.NONE:
            raise GXDLMSException(resultComponent, resultDiagnosticValue)
        return resultDiagnosticValue

    @classmethod
    def parseResult(cls, settings, buff, xml):
        if settings.isServer:
            #  Get len.
            if buff.getUInt8() != 3:
                raise ValueError("Invalid tag.")
            #  Choice for result (Universal, Octetstring type)
            if buff.getUInt8() != BerType.INTEGER:
                raise ValueError("Invalid tag.")
            if buff.getUInt8() != 1:
                raise ValueError("Invalid tag length.")
            #  Get value.
            len_ = buff.getUInt8()
            if xml:
                #  RespondingAPTitle
                xml.appendLine(TranslatorTags.CALLED_AP_INVOCATION_ID, "Value", xml.integerToHex(len_, 2))
        else:
            #  Get length.
            if buff.getUInt8() != 0xA:
                raise ValueError("Invalid tag.")
            #  Choice for result (Universal, Octet string type)
            if buff.getUInt8() != BerType.OCTET_STRING:
                raise ValueError("Invalid tag.")
            #  responding-AP-title-field
            #  Get length.
            len_ = buff.getUInt8()
            tmp = bytearray(len_)
            buff.get(tmp)
            settings.setSourceSystemTitle(tmp)
            cls.appendResultToXml(settings, xml)

    @classmethod
    def parseSourceDiagnostic(cls, settings, buff, xml):
        tag = int()
        resultDiagnosticValue = SourceDiagnostic.NONE
        len_ = buff.getUInt8()
        #  ACSE service user tag.
        tag = buff.getUInt8()
        len_ = buff.getUInt8()
        if settings.isServer:
            calledAEQualifier = bytearray(len_)
            buff.get(calledAEQualifier)
            if xml:
                xml.appendLine(TranslatorTags.CALLED_AE_QUALIFIER, "Value", GXByteBuffer.hex(calledAEQualifier, False))
        else:
            #  Result source diagnostic component.
            tag = buff.getUInt8()
            if tag != BerType.INTEGER:
                raise ValueError("Invalid tag.")
            len_ = buff.getUInt8()
            if len_ != 1:
                raise ValueError("Invalid tag.")
            resultDiagnosticValue = buff.getUInt8()
            if xml:
                if resultDiagnosticValue != SourceDiagnostic.NONE:
                    xml.appendComment(resultDiagnosticValue.__str__())
                xml.appendLine(TranslatorGeneralTags.ACSE_SERVICE_USER, "Value", xml.integerToHex(resultDiagnosticValue, 2))
                xml.appendEndTag(TranslatorGeneralTags.RESULT_SOURCE_DIAGNOSTIC)
        return resultDiagnosticValue

    @classmethod
    def appendServerSystemTitleToXml(cls, settings, xml, tag):
        if xml:
            #  RespondingAuthentication
            if xml.outputType == TranslatorOutputType.SIMPLE_XML:
                xml.appendLine(tag, None, GXByteBuffer.hex(settings.getStoCChallenge(), False))
            else:
                xml.append(tag, True)
                xml.append(TranslatorGeneralTags.CHAR_STRING, True)
                xml.append(GXByteBuffer.hex(settings.getStoCChallenge(), False))
                xml.append(TranslatorGeneralTags.CHAR_STRING, False)
                xml.append(tag, False)
                xml.append("\n")

    @classmethod
    def appendClientSystemTitleToXml(cls, settings, xml):
        if xml:
            #  CallingAPTitle
            xml.appendLine(TranslatorGeneralTags.CALLING_AP_TITLE, "Value", GXByteBuffer.hex(settings.sourceSystemTitle, False))

    @classmethod
    def appendResultToXml(cls, settings, xml):
        if xml:
            #  RespondingAPTitle
            xml.appendLine(TranslatorGeneralTags.RESPONDING_AP_TITLE, "Value", GXByteBuffer.hex(settings.sourceSystemTitle, False))

    @classmethod
    def updatePassword(cls, settings, buff, xml):
        tmp = []
        len_ = buff.getUInt8()
        #  Get authentication information.
        if buff.getUInt8() != 0x80:
            raise ValueError("Invalid tag.")
        len_ = buff.getUInt8()
        tmp = bytearray(len_)
        buff.get(tmp)
        if settings.authentication == Authentication.LOW:
            settings.password = tmp
        else:
            settings.ctoSChallenge = tmp
        if xml:
            if xml.outputType == TranslatorOutputType.SIMPLE_XML:
                if GXByteBuffer.isAsciiString(tmp):
                    xml.appendComment(tmp.decode("utf-8"))
                xml.appendLine(TranslatorGeneralTags.CALLING_AUTHENTICATION, "Value", GXByteBuffer.hex(tmp, False))
            else:
                xml.appendStartTag(TranslatorGeneralTags.CALLING_AUTHENTICATION)
                xml.appendStartTag(TranslatorGeneralTags.CHAR_STRING)
                if settings.authentication == Authentication.LOW:
                    xml.append(GXByteBuffer.hex(settings.password, False))
                else:
                    xml.append(GXByteBuffer.hex(settings.ctoSChallenge, False))
                xml.appendEndTag(TranslatorGeneralTags.CHAR_STRING)
                xml.appendEndTag(TranslatorGeneralTags.CALLING_AUTHENTICATION)

    @classmethod
    def updateAuthentication(cls, settings, buff):
        ch = buff.getUInt8()
        if buff.getUInt8() != 0x60:
            raise ValueError("Invalid tag.")
        if buff.getUInt8() != 0x85:
            raise ValueError("Invalid tag.")
        if buff.getUInt8() != 0x74:
            raise ValueError("Invalid tag.")
        if buff.getUInt8() != 0x05:
            raise ValueError("Invalid tag.")
        if buff.getUInt8() != 0x08:
            raise ValueError("Invalid tag.")
        if buff.getUInt8() != 0x02:
            raise ValueError("Invalid tag.")
        ch = buff.getUInt8()
        if ch < 0 or ch > 7:
            raise ValueError("Invalid tag.")
        settings.authentication = ch

    #pylint: disable=too-many-function-args
    @classmethod
    def getUserInformation(cls, settings, cipher):
        data = GXByteBuffer()
        #  Tag for xDLMS-Initiate response
        data.setUInt8(Command.INITIATE_RESPONSE)
        #  Usage field for the response allowed component (not used)
        data.setUInt8(0x00)
        #  DLMS Version Number
        data.setUInt8(6)
        data.setUInt8(0x5F)
        data.setUInt8(0x1F)
        #  length of the conformance block
        data.setUInt8(0x04)
        #  encoding the number of unused bits in the bit string
        data.setUInt8(0x00)
        cls.setConformanceToArray(settings.negotiatedConformance, data)
        data.setUInt16(settings.maxPduSize)
        #  VAA Name VAA name (0x0007 for LN referencing and 0xFA00 for SN)
        if settings.getUseLogicalNameReferencing():
            data.setUInt16(0x0007)
        else:
            data.setUInt16(0xFA00)
        if cipher and cipher.isCiphered():
            p = AesGcmParameter(Command.GLO_INITIATE_RESPONSE, cipher.systemTitle, cipher.blockCipherKey, cipher.authenticationKey)
            p.security = cipher.security
            p.invocationCounter = cipher.invocationCounter
            return GXCiphering.encrypt(p, data.array())

        if settings.increaseInvocationCounterForGMacAuthentication:
            cipher.InvocationCounter += 1
        return data.array()

    #
    # Server generates AARE message.
    # pylint: disable=too-many-arguments
    @classmethod
    def generateAARE(cls, settings, data, result, diagnostic, cipher, errorData, encryptedData):
        offset = len(data)
        #  Set AARE tag and length 0x61
        data.setUInt8(BerType.APPLICATION | BerType.CONSTRUCTED | PduType.APPLICATION_CONTEXT_NAME)
        #  Length is updated later.
        data.setUInt8(0)
        cls.generateApplicationContextName(settings, data, cipher)
        #  Result 0xA2
        data.setUInt8(BerType.CONTEXT | BerType.CONSTRUCTED | BerType.INTEGER)
        data.setUInt8(3)
        #  len
        data.setUInt8(BerType.INTEGER)
        #  Tag
        #  Choice for result (INTEGER, universal)
        data.setUInt8(1)
        #  Len
        data.setUInt8(result)
        #  ResultValue
        #  SourceDiagnostic
        data.setUInt8(0xA3)
        data.setUInt8(5)
        #  len
        data.setUInt8(0xA1)
        #  Tag
        data.setUInt8(3)
        #  len
        data.setUInt8(2)
        #  Tag
        #  Choice for result (INTEGER, universal)
        data.setUInt8(1)
        #  Len
        #  diagnostic
        data.setUInt8(diagnostic)
        #  SystemTitle
        if cipher and (settings.authentication == Authentication.HIGH_GMAC or cipher.isCiphered()):
            data.setUInt8(BerType.CONTEXT | BerType.CONSTRUCTED | PduType.CALLED_AP_INVOCATION_ID)
            data.setUInt8((len(cipher.systemTitle)))
            data.setUInt8(BerType.OCTET_STRING)
            data.setUInt8()
            data.set(cipher.systemTitle)
        #  Add CalledAEInvocationId.
        if settings.userId != -1:
            data.setUInt8(BerType.CONTEXT | BerType.CONSTRUCTED | PduType.CALLED_AE_INVOCATION_ID)
            #  LEN
            data.setUInt8(3)
            data.setUInt8(BerType.INTEGER)
            #  LEN
            data.setUInt8(1)
            data.setUInt8(settings.userId)
        if settings.authentication > Authentication.LOW:
            #  Add server ACSE-requirenents field component.
            data.setUInt8(0x88)
            data.setUInt8(0x02)
            #  Len.
            data.setUInt16(0x0780)
            #  Add tag.
            data.setUInt8(0x89)
            data.setUInt8(0x07)
            #  Len
            data.setUInt8(0x60)
            data.setUInt8(0x85)
            data.setUInt8(0x74)
            data.setUInt8(0x05)
            data.setUInt8(0x08)
            data.setUInt8(0x02)
            data.setUInt8(settings.authentication)
            #  Add tag.
            data.setUInt8(0xAA)
            data.setUInt8((len(settings.stoCChallenge)))
            #  Len
            data.setUInt8(BerType.CONTEXT)
            data.setUInt8(len(settings.stoCChallenge))
            data.set(settings.stoCChallenge)
        if result == AssociationResult.ACCEPTED or not cipher or cipher.security == Security.NONE:
            #  Add User Information
            #  Tag 0xBE
            data.setUInt8(BerType.CONTEXT | BerType.CONSTRUCTED | PduType.USER_INFORMATION)
            if encryptedData:
                tmp2 = GXByteBuffer(2 + len(encryptedData))
                tmp2.setUInt8(Command.GLO_INITIATE_RESPONSE)
                _GXCommon.setObjectCount(len(encryptedData), tmp2)
                tmp2.set(encryptedData)
                tmp = tmp2.array()
            else:
                if errorData:
                    tmp = errorData
                else:
                    tmp = cls.getUserInformation(settings, cipher)
            data.setUInt8(2 + (len(tmp)))
            #  Coding the choice for user-information (Octet STRING, universal)
            data.setUInt8(BerType.OCTET_STRING)
            #  Length
            data.setUInt8(len(tmp))
            data.set(tmp)
        data.setUInt8((len(data) - offset - 2), (offset + 1))

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
from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from ..enums import ErrorCode, ObjectType, DataType
from .enums import SecuritySuite, CertificateEntity, CertificateType, SecurityPolicy0, SecurityPolicy
from .GXDLMSCertificateInfo import GXDLMSCertificateInfo
from ..enums.Security import Security
from .enums.GlobalKeyType import GlobalKeyType

# pylint: disable=too-many-public-methods,too-many-instance-attributes
class GXDLMSSecuritySetup(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSSecuritySetup
    """
    def __init__(self, ln="0.0.43.0.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        super(GXDLMSSecuritySetup, self).__init__(ObjectType.SECURITY_SETUP, ln, sn)
        self.securityPolicy = SecurityPolicy0.NOTHING
        # Security policy for version 1.
        self.securitySuite = SecuritySuite.AES_GCM_128
        self.certificates = list()
        # Client system title.
        self.clientSystemTitle = None
        # Server system title.
        self.serverSystemTitle = None
        # Available certificates.
        self.certificates = list()

    def getValues(self):
        return [self.logicalName,
                self.securityPolicy,
                self.securitySuite,
                self.clientSystemTitle,
                self.serverSystemTitle,
                self.certificates]

    #
    # Activates and strengthens the security policy.
    #
    # client: DLMS client that is used to generate action.
    # security: New security level.
    # Generated action.
    def activate(self, client, security):
        return client.method(self, 1, security, DataType.ENUM)

    #
    # Updates one or more global keys.
    #
    # client: DLMS client that is used to generate action.
    # kek: Master key, also known as Key Encrypting Key.
    # list: List of Global key types and keys.
    # Generated action.
    #
    def globalKeyTransfer(self, client, kek, list_):
        # pylint: disable=import-outside-toplevel
        from ..secure.GXDLMSSecureClient import GXDLMSSecureClient
        if not list_:
            raise ValueError("Invalid list. It is empty.")
        bb = GXByteBuffer()
        bb.setUInt8(DataType.ARRAY)
        bb.setUInt8(int(len(list_)))
        for it in list_:
            bb.setUInt8(DataType.STRUCTURE)
            bb.setUInt8(2)
            _GXCommon.setData(None, bb, DataType.ENUM, it.getKey())
            tmp = GXDLMSSecureClient.encrypt(kek, it)
            _GXCommon.setData(None, bb, DataType.OCTET_STRING, tmp)
        return client.method(self, 2, bb.array(), DataType.ARRAY)

    #
    # Agree on one or more symmetric keys using the key agreement
    #      algorithm.
    #
    # @param client
    # DLMS client that is used to generate action.
    # @param list
    # List of keys.
    # Generated action.
    #
    def __keyAgreement(self, client, list_):
        if not list_:
            raise ValueError("Invalid list. It is empty.")
        bb = GXByteBuffer()
        bb.setUInt8(DataType.ARRAY)
        bb.setUInt8(int(len(list_)))
        for it in list_:
            bb.setUInt8(DataType.STRUCTURE)
            bb.setUInt8(2)
            _GXCommon.setData(None, bb, DataType.ENUM, it.getKey())
            _GXCommon.setData(None, bb, DataType.OCTET_STRING, it)
        return client.method(self, 3, bb.array(), DataType.ARRAY)

    #
    # Agree on one or more symmetric keys using the key agreement
    #      algorithm.
    #
    # @param client
    # DLMS client that is used to generate action.
    # @param type
    # Global key type.
    # Generated action.
    def keyAgreement(self, client, type_):
        bb = GXByteBuffer()
        data = self.getEphemeralPublicKeyData(type_, client.ciphering.ephemeralKeyPair.public)
        bb.set(data, 1, 64)
        print("Signin public key: " + str(client.ciphering.signingKeyPair.public))
        # sign = GXASymmetric.getEphemeralPublicKeySignature(type_ ,
        # client.ciphering.ephemeralKeyPair.public,
        # client.ciphering.signingKeyPair.private)
        #  bb.set(sign)
        # print("Data: " + GXByteBuffer.hex(data))
        #print("Sign: " + GXByteBuffer.hex(sign))
        list_ = list()
        list_.append((type_, bb.array()))
        return self.__keyAgreement(client, list_)

    def generateKeyPair(self, client, type_):
        return client.method(self, 4, type_, DataType.ENUM)

    def generateCertificate(self, client, type_):
        return client.method(self, 5, type_, DataType.ENUM)


    def importCertificate(self, client, certificate):
        return self.importCertificate(client, certificate.getEncoded())

    def importCertificate_0(self, client, key):
        return client.method(self, 6, key, DataType.OCTET_STRING)

    def exportCertificateByEntity(self, client, entity, type_, systemTitle):
        if not systemTitle:
            raise ValueError("Invalid system title.")
        bb = GXByteBuffer()
        bb.setUInt8(DataType.STRUCTURE)
        bb.setUInt8(2)
        bb.setUInt8(DataType.ENUM)
        bb.setUInt8(0)
        bb.setUInt8(DataType.STRUCTURE)
        bb.setUInt8(3)
        bb.setUInt8(DataType.ENUM)
        bb.setUInt8(entity)
        bb.setUInt8(DataType.ENUM)
        bb.setUInt8(type_)
        _GXCommon.setData(None, bb, DataType.OCTET_STRING, systemTitle)
        return client.method(self, 7, bb.array(), DataType.STRUCTURE)

    def exportCertificateBySerial(self, client, serialNumber, issuer):
        bb = GXByteBuffer()
        bb.setUInt8(DataType.STRUCTURE)
        bb.setUInt8(2)
        bb.setUInt8(DataType.ENUM)
        bb.setUInt8(1)
        bb.setUInt8(DataType.STRUCTURE)
        bb.setUInt8(2)
        _GXCommon.setData(None, bb, DataType.OCTET_STRING, serialNumber.encode())
        _GXCommon.setData(None, bb, DataType.OCTET_STRING, issuer.encode())
        return client.method(self, 7, bb.array(), DataType.STRUCTURE)

    def removeCertificateByEntity(self, client, entity, type_, systemTitle):
        bb = GXByteBuffer()
        bb.setUInt8(DataType.STRUCTURE)
        bb.setUInt8(2)
        bb.setUInt8(DataType.ENUM)
        bb.setUInt8(0)
        bb.setUInt8(DataType.STRUCTURE)
        bb.setUInt8(3)
        bb.setUInt8(DataType.ENUM)
        bb.setUInt8(entity)
        bb.setUInt8(DataType.ENUM)
        bb.setUInt8(type_)
        _GXCommon.setData(None, bb, DataType.OCTET_STRING, systemTitle)
        return client.method(self, 8, bb.array(), DataType.STRUCTURE)

    def removeCertificateBySerial(self, client, serialNumber, issuer):
        bb = GXByteBuffer()
        bb.setUInt8(DataType.STRUCTURE)
        bb.setUInt8(2)
        bb.setUInt8(DataType.ENUM)
        bb.setUInt8(1)
        bb.setUInt8(DataType.STRUCTURE)
        bb.setUInt8(2)
        _GXCommon.setData(None, bb, DataType.OCTET_STRING, serialNumber.encode())
        _GXCommon.setData(None, bb, DataType.OCTET_STRING, issuer.encode())
        return client.method(self, 8, bb.array(), DataType.STRUCTURE)

    @classmethod
    def systemTitleToSubject(cls, systemTitle):
        bb = GXByteBuffer(systemTitle)
        bb.setUInt8(0, 0)
        bb.setUInt8(0, 1)
        bb.setUInt8(0, 2)
        subject = "CN=" + str(systemTitle, 0, 3)
        subject += str(bb.getUInt64())
        return subject

    def invoke(self, settings, e):
        #pylint: disable=bad-option-value,redefined-variable-type
        if e.index == 1:
            if self.version == 0:
                self.securityPolicy = SecurityPolicy0(e.parameters)
                if self.securityPolicy == SecurityPolicy0.AUTHENTICATED:
                    settings.cipher.security = Security.AUTHENTICATION
                elif self.securityPolicy == SecurityPolicy0.ENCRYPTED:
                    settings.cipher.security = Security.ENCRYPTION
                elif self.securityPolicy == SecurityPolicy0.AUTHENTICATED_ENCRYPTED:
                    settings.cipher.security = Security.AUTHENTICATION_ENCRYPTION
            elif self.version == 1:
                self.securityPolicy = SecurityPolicy(e.parameters)
                if self.securityPolicy & SecurityPolicy.AUTHENTICATED_RESPONSE != 0:
                    settings.cipher.security = Security(settings.cipher.security | Security.AUTHENTICATION)
                if self.securityPolicy & SecurityPolicy.ENCRYPTED_RESPONSE != 0:
                    settings.cipher.security = Security(settings.cipher.security | Security.ENCRYPTION)
        elif e.index == 2:
            # pylint: disable=import-outside-toplevel
            from ..secure.GXDLMSSecureClient import GXDLMSSecureClient
            # if settings.Cipher is null non secure server is used.
            # Keys are take in action after reply is generated.
            for tmp in e.parameters:
                item = tmp
                type_ = GlobalKeyType(item[0])
                if type_ == GlobalKeyType.UNICAST_ENCRYPTION:
                    GXDLMSSecureClient.decrypt(settings.kek, item[1])
                elif type_ == GlobalKeyType.BROADCAST_ENCRYPTION:
                    e.error = ErrorCode.READ_WRITE_DENIED
                elif type_ == GlobalKeyType.AUTHENTICATION:
                    GXDLMSSecureClient.decrypt(settings.kek, item[1])
                elif type_ == GlobalKeyType.KEK:
                    GXDLMSSecureClient.decrypt(settings.kek, item[1])
                else:
                    e.error = ErrorCode.READ_WRITE_DENIED
        elif e.index == 3:
            e.rror = ErrorCode.HARDWARE_FAULT
        elif e.index == 4:
            e.rror = ErrorCode.HARDWARE_FAULT
        elif e.index == 5:
            e.rror = ErrorCode.HARDWARE_FAULT
        elif e.index == 6:
            e.rror = ErrorCode.HARDWARE_FAULT
        elif e.index == 8:
            e.error = ErrorCode.READ_WRITE_DENIED
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    @classmethod
    def applyKeys(cls, settings, e):
        #pylint: disable=import-outside-toplevel
        from ..secure.GXDLMSSecureClient import GXDLMSSecureClient
        for tmp in e.parameters:
            item = tmp
            type_ = GlobalKeyType(item[0])
            data = GXDLMSSecureClient.decrypt(settings.kek, item[1])
            if type_ == GlobalKeyType.UNICAST_ENCRYPTION:
                settings.cipher.blockCipherKey = data
            elif type_ == GlobalKeyType.BROADCAST_ENCRYPTION:
                e.error = ErrorCode.READ_WRITE_DENIED
            elif type_ == GlobalKeyType.AUTHENTICATION:
                settings.cipher.authenticationKey = data
            elif type_ == GlobalKeyType.KEK:
                settings.kek = data
            else:
                e.error = ErrorCode.READ_WRITE_DENIED

    def getAttributeIndexToRead(self, all_):
        attributes = list()
        if all_ or not self.logicalName:
            attributes.append(1)
        if all_ or self.canRead(2):
            attributes.append(2)
        if all_ or self.canRead(3):
            attributes.append(3)
        if all_ or self.canRead(4):
            attributes.append(4)
        if all_ or self.canRead(5):
            attributes.append(5)
        if self.version != 0:
            if all_ or self.canRead(6):
                attributes.append(6)
        return attributes

    def getAttributeCount(self):
        if self.version == 0:
            return 5
        return 6

    def getMethodCount(self):
        if self.version == 0:
            return 2
        return 8

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.ENUM
        elif index == 3:
            ret = DataType.ENUM
        elif index == 4:
            ret = DataType.OCTET_STRING
        elif index == 5:
            ret = DataType.OCTET_STRING
        elif self.version > 0:
            if index == 6:
                ret = DataType.ARRAY
            else:
                raise ValueError("getDataType failed. Invalid attribute index.")
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret

    @classmethod
    def getCertificatesByteArray(cls, settings):
        bb = GXByteBuffer()
        bb.setUInt8(DataType.ARRAY)
        if settings.cipher.certificates:
            _GXCommon.setObjectCount(len(settings.cipher.certificates), bb)
            for it in settings.cipher.certificates:
                bb.setUInt8(DataType.STRUCTURE)
                _GXCommon.setObjectCount(6, bb)
                bb.setUInt8(DataType.ENUM)
                bb.setUInt8(CertificateEntity.SERVER)
                bb.setUInt8(DataType.ENUM)
                bb.setUInt8(CertificateType.DIGITAL_SIGNATURE)
                _GXCommon.addString(it.serialNumber, bb)
                _GXCommon.addString(it.issuer, bb)
                _GXCommon.addString(it.subject, bb)
                _GXCommon.addString("", bb)
        else:
            bb.setUInt8(0)
        return bb.array()

    def getValue(self, settings, e):
        #pylint: disable=bad-option-value,redefined-variable-type
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.securityPolicy
        elif e.index == 3:
            ret = self.securitySuite
        elif e.index == 4:
            ret = self.clientSystemTitle
        elif e.index == 5:
            ret = self.serverSystemTitle
        elif e.index == 6:
            ret = self.getCertificatesByteArray(settings)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    def updateSertificates(self, list_):
        self.certificates = []
        if list_:
            for it in list_:
                info = GXDLMSCertificateInfo()
                info.entity = CertificateEntity(it[0])
                info.type_ = CertificateType(it[1])
                info.serialNumber = it[2]
                info.issuer = it[3]
                info.subject = it[4]
                info.subjectAltName = it[5]
                self.certificates.append(info)

    def setValue(self, settings, e):
        #pylint: disable=bad-option-value,redefined-variable-type
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            if settings.isServer:
                e.error = ErrorCode.READ_WRITE_DENIED
            else:
                if self.version == 0:
                    self.securityPolicy = SecurityPolicy0(e.value)
                else:
                    self.securityPolicy = SecurityPolicy(e.value)
        elif e.index == 3:
            self.securitySuite = e.value
        elif e.index == 4:
            self.clientSystemTitle = e.value
        elif e.index == 5:
            self.serverSystemTitle = e.value
        elif e.index == 6:
            self.updateSertificates(e.value)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    @classmethod
    def getEphemeralPublicKeyData(cls, keyId, ephemeralKey):
        # pylint: disable=unused-argument
        #tmp =
        #(GXAsn1Converter.fromByteArray(ephemeralKey.getEncoded())).get(1)
        #epk = GXByteBuffer(tmp.value)
        #epk.setUInt8(int(keyId), 0)
        #return epk
        return None

    def load(self, reader):
        self.securityPolicy = SecurityPolicy(reader.readElementContentAsInt("SecurityPolicy"))
        self.securitySuite = SecuritySuite(reader.readElementContentAsInt("SecuritySuite"))
        str_ = reader.readElementContentAsString("ClientSystemTitle")
        if str_ is None:
            self.clientSystemTitle = None
        else:
            self.clientSystemTitle = GXByteBuffer.hexToBytes(str_)
        str_ = reader.readElementContentAsString("ServerSystemTitle")
        if str_ is None:
            self.serverSystemTitle = None
        else:
            self.serverSystemTitle = GXByteBuffer.hexToBytes(str_)
        self.certificates = []
        if reader.isStartElement("Certificates", True):
            while reader.isStartElement("Item", True):
                it = GXDLMSCertificateInfo()
                self.certificates.append(it)
                it.entity = CertificateEntity(reader.readElementContentAsInt("Entity"))
                it.type_ = CertificateType(reader.readElementContentAsInt("Type"))
                it.serialNumber = reader.readElementContentAsString("SerialNumber")
                it.issuer = reader.readElementContentAsString("Issuer")
                it.subject = reader.readElementContentAsString("Subject")
                it.subjectAltName = reader.readElementContentAsString("SubjectAltName")
            reader.readEndElement("Certificates")

    def save(self, writer):
        writer.writeElementString("SecurityPolicy", int(self.securityPolicy))
        writer.writeElementString("SecuritySuite", int(self.securitySuite))
        writer.writeElementString("ClientSystemTitle", GXByteBuffer.hex(self.clientSystemTitle))
        writer.writeElementString("ServerSystemTitle", GXByteBuffer.hex(self.serverSystemTitle))
        writer.writeStartElement("Certificates")
        if self.certificates:
            for it in self.certificates:
                writer.writeStartElement("Item")
                writer.writeElementString("Entity", it.entity)
                writer.writeElementString("Type", it.type_)
                writer.writeElementString("SerialNumber", it.serialNumber)
                writer.writeElementString("Issuer", it.issuer)
                writer.writeElementString("Subject", it.subject)
                writer.writeElementString("SubjectAltName", it.subjectAltName)
                writer.writeEndElement()
        writer.writeEndElement()

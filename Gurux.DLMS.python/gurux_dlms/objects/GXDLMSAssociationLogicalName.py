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
from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ErrorCode
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from ..enums import DataType, ObjectType, Authentication
from .enums import AssociationStatus
from .GXDLMSObjectCollection import GXDLMSObjectCollection
from .GXApplicationContextName import GXApplicationContextName
from .GXxDLMSContextType import GXxDLMSContextType
from .GXAuthenticationMechanismName import GXAuthenticationMechanismName
from ..ValueEventArgs import ValueEventArgs
from ..GXSecure import GXSecure
from ..enums.Conformance import Conformance
from ..enums.AccessMode import AccessMode
from ..enums.MethodAccessMode import MethodAccessMode
from ..enums.AccessMode3 import AccessMode3
from ..enums.MethodAccessMode3 import MethodAccessMode3
from ..GXBitString import GXBitString


# pylint: disable=too-many-instance-attributes
class GXDLMSAssociationLogicalName(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSAssociationLogicalName
    """

    def __init__(self, ln="0.0.40.0.0.255"):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.ASSOCIATION_LOGICAL_NAME, ln)
        self.objectList = GXDLMSObjectCollection(self)
        self.applicationContextName = GXApplicationContextName()
        self.xDLMSContextInfo = GXxDLMSContextType()
        self.authenticationMechanismName = GXAuthenticationMechanismName()
        self.userList = []
        self.version = 2
        self.associationStatus = AssociationStatus.NON_ASSOCIATED
        self.clientSAP = None
        self.serverSAP = None
        self.secret = None
        self.securitySetupReference = None
        self.userList = []
        self.currentUser = None

    #
    # Updates secret.
    #
    # @param client
    # DLMS client.
    # Action bytes.
    #
    def updateSecret(self, client):
        if self.authenticationMechanismName.mechanismId == Authentication.NONE:
            raise ValueError("Invalid authentication level in MechanismId.")
        if self.authenticationMechanismName.mechanismId == Authentication.HIGH_GMAC:
            raise ValueError("HighGMAC secret is updated using Security setup.")
        if self.authenticationMechanismName.mechanismId == Authentication.LOW:
            return client.write(self, 7)
        #  Action is used to update High authentication password.
        return client.method(self, 2, self.secret, DataType.OCTET_STRING)

    #
    # Add user to user list.
    #
    # @param client
    # DLMS client.
    # @param id
    # User ID.
    # @param name
    # User name.
    # Action bytes.
    #
    def addUser(self, client, id_, name):
        data = GXByteBuffer()
        data.setUInt8(DataType.STRUCTURE)
        #  Add structure size.
        data.setUInt8(2)
        _GXCommon.setData(None, data, DataType.UINT8, id_)
        _GXCommon.setData(None, data, DataType.STRING, name)
        return client.method(self, 5, data.array(), DataType.STRUCTURE)

    #
    # Remove user from user list.
    #
    # @param client
    # DLMS client.
    # @param id
    # User ID.
    # @param name
    # User name.
    # Action bytes.
    #
    def removeUser(self, client, id_, name):
        data = GXByteBuffer()
        data.setUInt8(DataType.STRUCTURE)
        #  Add structure size.
        data.setUInt8(2)
        _GXCommon.setData(None, data, DataType.UINT8, id_)
        _GXCommon.setData(None, data, DataType.STRING, name)
        return client.method(self, 6, data.array(), DataType.STRUCTURE)

    def getValues(self):
        return [
            self.logicalName,
            self.objectList,
            [self.clientSAP, self.serverSAP],
            self.applicationContextName,
            self.xDLMSContextInfo,
            self.authenticationMechanismName,
            self.secret,
            self.associationStatus,
            self.securitySetupReference,
            self.userList,
            self.currentUser,
        ]

    def invoke(self, settings, e):
        # pylint: disable=bad-option-value,redefined-variable-type
        #  Check reply_to_HLS_authentication
        if e.index == 1:
            serverChallenge = None
            clientChallenge = None
            ic = 0
            readSecret = []
            accept = True
            if settings.authentication == Authentication.HIGH_ECDSA:
                raise ValueError("ECDSA is not implemented.")
            if settings.authentication == Authentication.HIGH_GMAC:
                readSecret = settings.sourceSystemTitle
                bb = GXByteBuffer(int(e.parameters))
                bb.getUInt8()
                ic = bb.getUInt32()
            else:
                readSecret = self.secret
            serverChallenge = GXSecure.secure(
                settings, settings.cipher, ic, settings.stoCChallenge, readSecret
            )
            clientChallenge = int(e.parameters)
            accept = serverChallenge == clientChallenge
            if accept:
                if settings.authentication in (
                    Authentication.HIGH_GMAC,
                    Authentication.HIGH_ECDSA,
                ):
                    readSecret = settings.cipher.getSystemTitle()
                    ic = settings.cipher.invocationCounter
                else:
                    readSecret = self.secret
                tmp = GXSecure.secure(
                    settings,
                    settings.cipher,
                    ic,
                    settings.getCtoSChallenge(),
                    readSecret,
                )
                self.associationStatus = AssociationStatus.ASSOCIATED
                return tmp
            self.associationStatus = AssociationStatus.NON_ASSOCIATED
        elif e.index == 2:
            if not e.parameters:
                e.error = ErrorCode.READ_WRITE_DENIED
            else:
                self.secret = e.parameters
        elif e.index == 5:
            if not e.parameters:
                e.error = ErrorCode.READ_WRITE_DENIED
            else:
                self.userList.append((e.parameters[0], str(e.parameters[1])))
        elif e.index == 6:
            tmp = e.parameters
            if not tmp:
                e.error = ErrorCode.READ_WRITE_DENIED
            else:
                id_ = tmp[0]
                name = str(tmp[1])
                for k, v in self.userList:
                    if k == id_ and v == name:
                        self.userList.remove(k)
                        break
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return None

    def getAttributeIndexToRead(self, all_):
        attributes = []
        if all_ or not self.logicalName:
            attributes.append(1)
        if all_ or not self.isRead(2):
            attributes.append(2)
        if all_ or not self.isRead(3):
            attributes.append(3)
        if all_ or not self.isRead(4):
            attributes.append(4)
        if all_ or not self.isRead(5):
            attributes.append(5)
        if all_ or not self.isRead(6):
            attributes.append(6)
        if all_ or not self.isRead(7):
            attributes.append(7)
        if all_ or not self.isRead(8):
            attributes.append(8)
        if self.version > 0 and (all_ or not self.isRead(9)):
            attributes.append(9)
        if self.version > 1:
            if all_ or not self.isRead(10):
                attributes.append(10)
            if all_ or not self.isRead(11):
                attributes.append(11)
        return attributes

    def getAttributeCount(self):
        if self.version > 1:
            return 11
        if self.version > 0:
            return 9
        return 8

    def getMethodCount(self):
        if self.version > 1:
            return 6
        return 4

    def getObjects(self, settings, e):
        data = GXByteBuffer()
        if settings.index == 0:
            settings.setCount(len(self.objectList))
            data.setUInt8(DataType.ARRAY)
            _GXCommon.setObjectCount(len(self.objectList), data)
        pos = 0
        for it in self.objectList:
            pos += 1
            if not pos <= settings.index:
                data.setUInt8(DataType.STRUCTURE)
                data.setUInt8(4)
                _GXCommon.setData(settings, data, DataType.UINT16, it.objectType)
                _GXCommon.setData(settings, data, DataType.UINT8, it.version)
                _GXCommon.setData(
                    settings,
                    data,
                    DataType.OCTET_STRING,
                    _GXCommon.logicalNameToBytes(it.logicalName),
                )
                self.__getAccessRights(settings, it, e.server, data)
                settings.index = settings.index + 1
                if settings.isServer:
                    if not e.isSkipMaxPduSize and len(data) >= settings.maxPduSize:
                        break
        return data

    def __getAccessRights(self, settings, item, server, data):
        data.setUInt8(DataType.STRUCTURE)
        data.setUInt8(2)
        if server is None:
            data.setUInt8(DataType.ARRAY)
            data.setUInt8(0)
            data.setUInt8(DataType.ARRAY)
            data.setUInt8(0)
        else:
            data.setUInt8(DataType.ARRAY)
            cnt = item.getAttributeCount()
            data.setUInt8(cnt)
            e = ValueEventArgs(server, item, 0, 0, None)
            pos = 0
            while pos != cnt:
                e.index = pos + 1
                m = server.onGetAttributeAccess(e)
                data.setUInt8(DataType.STRUCTURE)
                data.setUInt8(3)
                _GXCommon.setData(settings, data, DataType.INT8, pos + 1)
                _GXCommon.setData(settings, data, DataType.ENUM, m)
                _GXCommon.setData(settings, data, DataType.NONE, None)
                pos += 1
            data.setUInt8(DataType.ARRAY)
            cnt = item.getMethodCount()
            data.setUInt8(cnt)
            pos = 0
            while pos != cnt:
                e.index = pos + 1
                data.setUInt8(DataType.STRUCTURE)
                data.setUInt8(2)
                _GXCommon.setData(settings, data, DataType.INT8, pos + 1)
                m = server.onGetMethodAccess(e)
                if self.version == 0:
                    _GXCommon.setData(settings, data, DataType.BOOLEAN, m != 0)
                else:
                    _GXCommon.setData(settings, data, DataType.ENUM, m)
                pos += 1

    def updateAccessRights(self, obj, buff):
        if buff:
            for attributeAccess in buff[0]:
                id_ = attributeAccess[0]
                tmp = attributeAccess[1]
                if self.version < 3:
                    obj.setAccess(id_, AccessMode(tmp))
                else:
                    obj.setAccess(id_, AccessMode3(tmp))

            for methodAccess in buff[1]:
                id_ = methodAccess[0]
                tmp = 0
                if isinstance(methodAccess[1], bool):
                    if methodAccess[1]:
                        tmp = 1
                    else:
                        tmp = 0
                else:
                    tmp = methodAccess[1]
                if self.version < 3:
                    obj.setMethodAccess(id_, MethodAccessMode(tmp))
                else:
                    obj.setMethodAccess3(id_, MethodAccessMode3(tmp))

    def getUserList(self, settings):
        data = GXByteBuffer()
        if settings.index == 0:
            settings.setCount(len(self.userList))
            data.setUInt8(DataType.ARRAY)
            _GXCommon.setObjectCount(len(self.userList), data)
        pos = 0
        for k, v in self.userList:
            pos += 1
            if not pos <= settings.index:
                settings.index = settings.index + 1
                data.setUInt8(DataType.STRUCTURE)
                data.setUInt8(2)
                _GXCommon.setData(settings, data, DataType.UINT8, k)
                _GXCommon.setData(settings, data, DataType.STRING, v)
        return data

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.ARRAY
        elif index == 3:
            ret = DataType.STRUCTURE
        elif index == 4:
            ret = DataType.STRUCTURE
        elif index == 5:
            ret = DataType.STRUCTURE
        elif index == 6:
            ret = DataType.STRUCTURE
        elif index == 7:
            ret = DataType.OCTET_STRING
        elif index == 8:
            ret = DataType.ENUM
        elif self.version > 0 and index == 9:
            ret = DataType.OCTET_STRING
        elif self.version > 1:
            if index == 10:
                ret = DataType.ARRAY
            if index == 11:
                ret = DataType.STRUCTURE
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret

    def getValue(self, settings, e):
        # pylint: disable=bad-option-value,redefined-variable-type
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.getObjects(settings, e)
        elif e.index == 3:
            data = GXByteBuffer()
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(2)
            data.setUInt8(DataType.INT8)
            data.setUInt8(self.clientSAP)
            data.setUInt8(DataType.UINT16)
            data.setUInt16(self.serverSAP)
            ret = data
        elif e.index == 4:
            data = GXByteBuffer()
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(0x7)
            _GXCommon.setData(
                settings, data, DataType.UINT8, self.applicationContextName.jointIsoCtt
            )
            _GXCommon.setData(
                settings, data, DataType.UINT8, self.applicationContextName.country
            )
            _GXCommon.setData(
                settings, data, DataType.UINT16, self.applicationContextName.countryName
            )
            _GXCommon.setData(
                settings,
                data,
                DataType.UINT8,
                self.applicationContextName.identifiedOrganization,
            )
            _GXCommon.setData(
                settings, data, DataType.UINT8, self.applicationContextName.dlmsUA
            )
            _GXCommon.setData(
                settings,
                data,
                DataType.UINT8,
                self.applicationContextName.applicationContext,
            )
            _GXCommon.setData(
                settings, data, DataType.UINT8, self.applicationContextName.contextId
            )
            ret = data
        elif e.index == 5:
            data = GXByteBuffer()
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(6)
            _GXCommon.setData(
                settings,
                data,
                DataType.BITSTRING,
                GXBitString.toBitString(self.xDLMSContextInfo.conformance, 24),
            )
            _GXCommon.setData(
                settings, data, DataType.UINT16, self.xDLMSContextInfo.maxReceivePduSize
            )
            _GXCommon.setData(
                settings, data, DataType.UINT16, self.xDLMSContextInfo.maxSendPduSize
            )
            _GXCommon.setData(
                settings, data, DataType.UINT8, self.xDLMSContextInfo.dlmsVersionNumber
            )
            _GXCommon.setData(
                settings, data, DataType.INT8, self.xDLMSContextInfo.qualityOfService
            )
            _GXCommon.setData(
                settings,
                data,
                DataType.OCTET_STRING,
                self.xDLMSContextInfo.cypheringInfo,
            )
            ret = data
        elif e.index == 6:
            data = GXByteBuffer()
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(0x7)
            _GXCommon.setData(
                settings,
                data,
                DataType.UINT8,
                self.authenticationMechanismName.jointIsoCtt,
            )
            _GXCommon.setData(
                settings, data, DataType.UINT8, self.authenticationMechanismName.country
            )
            _GXCommon.setData(
                settings,
                data,
                DataType.UINT16,
                self.authenticationMechanismName.countryName,
            )
            _GXCommon.setData(
                settings,
                data,
                DataType.UINT8,
                self.authenticationMechanismName.identifiedOrganization,
            )
            _GXCommon.setData(
                settings, data, DataType.UINT8, self.authenticationMechanismName.dlmsUA
            )
            _GXCommon.setData(
                settings,
                data,
                DataType.UINT8,
                self.authenticationMechanismName.authenticationMechanismName,
            )
            _GXCommon.setData(
                settings,
                data,
                DataType.UINT8,
                self.authenticationMechanismName.mechanismId,
            )
            ret = data
        elif e.index == 7:
            ret = self.secret
        elif e.index == 8:
            ret = self.associationStatus
        elif e.index == 9:
            ret = _GXCommon.logicalNameToBytes(self.securitySetupReference)
        elif e.index == 10:
            ret = self.getUserList(settings)
        elif e.index == 11:
            data = GXByteBuffer()
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(2)
            if self.currentUser is None:
                _GXCommon.setData(settings, data, DataType.UINT8, 0)
                _GXCommon.setData(settings, data, DataType.STRING, None)
            else:
                _GXCommon.setData(settings, data, DataType.UINT8, self.currentUser[0])
                _GXCommon.setData(settings, data, DataType.STRING, self.currentUser[1])
            ret = data
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    def updateObjectList(self, settings, target, value):
        # pylint: disable=import-outside-toplevel,unidiomatic-typecheck
        from .._GXObjectFactory import _GXObjectFactory

        target.clear()
        if value:
            for item in value:
                type_ = item[0]
                version = item[1]
                ln = _GXCommon.toLogicalName(item[2])
                obj = settings.objects.findByLN(type_, ln)
                if obj is None:
                    obj = _GXObjectFactory.createObject(type_)
                    obj.logicalName = ln
                    obj.version = version
                if type(obj) != GXDLMSObject:
                    self.updateAccessRights(obj, item[3])
                    target.append(obj)

    def updateApplicationContextName(self, value):
        if isinstance(value, bytearray):
            buff = GXByteBuffer(value)
            if buff.getUInt8(0) == 0x60:
                self.applicationContextName.jointIsoCtt = 0
                self.applicationContextName.country = 0
                self.applicationContextName.countryName = 0
                buff.position = buff.position + 3
                self.applicationContextName.identifiedOrganization = buff.getUInt8()
                self.applicationContextName.dlmsUA = buff.getUInt8()
                self.applicationContextName.applicationContext = buff.getUInt8()
                self.applicationContextName.contextId = buff.getUInt8()
            else:
                if buff.getUInt8() != 2 and buff.getUInt8() != 7:
                    raise ValueError()
                if buff.getUInt8() != 0x11:
                    raise ValueError()
                self.applicationContextName.jointIsoCtt = buff.getUInt8()
                if buff.getUInt8() != 0x11:
                    raise ValueError()
                self.applicationContextName.country = buff.getUInt8()
                if buff.getUInt8() != 0x12:
                    raise ValueError()
                self.applicationContextName.countryName = buff.getUInt16()
                if buff.getUInt8() != 0x11:
                    raise ValueError()
                self.applicationContextName.identifiedOrganization = buff.getUInt8()
                if buff.getUInt8() != 0x11:
                    raise ValueError()
                self.applicationContextName.dlmsUA = buff.getUInt8()
                if buff.getUInt8() != 0x11:
                    raise ValueError()
                self.applicationContextName.applicationContext = buff.getUInt8()
                if buff.getUInt8() != 0x11:
                    raise ValueError()
                self.applicationContextName.contextId = buff.getUInt8()
        else:
            if value:
                self.applicationContextName.jointIsoCtt = value[0]
                self.applicationContextName.country = value[1]
                self.applicationContextName.countryName = value[2]
                self.applicationContextName.identifiedOrganization = value[3]
                self.applicationContextName.dlmsUA = value[4]
                self.applicationContextName.applicationContext = value[5]
                self.applicationContextName.contextId = value[6]

    def updateAuthenticationMechanismName(self, value):
        if value:
            if isinstance(value, bytearray):
                buff = GXByteBuffer(value)
                if buff.getUInt8(0) == 0x60:
                    self.authenticationMechanismName.jointIsoCtt = 0
                    self.authenticationMechanismName.country = 0
                    self.authenticationMechanismName.countryName = 0
                    buff.position = buff.position + 3
                    self.authenticationMechanismName.identifiedOrganization = (
                        buff.getUInt8()
                    )
                    self.authenticationMechanismName.dlmsUA = buff.getUInt8()
                    self.authenticationMechanismName.authenticationMechanismName = (
                        buff.getUInt8()
                    )
                    self.authenticationMechanismName.mechanismId = buff.getUInt8()
                else:
                    if buff.getUInt8() != 2 and buff.getUInt8() != 7:
                        raise ValueError()
                    if buff.getUInt8() != 0x11:
                        raise ValueError()
                    self.authenticationMechanismName.jointIsoCtt = buff.getUInt8()
                    if buff.getUInt8() != 0x11:
                        raise ValueError()
                    self.authenticationMechanismName.country = buff.getUInt8()
                    if buff.getUInt8() != 0x12:
                        raise ValueError()
                    self.authenticationMechanismName.countryName = buff.getUInt16()
                    if buff.getUInt8() != 0x11:
                        raise ValueError()
                    self.authenticationMechanismName.identifiedOrganization = (
                        buff.getUInt8()
                    )
                    if buff.getUInt8() != 0x11:
                        raise ValueError()
                    self.authenticationMechanismName.dlmsUA = buff.getUInt8()
                    if buff.getUInt8() != 0x11:
                        raise ValueError()
                    self.authenticationMechanismName.authenticationMechanismName = (
                        buff.getUInt8()
                    )
                    if buff.getUInt8() != 0x11:
                        raise ValueError()
                    self.authenticationMechanismName.mechanismId = buff.getUInt8()
            else:
                if value:
                    self.authenticationMechanismName.jointIsoCtt = value[0]
                    self.authenticationMechanismName.country = value[1]
                    self.authenticationMechanismName.countryName = value[2]
                    self.authenticationMechanismName.identifiedOrganization = value[3]
                    self.authenticationMechanismName.dlmsUA = value[4]
                    self.authenticationMechanismName.authenticationMechanismName = (
                        value[5]
                    )
                    self.authenticationMechanismName.mechanismId = value[6]

    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.updateObjectList(settings, self.objectList, e.value)
        elif e.index == 3:
            if e.value:
                self.clientSAP = e.value[0]
                self.serverSAP = e.value[1]
        elif e.index == 4:
            self.updateApplicationContextName(e.value)
        elif e.index == 5:
            if e.value:
                self.xDLMSContextInfo.conformance = Conformance(e.value[0].toInteger())
                self.xDLMSContextInfo.maxReceivePduSize = e.value[1]
                self.xDLMSContextInfo.maxSendPduSize = e.value[2]
                self.xDLMSContextInfo.dlmsVersionNumber = e.value[3]
                self.xDLMSContextInfo.qualityOfService = e.value[4]
                self.xDLMSContextInfo.cypheringInfo = e.value[5]
        elif e.index == 6:
            self.updateAuthenticationMechanismName(e.value)
        elif e.index == 7:
            self.secret = e.value
        elif e.index == 8:
            # pylint: disable=bad-option-value,redefined-variable-type
            if e.value is None:
                self.associationStatus = AssociationStatus.NON_ASSOCIATED
            else:
                self.associationStatus = e.value
        elif e.index == 9:
            self.securitySetupReference = _GXCommon.toLogicalName(e.value)
        elif e.index == 10:
            self.userList = []
            if e.value:
                for tmp in e.value:
                    item = tmp
                    self.userList.append((int(item[0]), str(item[1])))
        elif e.index == 11:
            if e.value:
                tmp = e.value
                self.currentUser = (tmp[0], str(tmp[1]))
            else:
                self.currentUser = None
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.clientSAP = reader.readElementContentAsInt("ClientSAP")
        self.serverSAP = reader.readElementContentAsInt("ServerSAP")
        if reader.isStartElement("ApplicationContextName", True):
            self.applicationContextName.jointIsoCtt = reader.readElementContentAsInt(
                "JointIsoCtt"
            )
            self.applicationContextName.country = reader.readElementContentAsInt(
                "Country"
            )
            self.applicationContextName.countryName = reader.readElementContentAsInt(
                "CountryName"
            )
            self.applicationContextName.identifiedOrganization = (
                reader.readElementContentAsInt("IdentifiedOrganization")
            )
            self.applicationContextName.dlmsUA = reader.readElementContentAsInt(
                "DlmsUA"
            )
            self.applicationContextName.applicationContext = (
                reader.readElementContentAsInt("ApplicationContext")
            )
            self.applicationContextName.contextId = reader.readElementContentAsInt(
                "ContextId"
            )
            reader.readEndElement("ApplicationContextName")
        if reader.isStartElement("XDLMSContextInfo", True):
            self.xDLMSContextInfo.conformance = Conformance(
                reader.readElementContentAsInt("Conformance")
            )
            self.xDLMSContextInfo.maxReceivePduSize = reader.readElementContentAsInt(
                "MaxReceivePduSize"
            )
            self.xDLMSContextInfo.maxSendPduSize = reader.readElementContentAsInt(
                "MaxSendPduSize"
            )
            self.xDLMSContextInfo.dlmsVersionNumber = reader.readElementContentAsInt(
                "DlmsVersionNumber"
            )
            self.xDLMSContextInfo.qualityOfService = reader.readElementContentAsInt(
                "QualityOfService"
            )
            self.xDLMSContextInfo.cypheringInfo = GXByteBuffer.hexToBytes(
                reader.readElementContentAsString("CypheringInfo")
            )
            reader.readEndElement("XDLMSContextInfo")
        if reader.isStartElement("AuthenticationMechanismName", True):
            self.authenticationMechanismName.JointIsoCtt = (
                reader.readElementContentAsInt("JointIsoCtt")
            )
            self.authenticationMechanismName.country = reader.readElementContentAsInt(
                "Country"
            )
            self.authenticationMechanismName.countryName = (
                reader.readElementContentAsInt("CountryName")
            )
            self.authenticationMechanismName.identifiedOrganization = (
                reader.readElementContentAsInt("IdentifiedOrganization")
            )
            self.authenticationMechanismName.dlmsUA = reader.readElementContentAsInt(
                "DlmsUA"
            )
            self.authenticationMechanismName.authenticationMechanismName = (
                reader.readElementContentAsInt("AuthenticationMechanismName")
            )
            self.authenticationMechanismName.mechanismId = (
                reader.readElementContentAsInt("MechanismId")
            )
            reader.readEndElement("AuthenticationMechanismName")
        str_ = reader.readElementContentAsString("Secret")
        if str_ is None:
            self.secret = None
        else:
            self.secret = GXByteBuffer.hexToBytes(str_)
        self.associationStatus = reader.readElementContentAsInt("AssociationStatus")
        self.securitySetupReference = reader.readElementContentAsString(
            "SecuritySetupReference"
        )

    def save(self, writer):
        writer.writeElementString("ClientSAP", self.clientSAP)
        writer.writeElementString("ServerSAP", self.serverSAP)
        if self.applicationContextName:
            writer.writeStartElement("ApplicationContextName")
            writer.writeElementString(
                "JointIsoCtt", self.applicationContextName.jointIsoCtt
            )
            writer.writeElementString("Country", self.applicationContextName.country)
            writer.writeElementString(
                "CountryName", self.applicationContextName.countryName
            )
            writer.writeElementString(
                "IdentifiedOrganization",
                self.applicationContextName.identifiedOrganization,
            )
            writer.writeElementString("DlmsUA", self.applicationContextName.dlmsUA)
            writer.writeElementString(
                "ApplicationContext", self.applicationContextName.applicationContext
            )
            writer.writeElementString(
                "ContextId", int(self.applicationContextName.contextId)
            )
            writer.writeEndElement()
        if self.xDLMSContextInfo:
            writer.writeStartElement("XDLMSContextInfo")
            writer.writeElementString(
                "Conformance", int(self.xDLMSContextInfo.conformance)
            )
            writer.writeElementString(
                "MaxReceivePduSize", self.xDLMSContextInfo.maxReceivePduSize
            )
            writer.writeElementString(
                "MaxSendPduSize", self.xDLMSContextInfo.maxSendPduSize
            )
            writer.writeElementString(
                "DlmsVersionNumber", self.xDLMSContextInfo.dlmsVersionNumber
            )
            writer.writeElementString(
                "QualityOfService", self.xDLMSContextInfo.qualityOfService
            )
            writer.writeElementString(
                "CypheringInfo", GXByteBuffer.hex(self.xDLMSContextInfo.cypheringInfo)
            )
            writer.writeEndElement()
        if self.authenticationMechanismName:
            writer.writeStartElement("AuthenticationMechanismName")
            writer.writeElementString(
                "JointIsoCtt", self.authenticationMechanismName.jointIsoCtt
            )
            writer.writeElementString(
                "Country", self.authenticationMechanismName.country
            )
            writer.writeElementString(
                "CountryName", self.authenticationMechanismName.countryName
            )
            writer.writeElementString(
                "IdentifiedOrganization",
                self.authenticationMechanismName.identifiedOrganization,
            )
            writer.writeElementString("DlmsUA", self.authenticationMechanismName.dlmsUA)
            writer.writeElementString(
                "AuthenticationMechanismName",
                self.authenticationMechanismName.authenticationMechanismName,
            )
            writer.writeElementString(
                "MechanismId", int(self.authenticationMechanismName.mechanismId)
            )
            writer.writeEndElement()
        writer.writeElementString("Secret", GXByteBuffer.hex(self.secret))
        writer.writeElementString("AssociationStatus", int(self.associationStatus))
        writer.writeElementString("SecuritySetupReference", self.securitySetupReference)

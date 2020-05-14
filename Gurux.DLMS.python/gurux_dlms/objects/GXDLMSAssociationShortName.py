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
from ..enums import ObjectType, DataType, AccessMode, MethodAccessMode, Authentication
from .GXDLMSObjectCollection import GXDLMSObjectCollection
from ..GXSecure import GXSecure
from ..ConnectionState import ConnectionState

# pylint: disable=too-many-instance-attributes
class GXDLMSAssociationShortName(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSAssociationShortName
    """

    def __init__(self, ln="0.0.40.0.0.255", sn=0xFA00):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.ASSOCIATION_SHORT_NAME, ln, sn)
        self.secret = bytearray()
        self.objectList = GXDLMSObjectCollection(self)
        self.version = 2
        self.securitySetupReference = None

    def getValues(self):
        return [self.logicalName,
                self.objectList,
                None,
                self.securitySetupReference]

    #
    # Invokes method.
    # @param index Method index.
    #
    def invoke(self, settings, e):
        #  Check reply_to_HLS_authentication
        if e.index == 8:
            serverChallenge = None
            clientChallenge = None
            ic = 0
            readSecret = []
            accept = False
            if settings.authentication == Authentication.HIGH_ECDSA:
                accept = False
            else:
                if settings.authentication == Authentication.HIGH_GMAC:
                    readSecret = settings.sourceSystemTitle
                    bb = GXByteBuffer(e.parameters)
                    bb.getUInt8()
                    ic = bb.getUInt32()
                else:
                    readSecret = self.secret
                serverChallenge = GXSecure.secure(settings, settings.cipher, ic, settings.getStoCChallenge(), readSecret)
                clientChallenge = int(e.parameters)
                accept = serverChallenge == clientChallenge
            if accept:
                if settings.authentication == Authentication.HIGH_GMAC:
                    readSecret = settings.cipher.getSystemTitle()
                    ic = settings.cipher.invocationCounter
                else:
                    readSecret = self.secret
                settings.setConnected(settings.connected | ConnectionState.DLMS)
                return GXSecure.secure(settings, settings.cipher, ic, settings.getCtoSChallenge(), readSecret)
        else:
            settings.setConnected(settings.connected & ~ConnectionState.DLMS)
            e.error = ErrorCode.READ_WRITE_DENIED
        return None

    def getAttributeIndexToRead(self, all_):
        attributes = list()
        if all_ or not self.logicalName:
            attributes.append(1)
        if all_ or not self.isRead(2):
            attributes.append(2)
        if self.version > 1:
            if all_ or not self.isRead(3):
                attributes.append(3)
            if all_ or not self.isRead(4):
                attributes.append(4)
        return attributes

    def getAttributeCount(self):
        if self.version < 2:
            return 2
        return 4

    def getMethodCount(self):
        return 8

    @classmethod
    def __getAccessRights_(cls, settings, item, data):
        data.setUInt8(DataType.STRUCTURE)
        data.setUInt8(3)
        _GXCommon.setData(settings, data, DataType.UINT16, item.shortName)
        data.setUInt8(DataType.ARRAY)
        data.setUInt8(len(item.attributes))
        for att in item.attributes:
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(3)
            _GXCommon.setData(settings, data, DataType.INT8, att.index)
            _GXCommon.setData(settings, data, DataType.ENUM, att.access.value)
            _GXCommon.setData(settings, data, DataType.NONE, None)
        data.setUInt8(DataType.ARRAY)
        data.setUInt8(len(item.methodAttributes))
        for it in item.methodAttributes:
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(2)
            _GXCommon.setData(settings, data, DataType.INT8, it.index)
            _GXCommon.setData(settings, data, DataType.ENUM, it.getMethodAccess().value)

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.ARRAY
        elif index == 3:
            ret = DataType.ARRAY
        elif index == 4:
            return DataType.OCTET_STRING
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret

    def getObjects(self, settings, e):
        bb = GXByteBuffer()
        cnt = len(self.objectList)
        if settings.index == 0:
            settings.setCount(cnt)
            bb.setUInt8(DataType.ARRAY)
            _GXCommon.setObjectCount(cnt, bb)
        pos = 0
        if cnt != 0:
            for it in self.objectList:
                pos += 1
                if not pos <= settings.index:
                    bb.setUInt8(DataType.STRUCTURE)
                    bb.setUInt8(4)
                    _GXCommon.setData(settings, bb, DataType.INT16, it.shortName)
                    _GXCommon.setData(settings, bb, DataType.UINT16, it.objectType)
                    _GXCommon.setData(settings, bb, DataType.UINT8, 0)
                    _GXCommon.setData(settings, bb, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(it.logicalName))
                    settings.index = settings.index + 1
                    if settings.isServer:
                        if not e.isSkipMaxPduSize() and len(bb) >= settings.maxPduSize:
                            break
        return bb.array()

    def getValue(self, settings, e):
        ret = None
        bb = GXByteBuffer()
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.getObjects(settings, e)
        elif e.index == 3:
            lnExists = self.objectList.findBySN(self.shortName) is not None
            cnt = len(self.objectList)
            if not lnExists:
                cnt += 1
            bb.setUInt8(DataType.ARRAY)
            _GXCommon.setObjectCount(cnt, bb)
            for it in self.objectList:
                self.__getAccessRights_(settings, it, bb)
            if not lnExists:
                self.__getAccessRights_(settings, self, bb)
            ret = bb.array()
        elif e.index == 4:
            ret = _GXCommon.getBytes(self.securitySetupReference)
        e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    def updateAccessRights(self, buff):
        for access in buff:
            sn = access[0]
            obj = self.objectList.findBySN(sn)
            if obj:
                for attributeAccess in access[1]:
                    id1 = attributeAccess[0]
                    mode1 = AccessMode(attributeAccess[1])
                    obj.setAccess(id1, mode1)
                for methodAccess in access[2]:
                    id2 = methodAccess[0]
                    mode2 = MethodAccessMode(methodAccess[1])
                    obj.setMethodAccess(id2, mode2)

    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            #pylint: disable=import-outside-toplevel
            from .._GXObjectFactory import _GXObjectFactory
            self.objectList.clear()
            if e.value:
                for item in e.value:
                    sn = item[0]
                    ot = item[1]
                    version = item[2]
                    ln = _GXCommon.toLogicalName(item[3])
                    obj = _GXObjectFactory.createObject(ot)
                    obj.logicalName = ln
                    obj.shortName = sn
                    obj.version = version
                    self.objectList.append(obj)
        elif e.index == 3:
            if e.value is None:
                for it in self.objectList:
                    pos = 1
                    while pos != it.getAttributeCount():
                        it.setAccess(pos, AccessMode.NO_ACCESS)
                        pos += 1
            else:
                self.updateAccessRights(e.value)
        elif e.index == 4:
            self.securitySetupReference = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        str_ = reader.readElementContentAsString("Secret")
        if str_ is None:
            self.secret = None
        else:
            self.secret = GXByteBuffer.hexToBytes(str_)
        self.securitySetupReference = reader.readElementContentAsString("SecuritySetupReference")

    def save(self, writer):
        writer.writeElementString("Secret", GXByteBuffer.hex(self.secret))
        writer.writeElementString("SecuritySetupReference", self.securitySetupReference)

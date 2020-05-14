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
from .enums import PppSetupLcpOptionType
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from ..enums import ErrorCode, ObjectType, DataType
from .GXDLMSPppSetupLcpOption import GXDLMSPppSetupLcpOption
from .GXDLMSPppSetupIPCPOption import GXDLMSPppSetupIPCPOption
from .enums import PppSetupIPCPOptionType

# pylint: disable=too-many-instance-attributes
class GXDLMSPppSetup(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSPppSetup
    """

    #
    # Constructor.
    #
    # @param ln
    # Logical Name of the object.
    # @param sn
    # Short Name of the object.
    #
    def __init__(self, ln=None, sn=0):
        super(GXDLMSPppSetup, self).__init__(ObjectType.PPP_SETUP, ln, sn)
        self.ipcpOptions = list()
        self.phyReference = None
        self.lcpOptions = list()
        # PPP authentication procedure user name.
        self.userName = None
        # PPP authentication procedure password.
        self.password = None
        self.authentication = None

    def getValues(self):
        return [self.logicalName,
                self.phyReference,
                self.lcpOptions,
                self.ipcpOptions,
                [self.userName, self.password]]

    #
    # Returns collection of attributes to read.  If attribute is static
    #      and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  PHYReference
        if all_ or not self.isRead(2):
            attributes.append(2)
        #  LCPOptions
        if all_ or not self.isRead(3):
            attributes.append(3)
        #  IPCPOptions
        if all_ or not self.isRead(4):
            attributes.append(4)
        #  PPPAuthentication
        if all_ or not self.isRead(5):
            attributes.append(5)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 5

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 0

    def getDataType(self, index):
        if index == 1:
            return DataType.OCTET_STRING
        if index == 2:
            return DataType.OCTET_STRING
        if index == 3:
            return DataType.ARRAY
        if index == 4:
            return DataType.ARRAY
        if index == 5:
            if not self.userName:
                return DataType.NONE
            return DataType.STRUCTURE
        raise ValueError("getDataType failed. Invalid attribute index.")

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = _GXCommon.logicalNameToBytes(self.phyReference)
        elif e.index == 3:
            data = GXByteBuffer()
            data.setUInt8(DataType.ARRAY)
            if not self.lcpOptions:
                data.setUInt8(0)
            else:
                data.setUInt8(len(self.lcpOptions))
                for it in self.lcpOptions:
                    data.setUInt8(DataType.STRUCTURE)
                    data.setUInt8(3)
                    _GXCommon.setData(settings, data, DataType.UINT8, it.type_.value)
                    _GXCommon.setData(settings, data, DataType.UINT8, it.length)
                    _GXCommon.setData(settings, data, _GXCommon.getDLMSDataType(it.data), it.data)
            ret = data.array()
        elif e.index == 4:
            data = GXByteBuffer()
            data.setUInt8(DataType.ARRAY)
            if not self.ipcpOptions:
                data.setUInt8(0)
            else:
                data.setUInt8(len(self.ipcpOptions))
                for it in self.ipcpOptions:
                    data.setUInt8(DataType.STRUCTURE)
                    data.setUInt8(3)
                    _GXCommon.setData(settings, data, DataType.UINT8, it.type_.value)
                    _GXCommon.setData(settings, data, DataType.UINT8, it.length)
                    _GXCommon.setData(settings, data, _GXCommon.getDLMSDataType(it.data), it.data)
            ret = data.array()
        elif e.index == 5:
            if self.userName:
                data = GXByteBuffer()
                data.setUInt8(DataType.STRUCTURE)
                data.setUInt8(2)
                _GXCommon.setData(settings, data, DataType.OCTET_STRING, self.userName)
                _GXCommon.setData(settings, data, DataType.OCTET_STRING, self.password)
                ret = data.array()
            else:
                ret = None
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.phyReference = _GXCommon.toLogicalName(e.value)
        elif e.index == 3:
            self.lcpOptions = []
            if e.value:
                for item in e.value:
                    it1 = GXDLMSPppSetupLcpOption()
                    it1.type_ = PppSetupLcpOptionType(item[0])
                    it1.length = item[1]
                    it1.data = item[2]
                    self.lcpOptions.append(it1)
        elif e.index == 4:
            self.ipcpOptions = []
            if e.value:
                for item in e.value:
                    it2 = GXDLMSPppSetupIPCPOption()
                    it2.type_ = item[0]
                    it2.length = item[1]
                    it2.data = item[2]
                    self.ipcpOptions.append(it2)
        elif e.index == 5:
            if e.value:
                self.userName = e.value[0]
                self.password = e.value[1]
            else:
                self.userName = None
                self.password = None
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.phyReference = reader.readElementContentAsString("PHYReference")
        self.lcpOptions = []
        if reader.isStartElement("LCPOptions", True):
            while reader.isStartElement("Item", True):
                it1 = GXDLMSPppSetupLcpOption()
                it1.type_ = PppSetupLcpOptionType(reader.readElementContentAsInt("Type"))
                it1.length = reader.readElementContentAsInt("Length")
                it1.data = reader.readElementContentAsObject("Data", None)
                self.lcpOptions.append(it1)
            reader.readEndElement("LCPOptions")

        self.ipcpOptions = []
        if reader.isStartElement("IPCPOptions", True):
            while reader.isStartElement("Item", True):
                it2 = GXDLMSPppSetupIPCPOption()
                it2.type_ = PppSetupIPCPOptionType(reader.readElementContentAsInt("Type"))
                it2.length = reader.readElementContentAsInt("Length")
                it2.data = reader.readElementContentAsObject("Data", None)
                self.ipcpOptions.append(it2)
            reader.readEndElement("IPCPOptions")
        self.userName = GXByteBuffer.hexToBytes(reader.readElementContentAsString("UserName"))
        self.password = GXByteBuffer.hexToBytes(reader.readElementContentAsString("Password"))

    def save(self, writer):
        writer.writeElementString("PHYReference", self.phyReference)
        writer.writeStartElement("LCPOptions")
        if self.lcpOptions:
            for it in self.lcpOptions:
                writer.writeStartElement("Item")
                writer.writeElementString("Type", it.type_)
                writer.writeElementString("Length", it.length)
                writer.writeElementObject("Data", it.data)
                writer.writeEndElement()
        writer.writeEndElement()
        writer.writeStartElement("IPCPOptions")
        if self.ipcpOptions:
            for it in self.ipcpOptions:
                writer.writeStartElement("Item")
                writer.writeElementString("Type", it.type_)
                writer.writeElementString("Length", it.length)
                writer.writeElementObject("Data", it.data)
                writer.writeEndElement()
        writer.writeEndElement()
        writer.writeElementString("UserName", GXByteBuffer.hex(self.userName))
        writer.writeElementString("Password", GXByteBuffer.hex(self.password))

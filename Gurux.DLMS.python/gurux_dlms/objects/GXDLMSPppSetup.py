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
            data.setUInt8(int(DataType.ARRAY.value))
            if not self.lcpOptions:
                data.setUInt8(0)
            else:
                data.setUInt8(len(self.lcpOptions))
                for it in self.lcpOptions:
                    data.setUInt8(DataType.STRUCTURE.value)
                    data.setUInt8(3)
                    _GXCommon.setData(data, DataType.UINT8, it.type_.value)
                    _GXCommon.setData(data, DataType.UINT8, it.length)
                    _GXCommon.setData(data, _GXCommon.getDLMSDataType(it.data), it.data)
            ret = data.array()
        elif e.index == 4:
            data = GXByteBuffer()
            data.setUInt8(int(DataType.ARRAY.value))
            if not self.ipcpOptions:
                data.setUInt8(0)
            else:
                data.setUInt8(len(self.ipcpOptions))
                for it in self.ipcpOptions:
                    data.setUInt8(DataType.STRUCTURE.value)
                    data.setUInt8(3)
                    _GXCommon.setData(data, DataType.UINT8, it.type_.value)
                    _GXCommon.setData(data, DataType.UINT8, it.length)
                    _GXCommon.setData(data, _GXCommon.getDLMSDataType(it.data), it.data)
            ret = data.array()
        elif e.index == 5:
            data = GXByteBuffer()
            data.setUInt8(int(DataType.STRUCTURE.value))
            data.setUInt8(2)
            _GXCommon.setData(data, DataType.OCTET_STRING, self.userName)
            _GXCommon.setData(data, DataType.OCTET_STRING, self.password)
            ret = data.array()
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
            self.lcpOptions.clear()
            if e.value:
                for item in e.value:
                    it = GXDLMSPppSetupLcpOption()
                    it.type_ = PppSetupLcpOptionType(item[0])
                    it.length = item[1]
                    it.data = item[2]
                    self.lcpOptions.append(it)
        elif e.index == 4:
            self.ipcpOptions.clear()
            if e.value:
                for item in e.value:
                    it = GXDLMSPppSetupIPCPOption()
                    it.type_ = PppSetupIPCPOptionType(item[0])
                    it.length = item[1]
                    it.data = item[2]
                    self.ipcpOptions.append(it)
        elif e.index == 5:
            self.userName = e.value[0]
            self.password = e.value[1]
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.phyReference = reader.readElementContentAsString("PHYReference")
        self.lcpOptions.clear()
        if reader.isStartElement("LCPOptions", True):
            while reader.isStartElement("Item", True):
                it = GXDLMSPppSetupLcpOption()
                it.type_ = PppSetupLcpOptionType(reader.readElementContentAsInt("Type"))
                it.length = reader.readElementContentAsInt("Length")
                it.data = reader.readElementContentAsObject("Data", None)
                self.lcpOptions.append(it)
            reader.readEndElement("LCPOptions")

        self.ipcpOptions.clear()
        if reader.isStartElement("IPCPOptions", True):
            while reader.isStartElement("Item", True):
                it = GXDLMSPppSetupIPCPOption()
                it.type_ = PppSetupIPCPOptionType(reader.readElementContentAsInt("Type"))
                it.length = reader.readElementContentAsInt("Length")
                it.data = reader.readElementContentAsObject("Data", None)
                self.ipcpOptions.append(it)
            reader.readEndElement("IPCPOptions")
        self.userName = GXByteBuffer.hexToBytes(reader.readElementContentAsString("UserName"))
        self.password = GXByteBuffer.hexToBytes(reader.readElementContentAsString("Password"))

    def save(self, writer):
        writer.writeElementString("PHYReference", self.phyReference)
        if self.lcpOptions:
            writer.writeStartElement("LCPOptions")
            for it in self.lcpOptions:
                writer.writeStartElement("Item")
                writer.writeElementString("Type", it.type_)
                writer.writeElementString("Length", it.length)
                writer.writeElementObject("Data", it.data)
                writer.writeEndElement()
            writer.writeEndElement()
        if self.ipcpOptions:
            writer.writeStartElement("IPCPOptions")
            for it in self.ipcpOptions:
                writer.writeStartElement("Item")
                writer.writeElementString("Type", it.type_)
                writer.writeElementString("Length", it.length)
                writer.writeElementObject("Data", it.data)
                writer.writeEndElement()
            writer.writeEndElement()
        writer.writeElementString("UserName", GXByteBuffer.hex(self.userName))
        writer.writeElementString("Password", GXByteBuffer.hex(self.password))

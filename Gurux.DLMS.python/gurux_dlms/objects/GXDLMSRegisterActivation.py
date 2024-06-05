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
from ..enums import ObjectType, DataType
from .GXDLMSObjectDefinition import GXDLMSObjectDefinition

# pylint: disable=too-many-instance-attributes
class GXDLMSRegisterActivation(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSRegisterActivation
    """

    #
    # Constructor.
    #
    # @param ln
    #            Logical Name of the object.
    # @param sn
    #            Short Name of the object.
    #
    def __init__(self, ln=None, sn=0):
        #pylint: disable=super-with-arguments
        super(GXDLMSRegisterActivation, self).__init__(ObjectType.REGISTER_ACTIVATION, ln, sn)
        self.registerAssignment = []
        self.maskList = []
        self.activeMask = bytearray()

    def addRegister(self, client, target):
        """Add new register."""
        bb = GXByteBuffer()
        bb.setUInt8(DataType.STRUCTURE)
        bb.setUInt8(2)
        _GXCommon.setData(None, bb, DataType.UINT16, target.objectType)
        _GXCommon.setData(None, bb, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(target.logicalName))
        return client.method(self, 1, bb.array(), DataType.ARRAY)

    def addMask(self, client, name, indexes):
        """Add new register activation mask."""
        bb = GXByteBuffer()
        bb.setUInt8(DataType.STRUCTURE)
        bb.setUInt8(2)
        _GXCommon.setData(None, bb, DataType.OCTET_STRING, name)
        bb.setUInt8(DataType.ARRAY)
        bb.setUInt8(len(indexes))
        for it in indexes:
            _GXCommon.setData(None, bb, DataType.UINT8, it)
        return client.method(self, 2, bb.array(), DataType.ARRAY)

    def removeMask(self, client, name):
        """Remove register activation mask."""
        return client.method(self, 3, name, DataType.OCTET_STRING)

    def getValues(self):
        return [self.logicalName,
                self.registerAssignment,
                self.maskList,
                self.activeMask]

    #
    # Returns collection of attributes to read.  If attribute is static
    #      and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = []
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        if all_ or not self.isRead(2):
            attributes.append(2)
        #  MaskList
        if all_ or not self.isRead(3):
            attributes.append(3)
        #  ActiveMask
        if all_ or not self.isRead(4):
            attributes.append(4)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 4

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 3

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.ARRAY
        elif index == 3:
            ret = DataType.ARRAY
        elif index == 4:
            ret = DataType.OCTET_STRING
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            return _GXCommon.logicalNameToBytes(self.logicalName)
        if e.index == 2:
            data = GXByteBuffer()
            data.setUInt8(DataType.ARRAY)
            if not self.registerAssignment:
                data.setUInt8(0)
            else:
                data.setUInt8(len(self.registerAssignment))
                for it in self.registerAssignment:
                    data.setUInt8(DataType.STRUCTURE)
                    data.setUInt8(2)
                    _GXCommon.setData(settings, data, DataType.UINT16, it.objectType)
                    _GXCommon.setData(settings, data, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(it.logicalName))
            return data
        if e.index == 3:
            data = GXByteBuffer()
            data.setUInt8(DataType.ARRAY)
            data.setUInt8(len(self.maskList))
            for k, v in self.maskList:
                data.setUInt8(DataType.STRUCTURE)
                data.setUInt8(2)
                _GXCommon.setData(settings, data, DataType.OCTET_STRING, k)
                data.setUInt8(DataType.ARRAY)
                data.setUInt8(len(v))
                for b in v:
                    _GXCommon.setData(settings, data, DataType.UINT8, b)
            return data
        if e.index == 4:
            return self.activeMask
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.registerAssignment = []
            if e.value:
                for it in e.value:
                    item = GXDLMSObjectDefinition()
                    item.objectType = ObjectType(it[0])
                    item.logicalName = _GXCommon.toLogicalName(it[1])
                    self.registerAssignment.append(item)
        elif e.index == 3:
            self.maskList = []
            if e.value:
                for it in e.value:
                    self.maskList.append((it[0], it[1]))
        elif e.index == 4:
            if not e.value:
                self.activeMask = None
            else:
                self.activeMask = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.registerAssignment = []
        if reader.isStartElement("RegisterAssignment", True):
            while reader.isStartElement("Item", True):
                it = GXDLMSObjectDefinition()
                it.objectType = ObjectType(reader.readElementContentAsInt("ObjectType"))
                it.logicalName = reader.readElementContentAsString("LN")
                self.registerAssignment.append(it)
        self.maskList = []
        if reader.isStartElement("MaskList", True):
            while reader.isStartElement("Item", True):
                mask = GXByteBuffer.hexToBytes(reader.readElementContentAsString("Mask"))
                str_ = reader.readElementContentAsString("Index")
                i = GXByteBuffer.hexToBytes(str_.replace(";", " "))
                self.maskList.append((mask, i))
            reader.readEndElement("MaskList")
        self.activeMask = GXByteBuffer.hexToBytes(reader.readElementContentAsString("ActiveMask"))

    def save(self, writer):
        if self.registerAssignment:
            writer.writeStartElement("RegisterAssignment")
            for it in self.registerAssignment:
                writer.writeStartElement("Item")
                writer.writeElementString("ObjectType", int(it.objectType))
                writer.writeElementString("LN", it.logicalName)
                writer.writeEndElement()
            writer.writeEndElement()

        if self.maskList:
            writer.writeStartElement("MaskList")
            for k, v in self.maskList:
                writer.writeStartElement("Item")
                writer.writeElementString("Mask", GXByteBuffer.hex(k))
                writer.writeElementString("Index", GXByteBuffer.hex(v).replace(" ", ";"))
                writer.writeEndElement()
            writer.writeEndElement()
        if self.activeMask:
            writer.writeElementString("ActiveMask", GXByteBuffer.hex(self.activeMask))

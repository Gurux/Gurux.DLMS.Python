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
from .GXDLMSTarget import GXDLMSTarget

# pylint: disable=too-many-instance-attributes
class GXDLMSParameterMonitor(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSParameterMonitor
    """
    def __init__(self, ln="0.0.16.2.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        super(GXDLMSParameterMonitor, self).__init__(ObjectType.PARAMETER_MONITOR, ln, sn)
        self.parameters = list()
        self.captureTime = None
        self.changedParameter = GXDLMSTarget()

    def getValues(self):
        return [self.logicalName,
                self.changedParameter,
                self.captureTime,
                self.parameters]

    #
    # Inserts a new entry in the table.
    #
    # @param client
    # DLMS Client.
    # @param entry
    # Removed entry.
    # If a special day with the same index or with the same date
    #      as an
    # already defined day is inserted, the old entry will be
    # overwritten.
    #
    def insert(self, client, entry):
        bb = GXByteBuffer()
        bb.setUInt8(DataType.STRUCTURE)
        bb.setUInt8(3)
        _GXCommon.setData(None, bb, DataType.UINT16, entry.target.objectType)
        _GXCommon.setData(None, bb, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(entry.target.logicalName))
        _GXCommon.setData(None, bb, DataType.INT8, entry.attributeIndex)
        return client.method(self, 1, bb.array(), DataType.ARRAY)

    def delete(self, client, entry):
        bb = GXByteBuffer()
        bb.setUInt8(DataType.STRUCTURE)
        bb.setUInt8(3)
        _GXCommon.setData(None, bb, DataType.UINT16, entry.target.objectType)
        _GXCommon.setData(None, bb, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(entry.target.logicalName))
        _GXCommon.setData(None, bb, DataType.INT8, entry.attributeIndex)
        return client.method(self, 2, bb.array(), DataType.ARRAY)

    def invoke(self, settings, e):
        if e.index != 1 and e.index != 2:
            e.error = ErrorCode.READ_WRITE_DENIED
        else:
            if e.index == 1:
                #pylint: disable=import-outside-toplevel
                from .._GXObjectFactory import _GXObjectFactory
                tmp = e.parameters
                type_ = ObjectType(tmp[0])
                ln = _GXCommon.toLogicalName(tmp[1])
                index = tmp[2]
                for item in self.parameters:
                    if item.target.objectType == type_ and item.target.logicalName == ln and item.attributeIndex == index:
                        self.parameters.remove(item)
                        break
                it = GXDLMSTarget()
                it.target = settings.objects.findByLN(type_, ln)
                if it.target is None:
                    it.target = _GXObjectFactory.createObject(type_)
                    it.target.logicalName = ln
                it.attributeIndex = index
                self.parameters.append(it)
            elif e.index == 2:
                tmp = e.parameters
                type_ = ObjectType(tmp[0])
                ln = _GXCommon.toLogicalName(tmp[1])
                index = tmp[2]
                for item in self.parameters:
                    if item.target.objectType == type_ and item.target.logicalName == ln and item.attributeIndex == index:
                        self.parameters.remove(item)
                        break

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
        return attributes

    def getAttributeCount(self):

        return 4

    def getMethodCount(self):

        return 2

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.STRUCTURE
        elif index == 3:
            ret = DataType.OCTET_STRING
        elif index == 4:
            ret = DataType.ARRAY
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret

    def getValue(self, settings, e):
        #pylint: disable=bad-option-value,redefined-variable-type
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            data = GXByteBuffer()
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(4)
            if self.changedParameter is None:
                _GXCommon.setData(settings, data, DataType.UINT16, 0)
                _GXCommon.setData(settings, data, DataType.OCTET_STRING, [0, 0, 0, 0, 0, 0])
                _GXCommon.setData(settings, data, DataType.INT8, 1)
                _GXCommon.setData(settings, data, DataType.NONE, None)
            else:
                _GXCommon.setData(settings, data, DataType.UINT16, self.changedParameter.target.objectType)
                _GXCommon.setData(settings, data, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(self.changedParameter.target.logicalName))
                _GXCommon.setData(settings, data, DataType.INT8, self.changedParameter.attributeIndex)
                _GXCommon.setData(settings, data, _GXCommon.getDLMSDataType(self.changedParameter.value), self.changedParameter.value)
            ret = data
        elif e.index == 3:
            ret = self.captureTime
        elif e.index == 4:
            data = GXByteBuffer()
            data.setUInt8(DataType.ARRAY)
            if self.parameters is None:
                data.setUInt8(0)
            else:
                data.setUInt8(len(self.parameters))
                for it in self.parameters:
                    data.setUInt8(DataType.STRUCTURE)
                    data.setUInt8(3)
                    _GXCommon.setData(settings, data, DataType.UINT16, it.target.objectType)
                    _GXCommon.setData(settings, data, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(it.target.logicalName))
                    _GXCommon.setData(settings, data, DataType.INT8, it.attributeIndex)
            ret = data
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    def setValue(self, settings, e):
        #pylint: disable=import-outside-toplevel
        from .._GXObjectFactory import _GXObjectFactory
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.changedParameter = GXDLMSTarget()
            if len(e.value) != 4:
                raise Exception("Invalid structure format.")
            type_ = ObjectType(e.value[0])
            ln = _GXCommon.toLogicalName(e.value[1])
            self.changedParameter.target = settings.objects.findByLN(type_, ln)
            if self.changedParameter.target is None:
                self.changedParameter.target = _GXObjectFactory.createObject(type_)
                self.changedParameter.target.logicalName = ln
            self.changedParameter.attributeIndex = e.value[2]
            self.changedParameter.value = e.value[3]
        elif e.index == 3:
            if e.value is None:
                self.captureTime = None
            else:
                if isinstance(e.value, bytearray):
                    self.captureTime = _GXCommon.changeType(settings, e.value, DataType.DATETIME)
                else:
                    self.captureTime = e.value
        elif e.index == 4:
            self.parameters = []
            if e.value:
                for i in e.value:
                    if len(i) != 3:
                        raise Exception("Invalid structure format.")
                    obj = GXDLMSTarget()
                    type_ = ObjectType(i[0])
                    ln = _GXCommon.toLogicalName(i[1])
                    obj.target = settings.objects.findByLN(type_, ln)
                    if obj.target is None:
                        obj.target = _GXObjectFactory.createObject(type_)
                        obj.target.logicalName = ln
                    obj.attributeIndex = i[2]
                    self.parameters.append(obj)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        #pylint: disable=import-outside-toplevel
        from .._GXObjectFactory import _GXObjectFactory
        self.changedParameter = GXDLMSTarget()
        if reader.isStartElement("ChangedParameter", True):
            ot = ObjectType(reader.readElementContentAsInt("Type"))
            ln = reader.readElementContentAsString("LN")
            self.changedParameter.target = reader.objects.findByLN(ot, ln)
            if self.changedParameter.target is None:
                self.changedParameter.target = _GXObjectFactory.createObject(ot)
                self.changedParameter.target.logicalName = ln
            self.changedParameter.attributeIndex = reader.readElementContentAsInt("Index")
            self.changedParameter.value = reader.readElementContentAsObject("Value", None)
            reader.readEndElement("ChangedParameter")
        self.captureTime = reader.readElementContentAsDateTime("Time")
        self.parameters = []
        if reader.isStartElement("Parameters", True):
            while reader.isStartElement("Item", True):
                obj = GXDLMSTarget()
                ot = ObjectType(reader.readElementContentAsInt("Type"))
                ln = reader.readElementContentAsString("LN")
                obj.target = reader.objects.findByLN(ot, ln)
                if obj.target is None:
                    obj.target = _GXObjectFactory.createObject(ot)
                    obj.target.logicalName = ln
                obj.attributeIndex = reader.readElementContentAsInt("Index")
                self.parameters.append(obj)
            reader.readEndElement("Parameters")

    def save(self, writer):
        if self.changedParameter and self.changedParameter.target:
            writer.writeStartElement("ChangedParameter")
            writer.writeElementString("Type", int(self.changedParameter.target.objectType))
            writer.writeElementString("LN", self.changedParameter.target.logicalName)
            writer.writeElementString("Index", self.changedParameter.attributeIndex)
            writer.writeElementObject("Value", self.changedParameter.value)
            writer.writeEndElement()
        writer.writeElementString("Time", self.captureTime)
        writer.writeStartElement("Parameters")
        for it in self.parameters:
            writer.writeStartElement("Item")
            writer.writeElementString("Type", int(it.target.objectType))
            writer.writeElementString("LN", it.target.logicalName)
            writer.writeElementString("Index", it.attributeIndex)
            writer.writeEndElement()
        writer.writeEndElement()

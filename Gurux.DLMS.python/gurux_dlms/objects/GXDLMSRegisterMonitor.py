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
from .GXDLMSMonitoredValue import GXDLMSMonitoredValue
from .GXDLMSActionSet import GXDLMSActionSet

# pylint: disable=too-many-instance-attributes
class GXDLMSRegisterMonitor(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSRegisterMonitor
    """
    def __init__(self, ln=None, sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        super(GXDLMSRegisterMonitor, self).__init__(ObjectType.REGISTER_MONITOR, ln, sn)
        self.thresholds = list()
        self.monitoredValue = GXDLMSMonitoredValue()
        self.actions = list()

    def getValues(self):
        return [self.logicalName,
                self.thresholds,
                self.monitoredValue,
                self.actions]

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
        #  Thresholds
        if all_ or not self.isRead(2):
            attributes.append(2)
        #  MonitoredValue
        if all_ or not self.isRead(3):
            attributes.append(3)
        #  Actions
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
        return 0

    def getDataType(self, index):
        if index == 1:
            return DataType.OCTET_STRING
        if index == 2:
            return super(GXDLMSRegisterMonitor, self).getDataType(index)
        if index == 3:
            return DataType.ARRAY
        if index == 4:
            return DataType.ARRAY
        raise ValueError("getDataType failed. Invalid attribute index.")

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            return _GXCommon.logicalNameToBytes(self.logicalName)
        if e.index == 2:
            return self.thresholds
        if e.index == 3:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.STRUCTURE)
            bb.setUInt8(3)
            #  ClassID
            _GXCommon.setData(settings, bb, DataType.UINT16, self.monitoredValue.objectType)
            #  LN.
            _GXCommon.setData(settings, bb, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(self.monitoredValue.logicalName))
            #  Attribute index.
            _GXCommon.setData(settings, bb, DataType.INT8, self.monitoredValue.attributeIndex)
            return bb
        if e.index == 4:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.STRUCTURE)
            if not self.actions:
                bb.setUInt8(0)
            else:
                bb.setUInt8(len(self.actions))
                for it in self.actions:
                    bb.setUInt8(DataType.STRUCTURE)
                    bb.setUInt8(2)
                    bb.setUInt8(DataType.STRUCTURE)
                    bb.setUInt8(2)
                    #  LN
                    _GXCommon.setData(settings, bb, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(it.actionUp.logicalName))
                    #  ScriptSelector
                    _GXCommon.setData(settings, bb, DataType.UINT16, it.actionUp.scriptSelector)
                    bb.setUInt8(DataType.STRUCTURE)
                    bb.setUInt8(2)
                    #  LN
                    _GXCommon.setData(settings, bb, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(it.actionDown.logicalName))
                    #  ScriptSelector
                    _GXCommon.setData(settings, bb, DataType.UINT16, it.actionDown.scriptSelector)
            return bb
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.thresholds = e.value
        elif e.index == 3:
            if self.monitoredValue is None:
                self.monitoredValue = GXDLMSMonitoredValue()
            self.monitoredValue.objectType = e.value[0]
            self.monitoredValue.logicalName = _GXCommon.toLogicalName(e.value[1])
            self.monitoredValue.attributeIndex = e.value[2]
        elif e.index == 4:
            self.actions = []
            if e.value:
                for as_ in e.value:
                    set_ = GXDLMSActionSet()
                    target = as_[0]
                    set_.actionUp.logicalName = _GXCommon.toLogicalName(target[0])
                    set_.actionUp.scriptSelector = target[1]
                    target = as_[1]
                    set_.actionDown.logicalName = _GXCommon.toLogicalName(target[0])
                    set_.actionDown.scriptSelector = target[1]
                    self.actions.append(set_)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.thresholds = []
        if reader.isStartElement("Thresholds", True):
            while reader.isStartElement("Value", False):
                it = reader.readElementContentAsObject("Value", None)
                self.thresholds.append(it)
            reader.readEndElement("Thresholds")
        if reader.isStartElement("MonitoredValue", True):
            self.monitoredValue.objectType = ObjectType(reader.readElementContentAsInt("ObjectType"))
            self.monitoredValue.logicalName = reader.readElementContentAsString("LN")
            self.monitoredValue.attributeIndex = reader.readElementContentAsInt("Index")
            reader.readEndElement("MonitoredValue")
        self.actions = []
        if reader.isStartElement("Actions", True):
            while reader.isStartElement("Item", True):
                it = GXDLMSActionSet()
                self.actions.append(it)
                if reader.isStartElement("Up", True):
                    it.actionUp.logicalName = reader.readElementContentAsString("LN", None)
                    it.actionUp.scriptSelector = reader.readElementContentAsInt("Selector")
                    reader.readEndElement("Up")
                if reader.isStartElement("Down", True):
                    it.actionDown.logicalName = reader.readElementContentAsString("LN", None)
                    it.actionDown.scriptSelector = reader.readElementContentAsInt("Selector")
                    reader.readEndElement("Down")
            reader.readEndElement("Actions")

    def save(self, writer):
        if self.thresholds:
            writer.writeStartElement("Thresholds")
            for it in self.thresholds:
                writer.writeElementObject("Value", it)
            writer.writeEndElement()
        if self.monitoredValue:
            writer.writeStartElement("MonitoredValue")
            writer.writeElementString("ObjectType", int(self.monitoredValue.objectType))
            writer.writeElementString("LN", self.monitoredValue.logicalName)
            writer.writeElementString("Index", self.monitoredValue.attributeIndex)
            writer.writeEndElement()
        if self.actions:
            writer.writeStartElement("Actions")
            for it in self.actions:
                writer.writeStartElement("Item")
                writer.writeStartElement("Up")
                writer.writeElementString("LN", it.actionUp.logicalName)
                writer.writeElementString("Selector", it.actionUp.scriptSelector)
                writer.writeEndElement()
                writer.writeStartElement("Down")
                writer.writeElementString("LN", it.actionDown.logicalName)
                writer.writeElementString("Selector", it.actionDown.scriptSelector)
                writer.writeEndElement()
                writer.writeEndElement()
            writer.writeEndElement()

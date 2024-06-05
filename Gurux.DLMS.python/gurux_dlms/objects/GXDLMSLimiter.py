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
from .GXDLMSEmergencyProfile import GXDLMSEmergencyProfile
from .GXDLMSActionItem import GXDLMSActionItem

# pylint: disable=too-many-instance-attributes
class GXDLMSLimiter(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSLimiter

    """
    def __init__(self, ln=None, sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        #pylint: disable=super-with-arguments
        super(GXDLMSLimiter, self).__init__(ObjectType.LIMITER, ln, sn)
        self.monitoredValue = None
        self.monitoredAttributeIndex = 0
        self.thresholdActive = None
        self.thresholdNormal = None
        self.thresholdEmergency = None
        self.minOverThresholdDuration = None
        self.minUnderThresholdDuration = None
        self.emergencyProfileGroupIDs = []
        self.emergencyProfileActive = None
        self.emergencyProfile = GXDLMSEmergencyProfile()
        self.actionOverThreshold = GXDLMSActionItem()
        self.actionUnderThreshold = GXDLMSActionItem()

    def getValues(self):
        return [self.logicalName,
                self.monitoredValue,
                self.thresholdActive,
                self.thresholdNormal,
                self.thresholdEmergency,
                self.minOverThresholdDuration,
                self.minUnderThresholdDuration,
                self.emergencyProfile,
                self.emergencyProfileGroupIDs,
                self.emergencyProfileActive,
                [self.actionOverThreshold, self.actionUnderThreshold]]

    def getAttributeIndexToRead(self, all_):
        attributes = []
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  MonitoredValue
        if all_ or self.canRead(2):
            attributes.append(2)
        #  ThresholdActive
        if all_ or self.canRead(3):
            attributes.append(3)
        #  ThresholdNormal
        if all_ or self.canRead(4):
            attributes.append(4)
        #  ThresholdEmergency
        if all_ or self.canRead(5):
            attributes.append(5)
        #  MinOverThresholdDuration
        if all_ or self.canRead(6):
            attributes.append(6)
        #  MinUnderThresholdDuration
        if all_ or self.canRead(7):
            attributes.append(7)
        #  EmergencyProfile
        if all_ or self.canRead(8):
            attributes.append(8)
        #  EmergencyProfileGroup
        if all_ or self.canRead(9):
            attributes.append(9)
        #  EmergencyProfileActive
        if all_ or self.canRead(10):
            attributes.append(10)
        #  Actions
        if all_ or self.canRead(11):
            attributes.append(11)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 11

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 0

    def getDataType(self, index):
        #pylint: disable=super-with-arguments
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.STRUCTURE
        elif index == 3:
            ret = super(GXDLMSLimiter, self).getDataType(index)
        elif index == 4:
            ret = super(GXDLMSLimiter, self).getDataType(index)
        elif index == 5:
            ret = super(GXDLMSLimiter, self).getDataType(index)
        elif index == 6:
            ret = DataType.UINT32
        elif index == 7:
            ret = DataType.UINT32
        elif index == 8:
            ret = DataType.STRUCTURE
        elif index == 9:
            ret = DataType.ARRAY
        elif index == 10:
            ret = DataType.BOOLEAN
        elif index == 11:
            ret = DataType.STRUCTURE
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret
    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        #pylint: disable=bad-option-value,redefined-variable-type
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            data = GXByteBuffer()
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(3)
            if self.monitoredValue is None:
                _GXCommon.setData(settings, data, DataType.UINT16, int(0))
                _GXCommon.setData(settings, data, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(None))
                _GXCommon.setData(settings, data, DataType.INT8, 0)
            else:
                _GXCommon.setData(settings, data, DataType.UINT16, int(self.monitoredValue.objectType))
                _GXCommon.setData(settings, data, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(self.monitoredValue.logicalName))
                _GXCommon.setData(settings, data, DataType.INT8, self.monitoredAttributeIndex)
            ret = data
        elif e.index == 3:
            ret = self.thresholdActive
        elif e.index == 4:
            ret = self.thresholdNormal
        elif e.index == 5:
            ret = self.thresholdEmergency
        elif e.index == 6:
            ret = self.minOverThresholdDuration
        elif e.index == 7:
            ret = self.minUnderThresholdDuration
        elif e.index == 8:
            data = GXByteBuffer()
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(3)
            _GXCommon.setData(settings, data, DataType.UINT16, self.emergencyProfile.id)
            _GXCommon.setData(settings, data, DataType.OCTET_STRING, self.emergencyProfile.activationTime)
            _GXCommon.setData(settings, data, DataType.UINT32, self.emergencyProfile.duration)
            ret = data
        elif e.index == 9:
            data = GXByteBuffer()
            data.setUInt8(DataType.ARRAY)
            data.setUInt8(len(self.emergencyProfileGroupIDs))
            for it in self.emergencyProfileGroupIDs:
                _GXCommon.setData(settings, data, DataType.UINT16, it)
            ret = data
        elif e.index == 10:
            ret = self.emergencyProfileActive
        elif e.index == 11:
            data = GXByteBuffer()
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(2)
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(2)
            _GXCommon.setData(settings, data, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(self.actionOverThreshold.logicalName))
            _GXCommon.setData(settings, data, DataType.UINT16, self.actionOverThreshold.scriptSelector)
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(2)
            _GXCommon.setData(settings, data, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(self.actionUnderThreshold.logicalName))
            _GXCommon.setData(settings, data, DataType.UINT16, self.actionUnderThreshold.scriptSelector)
            ret = data
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
            ot = e.value[0]
            ln = _GXCommon.toLogicalName(e.value[1])
            self.monitoredAttributeIndex = e.value[2]
            self.monitoredValue = settings.objects.findByLN(ot, ln)
        elif e.index == 3:
            self.thresholdActive = e.value
        elif e.index == 4:
            self.thresholdNormal = e.value
        elif e.index == 5:
            self.thresholdEmergency = e.value
        elif e.index == 6:
            self.minOverThresholdDuration = e.value
        elif e.index == 7:
            self.minUnderThresholdDuration = e.value
        elif e.index == 8:
            self.emergencyProfile.id = e.value[0]
            self.emergencyProfile.activationTime = _GXCommon.changeType(settings, e.value[1], DataType.DATETIME)
            self.emergencyProfile.duration = e.value[2]
        elif e.index == 9:
            self.emergencyProfileGroupIDs = []
            if e.value:
                for it in e.value:
                    self.emergencyProfileGroupIDs.append(it)
        elif e.index == 10:
            self.emergencyProfileActive = e.value
        elif e.index == 11:
            self.actionOverThreshold.logicalName = _GXCommon.toLogicalName(e.value[0][0])
            self.actionOverThreshold.scriptSelector = e.value[0][1]
            self.actionUnderThreshold.logicalName = _GXCommon.toLogicalName(e.value[1][0])
            self.actionUnderThreshold.scriptSelector = e.value[1][1]
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        #pylint: disable=import-outside-toplevel
        from .._GXObjectFactory import _GXObjectFactory
        if reader.isStartElement("MonitoredValue", True):
            ot = reader.readElementContentAsInt("ObjectType")
            ln = reader.readElementContentAsString("LN")
            if ot != ObjectType.NONE and ln:
                self.monitoredValue = reader.objects.findByLN(ot, ln)
                #  If item is not serialized yet.
                if self.monitoredValue is None:
                    self.monitoredValue = _GXObjectFactory.createObject(ot)
                    self.monitoredValue.logicalName = ln
            reader.readEndElement("MonitoredValue")
        self.thresholdActive = reader.readElementContentAsObject("ThresholdActive", None, self, 3)
        self.thresholdNormal = reader.readElementContentAsObject("ThresholdNormal", None, self, 4)
        self.thresholdEmergency = reader.readElementContentAsObject("ThresholdEmergency", None, self, 5)
        self.minOverThresholdDuration = reader.readElementContentAsInt("MinOverThresholdDuration")
        self.minUnderThresholdDuration = reader.readElementContentAsInt("MinUnderThresholdDuration")
        if reader.isStartElement("EmergencyProfile", True):
            self.emergencyProfile.id = reader.readElementContentAsInt("ID")
            self.emergencyProfile.activationTime = reader.readElementContentAsDateTime("Time")
            self.emergencyProfile.duration = reader.readElementContentAsInt("Duration")
            reader.readEndElement("EmergencyProfile")
        self.emergencyProfileGroupIDs = []
        if reader.isStartElement("EmergencyProfileGroupIDs", True):
            while reader.isStartElement("Value", False):
                self.emergencyProfileGroupIDs.append(reader.readElementContentAsInt("Value"))
            reader.readEndElement("EmergencyProfileGroupIDs")
        self.emergencyProfileActive = reader.readElementContentAsInt("Active") != 0
        if reader.isStartElement("ActionOverThreshold", True):
            self.actionOverThreshold.logicalName = reader.readElementContentAsString("LN")
            self.actionOverThreshold.scriptSelector = reader.readElementContentAsInt("ScriptSelector")
            reader.readEndElement("ActionOverThreshold")
        if reader.isStartElement("ActionUnderThreshold", True):
            self.actionUnderThreshold.logicalName = reader.readElementContentAsString("LN")
            self.actionUnderThreshold.scriptSelector = reader.readElementContentAsInt("ScriptSelector")
            reader.readEndElement("ActionUnderThreshold")

    def save(self, writer):
        if self.monitoredValue:
            writer.writeStartElement("MonitoredValue")
            writer.writeElementString("ObjectType", int(self.monitoredValue.objectType))
            writer.writeElementString("LN", self.monitoredValue.logicalName)
            writer.writeEndElement()
        writer.writeElementObject("ThresholdActive", self.thresholdActive, self.getDataType(3), self.getUIDataType(3))
        writer.writeElementObject("ThresholdNormal", self.thresholdNormal, self.getDataType(4), self.getUIDataType(4))
        writer.writeElementObject("ThresholdEmergency", self.thresholdEmergency, self.getDataType(5), self.getUIDataType(5))
        writer.writeElementString("MinOverThresholdDuration", self.minOverThresholdDuration)
        writer.writeElementString("MinUnderThresholdDuration", self.minUnderThresholdDuration)
        if self.emergencyProfile:
            writer.writeStartElement("EmergencyProfile")
            writer.writeElementString("ID", self.emergencyProfile.id)
            writer.writeElementString("Time", self.emergencyProfile.activationTime)
            writer.writeElementString("Duration", self.emergencyProfile.duration)
            writer.writeEndElement()
        writer.writeStartElement("EmergencyProfileGroupIDs")
        if self.emergencyProfileGroupIDs:
            for it in self.emergencyProfileGroupIDs:
                writer.writeElementString("Value", it)
        writer.writeEndElement()
        writer.writeElementString("Active", self.emergencyProfileActive)
        if self.actionOverThreshold:
            writer.writeStartElement("ActionOverThreshold")
            writer.writeElementString("LN", self.actionOverThreshold.logicalName)
            writer.writeElementString("ScriptSelector", self.actionOverThreshold.scriptSelector)
            writer.writeEndElement()
        if self.actionUnderThreshold:
            writer.writeStartElement("ActionUnderThreshold")
            writer.writeElementString("LN", self.actionUnderThreshold.logicalName)
            writer.writeElementString("ScriptSelector", self.actionUnderThreshold.scriptSelector)
            writer.writeEndElement()

    def postLoad(self, reader):
        #  Upload Monitored Value after load.
        if self.monitoredValue:
            target = reader.objects.findByLN(self.monitoredValue.objectType, self.monitoredValue.logicalName)
            if target != self.monitoredValue:
                self.monitoredValue = target

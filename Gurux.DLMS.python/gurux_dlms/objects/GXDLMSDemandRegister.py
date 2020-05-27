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
import math
import datetime
from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ErrorCode
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from ..enums import ObjectType, DataType, Unit

# pylint: disable=too-many-instance-attributes
class GXDLMSDemandRegister(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSDemandRegister
    """

    def __init__(self, ln=None, sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.DEMAND_REGISTER, ln, sn)
        self.currentAverageValue = None
        self.lastAverageValue = None
        self.scaler = 1
        self.unit = Unit.NONE
        self.status = None
        self.captureTime = None
        self.startTimeCurrent = None
        self.period = 0
        self.numberOfPeriods = 0

    def getValues(self):
        return [self.logicalName,
                self.currentAverageValue,
                self.lastAverageValue,
                [self.scaler, self.unit],
                self.status,
                self.captureTime,
                self.startTimeCurrent,
                self.period,
                self.numberOfPeriods]

    def reset(self, client):
        """Reset value."""
        return client.method(self.getName(), self.objectType, 1, 0, DataType.INT8)

    def nextPeriod(self, client):
        """Closes the current period and starts a new one."""
        return client.method(self.getName(), self.objectType, 2, 0, DataType.INT8)

    def invoke(self, settings, e):
        #  Resets the value to the default value.
        #  The default value is an instance specific constant.
        if e.index == 1:
            self.currentAverageValue = None
            self.lastAverageValue = None
            self.startTimeCurrent = self.captureTime = datetime.datetime.now()
        elif e.index == 2:
            self.lastAverageValue = self.currentAverageValue
            self.currentAverageValue = None
            self.startTimeCurrent = self.captureTime = datetime.datetime.now()
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def isRead(self, index):
        if index == 4:
            return self.unit != 0
        return super(GXDLMSDemandRegister, self).isRead(index)

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
        #  ScalerUnit
        if all_ or not self.isRead(4):
            attributes.append(4)
        #  CurrentAvarageValue
        if all_ or self.canRead(2):
            attributes.append(2)
        #  LastAvarageValue
        if all_ or self.canRead(3):
            attributes.append(3)
        #  Status
        if all_ or self.canRead(5):
            attributes.append(5)
        #  CaptureTime
        if all_ or self.canRead(6):
            attributes.append(6)
        #  StartTimeCurrent
        if all_ or self.canRead(7):
            attributes.append(7)
        #  Period
        if all_ or self.canRead(8):
            attributes.append(8)
        #  NumberOfPeriods
        if all_ or self.canRead(9):
            attributes.append(9)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 9

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 2

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = super(GXDLMSDemandRegister, self).getDataType(index)
        elif index == 3:
            ret = super(GXDLMSDemandRegister, self).getDataType(index)
        elif index == 4:
            ret = DataType.ARRAY
        elif index == 5:
            ret = super(GXDLMSDemandRegister, self).getDataType(index)
        elif index == 6:
            ret = DataType.OCTET_STRING
        elif index == 7:
            ret = DataType.OCTET_STRING
        elif index == 8:
            ret = DataType.UINT32
        elif index == 9:
            ret = DataType.UINT16
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret
    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.currentAverageValue
        elif e.index == 3:
            ret = self.lastAverageValue
        elif e.index == 4:
            data = GXByteBuffer()
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(2)
            _GXCommon.setData(settings, data, DataType.INT8, math.floor(math.log(self.scaler, 10)))
            _GXCommon.setData(settings, data, DataType.ENUM, int(self.unit))
            ret = data.array()
        elif e.index == 5:
            ret = self.status
        elif e.index == 6:
            ret = self.captureTime
        elif e.index == 7:
            ret = self.startTimeCurrent
        elif e.index == 8:
            ret = self.period
        elif e.index == 9:
            ret = self.numberOfPeriods
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    #
    # Set value of given attribute.
    # pylint: disable=broad-except
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            if self.scaler != 1 and e.value:
                try:
                    if settings.isServer:
                        self.currentAverageValue = e.value
                    else:
                        self.currentAverageValue = e.value * self.scaler
                except Exception:
                    #  Sometimes scaler is set for wrong Object type.
                    self.currentAverageValue = e.value
            else:
                self.currentAverageValue = e.value
        elif e.index == 3:
            if self.scaler != 1 and e.value:
                try:
                    if settings.isServer:
                        self.lastAverageValue = e.value
                    else:
                        self.lastAverageValue = e.value * self.scaler
                except Exception:
                    #  Sometimes scaler is set for wrong Object type.
                    self.lastAverageValue = e.value
            else:
                self.lastAverageValue = e.value
        elif e.index == 4:
            #  Set default values.
            if e.value is None:
                self.scaler = 1
                self.unit = Unit.NONE
            else:
                if len(e.value) != 2:
                    raise ValueError("setValue failed. Invalid scaler unit value.")
                self.scaler = math.pow(10, e.value[0])
                self.unit = Unit(e.value[1])
        elif e.index == 5:
            if e.value is None:
                self.status = None
            else:
                self.status = e.value
        elif e.index == 6:
            if e.value is None:
                self.captureTime = None
            else:
                tmp = None
                if isinstance(e.value, bytearray):
                    tmp = _GXCommon.changeType(settings, e.value, DataType.DATETIME)
                else:
                    tmp = e.value
                self.captureTime = tmp
        elif e.index == 7:
            if e.value is None:
                self.startTimeCurrent = None
            else:
                tmp = None
                if isinstance(e.value, bytearray):
                    tmp = _GXCommon.changeType(settings, e.value, DataType.DATETIME)
                else:
                    tmp = e.value
                self.startTimeCurrent = tmp
        elif e.index == 8:
            if e.value is None:
                self.period = 0
            else:
                self.period = e.value
        elif e.index == 9:
            if e.value is None:
                self.numberOfPeriods = 0
            else:
                self.numberOfPeriods = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.currentAverageValue = reader.readElementContentAsObject("CurrentAverageValue", None, self, 2)
        self.lastAverageValue = reader.readElementContentAsObject("LastAverageValue", None, self, 3)
        self.scaler = reader.readElementContentAsDouble("Scaler", 1)
        self.unit = Unit(reader.readElementContentAsInt("Unit"))
        self.status = reader.readElementContentAsObject("Status", None, self, 5)
        self.captureTime = reader.readElementContentAsDateTime("CaptureTime")
        self.startTimeCurrent = reader.readElementContentAsDateTime("StartTimeCurrent")
        self.period = reader.readElementContentAsInt("Period")
        self.numberOfPeriods = reader.readElementContentAsInt("NumberOfPeriods")

    def save(self, writer):
        writer.writeElementObject("CurrentAverageValue", self.currentAverageValue)
        writer.writeElementObject("LastAverageValue", self.lastAverageValue)
        writer.writeElementString("Scaler", self.scaler, 1)
        writer.writeElementString("Unit", int(self.unit))
        writer.writeElementObject("Status", self.status)
        writer.writeElementString("CaptureTime", self.captureTime)
        writer.writeElementString("StartTimeCurrent", self.startTimeCurrent)
        writer.writeElementString("Period", self.period)
        writer.writeElementString("NumberOfPeriods", self.numberOfPeriods)

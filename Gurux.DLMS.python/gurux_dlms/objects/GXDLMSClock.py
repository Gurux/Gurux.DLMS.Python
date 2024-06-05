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
from ..GXDateTime import GXDateTime
from ..enums import ObjectType, DataType, ClockStatus
from .enums import ClockBase

# pylint: disable=too-many-instance-attributes
class GXDLMSClock(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSClock
    """

    def __init__(self, ln="0.0.1.0.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.CLOCK, ln, sn)
        self.time = None
        self.timeZone = 0
        self.status = ClockStatus.OK
        self.deviation = 0
        self.begin = GXDateTime()
        self.end = GXDateTime()
        self.enabled = False
        self.clockBase = ClockBase.NONE

    def getUIDataType(self, index):
        if index in (2, 5, 6):
            return DataType.DATETIME
        #pylint: disable=super-with-arguments
        return super(GXDLMSClock, self).getUIDataType(index)

    def getValues(self):
        return [self.logicalName,
                self.time,
                self.timeZone,
                self.status,
                self.begin,
                self.end,
                self.deviation,
                self.enabled,
                self.clockBase]

    def invoke(self, settings, e):
        e.error = ErrorCode.READ_WRITE_DENIED

    #
    # Sets the meter's time to the nearest (+/-) quarter of an hour
    #      value
    # (*:00, *:15, *:30, *:45).
    #
    def adjustToQuarter(self, client):
        return client.method(self, 1, 0, DataType.INT8)

    def adjustToMeasuringPeriod(self, client):
        return client.method(self, 2, 0, DataType.INT8)

    def adjustToMinute(self, client):
        return client.method(self, 3, 0, DataType.INT8)

    def adjustToPresetTime(self, client):
        return client.method(self, 4, 0, DataType.INT8)

    def presetAdjustingTime(self, client, presetTime, validityIntervalStart, validityIntervalEnd):
        buff = GXByteBuffer(44)
        buff.setUInt8(DataType.STRUCTURE)
        buff.setUInt8(3)
        _GXCommon.setData(None, buff, DataType.OCTET_STRING, presetTime)
        _GXCommon.setData(None, buff, DataType.OCTET_STRING, validityIntervalStart)
        _GXCommon.setData(None, buff, DataType.OCTET_STRING, validityIntervalEnd)
        return client.method(self, 5, buff.array(), DataType.ARRAY)

    #
    # Shifts the time by n (-900 <= n <= 900) s.
    #
    def shiftTime(self, client, forTime):
        if forTime < -900 or forTime > 900:
            raise ValueError("Invalid shift time.")
        return client.method(self, 6, int(forTime), DataType.INT16)

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
        #  Time
        if all_ or self.canRead(2):
            attributes.append(2)
        #  TimeZone
        if all_ or not self.isRead(3):
            attributes.append(3)
        #  Status
        if all_ or self.canRead(4):
            attributes.append(4)
        #  Begin
        if all_ or not self.isRead(5):
            attributes.append(5)
        #  End
        if all_ or not self.isRead(6):
            attributes.append(6)
        #  Deviation
        if all_ or not self.isRead(7):
            attributes.append(7)
        #  Enabled
        if all_ or not self.isRead(8):
            attributes.append(8)
        #  ClockBase
        if all_ or not self.isRead(9):
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
        return 6

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.OCTET_STRING
        elif index == 3:
            ret = DataType.INT16
        elif index == 4:
            ret = DataType.UINT8
        elif index == 5:
            ret = DataType.OCTET_STRING
        elif index == 6:
            ret = DataType.OCTET_STRING
        elif index == 7:
            ret = DataType.INT8
        elif index == 8:
            ret = DataType.BOOLEAN
        elif index == 9:
            ret = DataType.ENUM
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
            ret = self.time
        elif e.index == 3:
            ret = int(self.timeZone)
        elif e.index == 4:
            ret = self.status
        elif e.index == 5:
            ret = self.begin
        elif e.index == 6:
            ret = self.end
        elif e.index == 7:
            ret = self.deviation
        elif e.index == 8:
            ret = self.enabled
        elif e.index == 9:
            ret = self.clockBase
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        #pylint: disable=bad-option-value,redefined-variable-type
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            if isinstance(e.value, bytearray):
                self.time = _GXCommon.changeType(settings, e.value, DataType.DATETIME)
            else:
                self.time = e.value
        elif e.index == 3:
            if e.value is None:
                self.timeZone = 0
            else:
                self.timeZone = e.value
        elif e.index == 4:
            if e.value is None:
                self.status = ClockStatus.OK
            else:
                self.status = e.value
        elif e.index == 5:
            if e.value is None:
                self.begin = GXDateTime()
            elif isinstance(e.value, bytearray):
                self.begin = _GXCommon.changeType(settings, e.value, DataType.DATETIME)
            else:
                self.begin = e.value
        elif e.index == 6:
            if e.value is None:
                self.end = GXDateTime()
            elif isinstance(e.value, bytearray):
                self.end = _GXCommon.changeType(settings, e.value, DataType.DATETIME)
            else:
                self.end = e.value
        elif e.index == 7:
            if e.value is None:
                self.deviation = 0
            else:
                self.deviation = e.value
        elif e.index == 8:
            if e.value is None:
                self.enabled = False
            else:
                self.enabled = e.value
        elif e.index == 9:
            if e.value is None:
                self.clockBase = ClockBase.NONE
            else:
                self.clockBase = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.time = reader.readElementContentAsDateTime("Time")
        self.timeZone = reader.readElementContentAsInt("TimeZone")
        self.status = ClockStatus(reader.readElementContentAsInt("Status"))
        self.begin = reader.readElementContentAsDateTime("Begin")
        self.end = reader.readElementContentAsDateTime("End")
        self.deviation = reader.readElementContentAsInt("Deviation")
        self.enabled = reader.readElementContentAsInt("Enabled") != 0
        self.clockBase = ClockBase(reader.readElementContentAsInt("ClockBase"))

    def save(self, writer):
        writer.writeElementString("Time", self.time)
        writer.writeElementString("TimeZone", self.timeZone)
        writer.writeElementString("Status", int(self.status))
        writer.writeElementString("Begin", self.begin)
        writer.writeElementString("End", self.end)
        writer.writeElementString("Deviation", self.deviation)
        writer.writeElementString("Enabled", self.enabled)
        writer.writeElementString("ClockBase", int(self.clockBase))

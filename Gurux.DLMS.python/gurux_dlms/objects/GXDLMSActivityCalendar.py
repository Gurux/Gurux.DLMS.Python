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
from ..GXDateTime import GXDateTime
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from ..enums import ObjectType, DataType
from .GXDLMSSeasonProfile import GXDLMSSeasonProfile
from .GXDLMSWeekProfile import GXDLMSWeekProfile
from .GXDLMSDayProfile import GXDLMSDayProfile
from .GXDLMSDayProfileAction import GXDLMSDayProfileAction

# pylint: disable=too-many-public-methods, too-many-instance-attributes
class GXDLMSActivityCalendar(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSActivityCalendar
    """

    def __init__(self, ln="0.0.13.0.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.ACTIVITY_CALENDAR, ln, sn)
        self.calendarNameActive = None
        self.seasonProfileActive = None
        self.weekProfileTableActive = None
        self.dayProfileTableActive = None
        self.calendarNamePassive = None
        self.seasonProfilePassive = None
        self.weekProfileTablePassive = None
        self.dayProfileTablePassive = None
        self.time = None
        self.isSec = False

    def getValues(self):
        return [self.logicalName,
                self.calendarNameActive,
                self.seasonProfileActive,
                self.weekProfileTableActive,
                self.dayProfileTableActive,
                self.calendarNamePassive,
                self.seasonProfilePassive,
                self.weekProfileTablePassive,
                self.dayProfileTablePassive,
                self.time]

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
        #  CalendarNameActive
        if all_ or self.canRead(2):
            attributes.append(2)
        #  SeasonProfileActive
        if all_ or self.canRead(3):
            attributes.append(3)
        #  WeekProfileTableActive
        if all_ or self.canRead(4):
            attributes.append(4)
        #  DayProfileTableActive
        if all_ or self.canRead(5):
            attributes.append(5)
        #  CalendarNamePassive
        if all_ or self.canRead(6):
            attributes.append(6)
        #  SeasonProfilePassive
        if all_ or self.canRead(7):
            attributes.append(7)
        #  WeekProfileTablePassive
        if all_ or self.canRead(8):
            attributes.append(8)
        #  DayProfileTablePassive
        if all_ or self.canRead(9):
            attributes.append(9)
        #  Time.
        if all_ or self.canRead(10):
            attributes.append(10)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 10

    #
    # This method copies all passive properties to the active.
    #
    def activatePassiveCalendar(self, client):
        return client.method(self, 1, int(0), DataType.INT8)

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 1

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.OCTET_STRING
        elif index == 3:
            ret = DataType.ARRAY
        elif index == 4:
            ret = DataType.ARRAY
        elif index == 5:
            ret = DataType.ARRAY
        elif index == 6:
            ret = DataType.OCTET_STRING
        elif index == 7:
            ret = DataType.ARRAY
        elif index == 8:
            ret = DataType.ARRAY
        elif index == 9:
            ret = DataType.ARRAY
        elif index == 10:
            if self.isSec:
                ret = DataType.DATETIME
            else:
                ret = DataType.OCTET_STRING
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret

    @classmethod
    def __getSeasonProfile(cls, settings, target):
        data = GXByteBuffer()
        data.setUInt8(DataType.ARRAY)
        if target is None:
            #  Add count
            _GXCommon.setObjectCount(0, data)
        else:
            #  Add count
            _GXCommon.setObjectCount(len(target), data)
            for it in target:
                data.setUInt8(DataType.STRUCTURE)
                data.setUInt8(3)
                _GXCommon.setData(settings, data, DataType.OCTET_STRING, it.name)
                _GXCommon.setData(settings, data, DataType.OCTET_STRING, it.start)
                _GXCommon.setData(settings, data, DataType.OCTET_STRING, it.weekName)
        return data.array()

    @classmethod
    def __getWeekProfileTable(cls, settings, target):
        data = GXByteBuffer()
        data.setUInt8(DataType.ARRAY)
        if target is None:
            #  Add count
            _GXCommon.setObjectCount(0, data)
        else:
            #  Add count
            _GXCommon.setObjectCount(len(target), data)
            for it in target:
                data.setUInt8(DataType.STRUCTURE)
                data.setUInt8(8)
                _GXCommon.setData(settings, data, DataType.OCTET_STRING, it.name)
                _GXCommon.setData(settings, data, DataType.UINT8, it.monday)
                _GXCommon.setData(settings, data, DataType.UINT8, it.tuesday)
                _GXCommon.setData(settings, data, DataType.UINT8, it.wednesday)
                _GXCommon.setData(settings, data, DataType.UINT8, it.thursday)
                _GXCommon.setData(settings, data, DataType.UINT8, it.friday)
                _GXCommon.setData(settings, data, DataType.UINT8, it.saturday)
                _GXCommon.setData(settings, data, DataType.UINT8, it.sunday)
        return data.array()

    @classmethod
    def __getDayProfileTable(cls, settings, target):
        data = GXByteBuffer()
        data.setUInt8(DataType.ARRAY)
        if target is None:
            #  Add count
            _GXCommon.setObjectCount(0, data)
        else:
            #  Add count
            _GXCommon.setObjectCount(len(target), data)
            for it in target:
                data.setUInt8(DataType.STRUCTURE)
                data.setUInt8(2)
                _GXCommon.setData(settings, data, DataType.UINT8, it.dayId)
                data.setUInt8(DataType.ARRAY)
                #  Add count
                _GXCommon.setObjectCount(len(it.daySchedules), data)
                for action in it.daySchedules:
                    data.setUInt8(DataType.STRUCTURE)
                    data.setUInt8(3)
                    _GXCommon.setData(settings, data, DataType.OCTET_STRING, action.startTime)
                    _GXCommon.setData(settings, data, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(action.scriptLogicalName))
                    _GXCommon.setData(settings, data, DataType.UINT16, int(action.scriptSelector))
        return data.array()

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            #pylint: disable=bad-option-value,redefined-variable-type
            if not self.calendarNameActive:
                ret = None
            elif self.isSec:
                ret = GXByteBuffer.hexToBytes(self.calendarNameActive)
            else:
                ret = self.calendarNameActive.encode("utf-8")
        elif e.index == 3:
            ret = self.__getSeasonProfile(settings, self.seasonProfileActive)
        elif e.index == 4:
            ret = self.__getWeekProfileTable(settings, self.weekProfileTableActive)
        elif e.index == 5:
            ret = self.__getDayProfileTable(settings, self.dayProfileTableActive)
        elif e.index == 6:
            if self.calendarNamePassive is None:
                ret = None
            elif self.isSec:
                ret = GXByteBuffer.hexToBytes(self.calendarNamePassive)
            else:
                ret = self.calendarNamePassive.encode()
        elif e.index == 7:
            ret = self.__getSeasonProfile(settings, self.seasonProfilePassive)
        elif e.index == 8:
            ret = self.__getWeekProfileTable(settings, self.weekProfileTablePassive)
        elif e.index == 9:
            ret = self.__getDayProfileTable(settings, self.dayProfileTablePassive)
        elif e.index == 10:
            ret = self.time
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    @classmethod
    def __setSeasonProfile(cls, settings, value):
        items = []
        if value:
            for item in value:
                it = GXDLMSSeasonProfile()
                it.name = item[0]
                it.start = _GXCommon.changeType(settings, item[1], DataType.DATETIME)
                it.weekName = item[2]
                items.append(it)
        return items

    @classmethod
    def __setWeekProfileTable(cls, value):
        items = []
        if value:
            for item in value:
                it = GXDLMSWeekProfile()
                it.name = item[0]
                it.monday = item[1]
                it.tuesday = item[2]
                it.wednesday = item[3]
                it.thursday = item[4]
                it.friday = item[5]
                it.saturday = item[6]
                it.sunday = item[7]
                items.append(it)
        return items

    @classmethod
    def __setDayProfileTable(cls, settings, value):
        items = []
        if value:
            for item in value:
                it = GXDLMSDayProfile()
                it.dayId = item[0]
                it.daySchedules = []
                for it2 in item[1]:
                    ac = GXDLMSDayProfileAction()
                    ac.startTime = _GXCommon.changeType(settings, it2[0], DataType.TIME)
                    ac.scriptLogicalName = _GXCommon.toLogicalName(it2[1])
                    ac.scriptSelector = it2[2]
                    it.daySchedules.append(ac)
                items.append(it)
        return items

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            if self.isSec or not GXByteBuffer.isAsciiString(e.value):
                self.calendarNameActive = GXByteBuffer.hex(e.value)
            else:
                self.calendarNameActive = e.value.decode("utf-8").strip('\x00')
        elif e.index == 3:
            self.seasonProfileActive = self.__setSeasonProfile(settings, e.value)
        elif e.index == 4:
            self.weekProfileTableActive = self.__setWeekProfileTable(e.value)
        elif e.index == 5:
            self.dayProfileTableActive = self.__setDayProfileTable(settings, e.value)
        elif e.index == 6:
            if self.isSec or not GXByteBuffer.isAsciiString(e.value):
                self.calendarNamePassive = GXByteBuffer.hex(e.value)
            else:
                self.calendarNamePassive = e.value.decode("utf-8").strip('\x00')
        elif e.index == 7:
            self.seasonProfilePassive = self.__setSeasonProfile(settings, e.value)
        elif e.index == 8:
            self.weekProfileTablePassive = self.__setWeekProfileTable(e.value)
        elif e.index == 9:
            self.dayProfileTablePassive = self.__setDayProfileTable(settings, e.value)
        elif e.index == 10:
            if isinstance(e.value, GXDateTime):
                self.time = e.value
            else:
                self.time = _GXCommon.changeType(settings, e.value, DataType.DATETIME)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    @classmethod
    def loadSeasonProfile(cls, reader, name):
        list_ = []
        if reader.isStartElement(name, True):
            while reader.isStartElement("Item", True):
                it = GXDLMSSeasonProfile()
                it.name = GXByteBuffer.hexToBytes(reader.readElementContentAsString("Name"))
                it.start = reader.readElementContentAsDateTime("Start")
                it.weekName = GXByteBuffer.hexToBytes(reader.readElementContentAsString("WeekName"))
                list_.append(it)
            reader.readEndElement(name)
        return list_

    @classmethod
    def loadWeekProfileTable(cls, reader, name):
        list_ = []
        if reader.isStartElement(name, True):
            while reader.isStartElement("Item", True):
                it = GXDLMSWeekProfile()
                it.name = GXByteBuffer.hexToBytes(reader.readElementContentAsString("Name"))
                it.monday = reader.readElementContentAsInt("Monday")
                it.tuesday = reader.readElementContentAsInt("Tuesday")
                it.wednesday = reader.readElementContentAsInt("Wednesday")
                it.thursday = reader.readElementContentAsInt("Thursday")
                it.friday = reader.readElementContentAsInt("Friday")
                it.saturday = reader.readElementContentAsInt("Saturday")
                it.sunday = reader.readElementContentAsInt("Sunday")
                list_.append(it)
            reader.readEndElement(name)
        return list_

    @classmethod
    def loadDayProfileTable(cls, reader, name):
        list_ = []
        if reader.isStartElement(name, True):
            while reader.isStartElement("Item", True):
                it = GXDLMSDayProfile()
                it.dayId = reader.readElementContentAsInt("DayId")
                list_.append(it)
                it.daySchedules = []
                if reader.isStartElement("Actions", True):
                    while reader.isStartElement("Action", True):
                        d = GXDLMSDayProfileAction()
                        it.daySchedules.append(d)
                        d.startTime = reader.readElementContentAsTime("Start")
                        d.scriptLogicalName = reader.readElementContentAsString("LN")
                        d.scriptSelector = reader.readElementContentAsInt("Selector")
                    reader.readEndElement("Actions")
            reader.readEndElement(name)
        return list_

    def load(self, reader):
        self.calendarNameActive = reader.readElementContentAsString("CalendarNameActive")
        self.seasonProfileActive = self.loadSeasonProfile(reader, "SeasonProfileActive")
        self.weekProfileTableActive = self.loadWeekProfileTable(reader, "WeekProfileTableActive")
        self.dayProfileTableActive = self.loadDayProfileTable(reader, "DayProfileTableActive")
        self.calendarNamePassive = reader.readElementContentAsString("CalendarNamePassive")
        self.seasonProfilePassive = self.loadSeasonProfile(reader, "SeasonProfilePassive")
        self.weekProfileTablePassive = self.loadWeekProfileTable(reader, "WeekProfileTablePassive")
        self.dayProfileTablePassive = self.loadDayProfileTable(reader, "DayProfileTablePassive")
        self.time = reader.readElementContentAsDateTime("Time")

    @classmethod
    def saveSeasonProfile(cls, writer, list_, name):
        if list_:
            writer.writeStartElement(name)
            for it in list_:
                writer.writeStartElement("Item")
                str_ = it.name
                if isinstance(str_, (bytearray, bytes)):
                    str_ = GXByteBuffer.hex(str_)
                writer.writeElementString("Name", str_)
                writer.writeElementString("Start", it.start)
                writer.writeElementString("WeekName", GXByteBuffer.hex(it.weekName))
                writer.writeEndElement()
            writer.writeEndElement()

    @classmethod
    def saveWeekProfileTable(cls, writer, list_, name):
        if list_:
            writer.writeStartElement(name)
            for it in list_:
                writer.writeStartElement("Item")
                writer.writeElementString("Name", GXByteBuffer.hex(it.name))
                writer.writeElementString("Monday", it.monday)
                writer.writeElementString("Tuesday", it.tuesday)
                writer.writeElementString("Wednesday", it.wednesday)
                writer.writeElementString("Thursday", it.thursday)
                writer.writeElementString("Friday", it.friday)
                writer.writeElementString("Saturday", it.saturday)
                writer.writeElementString("Sunday", it.sunday)
                writer.writeEndElement()
            writer.writeEndElement()

    @classmethod
    def saveDayProfileTable(cls, writer, list_, name):
        if list_:
            writer.writeStartElement(name)
            for it in list_:
                writer.writeStartElement("Item")
                writer.writeElementString("DayId", it.dayId)
                writer.writeStartElement("Actions")
                for d in it.daySchedules:
                    writer.writeStartElement("Action")
                    writer.writeElementString("Start", d.startTime)
                    writer.writeElementString("LN", d.scriptLogicalName)
                    writer.writeElementString("Selector", d.scriptSelector)
                    writer.writeEndElement()
                writer.writeEndElement()
                writer.writeEndElement()
            writer.writeEndElement()

    def save(self, writer):
        writer.writeElementString("CalendarNameActive", self.calendarNameActive)
        self.saveSeasonProfile(writer, self.seasonProfileActive, "SeasonProfileActive")
        self.saveWeekProfileTable(writer, self.weekProfileTableActive, "WeekProfileTableActive")
        self.saveDayProfileTable(writer, self.dayProfileTableActive, "DayProfileTableActive")
        writer.writeElementString("CalendarNamePassive", self.calendarNamePassive)
        self.saveSeasonProfile(writer, self.seasonProfilePassive, "SeasonProfilePassive")
        self.saveWeekProfileTable(writer, self.weekProfileTablePassive, "WeekProfileTablePassive")
        self.saveDayProfileTable(writer, self.dayProfileTablePassive, "DayProfileTablePassive")
        writer.writeElementString("Time", self.time)

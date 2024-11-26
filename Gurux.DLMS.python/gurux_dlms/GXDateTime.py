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
import datetime
import calendar
import time
from .enums import DateTimeSkips, ClockStatus, DateTimeExtraInfo
from .GXTimeZone import GXTimeZone


###Python 2 requires this
# pylint: disable=bad-option-value,old-style-class
class GXDateTime:
    def __init__(self, value=None, pattern=None):
        """
        Constructor.

        value: Date-time value.
        pattern: Date-time pattern that is used when value is a string.
        """
        self.extra = DateTimeExtraInfo.NONE
        self.skip = DateTimeSkips.NONE
        self.status = ClockStatus.OK
        self.dayOfWeek = 0
        if isinstance(value, datetime.datetime):
            if value.tzinfo is None:
                if time.localtime().tm_isdst:
                    # If DST is used.
                    tz = GXTimeZone(int(-time.altzone / 60))
                else:
                    tz = GXTimeZone(int(-time.timezone / 60))
                self.value = datetime.datetime(
                    value.year,
                    value.month,
                    value.day,
                    value.hour,
                    value.minute,
                    value.second,
                    0,
                    tzinfo=tz,
                )
            else:
                self.value = value
        elif isinstance(value, str):
            self.value = self.fromString(value, pattern)
        elif isinstance(value, GXDateTime):
            self.value = value.value
            self.skip = value.skip
            self.extra = value.extra
        elif not value:
            self.value = None
        else:
            raise ValueError("Invalid datetime value.")

    @classmethod
    def __isNumeric(cls, value):
        return "0" <= value <= "9"

    @classmethod
    def __get_pattern(cls, loading):
        tm = datetime.datetime(1901, 2, 3, 13, 14, 15)
        pm = tm.strftime("%p")
        date = tm.strftime("%x")
        for s in date:
            if s < "0" or s > "9":
                sep = s
                break
        dp = ""
        tp = ""
        appendPM = ""
        date = date.replace(" ", sep).replace(" ", "")
        for d in date.split(sep):
            if not cls.__isNumeric(d):
                if d == "" and sep != ".":
                    d = "."
                appendPM += d
                continue
            dp += sep
            tmp = int(d)
            if tmp in (1901, 1):
                if loading:
                    dp += "%Y"
                elif len(d) == 2:
                    dp += "%y"
                elif len(d) == 1:
                    dp += "%-y"
                else:
                    dp += "%Y"
            elif tmp == 2:
                if len(d) == 2 or loading:
                    dp += "%m"
                else:
                    dp += "%-m"
            elif tmp == 3:
                if len(d) == 2 or loading:
                    dp += "%d"
                else:
                    dp += "%-d"

        date = tm.strftime("%X").replace(pm, "").replace(" ", "")
        for s in date:
            if s < "0" or s > "9":
                sep = s
                break
        for t in date.split(sep):
            tp += sep
            tmp = int(t)
            if tmp in (13, 1):
                if len(t) == 2 or loading:
                    tp += "%H"
                else:
                    tp += "%-H"
            elif tmp == 14:
                if len(t) == 2 or loading:
                    tp += "%M"
                else:
                    tp += "%-M"
            elif tmp == 15:
                if len(t) == 2 or loading:
                    tp += "%S"
                else:
                    tp += "%-S"
        if not pm or tm.strftime("%c").find(pm) == -1:
            return dp[1:] + appendPM + " " + tp[1:]
        tp = tp.replace("H", "I")
        if not appendPM:
            return dp[1:] + " " + tp[1:] + " " + pm
        return dp[1:] + " " + appendPM + " " + tp[1:]

    # Check is time zone included and return index of time zone.
    @classmethod
    def __timeZonePosition(cls, value):
        if len(value) > 5:
            pos = len(value) - 6
            sep = value[pos]
            if sep in ("-", "+"):
                return pos
            if value[len(value) - 1] == "Z":
                return len(value) - 1
        return -1

    #
    # Constructor
    #
    # @param value
    #            Date time value as a string.
    # pylint: disable=too-many-nested-blocks
    def fromString(self, value, pattern=None):
        if self.skip is None:
            self.skip = DateTimeSkips.NONE
        if self.status is None:
            self.status = ClockStatus.OK
        if self.extra is None:
            self.extra = DateTimeExtraInfo.NONE
        if value:
            if not pattern:
                pattern = self.__get_pattern(True)
            pattern = self._remove(pattern)
            if value.find("BEGIN") != -1:
                self.extra |= DateTimeExtraInfo.DST_BEGIN
                value = value.replace("BEGIN", "01")
            if value.find("END") != -1:
                self.extra |= DateTimeExtraInfo.DST_END
                value = value.replace("END", "01")
            if value.find("LASTDAY2") != -1:
                self.extra |= DateTimeExtraInfo.LAST_DAY2
                value = value.replace("LASTDAY2", "01")
            if value.find("LASTDAY") != -1:
                self.extra |= DateTimeExtraInfo.LAST_DAY
                value = value.replace("LASTDAY", "01")
            v = value
            # Time zone is not added to time or date objects.
            addTimeZone = type(self).__name__ == GXDateTime.__name__
            if value.find("*") != -1:
                lastFormatIndex = -1
                pos = 0
                while pos < len(value):
                    c = value[pos]
                    if not self.__isNumeric(c):
                        if c == "*":
                            end = lastFormatIndex + 1
                            c = pattern[end]
                            while end + 1 < len(pattern) and pattern[end] == c:
                                end += 1
                            if pattern[end] == "Y":
                                v = str(v[0:pos]) + "Y" + str(v[pos + 1 :])
                            elif pattern[end] == "%-Y":
                                v = str(v[0:pos]) + "Y" + str(v[pos + 1 :])
                            elif pattern[end] == "%Y":
                                v = str(v[0:pos]) + "Y" + str(v[pos + 1 :])
                            else:
                                v = str(v[0:pos]) + "1" + str(v[pos + 1 :])
                            tmp = pattern[lastFormatIndex + 1 : end + 1].strip()
                            if tmp in ("%y", "%-y", "%Y", "%-Y"):
                                addTimeZone = False
                                self.skip |= DateTimeSkips.YEAR
                            elif tmp in ("%m", "%-m"):
                                addTimeZone = False
                                self.skip |= DateTimeSkips.MONTH
                            elif tmp in ("%d", "%-d"):
                                addTimeZone = False
                                self.skip |= DateTimeSkips.DAY
                            elif tmp in ("%H", "%-H"):
                                addTimeZone = False
                                self.skip |= DateTimeSkips.HOUR
                                pos2 = pattern.find("%p")
                                if pos2 != -1:
                                    pattern.replace(pos2, pos2 + 1, "")
                            elif tmp in ("%M", "%-M"):
                                addTimeZone = False
                                self.skip |= DateTimeSkips.MINUTE
                            elif tmp in ("%S", "%-S"):
                                self.skip |= DateTimeSkips.SECOND
                            elif tmp and not tmp == "G":
                                raise ValueError("Invalid date time format.")
                        else:
                            lastFormatIndex = pattern.find(str(c), lastFormatIndex + 1)
                    pos += 1
                v = v.replace("Y", "2000")
            self.skip |= DateTimeSkips.DAY_OF_WEEK | DateTimeSkips.MILLISECOND
            # If time zone is used.
            if addTimeZone:
                pos = self.__timeZonePosition(v)
                tz = None
                if pos != -1:
                    if v[pos] != "Z":
                        tz = 60 * int(v[pos + 1 : pos + 3]) + int(v[pos + 4 :])
                    else:
                        tz = 0
                    v = v[0:pos]
                tmp = datetime.datetime.strptime(v, pattern)
                if tz is None:
                    tmp = datetime.datetime(
                        tmp.year,
                        tmp.month,
                        tmp.day,
                        tmp.hour,
                        tmp.minute,
                        tmp.second,
                        0,
                    )
                else:
                    tmp = datetime.datetime(
                        tmp.year,
                        tmp.month,
                        tmp.day,
                        tmp.hour,
                        tmp.minute,
                        tmp.second,
                        0,
                        tzinfo=GXTimeZone(tz),
                    )
                return tmp
            return datetime.datetime.strptime(v.strip(), pattern.strip())
        return None

    # pylint: disable=no-self-use
    def _remove(self, format_):
        # Do nothing.
        return format_

    def toFormatString(self, pattern=None):
        return self.__toFormatString(True, pattern)

    def toFormatMeterString(self, pattern=None):
        return self.__toFormatString(False, pattern)

    @classmethod
    def __toLocal(cls, value):
        # Convert current time to local.
        if value.tzinfo is None:
            # If meter is not use time zone.
            return value
        timestamp = calendar.timegm(value.utctimetuple())
        local_dt = datetime.datetime.fromtimestamp(timestamp)
        assert value.resolution >= datetime.timedelta(microseconds=1)
        return local_dt.replace(microsecond=value.microsecond)

    def __getTimeZone(self):
        if self.value.tzinfo:
            return self.value.tzname()
        return ""

    def __toFormatString(self, useLocalTime, pattern=None):
        if not self.value:
            return ""
        if self.skip != DateTimeSkips.NONE:
            #  Separate date and time parts.
            if not pattern:
                pattern = self.__get_pattern(True)
            pattern = self._remove(pattern)

            if self.extra & DateTimeExtraInfo.DST_BEGIN != 0:
                pattern = self._replace(pattern, "%m", "BEGIN")
                pattern = self._replace(pattern, "%-m", "BEGIN")
            elif self.extra & DateTimeExtraInfo.DST_END != 0:
                pattern = self._replace(pattern, "%m", "END")
                pattern = self._replace(pattern, "%-m", "END")
            elif self.extra & DateTimeExtraInfo.LAST_DAY != 0:
                pattern = self._replace(pattern, "%d", "LASTDAY")
                pattern = self._replace(pattern, "%-d", "LASTDAY")
            elif self.extra & DateTimeExtraInfo.LAST_DAY2 != 0:
                pattern = self._replace(pattern, "%d", "LASTDAY2")
                pattern = self._replace(pattern, "%-d", "LASTDAY2")

            if self.skip & DateTimeSkips.YEAR != DateTimeSkips.NONE:
                pattern = self._replace(pattern, "%y", "*")
                pattern = self._replace(pattern, "%-y", "*")
                pattern = self._replace(pattern, "%-Y", "*")
                pattern = self._replace(pattern, "%Y", "*")
            if self.skip & DateTimeSkips.MONTH != DateTimeSkips.NONE:
                pattern = self._replace(pattern, "%m", "*")
                pattern = self._replace(pattern, "%-m", "*")
            if self.skip & DateTimeSkips.DAY != DateTimeSkips.NONE:
                pattern = self._replace(pattern, "%d", "*")
                pattern = self._replace(pattern, "%-d", "*")
            if self.skip & DateTimeSkips.HOUR != DateTimeSkips.NONE:
                pattern = self._replace(pattern, "%H", "*")
                pattern = self._replace(pattern, "%-H", "*")
                pattern = self._replace(pattern, "%I", "*")
                pattern = self._replace(pattern, "%-I", "*")
                pattern = self._remove_(pattern, "p", False)
            if self.skip & DateTimeSkips.MILLISECOND != DateTimeSkips.NONE:
                pattern = self._replace(pattern, "%f", "*")
            else:
                index = pattern.find("%S")
                if index != -1:
                    sep = pattern[index - 1]
                    pattern.replace("%S", "%S" + sep + "%f")
                else:
                    index = pattern.find("%-S")
                    if index != -1:
                        sep = pattern[index - 1]
                        pattern.replace("%-S", "%-S" + sep + "%f")
            if self.skip & DateTimeSkips.SECOND != DateTimeSkips.NONE:
                pattern = self._replace(pattern, "%S", "*")
                pattern = self._replace(pattern, "%-S", "*")
            else:
                index = pattern.find("%M")
                if index != -1:
                    sep = pattern[index - 1]
                    pattern.replace("%M", "%M" + sep + "%S")
            if self.skip & DateTimeSkips.MINUTE != DateTimeSkips.NONE:
                pattern = self._replace(pattern, "%M", "*")
                pattern = self._replace(pattern, "%-M", "*")

            if useLocalTime:
                return self.__toLocal(self.value).strftime(pattern)
            return self.value.strftime(pattern) + self.__getTimeZone()
        if pattern:
            if useLocalTime:
                return self.__toLocal(self.value).strftime(pattern)
            return self.value.strftime(pattern) + self.__getTimeZone()
        if useLocalTime:
            return self.__toLocal(self.value).strftime("%x %X")
        return self.value.strftime(self.__get_pattern(True)) + self.__getTimeZone()

    @classmethod
    def _remove_(cls, value, tag, removeSeparator):
        pos = value.find(tag)
        if pos != -1:
            len_ = pos + len(tag)
            if pos != 0 and removeSeparator:
                pos -= 1
            value = value[0:pos] + value[len_:]
        return value

    @classmethod
    def _replace(cls, value, tag, replacement):
        pos = value.find(tag)
        if pos != -1:
            value = value.replace(tag, replacement)
        return value

    def __str__(self):
        # Returns date-time of the meter using local time zone.
        return self.__toString(True)

    def toString(self, pattern=None):
        return self.__toString(True, pattern)

    def toMeterString(self, pattern=None):
        # Returns date-time of the meter using meter time zone.
        return self.__toString(False, pattern)

    def __toString(self, useLocalTime, pattern=None):
        if not self.value:
            return ""
        if self.skip != DateTimeSkips.NONE:
            #  Separate date and time parts.
            if not pattern:
                pattern = self.__get_pattern(False)
            pattern = self._remove(pattern)
            if self.skip & DateTimeSkips.YEAR != DateTimeSkips.NONE:
                pattern = self._remove_(pattern, "%Y", True)
                pattern = self._remove_(pattern, "%y", True)
                pattern = self._remove_(pattern, "%-y", True)
                pattern = self._remove_(pattern, "%-Y", True)
            if self.skip & DateTimeSkips.MONTH != DateTimeSkips.NONE:
                pattern = self._remove_(pattern, "%m", True)
                pattern = self._remove_(pattern, "%-m", True)
            if self.skip & DateTimeSkips.DAY != DateTimeSkips.NONE:
                pattern = self._remove_(pattern, "%d", True)
                pattern = self._remove_(pattern, "%-d", True)
            if self.skip & DateTimeSkips.HOUR != DateTimeSkips.NONE:
                pattern = self._remove_(pattern, "%H", True)
                pattern = self._remove_(pattern, "%-H", True)
                pattern = self._remove_(pattern, "%p", True)
            if self.skip & DateTimeSkips.MILLISECOND != DateTimeSkips.NONE:
                pattern = self._remove_(pattern, "%f", True)
            else:
                index = pattern.find("%S")
                if index != -1:
                    sep = pattern[index - 1]
                    pattern = pattern.replace("%S", "%S" + sep + "%f")
                else:
                    index = pattern.find("%-S")
                    if index != -1:
                        sep = pattern[index - 1]
                        pattern = pattern.replace("%-S", "%-S" + sep + "%f")
            if self.skip & DateTimeSkips.SECOND != DateTimeSkips.NONE:
                pattern = self._remove_(pattern, "%S", True)
                pattern = self._remove_(pattern, "%-S", True)
            else:
                index = pattern.find("%M")
                if index == -1:
                    index = pattern.find("%-M")
                    if index != -1:
                        sep = pattern[index - 1]
                        pattern.replace("%-M", "%-M" + sep + "-S")
                    else:
                        sep = pattern[index - 1]
                        pattern.replace("%M", "%M" + sep + "S")
            if self.skip & DateTimeSkips.MINUTE != DateTimeSkips.NONE:
                pattern = self._remove_(pattern, "%M", True)
                pattern = self._remove_(pattern, "%-M", True)
            if useLocalTime:
                return self.__toLocal(self.value).strftime(pattern.strip())
            return self.value.strftime(pattern.strip()) + self.__getTimeZone()
        if pattern:
            if useLocalTime:
                return self.__toLocal(self.value).strftime(pattern)
            return self.value.strftime(pattern) + self.__getTimeZone()
        if useLocalTime:
            return self.__toLocal(self.value).strftime("%x %X")
        return self.value.strftime("%x %X") + self.__getTimeZone()

    #
    # Get difference between given time and run time in ms.
    #
    # @param start
    #            Start date time.
    # @param to
    #            Compared time.
    # Difference in milliseconds.
    #
    @classmethod
    def getDifference(cls, start, to):
        diff = 0
        cal = to.value
        #  Compare seconds.
        if to.skip & DateTimeSkips.SECOND == DateTimeSkips.NONE:
            if start.second < cal.second:
                diff += (cal.second - start.second) * 1000
            else:
                diff -= (start.second - cal.second) * 1000
        elif diff < 0:
            diff += 60000
        #  Compare minutes.
        if to.skip & DateTimeSkips.MINUTE == DateTimeSkips.NONE:
            if start.minute < cal.minute:
                diff += (cal.minute - start.minute) * 60000
            else:
                diff -= (start.minute - cal.minute) * 60000
        elif diff < 0:
            diff += 60 * 60000
        #  Compare hours.
        if to.skip & DateTimeSkips.HOUR == DateTimeSkips.NONE:
            if start.hour < cal.hour:
                diff += (cal.hour - start.hour) * 60 * 60000
            else:
                diff -= (start.hour - cal.hour) * 60 * 60000
        elif diff < 0:
            diff += 60 * 60000
        #  Compare days.
        if to.skip & DateTimeSkips.DAY == DateTimeSkips.NONE:
            if start.day < cal.day:
                diff += (cal.day - start.day) * 24 * 60 * 60000
            elif start.day != cal.day:
                if not to.skip & DateTimeSkips.DAY != DateTimeSkips.NONE:
                    if to.extra & DateTimeExtraInfo.LAST_DAY:
                        diff += (
                            (cls.daysInMonth(start.year, start.month) - start.day)
                            * 24
                            * 60
                            * 60000
                        )
                    elif to.extra & DateTimeExtraInfo.LAST_DAY2:
                        diff += (
                            (cls.daysInMonth(start.year, start.month) - 1 - start.day)
                            * 24
                            * 60
                            * 60000
                        )
                    else:
                        diff += (cal.day - start.day) * 24 * 60 * 60000
                else:
                    diff += (
                        (cls.daysInMonth(start.year, start.month) - start.day + cal.day)
                        * 24
                        * 60
                        * 60000
                    )
        elif diff < 0:
            diff += 24 * 60 * 60000
        #  Compare months.
        if to.skip & DateTimeSkips.MONTH == DateTimeSkips.NONE:
            if start.month < cal.month:
                m = start.month
                while m != cal.month:
                    diff += cls.daysInMonth(start.year, m) * 24 * 60 * 60000
                    m += 1
            else:
                m = cal.month
                while m != start.month:
                    diff -= cls.daysInMonth(start.year, m) * 24 * 60 * 60000
                    m += 1
        elif diff < 0:
            diff = cls.daysInMonth(start.year, start.month) * 24 * 60 * 60000 + diff
        #  Compare years.
        if to.skip & DateTimeSkips.YEAR == DateTimeSkips.NONE:
            if start.year < cal.year:
                y = start.year
                while y != cal.year:
                    for m in range(1, 13):
                        diff += cls.daysInMonth(y, m) * 24 * 60 * 60000
                    y += 1
            else:
                y = cal.year
                while y != start.year:
                    for m in range(1, 13):
                        diff -= cls.daysInMonth(y, m) * 24 * 60 * 60000
                    y += 1
        elif diff < 0:
            for m in range(1, 13):
                diff += cls.daysInMonth(start.year, m) * 24 * 60 * 60000
        return diff

    #
    # Get the number of days in that month.
    #
    # year
    # Year.
    # month
    # Month.
    # Number of days in month.
    #
    @classmethod
    def daysInMonth(cls, year, month):
        return calendar.monthrange(year, month)[1]

    #
    # Get date time from Epoch time.
    #
    # @param unixTime
    #            Unix time.
    # Date and time.
    #
    @classmethod
    def fromUnixTime(cls, unixTime):
        return GXDateTime(datetime.datetime(unixTime * 1000))

    #
    # Convert date time to Epoch time.
    #
    # @param value
    #            Date and time.
    # Returns unix time.
    #
    @classmethod
    def toUnixTime(cls, value):
        if isinstance(value, (datetime.datetime)):
            return value.utctimetuple()
        if isinstance(value, (GXDateTime)):
            return value.value.utctimetuple()
        return int(value.value / 1000)

    #
    # Get date time from high resolution clock time.
    #
    # highResolution:  High resolution clock time is milliseconds since 1970-01-01 00:00:00.
    # Returns Date and time.
    #
    @classmethod
    def fromHighResolutionTime(cls, unixTime):
        return GXDateTime(datetime.datetime(unixTime))

    #
    # Convert date time to high resolution time.
    #
    # @param value
    #            Date and time.
    # Returns high resolution time.
    #
    @classmethod
    def toHighResolutionTime(cls, value):
        if isinstance(value, datetime.datetime):
            return value.utctimetuple() * 1000.0
        if isinstance(value, GXDateTime):
            return value.value.utctimetuple() * 1000.0
        return int(value.value)

    #
    # Get date time as hex string.
    #
    # @param addSpace
    #           Add space between bytes.
    # @param useMeterTimeZone
    #           Date-Time values are shown using meter's time zone and it's not localized to use PC time.</param>
    # Returns date time as a hex string.
    #
    def toHex(self, addSpace, useMeterTimeZone):
        # pylint: disable=import-outside-toplevel
        from .GXByteBuffer import GXByteBuffer
        from .enums import DataType
        from .internal._GXCommon import _GXCommon
        from .GXDLMSSettings import GXDLMSSettings

        buff = GXByteBuffer()
        settings = GXDLMSSettings(False, None)
        settings.UseUtc2NormalTime = useMeterTimeZone
        _GXCommon.setData(settings, buff, DataType.OCTET_STRING, self)
        # Dont add data type or length.
        return buff.toHex(addSpace, 2)

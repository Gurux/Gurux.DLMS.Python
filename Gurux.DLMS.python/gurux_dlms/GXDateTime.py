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
from .enums import DateTimeSkips, ClockStatus, DateTimeExtraInfo

###Python 2 requires this
#pylint: disable=bad-option-value,old-style-class
class GXDateTime:
    #
    # Constructor.
    #
    # @param value
    #            Date value.
    #
    def __init__(self, value=None):
        self.extra = DateTimeExtraInfo.NONE
        self.skip = DateTimeSkips.NONE
        self.status = ClockStatus.OK
        self.dayOfWeek = 0
        if isinstance(value, datetime.datetime):
            self.value = value
        elif isinstance(value, str):
            self.value = self.fromString(value)
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
        return '0' <= value <= '9'

    @classmethod
    def __get_pattern(cls, loading):
        tm = datetime.datetime(1900, 2, 3, 13, 14, 15)
        pm = tm.strftime('%p')
        date = tm.strftime('%x')
        for s in date:
            if s < '0' or s > '9':
                sep = s
                break
        dp = ""
        tp = ""
        appendPM = ""
        date = date.replace(" ", sep).replace(" ", "")
        for d in date.split(sep):
            if not cls.__isNumeric(d):
                if d == '' and sep != '.':
                    d = '.'
                appendPM += d
                continue
            dp += sep
            tmp = int(d)
            if tmp == 1900:
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

        date = tm.strftime('%X').replace(pm, "").replace(" ", "")
        for s in date:
            if s < '0' or s > '9':
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
        if not pm or tm.strftime('%c').find(pm) == -1:
            return dp[1:] + appendPM + " " + tp[1:]
        tp = tp.replace("H", "I")
        if not appendPM:
            return dp[1:] + " " + tp[1:] + " " + pm
        return dp[1:] + " " + appendPM + " " + tp[1:]

    #
    # Constructor
    #
    # @param value
    #            Date time value as a string.
    #pylint: disable=too-many-nested-blocks
    def fromString(self, value):
        if self.skip is None:
            self.skip = DateTimeSkips.NONE
        if self.status is None:
            self.status = ClockStatus.OK
        if self.extra is None:
            self.extra = DateTimeExtraInfo.NONE
        if value:
            str_ = self.__get_pattern(True)
            str_ = self._remove(str_)
            v = value

            if value.find('BEGIN') != -1:
                self.extra |= DateTimeExtraInfo.DST_BEGIN
                v = v.replace("BEGIN", "01")
            if value.find("END") != -1:
                self.extra |= DateTimeExtraInfo.DST_END
                v = v.replace("END", "01")
            if value.find("LASTDAY2") != -1:
                self.extra |= DateTimeExtraInfo.LAST_DAY2
                v = v.replace("LASTDAY2", "01")
            if value.find("LASTDAY") != -1:
                self.extra |= DateTimeExtraInfo.LAST_DAY
                v = v.replace("LASTDAY", "01")

            if value.find('*') != -1:
                lastFormatIndex = -1
                pos = 0
                while pos < len(value):
                    c = value[pos]
                    if not self.__isNumeric(c):
                        if c == '*':
                            end = lastFormatIndex + 1
                            c = str_[end]
                            while end + 1 < len(str_) and str_[end] == c:
                                end += 1
                            v = str(v[0:pos]) + "1" + str(v[pos + 1:])
                            tmp = str_[lastFormatIndex + 1: end + 1].strip()
                            if tmp.startswith("y"):
                                self.skip |= DateTimeSkips.YEAR
                            elif tmp in ("%m", "%-m"):
                                self.skip |= DateTimeSkips.MONTH
                            elif tmp in ("%d", "%-d"):
                                self.skip |= DateTimeSkips.DAY
                            elif tmp in ("%H", "%-H"):
                                self.skip |= DateTimeSkips.HOUR
                                pos2 = str_.find("%p")
                                if pos2 != -1:
                                    str_.replace(pos2, pos2 + 1, "")
                            elif tmp in ("%M", "%-M"):
                                self.skip |= DateTimeSkips.MINUTE
                            elif tmp in ("%S", "%-S"):
                                self.skip |= DateTimeSkips.SECOND
                            elif tmp and not tmp == "G":
                                raise ValueError("Invalid date time format.")
                        else:
                            lastFormatIndex = str_.find(str(c), lastFormatIndex + 1)
                    pos += 1
                self.value = datetime.datetime.strptime(v, str_)
            self.skip |= DateTimeSkips.SECOND | DateTimeSkips.MILLISECOND
            return datetime.datetime.strptime(v, str_)
        return None

     #pylint: disable=no-self-use
    def _remove(self, format_):
        #Do nothing.
        return format_

    def toFormatString(self):
        if not self.value:
            return ""

        if self.skip != DateTimeSkips.NONE:
            #  Separate date and time parts.
            str_ = self.__get_pattern(True)
            str_ = self._remove(str_)

            if self.extra & DateTimeExtraInfo.DST_BEGIN != 0:
                str_ = self._replace(str_, "%m", "BEGIN")
                str_ = self._replace(str_, "%-m", "BEGIN")
            elif self.extra & DateTimeExtraInfo.DST_END != 0:
                str_ = self._replace(str_, "%m", "END")
                str_ = self._replace(str_, "%-m", "END")
            elif self.extra & DateTimeExtraInfo.LAST_DAY != 0:
                str_ = self._replace(str_, "%d", "LASTDAY")
                str_ = self._replace(str_, "%-d", "LASTDAY")
            elif self.extra & DateTimeExtraInfo.LAST_DAY2 != 0:
                str_ = self._replace(str_, "%d", "LASTDAY2")
                str_ = self._replace(str_, "%-d", "LASTDAY2")

            if self.skip & DateTimeSkips.YEAR != DateTimeSkips.NONE:
                str_ = self._replace(str_, "%y", "*")
                str_ = self._replace(str_, "%-y", "*")
            if self.skip & DateTimeSkips.MONTH != DateTimeSkips.NONE:
                str_ = self._replace(str_, "%m", "*")
                str_ = self._replace(str_, "%-m", "*")
            if self.skip & DateTimeSkips.DAY != DateTimeSkips.NONE:
                str_ = self._replace(str_, "%d", "*")
                str_ = self._replace(str_, "%-d", "*")
            if self.skip & DateTimeSkips.HOUR != DateTimeSkips.NONE:
                str_ = self._replace(str_, "%H", "*")
                str_ = self._replace(str_, "%-H", "*")
                str_ = self._replace(str_, "%I", "*")
                str_ = self._replace(str_, "%-I", "*")
                str_ = self._remove_(str_, "p", False)
            if self.skip & DateTimeSkips.MILLISECOND != DateTimeSkips.NONE:
                str_ = self._replace(str_, "%f", "*")
            else:
                index = str_.find("%S")
                if index != -1:
                    sep = str_[index - 1]
                    str_.replace("%S", "%S" + sep + "%f")
                else:
                    index = str_.find("%-S")
                    if index != -1:
                        sep = str_[index - 1]
                        str_.replace("%-S", "%-S" + sep + "%f")
            if self.skip & DateTimeSkips.SECOND != DateTimeSkips.NONE:
                str_ = self._replace(str_, "%S", "*")
                str_ = self._replace(str_, "%-S", "*")
            else:
                index = str_.find("%M")
                if index != -1:
                    sep = str_[index - 1]
                    str_.replace("%M", "%M" + sep + "%S")
            if self.skip & DateTimeSkips.MINUTE != DateTimeSkips.NONE:
                str_ = self._replace(str_, "%M", "*")
                str_ = self._replace(str_, "%-M", "*")
            return self.value.strftime(str_)
        return self.value.strftime("%x %X")

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
        if not self.value:
            return ""
        str_ = ""
        if self.skip != DateTimeSkips.NONE:
            #  Separate date and time parts.
            str_ = self.__get_pattern(False)
            str_ = self._remove(str_)
            if self.skip & DateTimeSkips.YEAR != DateTimeSkips.NONE:
                str_ = self._remove_(str_, "%Y", True)
                str_ = self._remove_(str_, "%y", True)
                str_ = self._remove_(str_, "%-y", True)
            if self.skip & DateTimeSkips.MONTH != DateTimeSkips.NONE:
                str_ = self._remove_(str_, "%m", True)
                str_ = self._remove_(str_, "%-m", True)
            if self.skip & DateTimeSkips.DAY != DateTimeSkips.NONE:
                str_ = self._remove_(str_, "%d", True)
                str_ = self._remove_(str_, "%-d", True)
            if self.skip & DateTimeSkips.HOUR != DateTimeSkips.NONE:
                str_ = self._remove_(str_, "%H", True)
                str_ = self._remove_(str_, "%-H", True)
                str_ = self._remove_(str_, "%p", True)
            if self.skip & DateTimeSkips.MILLISECOND != DateTimeSkips.NONE:
                str_ = self._remove_(str_, "%f", True)
            else:
                index = str_.find("%S")
                if index != -1:
                    sep = str_[index - 1]
                    str_ = str_.replace("%S", "%S" + sep + "%f")
                else:
                    index = str_.find("%-S")
                    if index != -1:
                        sep = str_[index - 1]
                        str_ = str_.replace("%-S", "%-S" + sep + "%f")
            if self.skip & DateTimeSkips.SECOND != DateTimeSkips.NONE:
                str_ = self._remove_(str_, "%S", True)
                str_ = self._remove_(str_, "%-S", True)
            else:
                index = str_.find("%M")
                if index == -1:
                    index = str_.find("%-M")
                    if index != -1:
                        sep = str_[index - 1]
                        str_.replace("%-M", "%-M" + sep + "-S")
                    else:
                        sep = str_[index - 1]
                        str_.replace("%M", "%M" + sep + "S")
            if self.skip & DateTimeSkips.MINUTE != DateTimeSkips.NONE:
                str_ = self._remove_(str_, "%M", True)
                str_ = self._remove_(str_, "%-M", True)
            return self.value.strftime(str_.strip())
        return self.value.strftime("%x %X")

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
        cal = to.getLocalCalendar()
        #  Compare seconds.
        if not to.skip & DateTimeSkips.SECOND != DateTimeSkips.NONE:
            if start.second < cal.second:
                diff += (cal.second - start.second) * 1000
            else:
                diff -= (start.second - cal.second) * 1000
        elif diff < 0:
            diff = 60000 + diff
        #  Compare minutes.
        if not to.skip & DateTimeSkips.MINUTE != DateTimeSkips.NONE:
            if start.minute < cal.minute:
                diff += (cal.minute - start.minute) * 60000
            else:
                diff -= (start.minute - cal.minute) * 60000
        elif diff < 0:
            diff = 60 * 60000 + diff
        #  Compare hours.
        if not to.skip & DateTimeSkips.HOUR != DateTimeSkips.NONE:
            if start.hour < cal.hour:
                diff += (cal.hour - start.hour) * 60 * 60000
            else:
                diff -= (start.hour - cal.hour) * 60 * 60000
        elif diff < 0:
            diff = 60 * 60000 + diff
        #  Compare days.
        if not to.skip & DateTimeSkips.DAY != DateTimeSkips.NONE:
            if start.day < cal.day:
                diff += (cal.month - start.month) * 24 * 60 * 60000
            elif start.month != cal.month:
                if not to.skip & DateTimeSkips.DAY != DateTimeSkips.NONE:
                    diff += (cal.month - start.month) * 24 * 60 * 60000
                else:
                    diff = ((cls.daysInMonth(start.year, start.month) - start.day + cal.day) * 24 * 60 * 60000) + diff
        elif diff < 0:
            diff = 24 * 60 * 60000 + diff
        #  Compare months.
        if not to.skip & DateTimeSkips.MONTH != DateTimeSkips.NONE:
            if start.month < cal.month:
                m = start.day
                while m != cal.day:
                    diff += cls.daysInMonth(start.year, m) * 24 * 60 * 60000
                    m += 1
            else:
                m = cal.day
                while m != start.day:
                    diff -= cls.daysInMonth(start.year, m) * 24 * 60 * 60000
                    m += 1
        elif diff < 0:
            diff = cls.daysInMonth(start.year, start.month) * 24 * 60 * 60000 + diff
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
        return calendar.monthrange(year, month)

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
    # @param date
    #            Date and time.
    # Unix time.
    #
    @classmethod
    def toUnixTime(cls, date):
        return int(date.value / 1000)

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
#pylint: disable=broad-except,no-name-in-module
from datetime import datetime
from ..GXTimeZone import GXTimeZone
from ._GXDataInfo import _GXDataInfo
from ..GXByteBuffer import GXByteBuffer
from ..GXBitString import GXBitString
from ..enums import DataType
from ..enums import DateTimeSkips, DateTimeExtraInfo, ClockStatus
from ..TranslatorTags import TranslatorTags
from ..TranslatorOutputType import TranslatorOutputType
from ..GXArray import GXArray
from ..GXStructure import GXStructure
from ..enums.Standard import Standard
from ..GXEnum import GXEnum
from ..GXInt8 import GXInt8
from ..GXInt16 import GXInt16
from ..GXInt32 import GXInt32
from ..GXInt64 import GXInt64
from ..GXUInt8 import GXUInt8
from ..GXUInt16 import GXUInt16
from ..GXUInt32 import GXUInt32
from ..GXUInt64 import GXUInt64
from ..GXDateTime import GXDateTime
from ..GXDate import GXDate
from ..GXTime import GXTime
from ..GXFloat32 import GXFloat32
from ..GXFloat64 import GXFloat64

# pylint: disable=too-many-public-methods
class _GXCommon:
    """This class is for internal use only and is subject to changes or removal
    in future versions of the API.  Don't use it."""

    #      HDLC frame start and end character.
    HDLC_FRAME_START_END = 0x7E
    LLC_SEND_BYTES = bytearray([0xE6, 0xE6, 0x00])
    LLC_REPLY_BYTES = bytearray([0xE6, 0xE7, 0x00])
    DATA_TYPE_OFFSET = 0xFF0000
    zeroes = "00000000000000000000000000000000"


    @classmethod
    def getBytes(cls, value):
        """
        Convert string to byte array.
        value: String value.
        returns String as bytes.
        """
        if not value:
            return None
        return value.encode()

    #
    # Is string hex string.
    #
    # value: String value.
    # Return true, if string is hex string.
    #
    @classmethod
    def isHexString(cls, value):
        # pylint: disable=chained-comparison
        if not value:
            return False
        ch = str()
        pos = 0
        while pos != len(value):
            ch = value.charAt(pos)
            if ch != ' ':
                if not ((ch > 0x40 and ch < 'G') or (ch > 0x60 and ch < 'g') or (ch > '/' and ch < ':')):
                    return False
            pos += 1
        return True

    #
    # Get object count.  If first byte is 0x80 or higger it will tell
    #      bytes
    # count.
    # data received data.
    # Object count.
    #
    @classmethod
    def getObjectCount(cls, data):
        cnt = data.getUInt8()
        if cnt > 0x80:
            if cnt == 0x81:
                cnt = data.getUInt8()
            elif cnt == 0x82:
                cnt = data.getUInt16()
            elif cnt == 0x84:
                cnt = int(data.getUInt32())
            else:
                raise ValueError("Invalid count.")
        return cnt

    #
    # Return how many bytes object count takes.
    #
    # count
    # Value
    # Value size in bytes.
    #
    @classmethod
    def getObjectCountSizeInBytes(cls, count):
        if count < 0x80:
            ret = 1
        elif count < 0x100:
            ret = 2
        elif count < 0x10000:
            ret = 3
        else:
            ret = 5
        return ret

    #
    # Add string to byte buffer.
    #
    # value
    # String to add.
    # bb
    # Byte buffer where string is added.
    #
    @classmethod
    def addString(cls, value, bb):
        bb.setUInt8(DataType.OCTET_STRING)
        if not value:
            _GXCommon.setObjectCount(0, bb)
        else:
            _GXCommon.setObjectCount(len(value), bb)
            bb.set(value.encode())

    #
    # Set item count.
    # count
    # buff
    #
    @classmethod
    def setObjectCount(cls, count, buff):
        if count < 0x80:
            buff.setUInt8(count)
            ret = 1
        elif count < 0x100:
            buff.setUInt8(0x81)
            buff.setUInt8(count)
            ret = 2
        elif count < 0x10000:
            buff.setUInt8(0x82)
            buff.setUInt16(count)
            ret = 3
        else:
            buff.setUInt8(0x84)
            buff.setUInt32(count)
            ret = 5
        return ret

    #
    # Reserved for internal use.
    #
    @classmethod
    def toBitString(cls, value, count):
        count2 = count
        sb = ""
        if count2 > 0:
            if count2 > 8:
                count2 = 8
            pos = 7
            while pos != 8 - count2 - 1:
                if (value & (1 << pos)) != 0:
                    sb += '1'
                else:
                    sb += '0'
                pos -= 1
        return sb

    @classmethod
    def changeType(cls, settings, value, type_):
        #pylint: disable=import-outside-toplevel
        if value is None:
            ret = None
        elif type_ == DataType.NONE:
            ret = GXByteBuffer.hex(value, True)
        elif type_ in (DataType.STRING, DataType.OCTET_STRING) and not value:
            ret = ""
        elif type_ == DataType.OCTET_STRING:
            ret = GXByteBuffer(value)
        elif type_ == DataType.STRING and not GXByteBuffer.isAsciiString(value):
            ret = GXByteBuffer(value)
        elif type_ == DataType.DATETIME and not value:
            ret = GXDateTime(None)
        elif type_ == DataType.DATE and not value:
            ret = GXDate(None)
        elif type_ == DataType.TIME and not value:
            ret = GXTime(None)
        else:
            info = _GXDataInfo()
            info.type_ = type_
            ret = _GXCommon.getData(settings, GXByteBuffer(value), info)
            if not info.complete:
                raise ValueError("Change type failed. Not enought data.")
            if type_ == DataType.OCTET_STRING and isinstance(ret, bytes):
                ret = GXByteBuffer.hex(ret)
        return ret

    #
    # Get data from DLMS frame.
    #
    # data
    # received data.
    # info
    # Data info.
    # Received data.
    #
    @classmethod
    def getData(cls, settings, data, info):
        value = None
        startIndex = data.position
        if data.position == len(data):
            info.complete = False
            return None
        info.complete = True
        knownType = info.type_ != DataType.NONE
        #  Get data type if it is unknown.
        if not knownType:
            info.type_ = data.getUInt8()
        if info.type_ == DataType.NONE:
            if info.xml:
                info.xml.appendLine("<" + info.xml.getDataType(info.type_) + " />")
            return value
        if data.position == len(data):
            info.complete = False
            return None
        if info.type_ == DataType.ARRAY or info.type_ == DataType.STRUCTURE:
            value = cls.getArray(settings, data, info, startIndex)
        elif info.type_ == DataType.BOOLEAN:
            value = cls.getBoolean(data, info)
        elif info.type_ == DataType.BITSTRING:
            value = cls.getBitString(data, info)
        elif info.type_ == DataType.INT32:
            value = cls.getInt32(data, info)
        elif info.type_ == DataType.UINT32:
            value = cls.getUInt32(data, info)
        elif info.type_ == DataType.STRING:
            value = cls.getString(data, info, knownType)
        elif info.type_ == DataType.STRING_UTF8:
            value = cls.getUtfString(data, info, knownType)
        elif info.type_ == DataType.OCTET_STRING:
            value = cls.getOctetString(settings, data, info, knownType)
        elif info.type_ == DataType.BCD:
            value = cls.getBcd(data, info)
        elif info.type_ == DataType.INT8:
            value = cls.getInt8(data, info)
        elif info.type_ == DataType.INT16:
            value = cls.getInt16(data, info)
        elif info.type_ == DataType.UINT8:
            value = cls.getUInt8(data, info)
        elif info.type_ == DataType.UINT16:
            value = cls.getUInt16(data, info)
        elif info.type_ == DataType.COMPACT_ARRAY:
            value = cls.getCompactArray(settings, data, info)
        elif info.type_ == DataType.INT64:
            value = cls.getInt64(data, info)
        elif info.type_ == DataType.UINT64:
            value = cls.getUInt64(data, info)
        elif info.type_ == DataType.ENUM:
            value = cls.getEnum(data, info)
        elif info.type_ == DataType.FLOAT32:
            value = cls.getFloat(settings, data, info)
        elif info.type_ == DataType.FLOAT64:
            value = cls.getDouble(settings, data, info)
        elif info.type_ == DataType.DATETIME:
            value = cls.getDateTime(settings, data, info)
        elif info.type_ == DataType.DATE:
            value = cls.getDate(data, info)
        elif info.type_ == DataType.TIME:
            value = cls.getTime(data, info)
        else:
            raise ValueError("Invalid data type.")
        return value

    #
    # Convert value to hex string.
    # value value to convert.
    # desimals Amount of decimals.
    # @return
    #
    @classmethod
    def integerToHex(cls, value, desimals):
        if desimals:
            nbits = desimals * 4
            str_ = hex((value + (1 << nbits)) % (1 << nbits))[2:].upper()
        else:
            str_ = hex(value)[2:].upper()
        if not desimals or desimals == len(str_):
            return str_
        return _GXCommon.zeroes[0: desimals - len(str_)] + str_.upper()

    #
    # Convert value to hex string.
    # value value to convert.
    # desimals Amount of decimals.
    # @return
    #
    @classmethod
    def integerString(cls, value, desimals):
        str_ = str(value)
        if desimals == 0 or len(_GXCommon.zeroes) == len(str_):
            return str_
        return _GXCommon.zeroes[0: desimals - len(str_)] + str_

    #
    # Get array from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # index
    # starting index.
    # Object array.
    #
    @classmethod
    def getArray(cls, settings, buff, info, index):
        value = None
        if info.count == 0:
            info.count = _GXCommon.getObjectCount(buff)
        if info.xml:
            info.xml.appendStartTag(info.xml.getDataType(info.type_), "Qty", info.xml.integerToHex(info.count, 2))
        size = len(buff) - buff.position
        if info.count != 0 and size < 1:
            info.complete = False
            return None
        startIndex = index
        if info.type_ == DataType.ARRAY:
            value = GXArray()
        else:
            value = GXStructure()
        #  Position where last row was found.  Cache uses this info.
        pos = info.index
        while pos != info.count:
            info2 = _GXDataInfo()
            info2.xml = info.xml
            tmp = cls.getData(settings, buff, info2)
            if not info2.complete:
                buff.position = startIndex
                info.complete = False
                break
            if info2.count == info2.index:
                startIndex = buff.position
                value.append(tmp)
            pos += 1
        if info.xml:
            info.xml.appendEndTag(info.xml.getDataType(info.type_))
        info.index = pos
        return value

    #
    # Get time from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # Parsed time.
    #
    @classmethod
    def getTime(cls, buff, info):
        # pylint: disable=broad-except
        value = None
        if len(buff) - buff.position < 4:
            #  If there is not enough data available.
            info.complete = False
            return None
        str_ = None
        if info.xml:
            str_ = buff.toHex(False, buff.position, 4)
        try:
            value = GXTime(None)
            #  Get time.
            hour = buff.getUInt8()
            if hour == 0xFF:
                hour = 0
                value.skip |= DateTimeSkips.HOUR
            minute = buff.getUInt8()
            if minute == 0xFF:
                minute = 0
                value.skip |= DateTimeSkips.MINUTE
            second = buff.getUInt8()
            if second == 0xFF:
                second = 0
                value.skip |= DateTimeSkips.SECOND
            ms = buff.getUInt8()
            if ms != 0xFF:
                ms *= 10
            else:
                ms = 0
                value.skip |= DateTimeSkips.MILLISECOND
            value.value = datetime(1900, 1, 1, hour, minute, second, ms)
        except Exception as ex:
            if info.xml is None:
                raise ex
        if info.xml:
            if value:
                info.xml.appendComment(str(value))
            info.xml.appendLine(info.xml.getDataType(info.type_), None, str_)
        return value

    #
    # Get date from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # Parsed date.
    #
    @classmethod
    def getDate(cls, buff, info):
        # pylint: disable=broad-except
        value = None
        if len(buff) - buff.position < 5:
            #  If there is not enough data available.
            info.complete = False
            return None
        str_ = None
        if info.xml:
            str_ = buff.integerToHex(False, buff.position, 5)
        try:
            dt = GXDate()
            #  Get year.
            year = buff.getUInt16()
            if year < 1900 or year == 0xFFFF:
                dt.skip |= DateTimeSkips.YEAR
                year = 2000
            #  Get month
            month = buff.getUInt8()
            if month == 0xFE:
                dt.extra |= DateTimeExtraInfo.DST_BEGIN
                month = 1
            elif month == 0xFD:
                dt.extra |= DateTimeExtraInfo.DST_END
                month = 1
            else:
                if month < 1 or month > 12:
                    dt.skip |= DateTimeSkips.MONTH
                    month = 1
            #  Get day
            day = buff.getUInt8()
            if day == 0xFE:
                dt.extra |= DateTimeExtraInfo.LAST_DAY
                day = 1
            elif day == 0xFD:
                dt.extra |= DateTimeExtraInfo.LAST_DAY2
                day = 1
            else:
                if day < 1 or day > 31:
                    dt.skip |= DateTimeSkips.DAY
                    day = 1
            dt.value = datetime(year, month, day, 0, 0, 0, 0)
            value = dt
            #  Skip week day
            if buff.getUInt8() == 0xFF:
                dt.skip |= DateTimeSkips.DAY_OF_WEEK
        except Exception as ex:
            if info.xml is None:
                raise ex
        if info.xml:
            if value:
                info.xml.appendComment(str(value))
            info.xml.appendLine(info.xml.getDataType(info.type_), None, str_)
        return value

    #
    # Get date and time from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # Parsed date and time.
    #
    @classmethod
    def getDateTime(cls, settings, buff, info):
        # pylint: disable=too-many-locals, broad-except
        value = None
        skip = DateTimeSkips.NONE
        extra = DateTimeExtraInfo.NONE
        #  If there is not enough data available.
        if len(buff) - buff.position < 12:
            info.complete = False
            return None
        str_ = None
        if info.xml:
            str_ = buff.toHex(False, buff.position, 12)
        dt = GXDateTime()
        try:
            #  Get year.
            year = buff.getUInt16()
            #  Get month
            month = buff.getUInt8()
            #  Get day
            day = buff.getUInt8()
            #  Skip week day
            dayOfWeek = buff.getUInt8()
            if dayOfWeek == 0xFF:
                skip |= DateTimeSkips.DAY_OF_WEEK
            else:
                dt.dayOfWeek = dayOfWeek
            #  Get time.
            hour = buff.getUInt8()
            minute = buff.getUInt8()
            second = buff.getUInt8()
            ms = buff.getUInt8() & 0xFF
            if ms != 0xFF:
                ms *= 10
            else:
                ms = -1
            deviation = buff.getInt16()
            if deviation == -32768:
                deviation = 0x8000
                skip |= DateTimeSkips.DEVITATION
            status = buff.getUInt8()
            dt.status = status
            if year < 1900 or year == 0xFFFF:
                skip |= DateTimeSkips.YEAR
                year = 2000
            if month == 0xFE:
                extra |= DateTimeExtraInfo.DST_BEGIN
                month = 1
            elif month == 0xFD:
                extra |= DateTimeExtraInfo.DST_END
                month = 1
            else:
                if month < 1 or month > 12:
                    skip |= DateTimeSkips.MONTH
                    month = 1

            if day == 0xFE:
                extra |= DateTimeExtraInfo.LAST_DAY
                day = 1
            elif day == 0xFD:
                extra |= DateTimeExtraInfo.LAST_DAY2
                day = 1
            else:
                if day == -1 or day == 0 or day > 31:
                    skip |= DateTimeSkips.DAY
                    day = 1

            if hour < 0 or hour > 24:
                skip |= DateTimeSkips.HOUR
                hour = 0
            if minute < 0 or minute > 60:
                skip |= DateTimeSkips.MINUTE
                minute = 0
            if second < 0 or second > 60:
                skip |= DateTimeSkips.SECOND
                second = 0
            #  If ms is Zero it's skipped.
            if ms < 0 or ms > 100:
                skip |= DateTimeSkips.MILLISECOND
                ms = 0
            tz = None
            if deviation != 0x8000:
                if settings.useUtc2NormalTime:
                    tz = deviation
                else:
                    tz = -deviation
            if tz is None:
                dt.value = datetime(year, month, day, hour, minute, second, ms)
            else:
                dt.value = datetime(year, month, day, hour, minute, second, ms, tzinfo=GXTimeZone(tz))
            dt.skip = skip
            value = dt
        except Exception as ex:
            if info.xml is None:
                raise ex
        if info.xml:
            if dt.skip & DateTimeSkips.YEAR == 0 and value:
                info.xml.appendComment(str(value))
            info.xml.appendLine(info.xml.getDataType(info.type_), None, str_)
        return value

    #
    # Get double value from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # Parsed double value.
    #
    @classmethod
    def getDouble(cls, settings, buff, info):
        value = None
        #  If there is not enough data available.
        if len(buff) - buff.position < 8:
            info.complete = False
            return None
        value = buff.getDouble()
        if info.xml:
            if info.xml.comments:
                info.xml.appendComment("{:.2f}".format(value))
            tmp = GXByteBuffer()
            cls.setData(settings, tmp, DataType.FLOAT64, value)
            info.xml.appendLine(info.xml.getDataType(info.type_), None, GXByteBuffer.toHex(False, 1, len(tmp) - 1))
        return GXFloat64(value)

    #
    # Get float value from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # Parsed float value.
    #
    @classmethod
    def getFloat(cls, settings, buff, info):
        value = None
        #  If there is not enough data available.
        if len(buff) - buff.position < 4:
            info.complete = False
            return None
        value = buff.getFloat()
        if info.xml:
            if info.xml.comments:
                info.xml.appendComment("{:.2f}".format(value))
            tmp = GXByteBuffer()
            cls.setData(settings, tmp, DataType.FLOAT32, value)
            info.xml.appendLine(info.xml.getDataType(info.type_), None, tmp.toHex(False, 1, len(tmp) - 1))
        return GXFloat32(value)

    #
    # Get enumeration value from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # parsed enumeration value.
    #
    @classmethod
    def getEnum(cls, buff, info):
        value = None
        #  If there is not enough data available.
        if len(buff) - buff.position < 1:
            info.complete = False
            return None
        value = buff.getUInt8()
        if info.xml:
            info.xml.appendLine(info.xml.getDataType(info.type_), None, info.xml.integerToHex(value, 2))
        return GXEnum(value)

    #
    # Get UInt64 value from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # parsed UInt64 value.
    #
    @classmethod
    def getUInt64(cls, buff, info):
        value = None
        #  If there is not enough data available.
        if len(buff) - buff.position < 8:
            info.complete = False
            return None
        value = buff.getUInt64()
        if info.xml:
            info.xml.appendLine(info.xml.getDataType(info.type_), None, info.xml.integerToHex(value, 16))
        return GXUInt64(value)

    #
    # Get Int64 value from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # parsed Int64 value.
    #
    @classmethod
    def getInt64(cls, buff, info):
        value = None
        #  If there is not enough data available.
        if len(buff) - buff.position < 8:
            info.complete = False
            return None
        value = buff.getInt64()
        if info.xml:
            info.xml.appendLine(info.xml.getDataType(info.type_), None, info.xml.integerToHex(value, 16))
        return value

    #
    # Get UInt16 value from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # parsed UInt16 value.
    #
    @classmethod
    def getUInt16(cls, buff, info):
        value = None
        #  If there is not enough data available.
        if len(buff) - buff.position < 2:
            info.complete = False
            return None
        value = buff.getUInt16()
        if info.xml:
            info.xml.appendLine(info.xml.getDataType(info.type_), None, info.xml.integerToHex(value, 4))
        return GXUInt16(value)

    #pylint: disable=too-many-arguments
    @classmethod
    def getCompactArrayItem(cls, settings, buff, dt, list_, len_):
        if isinstance(dt, list):
            tmp2 = list()
            for it in dt:
                if isinstance(it, DataType):
                    cls.getCompactArrayItem(settings, buff, it, tmp2, 1)
                else:
                    cls.getCompactArrayItem(settings, buff, it, tmp2, 1)
            list_.append(tmp2)
            return

        tmp = _GXDataInfo()
        tmp.type_ = dt
        start = buff.position
        if dt == DataType.STRING:
            while buff.position - start < len_:
                tmp.clear()
                tmp.type = dt
                list_.append(cls.getString(buff, tmp, False))
                if not tmp.complete:
                    break
        elif dt == DataType.OCTET_STRING:
            while buff.position - start < len_:
                tmp.clear()
                tmp.type = dt
                list_.append(cls.getOctetString(settings, buff, tmp, False))
                if not tmp.complete:
                    break
        else:
            while buff.position - start < len_:
                tmp.clear()
                tmp.type_ = dt
                list_.append(cls.getData(settings, buff, tmp))
                if not tmp.complete:
                    break

    @classmethod
    def getDataTypes(cls, buff, cols, len_):
        dt = None
        pos = 0
        while pos != len_:
            dt = buff.getUInt8()
            if dt == DataType.ARRAY:
                cnt = buff.getUInt16()
                tmp = list()
                tmp2 = list()
                cls.getDataTypes(buff, tmp, 1)
                i = 0
                while i != cnt:
                    tmp2.append(tmp)
                    i += 1
                cols.append(tmp2)
            elif dt == DataType.STRUCTURE:
                tmp = list()
                cls.getDataTypes(buff, tmp, buff.getUInt8())
                cols.append(tmp)
            else:
                cols.append(dt)
            pos += 1

    @classmethod
    def appendDataTypeAsXml(cls, cols, info):
        for it in cols:
            if isinstance(it, (DataType,)):
                info.xml.appendEmptyTag(info.xml.getDataType(it))
            elif isinstance(it, GXStructure):
                info.xml.appendStartTag(cls.DATA_TYPE_OFFSET + DataType.STRUCTURE, None, None)
                cls.appendDataTypeAsXml(it, info)
                info.xml.appendEndTag(cls.DATA_TYPE_OFFSET + DataType.STRUCTURE)
            elif isinstance(it, GXArray):
                info.xml.appendStartTag(cls.DATA_TYPE_OFFSET + DataType.ARRAY, None, None)
                cls.appendDataTypeAsXml(it, info)
                info.xml.appendEndTag(cls.DATA_TYPE_OFFSET + DataType.ARRAY)

    #
    # Get compact array value from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # parsed UInt16 value.
    #
    @classmethod
    def getCompactArray(cls, settings, buff, info):
        # pylint: disable=too-many-nested-blocks

        #  If there is not enough data available.
        if len(buff) - buff.position < 2:
            info.complete = False
            return None
        dt = buff.getUInt8()
        if dt == DataType.ARRAY:
            raise ValueError("Invalid compact array data.")
        len_ = _GXCommon.getObjectCount(buff)
        list_ = list()
        if dt == DataType.STRUCTURE:
            #  Get data types.
            cols = list()
            cls.getDataTypes(buff, cols, len_)
            len_ = _GXCommon.getObjectCount(buff)
            if info.xml:
                info.xml.appendStartTag(info.xml.getDataType(DataType.COMPACT_ARRAY), None, None)
                info.xml.appendStartTag(TranslatorTags.CONTENTS_DESCRIPTION)
                cls.appendDataTypeAsXml(cols, info)
                info.xml.appendEndTag(TranslatorTags.CONTENTS_DESCRIPTION)
                if info.xml.outputType == TranslatorOutputType.STANDARD_XML:
                    info.xml.appendStartTag(TranslatorTags.ARRAY_CONTENTS, None, None, True)
                    info.xml.append(buff.remainingHexString(True))
                    info.xml.appendEndTag(TranslatorTags.ARRAY_CONTENTS, True)
                    info.xml.appendEndTag(info.xml.getDataType(DataType.COMPACT_ARRAY))
                else:
                    info.xml.appendStartTag(TranslatorTags.ARRAY_CONTENTS)
            start = buff.position
            while buff.position - start < len_:
                row = list()
                pos = 0
                while pos != len(cols):
                    if isinstance(cols[pos], GXArray):
                        cls.getCompactArrayItem(settings, buff, cols[pos], row, 1)
                    elif isinstance(cols[pos], GXStructure):
                        tmp2 = list()
                        cls.getCompactArrayItem(settings, buff, cols[pos], tmp2, 1)
                        row.append(tmp2[0])
                    else:
                        cls.getCompactArrayItem(settings, buff, cols[pos], row, 1)
                    if buff.position == len(buff):
                        break
                    pos += 1
                #  If all columns are read.
                if len(row) >= len(cols):
                    list_.append(row)
                else:
                    break
            if info.xml and info.xml.outputType == TranslatorOutputType.SIMPLE_XML:
                sb = ""
                for row in list_:
                    for it in row:
                        if isinstance(it, bytearray):
                            sb += GXByteBuffer.hex(it)
                        elif isinstance(it, list):
                            start = len(sb)
                            for it2 in it:
                                if isinstance(it2, bytearray):
                                    sb += GXByteBuffer.hex(it2)
                                else:
                                    sb += str(it2)
                                sb += ";"
                            if start != len(sb):
                                sb = sb[0:len(sb) - 1]
                        else:
                            sb += str(it)
                        sb += ";"
                    if sb:
                        sb = sb[0:len(sb) - 1]
                    info.xml.appendLine(sb)
                    sb = ""
            if info.xml and info.xml.outputType == TranslatorOutputType.SIMPLE_XML:
                info.xml.appendEndTag(TranslatorTags.ARRAY_CONTENTS)
                info.xml.appendEndTag(info.xml.getDataType(DataType.COMPACT_ARRAY))
        else:
            if info.xml:
                info.xml.appendStartTag(info.xml.getDataType(DataType.COMPACT_ARRAY), None, None)
                info.xml.appendStartTag(TranslatorTags.CONTENTS_DESCRIPTION)
                info.xml.appendEmptyTag(info.xml.getDataType(dt))
                info.xml.appendEndTag(TranslatorTags.CONTENTS_DESCRIPTION)
                info.xml.appendStartTag(TranslatorTags.ARRAY_CONTENTS, None, None, True)
                if info.xml.outputType == TranslatorOutputType.STANDARD_XML:
                    info.xml.append(buff.remainingHexStringFalse)
                    info.xml.appendEndTag(TranslatorTags.ARRAY_CONTENTS, True)
                    info.xml.appendEndTag(info.xml.getDataType(DataType.COMPACT_ARRAY))
            cls.getCompactArrayItem(settings, buff, dt, list_, len_)
            if info.xml and info.xml.outputType == TranslatorOutputType.SIMPLE_XML:
                for it in list_:
                    if isinstance(it, bytearray):
                        info.xml.append(GXByteBuffer.hex(it))
                    else:
                        info.xml.append(str(it))
                    info.xml.append(";")
                if list_:
                    info.xml.setXmlLength(info.xml.getXmlLength() - 1)
                info.xml.appendEndTag(TranslatorTags.ARRAY_CONTENTS, True)
                info.xml.appendEndTag(info.xml.getDataType(DataType.COMPACT_ARRAY))
        return list_

    #
    # Get UInt8 value from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # parsed UInt8 value.
    #
    @classmethod
    def getUInt8(cls, buff, info):
        value = None
        #  If there is not enough data available.
        if len(buff) - buff.position < 1:
            info.complete = False
            return None
        value = buff.getUInt8() & 0xFF
        if info.xml:
            info.xml.appendLine(info.xml.getDataType(info.type_), None, info.xml.integerToHex(value, 2))
        return GXUInt8(value)

    #
    # Get Int16 value from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # parsed Int16 value.
    #
    @classmethod
    def getInt16(cls, buff, info):
        value = None
        #  If there is not enough data available.
        if len(buff) - buff.position < 2:
            info.complete = False
            return None
        value = int(buff.getInt16())
        if info.xml:
            info.xml.appendLine(info.xml.getDataType(info.type_), None, info.xml.integerToHex(value, 4))
        return value

    #
    # Get Int8 value from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # parsed Int8 value.
    #
    @classmethod
    def getInt8(cls, buff, info):
        value = None
        #  If there is not enough data available.
        if len(buff) - buff.position < 1:
            info.complete = False
            return None
        value = int(buff.getInt8())
        if info.xml:
            info.xml.appendLine(info.xml.getDataType(info.type_), None, info.xml.integerToHex(value, 2))
        return GXInt8(value)

    #
    # Get BCD value from DLMS data.
    #
    # buff: Received DLMS data.
    # info: Data info.
    # Returns parsed BCD value.
    #
    @classmethod
    def getBcd(cls, buff, info):
        #  If there is not enough data available.
        if len(buff) - buff.position < 1:
            info.complete = False
            return None
        value = buff.getUInt8()
        if info.xml:
            info.xml.appendLine(info.xml.getDataType(info.type_), None, info.xml.integerToHex(value, 2))
        return value

    #
    # Get UTF string value from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # parsed UTF string value.
    #
    @classmethod
    def getUtfString(cls, buff, info, knownType):
        if knownType:
            len_ = len(buff)
        else:
            len_ = _GXCommon.getObjectCount(buff)
            #  If there is not enough data available.
            if len(buff) - buff.position < len_:
                info.complete = False
                return None
        if len_ > 0:
            value = buff.getString(buff.position, len_)
            buff.position += len_
        else:
            value = ""
        if info.xml:
            if info.xml.getShowStringAsHex:
                info.xml.appendLine(info.xml.getDataType(info.type_), None, buff.toHex(False, buff.position - len, len))
            else:
                info.xml.appendLine(info.xml.getDataType(info.type_), None, value)
        return value

    #
    # Get octet string value from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # parsed octet string value.
    #
    @classmethod
    def getOctetString(cls, settings, buff, info, knownType):
        # pylint: disable=too-many-nested-blocks,broad-except
        value = None
        if knownType:
            len_ = len(buff)
        else:
            len_ = _GXCommon.getObjectCount(buff)
            #  If there is not enough data available.
            if len(buff) - buff.position < len_:
                info.complete = False
                return None
        tmp = bytearray(len_)
        buff.get(tmp)
        value = tmp
        if info.xml:
            if info.xml.comments and tmp:
                #  This might be a logical name.
                if len(tmp) == 6 and tmp[5] == 255:
                    info.xml.appendComment(cls.toLogicalName(tmp))
                else:
                    isString = True
                    #  Try to move octect string to DateTie, Date or time.
                    if len(tmp) == 5 or len(tmp) == 5 or len(tmp) == 4:
                        try:
                            type_ = None
                            if len(tmp) == 12:
                                type_ = DataType.DATETIME
                            elif len(tmp) == 5:
                                type_ = DataType.DATE
                            else:
                                type_ = DataType.TIME
                            dt = _GXCommon.changeType(settings, tmp, type_)
                            year = dt.value.year
                            if 1970 < year > 2100:
                                info.xml.appendComment(str(dt))
                                isString = False
                        except Exception:
                            isString = True
                    if isString:
                        for it in tmp:
                            if it < 32 or it > 126:
                                isString = False
                                break
                        if isString:
                            info.xml.appendComment(str(tmp))
            info.xml.appendLine(info.xml.getDataType(info.type_), None, GXByteBuffer.hex(tmp, False))
        return value

    #
    # Get string value from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # parsed string value.
    #
    @classmethod
    def getString(cls, buff, info, knownType):
        value = None
        if knownType:
            len_ = len(buff)
        else:
            len_ = _GXCommon.getObjectCount(buff)
            #  If there is not enough data available.
            if len(buff) - buff.position < len_:
                info.complete = False
                return None
        if len_ > 0:
            value = buff.getString(buff.position, len_)
            buff.position += len_
        else:
            value = ""
        if info.xml:
            if info.xml.showStringAsHex:
                info.xml.appendLine(info.xml.getDataType(info.type_), None, buff.toHex(False, buff.position - len_, len_))
            else:
                info.xml.appendLine(info.xml.getDataType(info.type_), None, value)
        return value

    #
    # Get UInt32 value from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # parsed UInt32 value.
    #
    @classmethod
    def getUInt32(cls, buff, info):
        #  If there is not enough data available.
        if len(buff) - buff.position < 4:
            info.complete = False
            return None
        value = buff.getUInt32()
        if info.xml:
            info.xml.appendLine(info.xml.getDataType(info.type_), None, info.xml.integerToHex(value, 8))
        return GXUInt32(value)

    #
    # Get Int32 value from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # parsed Int32 value.
    #
    @classmethod
    def getInt32(cls, buff, info):
        #  If there is not enough data available.
        if len(buff) - buff.position < 4:
            info.complete = False
            return None
        value = int(buff.getInt32())
        if info.xml:
            info.xml.appendLine(info.xml.getDataType(info.type_), None, info.xml.integerToHex(value, 8))
        return value

    #
    # Get bit string value from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # parsed bit string value.
    #
    @classmethod
    def getBitString(cls, buff, info):
        cnt = cls.getObjectCount(buff)
        t = cnt
        t /= 8
        if cnt % 8 != 0:
            t += 1
        byteCnt = int(t)
        #  If there is not enough data available.
        if len(buff) - buff.position < byteCnt:
            info.complete = False
            return None
        sb = ""
        while cnt > 0:
            sb += cls.toBitString(buff.getInt8(), cnt)
            cnt -= 8
        if info.xml:
            info.xml.appendLine(info.xml.getDataType(info.type_), None, sb)
        return GXBitString(sb)

    #
    # Get boolean value from DLMS data.
    #
    # buff
    # Received DLMS data.
    # info
    # Data info.
    # parsed boolean value.
    #
    @classmethod
    def getBoolean(cls, buff, info):
        #  If there is not enough data available.
        if len(buff) - buff.position < 1:
            info.complete = False
            return None
        value = bool(buff.getUInt8() != 0)
        if info.xml:
            info.xml.appendLine(info.xml.getDataType(info.type_), None, value.__str__())
        return value

    #
    # Get HDLC address from byte array.
    #
    # buff
    # byte array.
    # HDLC address.
    #
    @classmethod
    def getHDLCAddress(cls, buff):
        size = 0
        pos = buff.position
        while pos != len(buff):
            size += 1
            if buff.getUInt8(pos) & 0x1 == 1:
                break
            pos += 1
        if size == 1:
            ret = (buff.getUInt8() & 0xFE) >> 1
        elif size == 2:
            ret = buff.getUInt16()
            ret = ((ret & 0xFE) >> 1) | ((ret & 0xFE00) >> 2)
        elif size == 4:
            ret = buff.getUInt32()
            ret = ((ret & 0xFE) >> 1) | ((ret & 0xFE00) >> 2) | ((ret & 0xFE0000) >> 3) | ((ret & 0xFE000000) >> 4)
        else:
            raise ValueError("Wrong size.")
        return ret

    #
    # Convert object to DLMS bytes.
    #
    # settings: DLMS settings.
    # buff: Byte buffer where data is write.
    # dataType: Data type.
    # value: Added Value.
    #
    @classmethod
    def setData(cls, settings, buff, dataType, value):
        if dataType in (DataType.ARRAY, DataType.STRUCTURE) and isinstance(value, (GXByteBuffer, bytearray, bytes)):
            #  If byte array is added do not add type.
            buff.set(value)
            return

        buff.setUInt8(dataType)
        if dataType == DataType.NONE:
            pass
        elif dataType == DataType.BOOLEAN:
            if value:
                buff.setUInt8(1)
            else:
                buff.setUInt8(0)
        elif dataType == DataType.UINT8:
            buff.setUInt8(value)
        elif dataType in (DataType.INT8, DataType.ENUM):
            buff.setInt8(value)
        elif dataType in (DataType.UINT16, DataType.INT16):
            buff.setUInt16(value)
        elif dataType in (DataType.UINT32, DataType.INT32):
            buff.setUInt32(value)
        elif dataType in (DataType.UINT64, DataType.INT64):
            buff.setUInt64(value)
        elif dataType == DataType.FLOAT32:
            buff.setFloat(value)
        elif dataType == DataType.FLOAT64:
            buff.setDouble(value)
        elif dataType == DataType.BITSTRING:
            cls.setBitString(buff, value, True)
        elif dataType == DataType.STRING:
            cls.setString(buff, value)
        elif dataType == DataType.STRING_UTF8:
            cls.setUtfString(buff, value)
        elif dataType == DataType.OCTET_STRING:
            if isinstance(value, GXDate):
                #  Add size
                buff.setUInt8(5)
                cls.setDate(buff, value)
            elif isinstance(value, GXTime):
                #  Add size
                buff.setUInt8(4)
                cls.setTime(buff, value)
            elif isinstance(value, (GXDateTime, datetime)):
                buff.setUInt8(12)
                cls.setDateTime(settings, buff, value)
            else:
                cls.setOctetString(buff, value)
        elif dataType in (DataType.ARRAY, DataType.STRUCTURE):
            cls.setArray(settings, buff, value)
        elif dataType == DataType.BCD:
            cls.setBcd(buff, value)
        elif dataType == DataType.COMPACT_ARRAY:
            #  Compact array is not work with python because we don't know data
            #  types of each element.
            raise ValueError("Invalid data type.")
        elif dataType == DataType.DATETIME:
            cls.setDateTime(settings, buff, value)
        elif dataType == DataType.DATE:
            cls.setDate(buff, value)
        elif dataType == DataType.TIME:
            cls.setTime(buff, value)
        else:
            raise ValueError("Invalid data type.")

    #
    # Convert time to DLMS bytes.
    #
    # buff
    # Byte buffer where data is write.
    # value
    # Added value.
    #
    @classmethod
    def setTime(cls, buff, value):
        dt = cls.__getDateTime(value)
        #  Add time.
        if dt.skip & DateTimeSkips.HOUR != DateTimeSkips.NONE:
            buff.setUInt8(0xFF)
        else:
            buff.setUInt8(dt.value.hour)
        if dt.skip & DateTimeSkips.MINUTE != DateTimeSkips.NONE:
            buff.setUInt8(0xFF)
        else:
            buff.setUInt8(dt.value.minute)
        if dt.skip & DateTimeSkips.SECOND != DateTimeSkips.NONE:
            buff.setUInt8(0xFF)
        else:
            buff.setUInt8(dt.value.second)
        if dt.skip & DateTimeSkips.MILLISECOND != DateTimeSkips.NONE:
            #  Hundredth of seconds is not used.
            buff.setUInt8(0xFF)
        else:
            ms = dt.value.microsecond
            if ms != 0:
                ms /= 10000
            buff.setUInt8(int(ms))

    #
    # Convert date to DLMS bytes.
    #
    # buff
    # Byte buffer where data is write.
    # value
    # Added value.
    #
    @classmethod
    def setDate(cls, buff, value):
        dt = cls.__getDateTime(value)
        #  Add year.
        if dt.skip & DateTimeSkips.YEAR != DateTimeSkips.NONE:
            buff.setUInt16(0xFFFF)
        else:
            buff.setUInt16(dt.value.year)
        #  Add month
        if dt.extra & DateTimeExtraInfo.DST_BEGIN != 0:
            buff.setUInt8(0xFE)
        elif dt.extra & DateTimeExtraInfo.DST_END != 0:
            buff.setUInt8(0xFD)
        elif dt.skip & DateTimeSkips.MONTH != 0:
            buff.setUInt8(0xFF)
        else:
            buff.setUInt8(dt.value.month)
        #  Add day
        if dt.extra & DateTimeExtraInfo.LAST_DAY2 != DateTimeSkips.NONE:
            buff.setUInt8(0xFD)
        elif dt.extra & DateTimeExtraInfo.LAST_DAY != DateTimeSkips.NONE:
            buff.setUInt8(0xFE)
        elif dt.skip & DateTimeSkips.DAY != DateTimeSkips.NONE:
            buff.setUInt8(0xFF)
        else:
            buff.setUInt8(dt.value.day)

        #  Day of week.
        if dt.skip & DateTimeSkips.DAY_OF_WEEK != DateTimeSkips.NONE:
            buff.setUInt8(0xFF)
        else:
            if dt.dayOfWeek == 0:
                buff.setUInt8(dt.value.weekday() + 1)
            else:
                buff.setUInt8(dt.dayOfWeek)

    @classmethod
    def __getDateTime(cls, value):
        dt = None
        if isinstance(value, (GXDateTime)):
            dt = value
        elif isinstance(value, (datetime, str)):
            dt = GXDateTime(value)
            dt.skip |= DateTimeSkips.MILLISECOND
        else:
            raise ValueError("Invalid date format.")
        return dt

    #
    # Convert date time to DLMS bytes.
    #
    # buff
    # Byte buffer where data is write.
    # value
    # Added value.
    #
    @classmethod
    def setDateTime(cls, settings, buff, value):
        dt = cls.__getDateTime(value)
        skip = dt.skip
        if settings and settings.dateTimeSkips:
            skip = skip or settings.dateTimeSkips

        #  Add year.
        if skip & DateTimeSkips.YEAR != DateTimeSkips.NONE:
            buff.setUInt16(0xFFFF)
        else:
            buff.setUInt16(dt.value.year)
        #  Add month
        if dt.extra & DateTimeExtraInfo.DST_BEGIN != 0:
            buff.setUInt8(0xFD)
        elif dt.extra & DateTimeExtraInfo.DST_END != 0:
            buff.setUInt8(0xFE)
        elif skip & DateTimeSkips.MONTH != DateTimeSkips.NONE:
            buff.setUInt8(0xFF)
        else:
            buff.setUInt8(dt.value.month)

        #  Add day
        if dt.extra & DateTimeExtraInfo.LAST_DAY2 != DateTimeSkips.NONE:
            buff.setUInt8(0xFD)
        elif dt.extra & DateTimeExtraInfo.LAST_DAY != DateTimeSkips.NONE:
            buff.setUInt8(0xFE)
        elif skip & DateTimeSkips.DAY != DateTimeSkips.NONE:
            buff.setUInt8(0xFF)
        else:
            buff.setUInt8(dt.value.day)
        #  Day of week.
        if skip & DateTimeSkips.DAY_OF_WEEK != DateTimeSkips.NONE:
            buff.setUInt8(0xFF)
        else:
            if dt.dayOfWeek == 0:
                buff.setUInt8(dt.value.weekday() + 1)
            else:
                buff.setUInt8(dt.dayOfWeek)
        #  Add time.
        if skip & DateTimeSkips.HOUR != DateTimeSkips.NONE:
            buff.setUInt8(0xFF)
        else:
            buff.setUInt8(dt.value.hour)
        if skip & DateTimeSkips.MINUTE != DateTimeSkips.NONE:
            buff.setUInt8(0xFF)
        else:
            buff.setUInt8(dt.value.minute)
        if skip & DateTimeSkips.SECOND != DateTimeSkips.NONE:
            buff.setUInt8(0xFF)
        else:
            buff.setUInt8(dt.value.second)
        if skip & DateTimeSkips.MILLISECOND != DateTimeSkips.NONE:
            #  Hundredth of seconds is not used.
            buff.setUInt8(0xFF)
        else:
            ms = dt.value.microsecond
            if ms != 0:
                ms /= 10000
            buff.setUInt8(int(ms))
        #  devitation not used.
        if skip & DateTimeSkips.DEVITATION != DateTimeSkips.NONE:
            buff.setUInt16(0x8000)
        else:
            #  Add devitation.
            d = int(dt.value.utcoffset().seconds / 60)
            if not (settings and settings.useUtc2NormalTime):
                d = -d
            buff.setUInt16(d)
        #  Add clock_status
        if skip & DateTimeSkips.STATUS == DateTimeSkips.NONE:
            if dt.value.dst() or dt.status & ClockStatus.DAYLIGHT_SAVE_ACTIVE != ClockStatus.OK:
                buff.setUInt8(dt.status | ClockStatus.DAYLIGHT_SAVE_ACTIVE)
            else:
                buff.setUInt8(dt.status)
        else:
            buff.setUInt8(0xFF)

    @classmethod
    def setBcd(cls, buff, value):
        buff.setUInt8(value)

    @classmethod
    def setArray(cls, settings, buff, value):
        if value:
            _GXCommon.setObjectCount(len(value), buff)
            for it in value:
                cls.setData(settings, buff, cls.getDLMSDataType(it), it)
        else:
            _GXCommon.setObjectCount(0, buff)

    @classmethod
    def setOctetString(cls, buff, value):
        if isinstance(value, str):
            tmp = GXByteBuffer.hexToBytes(value)
            _GXCommon.setObjectCount(len(tmp), buff)
            buff.set(tmp)
        elif isinstance(value, GXByteBuffer):
            cls.setObjectCount(len(value), buff)
            buff.set(value)
        elif isinstance(value, (bytearray, bytes)):
            cls.setObjectCount(len(value), buff)
            buff.set(value)
        elif value is None:
            cls.setObjectCount(0, buff)
        else:
            raise ValueError("Invalid data type.")

    @classmethod
    def setUtfString(cls, buff, value):
        if value:
            tmp = value.encode()
            _GXCommon.setObjectCount(len(tmp), buff)
            buff.set(tmp)
        else:
            buff.setUInt8(0)

    @classmethod
    def setString(cls, buff, value):
        if value:
            _GXCommon.setObjectCount(len(value), buff)
            buff.set(_GXCommon.getBytes(value))
        else:
            buff.setUInt8(0)

    @classmethod
    def setBitString(cls, buff, val1, addCount):
        value = val1
        if isinstance(value, GXBitString):
            value = value.value
        if isinstance(value, str):
            val = 0
            str_ = str(value)
            if addCount:
                _GXCommon.setObjectCount(len(str_), buff)
            index = 7
            pos = 0
            while pos != len(str_):
                it = str_[pos]
                if it == '1':
                    val |= (1 << index)
                elif it != '0':
                    raise ValueError("Not a bit string.")
                index -= 1
                if index == -1:
                    index = 7
                    buff.setUInt8(val)
                    val = 0
                pos += 1
            if index != 7:
                buff.setUInt8(val)
        elif isinstance(value, (bytearray, bytes)):
            _GXCommon.setObjectCount(8 * len(value), buff)
            buff.set(value)
        elif isinstance(value, int):
            _GXCommon.setObjectCount(8, buff)
            buff.setUInt8(value)
        elif value is None:
            buff.setUInt8(0)
        else:
            raise ValueError("BitString must give as string.")

    @classmethod
    def getDataType(cls, value):
        if value == DataType.NONE:
            ret = None
        elif value == DataType.OCTET_STRING:
            ret = bytes.__class__
        elif value == DataType.ENUM:
            ret = GXEnum.__class__
        elif value == DataType.INT8:
            ret = int.__class__
        elif value == DataType.INT16:
            ret = int.__class__
        elif value == DataType.INT32:
            ret = int.__class__
        elif value == DataType.INT64:
            ret = int.__class__
        elif value == DataType.UINT8:
            ret = GXUInt8.__class__
        elif value == DataType.UINT16:
            ret = GXUInt16.__class__
        elif value == DataType.UINT32:
            ret = GXUInt32.__class__
        elif value == DataType.UINT64:
            ret = GXUInt64.__class__
        elif value == DataType.TIME:
            ret = GXTime.__class__
        elif value == DataType.DATE:
            ret = GXDate.__class__
        elif value == DataType.DATETIME:
            ret = GXDateTime.__class__
        elif value == DataType.ARRAY:
            ret = list.__class__
        elif value == DataType.STRING:
            ret = str.__class__
        elif value == DataType.BOOLEAN:
            ret = bool.__class__
        elif value == DataType.FLOAT32:
            ret = GXFloat32.__class__
        elif value == DataType.FLOAT64:
            ret = GXFloat64.__class__
        elif value == DataType.BITSTRING:
            ret = GXBitString.__class__
        else:
            raise ValueError("Invalid value.")
        return ret

    @classmethod
    def getDLMSDataType(cls, value):
        # pylint: disable=undefined-variable
        if value is None:
            ret = DataType.NONE
        elif isinstance(value, (bytes, bytearray, GXByteBuffer)):
            ret = DataType.OCTET_STRING
        elif isinstance(value, (GXEnum)):
            ret = DataType.ENUM
        elif isinstance(value, (GXInt8)):
            ret = DataType.INT8
        elif isinstance(value, (GXInt16)):
            ret = DataType.INT16
        elif isinstance(value, (GXInt64)):
            ret = DataType.INT64
        elif isinstance(value, (GXUInt8)):
            ret = DataType.UINT8
        elif isinstance(value, (GXUInt16)):
            ret = DataType.UINT16
        elif isinstance(value, (GXUInt32)):
            ret = DataType.UINT32
        elif isinstance(value, (GXUInt64)):
            ret = DataType.UINT64
        elif isinstance(value, (bool)):
            ret = DataType.BOOLEAN
        elif isinstance(value, (GXInt32, int)):
            ret = DataType.INT32
        elif isinstance(value, (GXTime)):
            ret = DataType.TIME
        elif isinstance(value, (GXDate)):
            ret = DataType.DATE
        elif isinstance(value, (datetime, GXDateTime)):
            ret = DataType.DATETIME
        elif isinstance(value, (GXStructure)):
            ret = DataType.STRUCTURE
        elif isinstance(value, (GXArray, list)):
            ret = DataType.ARRAY
        elif isinstance(value, (str)):
            ret = DataType.STRING
        elif isinstance(value, (GXFloat64)):
            ret = DataType.FLOAT64
        elif isinstance(value, (GXFloat32, complex, float)):
            ret = DataType.FLOAT32
        elif isinstance(value, (GXBitString)):
            ret = DataType.BITSTRING
        else:
            ret = None
        if ret is None:
            #Python 2.7 uses unicode.
            try:
                if isinstance(value, (unicode)):
                    ret = DataType.STRING
            except Exception:
                ret = None
            if ret is None:
                raise ValueError("Invalid datatype " + type(value) + ".")
        return ret

    @classmethod
    def getDataTypeSize(cls, type_):
        size = -1
        if type_ == DataType.BCD:
            size = 1
        elif type_ == DataType.BOOLEAN:
            size = 1
        elif type_ == DataType.DATE:
            size = 5
        elif type_ == DataType.DATETIME:
            size = 12
        elif type_ == DataType.ENUM:
            size = 1
        elif type_ == DataType.FLOAT32:
            size = 4
        elif type_ == DataType.FLOAT64:
            size = 8
        elif type_ == DataType.INT16:
            size = 2
        elif type_ == DataType.INT32:
            size = 4
        elif type_ == DataType.INT64:
            size = 8
        elif type_ == DataType.INT8:
            size = 1
        elif type_ == DataType.NONE:
            size = 0
        elif type_ == DataType.TIME:
            size = 4
        elif type_ == DataType.UINT16:
            size = 2
        elif type_ == DataType.UINT32:
            size = 4
        elif type_ == DataType.UINT64:
            size = 8
        elif type_ == DataType.UINT8:
            size = 1
        return size

    @classmethod
    def toLogicalName(cls, value):
        if isinstance(value, bytearray):
            if not value:
                value = bytearray(6)
            if len(value) == 6:
                return str(value[0]) + "." + str(value[1]) + "." + str(value[2]) + "." + str(value[3]) + "." + str(value[4]) + "." + str(value[5])
            raise ValueError("Invalid Logical name.")
        return str(value)

    @classmethod
    def logicalNameToBytes(cls, value):
        if not value:
            return bytearray(6)
        items = value.split('.')
        if len(items) != 6:
            raise ValueError("Invalid Logical name.")
        buff = bytearray(6)
        pos = 0
        for it in items:
            v = int(it)
            if v < 0 or v > 255:
                raise ValueError("Invalid Logical name.")
            buff[pos] = int(v)
            pos += 1
        return buff

    @classmethod
    def getGeneralizedTime(cls, dateString):
        year = int(dateString[0:4])
        month = int(dateString[4:6])
        day = int(dateString[6:8])
        hour = int(dateString[8:10])
        minute = int(dateString[10:12])
        #If UTC time.
        if dateString.endsWith("Z"):
            if len(dateString) > 13:
                second = int(dateString[12:14])
            return datetime(year, month, day, hour, minute, second, 0, tzinfo=GXTimeZone(0))

        if len(dateString) > 17:
            second = int(dateString.substring(12, 14))
        tz = dateString[dateString.length() - 4:]
        return datetime(year, month, day, hour, minute, second, 0, tzinfo=GXTimeZone(tz))

    @classmethod
    def generalizedTime(cls, value):
        #Convert to UTC time.
        if isinstance(value, (GXDateTime)):
            value = value.value
        value = value.utctimetuple()
        sb = cls.integerString(value.tm_year, 4)
        sb += cls.integerString(value.tm_mon, 2)
        sb += cls.integerString(value.tm_mday, 2)
        sb += cls.integerString(value.tm_hour, 2)
        sb += cls.integerString(value.tm_min, 2)
        sb += cls.integerString(value.tm_sec, 2)
        #UTC time.
        sb += "Z"
        return sb

    @classmethod
    def encryptManufacturer(cls, flagName):
        if len(flagName) != 3:
            raise ValueError("Invalid Flag name.")
        value = ((flagName.charAt(0) - 0x40) & 0x1f)
        value <<= 5
        value += ((flagName.charAt(0) - 0x40) & 0x1f)
        value <<= 5
        value += ((flagName.charAt(0) - 0x40) & 0x1f)
        return value

    @classmethod
    def decryptManufacturer(cls, value):
        tmp = (value >> 8 | value << 8)
        c = str(((tmp & 0x1f) + 0x40))
        tmp = (tmp >> 5)
        c1 = str(((tmp & 0x1f) + 0x40))
        tmp = (tmp >> 5)
        c2 = str(((tmp & 0x1f) + 0x40))
        return str(c2, c1, c)

    @classmethod
    def idisSystemTitleToString(cls, st):
        sb = '\n'
        sb += "IDIS system title:\n"
        sb += "Manufacturer Code: "
        sb += cls.__getChar(st[0]) + cls.__getChar(st[1]) + cls.__getChar(st[2])
        sb += "\nFunction type: "
        ft = st[4] >> 4
        add = False
        if (ft & 0x1) != 0:
            sb += "Disconnector extension"
            add = True
        if (ft & 0x2) != 0:
            if add:
                sb += ", "
            add = True
            sb += "Load Management extension"

        if (ft & 0x4) != 0:
            if add:
                sb += ", "
            sb += "Multi Utility extension"
        #Serial number
        sn = (st[4] & 0xF) << 24
        sn |= st[5] << 16
        sn |= st[6] << 8
        sn |= st[7]
        sb += '\n'
        sb += "Serial number: "
        sb += str(sn) + '\n'
        return sb

    @classmethod
    def dlmsSystemTitleToString(cls, st):
        sb = '\n'
        sb += "IDIS system title:\n"
        sb += "Manufacturer Code: "
        sb += cls.__getChar(st[0]) + cls.__getChar(st[1]) + cls.__getChar(st[2])
        sb += "Serial number: "
        sb += cls.__getChar(st[3]) + cls.__getChar(st[4]) + cls.__getChar(st[5]) + cls.__getChar(st[6]) + cls.__getChar(st[7])
        return sb

    @classmethod
    def uniSystemTitleToString(cls, st):
        sb = '\n'
        sb += "UNI/TS system title:\n"
        sb += "Manufacturer: "
        m = st[0] << 8 | st[1]
        sb += cls.decryptManufacturer(m)
        sb += "\nSerial number: "
        sb += GXByteBuffer.toHex((st[7], st[6], st[5], st[4], st[3], st[2]), False)
        return sb

    @classmethod
    def __getChar(cls, ch):
        try:
            return str(chr(ch))
        except Exception:
            #If python 2.7 is used.
            #pylint: disable=undefined-variable
            return str(unichr(ch))

    @classmethod
    def systemTitleToString(cls, standard, st):
        ###Conver system title to string.
        #pylint: disable=too-many-boolean-expressions
        if standard == Standard.ITALY or not cls.__getChar(st[0]).isalpha() or \
            not cls.__getChar(st[1]).isalpha() or not cls.__getChar(st[2]).isalpha():
            return cls.uniSystemTitleToString(st)
        if standard == Standard.IDIS or not cls.__getChar(st[3]).isdigit() or \
            not cls.__getChar(st[4]).isdigit() or not cls.__getChar(st[5]).isdigit() or \
            not cls.__getChar(st[6]).isdigit() or not cls.__getChar(st[7]).isdigit():
            return cls.idisSystemTitleToString(st)
        return cls.dlmsSystemTitleToString(st)

    #Reserved for internal use.
    @classmethod
    def swapBits(cls, value):
        ret = 0
        pos = 0
        while pos != 8:
            ret = ret << 1 | value & 0x01
            value = value >> 1
            pos = pos + 1
        return ret

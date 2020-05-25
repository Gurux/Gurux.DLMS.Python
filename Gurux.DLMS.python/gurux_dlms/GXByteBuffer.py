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
import sys
import struct

#pylint: disable=import-error, no-name-in-module
if sys.version_info < (3, 0):
    __base = object
else:
    from collections.abc import Sequence
    __base = Sequence

# pylint: disable=too-many-public-methods
class GXByteBuffer(__base):
    """
    Byte array class is used to save received bytes.
    """

    __HEX_ARRAY = "0123456789ABCDEFGH"
    __NIBBLE = 4
    __LOW_BYTE_PART = 0x0F
    __ARRAY_CAPACITY = 10

    def __init__(self, value=None):
        """
        Constructor.
        value: Buffer or capacity.
        """
        self._data = bytearray()
        self.__size = 0
        self.__position = 0
        if isinstance(value, (bytearray, bytes)):
            self.setCapacity(len(value))
            self.set(value)
        elif isinstance(value, GXByteBuffer):
            self.setCapacity(value.size - value.position)
            self.set(value)
        elif isinstance(value, int):
            self.setCapacity(value)
        elif isinstance(value, str):
            self.setHexString(value)
        else:
            self.setCapacity(0)

    def clear(self):
        """
        Clear buffer but do not release memory.
        """
        self.position = 0
        self.size = 0

    #
    #      Buffer capacity.
    #
    # Buffer capacity.
    #
    def getCapacity(self):
        if not self._data:
            return 0
        return len(self._data)

    #
    #      Allocate new size for the array in bytes.
    #
    #      @param capacity
    #                 Buffer capacity.
    #
    def setCapacity(self, capacity):
        if capacity == 0:
            self._data = bytearray()
            self.__size = 0
            self.__position = 0
        else:
            if not self._data:
                self._data = bytearray(capacity)
            else:
                tmp = self._data
                self._data = bytearray(capacity)
                if self.size < capacity:
                    self._data[0:self.size] = tmp
                else:
                    self._data[0:capacity] = self._data
                    self.__size = capacity

    capacity = property(getCapacity, setCapacity)
    """Buffer capacity."""

    def getPosition(self):
        return self.__position

    def setPosition(self, value):
        if value < 0 or value > len(self):
            raise ValueError("position")
        self.__position = value

    position = property(getPosition, setPosition)
    """Buffer position."""

    def getSize(self):
        return self.__size

    def setsize(self, value):
        if value < 0 or value > self.capacity:
            raise ValueError("size")
        self.__size = value
        if self.__position > self.__size:
            self.__position = self.__size

    size = property(getSize, setsize)
    """Buffer size."""

    def __len__(self):
        """Buffer size."""
        return self.__size

    def __getitem__(self, i):
        return self._data[i]

    def available(self):
        """Amount of non read bytes in the buffer."""
        return self.size - self.position

    #
    # Get buffer data as byte array.
    #
    def array(self):
        return self.subArray(0, self.size)

    #
    #      Returns sub array from byte buffer.
    #
    #      @param index
    #                 Start index.
    #      @param count
    #                 Byte count.
    # Sub array.
    #
    def subArray(self, index, count):
        if count != 0:
            tmp = bytearray(count)
            tmp[0:count] = self._data[index:index + count]
            return tmp
        return bytearray(0)

    #
    #      Move content from source to destination.
    #
    #      @param srcPos
    #                 Source position.
    #      @param destPos
    #                 Destination position.
    #      @param count
    #                 Item count.
    #
    def move(self, srcPos, destPos, count):
        if count < 0:
            raise ValueError("count")
        if count != 0:
            self._data[destPos:destPos + count] = self._data[srcPos:srcPos + count]
            self.size = destPos + count
            if self.position > self.size:
                self.position = self.size

    #
    #      Remove handled bytes.  This can be used in debugging to remove
    #      handled
    #      bytes.
    #
    def trim(self):
        if self.size == self.position:
            self.size = 0
        else:
            self.move(self.position, 0, self.size - self.position)
        self.position = 0

    #
    #      Push the given byte into this buffer at the current position, and
    #      then
    #      increments the position.
    #
    #      @param item
    #                 The byte to be added.
    #
    def setUInt8(self, item, index=None):
        if index is None:
            self.setUInt8(item, self.size)
            self.size += 1
        else:
            if index >= self.capacity:
                self.capacity = index + self.__ARRAY_CAPACITY
            self._data[index] = item

    #
    #      Push the given byte into this buffer at the current position, and
    #      then
    #      increments the position.
    #
    #      @param item
    #                 The byte to be added.
    #
    def setInt8(self, item, index=None):
        self.setUInt8(item & 0xFF, index)

    def setUInt16(self, item, index=None):
        if index is None:
            self.setUInt16(item, self.size)
            self.size += 2
        else:
            if index + 2 >= self.capacity:
                self.capacity = (index + self.__ARRAY_CAPACITY)
            self._data[index] = int(((item >> 8) & 0xFF))
            self._data[index + 1] = int((item & 0xFF))

    def setUInt32(self, item, index=None):
        if index is None:
            self.setUInt32(item, self.size)
            self.size += 4
        else:
            if index + 4 >= self.capacity:
                self.capacity = index + self.__ARRAY_CAPACITY
            self._data[index] = int(((item >> 24) & 0xFF))
            self._data[index + 1] = int(((item >> 16) & 0xFF))
            self._data[index + 2] = int(((item >> 8) & 0xFF))
            self._data[index + 3] = int((item & 0xFF))

    def setUInt64(self, item, index=None):
        if index is None:
            self.setUInt64(item, self.size)
            self.size += 8
        else:
            if index + 8 >= self.capacity:
                self.capacity = (index + self.__ARRAY_CAPACITY)
            self._data[self.size] = int(((item >> 56) & 0xFF))
            self._data[self.size + 1] = int(((item >> 48) & 0xFF))
            self._data[self.size + 2] = int(((item >> 40) & 0xFF))
            self._data[self.size + 3] = int(((item >> 32) & 0xFF))
            self._data[self.size + 4] = int(((item >> 24) & 0xFF))
            self._data[self.size + 5] = int(((item >> 16) & 0xFF))
            self._data[self.size + 6] = int(((item >> 8) & 0xFF))
            self._data[self.size + 7] = int((item & 0xFF))

    def setFloat(self, value, index=None):
        if index is None:
            self.setFloat(value, self.size)
            self.size += 4
        else:
            self.set(struct.pack("f", value), index)

    def setDouble(self, value, index=None):
        if index is None:
            self.setDouble(value, self.size)
            self.size += 8
        else:
            self.set(struct.pack("d", value), index)

    def getUInt8(self, index=None):
        if index is None:
            index = self.position
            value = self._data[index] & 0xFF
            value = value % 2 ** 8
            self.position += 1
            return value
        if index >= self.size:
            raise ValueError("getUInt8")
        value = self._data[index] & 0xFF
        value = value % 2 ** 8
        return value

    def getInt8(self, index=None):
        if index is None:
            index = self.position
            value = self._data[index]
            value = (value + 2 ** 7) % 2 ** 8 - 2 ** 7
            self.position += 1
            return value
        if index >= self.size:
            raise ValueError("getInt8")
        value = self._data[index]
        value = (value + 2 ** 7) % 2 ** 8 - 2 ** 7
        return value

    def getUInt16(self, index=None):
        if index is None:
            index = self.position
            value = ((self._data[index] & 0xFF) << 8) | (self._data[index + 1] & 0xFF)
            value = value % 2 ** 16
            self.position += 2
            return value
        if index + 2 > self.size:
            raise ValueError("getUInt16")
        value = ((self._data[index] & 0xFF) << 8) | (self._data[index + 1] & 0xFF)
        value = value % 2 ** 16
        return value

    def getInt16(self):
        return (self.getUInt16() + 2 ** 15) % 2 ** 16 - 2 ** 15

    def getInt32(self, index=None):
        if index is None:
            index = self.position
            if index + 4 > self.size:
                raise ValueError("getInt32")
            value = (self._data[index] & 0xFF) << 24 | (self._data[index + 1] & 0xFF) << 16 | (self._data[index + 2] & 0xFF) << 8 | (self._data[index + 3] & 0xFF)
            value = (value + 2 ** 31) % 2 ** 32 - 2 ** 31
            self.position += 4
            return value

        if index + 4 > self.size:
            raise ValueError("getInt32")
        value = (self._data[index] & 0xFF) << 24 | (self._data[index + 1] & 0xFF) << 16 | (self._data[index + 2] & 0xFF) << 8 | (self._data[index + 3] & 0xFF)
        value = (value + 2 ** 31) % 2 ** 32 - 2 ** 31
        return value

    def getUInt32(self, index=None):
        if index is None:
            index = self.position
            self.position += 4
        if index + 4 > self.size:
            raise ValueError("getUInt32")
        value = self._data[index] & 0xFF
        value = value << 24
        value |= (self._data[index + 1] & 0xFF) << 16
        value |= (self._data[index + 2] & 0xFF) << 8
        value |= (self._data[index + 3] & 0xFF)
        value = value % 2 ** 32
        return value

    def getFloat(self):
        tmp = bytearray(4)
        self.get(tmp)
        # Swap bytes.
        tmp2 = tmp[0]
        tmp[0] = tmp[3]
        tmp[3] = tmp2
        tmp2 = tmp[1]
        tmp[1] = tmp[2]
        tmp[2] = tmp2
        return struct.unpack("f", tmp)[0]

    def getDouble(self):
        tmp = bytearray(8)
        self.get(tmp)
        # Swap bytes.
        tmp2 = tmp[0]
        tmp[0] = tmp[7]
        tmp[7] = tmp2
        tmp2 = tmp[1]
        tmp[1] = tmp[6]
        tmp[6] = tmp2
        tmp2 = tmp[2]
        tmp[2] = tmp[5]
        tmp[5] = tmp2
        tmp2 = tmp[3]
        tmp[3] = tmp[4]
        tmp[4] = tmp2
        return struct.unpack("d", tmp)[0]

    def getInt64(self, index=None):
        if index is None:
            index = self.position
            self.position += 8
        value = ((self._data[index] & 0xFF)) << 56
        value |= ((self._data[index + 1] & 0xFF)) << 48
        value |= ((self._data[index + 2] & 0xFF)) << 40
        value |= ((self._data[index + 3] & 0xFF)) << 32
        value |= ((self._data[index + 4] & 0xFF)) << 24
        value |= (self._data[index + 5] & 0xFF) << 16
        value |= (self._data[index + 6] & 0xFF) << 8
        value |= (self._data[index + 7] & 0xFF)
        value = (value + 2 ** 63) % 2 ** 64 - 2 ** 63
        return value

    def getUInt64(self, index=None):
        value = self.getInt64(index)
        return value % 2 ** 64

    #
    #      Check is byte buffer ASCII string.
    #
    #      @param value
    #                 Byte array.
    # Is ASCII string.
    #
    @classmethod
    def isAsciiString(cls, value):
        # pylint: disable=too-many-boolean-expressions
        if value:
            for it in value:
                if (it < 32 or it > 127) and it != '\r' and it != '\n' and it != '\t' and it != 0:
                    return False
        return True

    def getString(self, index, count):
        if index is None and count is None:
            tmp = self._data[0:self.size]
            if self.isAsciiString(tmp):
                str_ = tmp.decode("utf-8").rstrip('\x00')
            else:
                str_ = self.hex(tmp)
            self.position += count
            return str_

        if index + count > self.size:
            raise ValueError("getString")
        tmp = self._data[index:index + count]
        if self.isAsciiString(tmp):
            return tmp.decode("utf-8").rstrip('\x00')
        return self.hex(tmp)

    def set(self, value, index=None, count=None):
        # pylint: disable=protected-access
        if isinstance(value, str):
            value = value.encode()
        if value:
            if index is None:
                if isinstance(value, GXByteBuffer):
                    index = value.position
                else:
                    index = 0
            if count is None:
                count = len(value) - index
            if isinstance(value, GXByteBuffer):
                self.set(value._data, index, count)
                value.position = index + count
            elif value and count != 0:
                if self.size + count > self.capacity:
                    self.capacity = self.size + count + self.__ARRAY_CAPACITY
                self._data[self.size:self.size + count] = value[index:index + count]
                self.size += count

    def get(self, target):
        len1 = len(target)
        if self.size - self.position < len1:
            raise ValueError("get")
        index = 0
        for index in range(0, len1):
            target[index] = self._data[self.position]
            self.position = self.position + 1

    #
    #      Compares, whether two given arrays are similar starting from current
    #      position.
    #
    #      @param arr
    #                 Array to compare.
    # True, if arrays are similar.  False, if the arrays differ.
    #
    def compare(self, arr):
        len1 = len(arr)
        if not arr or (self.size - self.position < len1):
            return False
        bytes_ = bytearray(len1)
        self.get(bytes_)
        ret = arr == bytes_
        if not ret:
            self.position -= len1
        return ret

    #
    #      Reverses the order of the given array.
    #
    def reverse(self):
        first = self.position
        last = self.size - 1
        tmp = int()
        while last > first:
            tmp = self._data[last]
            self._data[last] = self._data[first]
            self._data[first] = tmp
            last -= 1
            first += 1

    #
    #      Push the given hex string as byte array into this buffer at the
    #      current
    #      position, and then increments the position.
    #
    #      @param value
    #                 Byte array to add.
    #      @param index
    #                 Byte index.
    #      @param count
    #                 Byte count.
    #
    def setHexString(self, value, index=0, count=None):
        tmp = self.hexToBytes(value)
        if count is None:
            count = len(tmp)
        self.set(tmp, index, count)

    def __str__(self):
        return self.hex(self._data, True, 0, self.size)

    #
    #      Get remaining data.
    #
    # Remaining data as byte array.
    #
    def remaining(self):
        return self.subArray(self.position, self.size - self.position)

    #
    #      Get remaining data as a hex string.
    #
    #      @param addSpace
    #                 Add space between bytes.
    # Remaining data as a hex string.
    #
    def remainingHexString(self, addSpace=True):
        return self.hex(self._data, addSpace, self.position, self.size - self.position)

    #
    #      Get data as hex string.
    #
    #      @param addSpace
    #                 Add space between bytes.
    #      @param index
    #                 Byte index.
    #      @param count
    #                 Byte count.
    # Data as hex string.
    #
    def toHex(self, addSpace=True, index=0, count=None):
        if count is None:
            count = len(self) - index
        return self.hex(self._data, addSpace, index, count)

    #Convert char hex value to byte value.
    @classmethod
    def ___getValue(cls, c):
        #Id char.
        if c.islower():
            c = c.upper()
        pos = GXByteBuffer.__HEX_ARRAY.find(c)
        if pos == -1:
            raise Exception("Invalid hex string")
        return pos

    @classmethod
    def hexToBytes(cls, value):
        """Convert string to byte array.
        value: Hex string.
        Returns byte array.
        """
        buff = bytearray()
        if value:
            lastValue = -1
            for ch in value:
                if ch != ' ':
                    if lastValue == -1:
                        lastValue = cls.___getValue(ch)
                    elif lastValue != -1:
                        buff.append(lastValue << GXByteBuffer.__NIBBLE | cls.___getValue(ch))
                        lastValue = -1
                elif lastValue != -1:
                    buff.append(cls.___getValue(ch))
                    lastValue = -1
        return buff

    @classmethod
    def hex(cls, value, addSpace=True, index=0, count=None):
        """
        Convert byte array to hex string.
        """
        #Return empty string if array is empty.
        if not value:
            return ""
        hexChars = ""
        #Python 2.7 handles bytes as a string array. It's changed to bytearray.
        if sys.version_info < (3, 0) and not isinstance(value, bytearray):
            value = bytearray(value)
        if count is None:
            count = len(value)
        for it in value[index:count]:
            hexChars += GXByteBuffer.__HEX_ARRAY[it >> GXByteBuffer.__NIBBLE]
            hexChars += GXByteBuffer.__HEX_ARRAY[it & GXByteBuffer.__LOW_BYTE_PART]
            if addSpace:
                hexChars += ' '
        return hexChars.strip()

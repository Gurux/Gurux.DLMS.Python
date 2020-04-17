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
#
#  --------------------------------------------------------------------------
#
from .GXUInt8 import GXUInt8

# BitString class is used with Bit strings.
class GXBitString:

    #
    # Constructor.
    #
    # @param val
    # Bit string value.
    #
    def __init__(self, val, count=None):
        if isinstance(val, (GXUInt8)):
            val = GXBitString._toBitString(val, 8)
            if count:
                val = val[0:count]
        self.value = val

    #
    # Reserved for internal use.
    #
    @classmethod
    def _toBitString(cls, value, count):
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
    #
    # Bit string value.
    #
    def getValue(self):
        return self.value

    #
    # @param val
    # Bit string value.
    #
    def setValue(self, val):
        self.value = val

    def __str__(self):
        return self.value

    #
    # Bit string value as byte.
    #
    def toByte(self):
        val = 0
        if self.value:
            index = 7
            for it in self.value:
                if it == '1':
                    val |= (1 << index)
                elif it != '0':
                    raise ValueError("Invalid parameter.")
                index = index - 1
        return val

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


class GXBitString:
    # pylint: disable=import-outside-toplevel
    def __init__(self, value=None, pad_count=None):
        from .internal._GXCommon import _GXCommon

        self.__padBits = 0
        self.value = bytearray()

        if isinstance(value, str):
            self.pad_bits = 8 - (len(value) % 8)
            if self.pad_bits == 8:
                self.pad_bits = 0
            bit_str = value + "0" * self.pad_bits
            self.value = bytearray(
                int(bit_str[i : i + 8], 2) for i in range(0, len(bit_str), 8)
            )

        elif isinstance(value, (bytes, bytearray)) and pad_count is not None:
            if pad_count < 0 or pad_count > 7:
                raise ValueError("PadCount must be in the range 0 to 7")
            self.value = bytearray(value)
            self.pad_bits = pad_count

        elif isinstance(value, (bytes, bytearray)):
            if len(value) == 0:
                raise ValueError("value cannot be empty")
            self.pad_bits = value[0]
            if self.pad_bits < 0 or self.pad_bits > 7:
                raise ValueError("PadCount must be in the range 0 to 7")
            self.value = bytearray(value[1:])

        elif isinstance(value, int) and pad_count is not None:
            self.pad_bits = pad_count % 8
            length = (pad_count // 8) + (1 if self.pad_bits else 0)
            self.value = bytearray()
            for _ in range(length):
                self.value.append(_GXCommon.swapBits(value & 0xFF))
                value >>= 8

    @property
    def padBits(self):
        """Number of extra bits at the end of the string."""
        return self.__padBits

    @property
    def length(self):
        return 0 if not self.value else (8 * len(self.value)) - self.pad_bits

    def __str__(self):
        return self.toString(False)

    # pylint: disable=import-outside-toplevel
    def toString(self, show_bits=False):
        from .internal._GXCommon import _GXCommon

        if not self.value:
            return ""
        bits = "".join(_GXCommon.toBitString(byte, 8) for byte in self.value)
        bits = bits[: len(bits) - self.pad_bits]

        return f"{len(bits)} bit {bits}" if show_bits else bits

    def toInteger(self):
        from .internal._GXCommon import _GXCommon

        result = 0
        pos = 0
        for byte in self.value:
            result |= _GXCommon.swapBits(byte) << pos
            pos += 8
        return result

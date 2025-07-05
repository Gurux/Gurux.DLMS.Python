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
#  More information of Gurux products: http:#www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http:#www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------


class GXAsn1Integer(int):
    # Integer length in bytes.
    length = 0

    """
    ASN1 integer value.
    """

    def __new__(cls, value):
        if isinstance(value, (bytearray, bytes)):
            tmp = super().__new__(cls, int.from_bytes(value, byteorder="big"))
            tmp.length = len(value)
        elif isinstance(value, int):
            tmp = super().__new__(cls, value)
            tmp.length = int((7 + value.bit_length()) / 8)
        else:
            raise ValueError("Invalid value.")
        return tmp

    def toArray(self):
        return self.to_bytes(self.length, byteorder="big")

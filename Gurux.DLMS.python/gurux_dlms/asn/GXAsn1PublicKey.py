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
from ..GXBitString import GXBitString
from ..asn.GXAsn1Sequence import GXAsn1Sequence
from ..GXByteBuffer import GXByteBuffer


# pylint: disable=too-few-public-methods, import-outside-toplevel
class GXAsn1PublicKey:
    """
    ASN1 Public key.
    """

    def __init__(self, key=None):
        """
        Constructor.
        - key: bytes or GXBitString
        """
        self.value = None
        if key is None:
            return

        if isinstance(key, GXBitString):
            from gurux_dlms.asn.GXAsn1Converter import GXAsn1Converter

            seq = GXAsn1Converter.fromByteArray(key.value)
            if not isinstance(seq, GXAsn1Sequence):
                raise ValueError("Invalid ASN1 sequence")
            self._init(GXAsn1Converter.toByteArray([seq[0], seq[1]]))
        elif isinstance(key, (bytes, bytearray)):
            self._init(key)
        else:
            raise TypeError("Invalid argument type for key")

    def _init(self, key: bytes):
        if key is None or len(key) != 270:
            raise ValueError("data")
        self.value = bytearray(key)  # Kopioidaan key ? value

    def __str__(self):
        """
        Returns the public key as a hex string.
        """
        if self.value is None:
            return ""
        return GXByteBuffer.hex(self.value, False)

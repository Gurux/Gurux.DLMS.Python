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
from gurux_dlms.GXIntEnum import GXIntEnum

class MBusEncryptionMode(GXIntEnum):
    """Encryption modes."""

    # Encryption is not used.
    NONE = 0

    # AES with Counter Mode = CTR) noPadding and IV.
    AES_128 = 1

    # DES with Cipher Block Chaining Mode = CBC).
    DES_CBC = 2

    # DES with Cipher Block Chaining Mode = CBC) and Initial Vector.
    DES_CBC_IV = 3

    # AES with Cipher Block Chaining Mode = CBC) and Initial Vector.
    AES_CBC_IV = 5

    # AES 128 with Cipher Block Chaining Mode = CBC) and dynamic key and
    # Initial Vector with 0.
    AES_CBC_IV0 = 7

    # TLS
    Tls = 13

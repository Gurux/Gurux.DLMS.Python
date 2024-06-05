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
from ..GXIntEnum import GXIntEnum


class MethodAccessMode3(GXIntEnum):
    """Enumerated method access types for logical name association version 3."""

    # pylint: disable=too-few-public-methods

    # No access.
    NO_ACCESS = 0

    # Access.
    ACCESS = 1

    # Authenticated request.
    AUTHENTICATED_REQUEST = 0x4

    # Encrypted request.
    ENCRYPTED_REQUEST = 0x8

    # Digitally signed request.
    DIGITALLY_SIGNED_REQUEST = 0x10

    # Authenticated response.
    Authenticated_Response = 0x20

    # Encrypted response.
    ENCRYPTED_RESPONSE = 0x40

    # Digitally signed response.
    DIGITALLY_SIGNED_RESPONSE = 0x80

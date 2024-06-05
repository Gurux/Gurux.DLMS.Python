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


class AccessMode3(GXIntEnum):
    """
    Enumerates access modes for Logical Name Association version 3.
    """

    # pylint: disable=too-few-public-methods

    # No access.
    NO_ACCESS = 0

    # The client is allowed only reading from the server.
    READ = 1

    # The client is allowed only writing to the server.
    WRITE = 2

    # The client is allowed both reading from the server and writing to it.
    READ_WRITE = 3

    # Request messages are authenticated.
    AUTHENTICATED_REQUEST = 4

    # Request messages are encrypted.
    ENCRYPTED_REQUEST = 8

    # Request messages are digitally signed.
    DIGITALLY_SIGNED_REQUEST = 16

    # Response messages are authenticated.
    AUTHENTICATED_RESPONSE = 32

    # Response messages are encrypted.
    ENCRYPTED_RESPONSE = 64

    # Response messages are digitally signed.
    DIGITALLY_SIGNED_RESPONSE = 128
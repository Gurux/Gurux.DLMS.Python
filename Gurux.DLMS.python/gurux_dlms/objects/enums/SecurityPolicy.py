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
from gurux_dlms.GXIntFlag import GXIntFlag

class SecurityPolicy(GXIntFlag):
    """
    Security policy Enforces authentication and/or encryption algorithm
    provided with security suite.  This enumeration is used for version 1.
    """
    #pylint: disable=too-few-public-methods

    #
    # Security is not used.
    #
    NOTHING = 0
    #
    # Request is authenticated.
    #
    AUTHENTICATED_REQUEST = 0x4

    #
    # Request is encrypted.
    #
    ENCRYPTED_REQUEST = 0x8

    #
    # Request is digitally signed.
    #
    DIGITALLY_SIGNED_REQUEST = 0x10

    #
    # Response authenticated.
    #
    AUTHENTICATED_RESPONSE = 0x20

    #
    # Response encrypted.
    #
    ENCRYPTED_RESPONSE = 0x40

    #
    # Response is digitally signed.
    #
    DIGITALLY_SIGNED_RESPONSE = 0x80

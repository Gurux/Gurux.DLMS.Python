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

class Authentication(GXIntEnum):
    """
    Authentication enumerates the authentication levels.
    """
    #pylint: disable=too-few-public-methods

    #No authentication is used.
    NONE = 0

    #Low authentication is used.
    LOW = 1

    #High authentication is used.
    HIGH = 2

    #High authentication is used.  Password is hashed with MD5.
    HIGH_MD5 = 3

    #High authentication is used.  Password is hashed with SHA1.
    HIGH_SHA1 = 4

    #High authentication is used.  Password is hashed with GMAC.
    HIGH_GMAC = 5

    #High authentication is used.  Password is hashed with SHA-256.
    HIGH_SHA256 = 6

    #High authentication is used.  Password is hashed with ECDSA.
    HIGH_ECDSA = 7

    @classmethod
    def valueofString(cls, value):
        return Authentication[value.upper()]

    @classmethod
    def toString(cls, value):
        if value == 0:
            tmp = "None"
        elif value == 1:
            tmp = "Low"
        elif value == 2:
            tmp = "High"
        elif value == 3:
            tmp = "HighMd5"
        elif value == 4:
            tmp = "HighSha1"
        elif value == 5:
            tmp = "HighGmac"
        elif value == 6:
            tmp = "HighSha256"
        elif value == 7:
            tmp = "HighEcdsa"
        else:
            raise ValueError("Invalid Authentication value.")
        return tmp

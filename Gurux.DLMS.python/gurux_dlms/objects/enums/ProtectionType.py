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
from gurux_dlms.GXIntEnum import GXIntEnum


class ProtectionType(GXIntEnum):
    """
    Enumerated data protection types.
    """

    AUTHENTICATION = 0
    """
    Authentication.
    """
    ENCRYPTION = 1
    """
    Encryption
    """
    AUTHENTICATION_ENCRYPTION = 2
    """
    Authentication and encryption.
    """
    DIGITAL_SIGNATURE = 3
    """
    Digital signature
    """

    @classmethod
    def valueofString(cls, value):
        if value == "Authentication":
            ret = ProtectionType.AUTHENTICATION
        elif value == "Encryption":
            ret = ProtectionType.ENCRYPTION
        elif value == "AuthenticationEncryption":
            ret = ProtectionType.AUTHENTICATION_ENCRYPTION
        elif value == "DigitalSignature":
            ret = ProtectionType.DIGITAL_SIGNATURE
        else:
            raise ValueError("Unknown enum value: " + str(value))
        return ret

    def __str__(self):
        if self.value == ProtectionType.AUTHENTICATION:
            ret = "Authentication"
        elif self.value == ProtectionType.ENCRYPTION:
            ret = "Encryption"
        elif self.value == ProtectionType.AUTHENTICATION_ENCRYPTION:
            ret = "AuthenticationEncryption"
        elif self.value == ProtectionType.DIGITAL_SIGNATURE:
            ret = "DigitalSignature"
        else:
            raise ValueError("Unknown enum value: " + str(self.value))
        return ret

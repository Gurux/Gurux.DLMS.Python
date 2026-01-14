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

class ProtectionMode(GXIntEnum):
    '''
    Enumerates communication port protection mode values.
    '''

    LOCKED = 0
    '''
    Port is locked. Communication is not possible.
    '''
    LOCKED_ON_FAILED_ATTEMPTS = 1
    '''
    The port becomes temporarily locked when failed connections exceeds an allowed.
    '''
    UNLOCKED = 2
    '''
    Port is unlocked.
    '''

    @classmethod
    def valueofString(cls, value):
        if value == "Locked":
            ret = ProtectionMode.LOCKED
        elif value == "LockedOnFailedAttempts":
            ret = ProtectionMode.LOCKED_ON_FAILED_ATTEMPTS
        elif value == "Unlocked":
            ret = ProtectionMode.UNLOCKED
        else:
            raise ValueError("Unknown enum value: " + str(value))
        return ret

    def __str__(self):
        if self.value == ProtectionMode.LOCKED:
            ret = "Locked"
        elif self.value == ProtectionMode.LOCKED_ON_FAILED_ATTEMPTS:
            ret = "LockedOnFailedAttempts"
        elif self.value == ProtectionMode.UNLOCKED:
            ret = "Unlocked"
        else:
            raise ValueError("Unknown enum value: " + str(self.value))
        return ret

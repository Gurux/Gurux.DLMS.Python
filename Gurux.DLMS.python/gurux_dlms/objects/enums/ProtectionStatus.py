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

class ProtectionStatus(GXIntEnum):
    '''
    Enumerates communication port protection status values.
    '''

    UNLOCKED = 0
    '''
    Port is unlocked.
    '''
    TEMPORARILY_LOCKED = 1
    '''
    The port is temporarily locked. Communication is not possible.
    '''
    LOCKED = 2
    '''
    Port is locked. Communication is not possible.
    '''

    @classmethod
    def valueofString(cls, value):
        if value == "Unlocked":
            ret = ProtectionStatus.UNLOCKED
        elif value == "TemporarilyLocked":
            ret = ProtectionStatus.TEMPORARILY_LOCKED
        elif value == "Locked":
            ret = ProtectionStatus.LOCKED
        else:
            raise ValueError("Unknown enum value: " + str(value))
        return ret

    def __str__(self):
        if self.value == ProtectionStatus.UNLOCKED:
            ret = "Unlocked"
        elif self.value == ProtectionStatus.TEMPORARILY_LOCKED:
            ret = "TemporarilyLocked"
        elif self.value == ProtectionStatus.LOCKED:
            ret = "Locked"
        else:
            raise ValueError("Unknown enum value: " + str(self.value))
        return ret

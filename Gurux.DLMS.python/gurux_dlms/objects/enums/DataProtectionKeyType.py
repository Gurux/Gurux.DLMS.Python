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

class DataProtectionKeyType(GXIntEnum):
    '''
    Enumerates data protection key types.
    '''

    IDENTIFIED = 0
    '''
    Identified key.
    '''
    WRAPPED = 1
    '''
    Wrapped key.
    '''
    AGREED = 2
    '''
    Agreed.
    '''

    @classmethod
    def valueofString(cls, value):
        if value == "Identified":
            ret = DataProtectionKeyType.IDENTIFIED
        elif value == "Wrapped":
            ret = DataProtectionKeyType.WRAPPED
        elif value == "Agreed":
            ret = DataProtectionKeyType.AGREED
        else:
            raise ValueError("Unknown enum value: " + str(value))
        return ret

    def __str__(self):
        if self.value == DataProtectionKeyType.IDENTIFIED:
            ret = "Identified"
        elif self.value == DataProtectionKeyType.WRAPPED:
            ret = "Wrapped"
        elif self.value == DataProtectionKeyType.AGREED:
            ret = "Agreed"
        else:
            raise ValueError("Unknown enum value: " + str(self.value))
        return ret

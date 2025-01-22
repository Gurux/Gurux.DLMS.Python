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

class DataProtectionIdentifiedKeyType(GXIntEnum):
    '''
    Data protection identified key types.
    '''

    UNICAST_ENCRYPTION = 0
    '''
    Global unicast encryption key.
    '''
    BROADCAST_ENCRYPTION = 1
    '''
    Global broadcast encryption key.
    '''

    @classmethod
    def valueofString(cls, value):
        if value == "UnicastEncryption":
            ret = DataProtectionIdentifiedKeyType.UNICAST_ENCRYPTION
        elif value == "BroadcastEncryption":
            ret = DataProtectionIdentifiedKeyType.BROADCAST_ENCRYPTION
        else:
            raise ValueError("Unknown enum value: " + str(value))
        return ret

    def __str__(self):
        if self.value == DataProtectionIdentifiedKeyType.UNICAST_ENCRYPTION:
            ret = "UnicastEncryption"
        elif self.value == DataProtectionIdentifiedKeyType.BROADCAST_ENCRYPTION:
            ret = "BroadcastEncryption"
        else:
            raise ValueError("Unknown enum value: " + str(self.value))
        return ret

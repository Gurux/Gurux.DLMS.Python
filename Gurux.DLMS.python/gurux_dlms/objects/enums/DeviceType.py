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

class DeviceType(GXIntEnum):
    '''
    Defines the type of the device connected to the modem.
    '''

    PAN_DEVICE = 0
    '''
    PAN device.
    '''
    PAN_COORDINATOR = 1
    '''
    PAN coordinator.
    '''
    NOT_DEFINED = 2
    '''
    Not Defined.
    '''

    @classmethod
    def valueofString(cls, value):
        if value == "PanDevice":
            ret = DeviceType.PAN_DEVICE
        elif value == "PanCoordinator":
            ret = DeviceType.PAN_COORDINATOR
        elif value == "NotDefined":
            ret = DeviceType.NOT_DEFINED
        else:
            raise ValueError("Unknown enum value: " + str(value))
        return ret

    def __str__(self):
        if self.value == DeviceType.PAN_DEVICE:
            ret = "PanDevice"
        elif self.value == DeviceType.PAN_COORDINATOR:
            ret = "PanCoordinator"
        elif self.value == DeviceType.NOT_DEFINED:
            ret = "NotDefined"
        else:
            raise ValueError("Unknown enum value: " + str(self.value))
        return ret

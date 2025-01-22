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

class PushOperationMethod(GXIntEnum):
    '''
    Push operation method defines what service class is used with push messages.
    '''

    UNCONFIRMED_FAILURE = 0
    '''
    Unconfirmed, retry on supporting protocol layer failure.
    '''
    UNCONFIRMED_MISSING = 1
    '''
    Unconfirmed, retry on missing supporting protocol layer confirmation.
    '''
    CONFIRMED = 2
    '''
    Confirmed, retry on missing confirmation.
    '''

    @classmethod
    def valueofString(cls, value):
        if value == "UnconfirmedFailure":
            ret = PushOperationMethod.UNCONFIRMED_FAILURE
        elif value == "UnconfirmedMissing":
            ret = PushOperationMethod.UNCONFIRMED_MISSING
        elif value == "Confirmed":
            ret = PushOperationMethod.CONFIRMED
        else:
            raise ValueError("Unknown enum value: " + str(value))
        return ret

    def __str__(self):
        if self.value == PushOperationMethod.UNCONFIRMED_FAILURE:
            ret = "UnconfirmedFailure"
        elif self.value == PushOperationMethod.UNCONFIRMED_MISSING:
            ret = "UnconfirmedMissing"
        elif self.value == PushOperationMethod.CONFIRMED:
            ret = "Confirmed"
        else:
            raise ValueError("Unknown enum value: " + str(self.value))
        return ret

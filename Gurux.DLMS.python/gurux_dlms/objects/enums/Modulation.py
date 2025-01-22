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

class Modulation(GXIntEnum):
    '''
    Enumerates modulation types.
    '''

    ROBUST_MODE = 0
    '''
    Robust Mode.
    '''
    DB_PSK = 1
    '''
    DBPSK.
    '''
    DQ_PSK = 2
    '''
    DQPSK.
    '''
    D8PSK = 3
    '''
    D8PSK.
    '''
    QAM16 = 4
    '''
    16-QAM.
    '''

    @classmethod
    def valueofString(cls, value):
        if value == "RobustMode":
            ret = Modulation.ROBUST_MODE
        elif value == "DbPsk":
            ret = Modulation.DB_PSK
        elif value == "DqPsk":
            ret = Modulation.DQ_PSK
        elif value == "D8Psk":
            ret = Modulation.D8PSK
        elif value == "Qam16":
            ret = Modulation.QAM16
        else:
            raise ValueError("Unknown enum value: " + str(value))
        return ret

    def __str__(self):
        if self.value == Modulation.ROBUST_MODE:
            ret = "RobustMode"
        elif self.value == Modulation.DB_PSK:
            ret = "DbPsk"
        elif self.value == Modulation.DQ_PSK:
            ret = "DqPsk"
        elif self.value == Modulation.D8PSK:
            ret = "D8Psk"
        elif self.value == Modulation.QAM16:
            ret = "Qam16"
        else:
            raise ValueError("Unknown enum value: " + str(self.value))
        return ret

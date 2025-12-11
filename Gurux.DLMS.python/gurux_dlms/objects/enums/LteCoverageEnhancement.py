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


class LteCoverageEnhancement(GXIntEnum):
    """
    Lte coverage enhancement.
    """

    LEVEL0 = 0
    """
    CE Mode A in LTE Cat M1 and CE Level 0 in NB-Iot.
    """
    LEVEL1 = 1
    """
    CE Mode B in LTE Cat M1 and CE Level 1 in NB-Iot.
    """
    LEVEL2 = 2
    """
    CE Level 2 in NB-Iot.
    """

    @classmethod
    def valueofString(cls, value):
        if value == "Level0":
            ret = LteCoverageEnhancement.LEVEL0
        elif value == "Level1":
            ret = LteCoverageEnhancement.LEVEL1
        elif value == "Level2":
            ret = LteCoverageEnhancement.LEVEL2
        else:
            raise ValueError("Unknown enum value: " + str(value))
        return ret

    def __str__(self):
        if self.value == LteCoverageEnhancement.LEVEL0:
            ret = "Level0"
        elif self.value == LteCoverageEnhancement.LEVEL1:
            ret = "Level1"
        elif self.value == LteCoverageEnhancement.LEVEL2:
            ret = "Level2"
        else:
            raise ValueError("Unknown enum value: " + str(self.value))
        return ret

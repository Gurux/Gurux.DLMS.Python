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
from gurux_dlms.objects.enums.LteCoverageEnhancement import LteCoverageEnhancement


class GXLteQualityOfService:
    """
    Quality of service of the LTE network.
    """

    __signalQuality = 0
    "Signal quality."

    __signalLevel = 0
    "Signal level."

    __signalToNoiseRatio = 0
    "Signal to noise ratio."

    __coverageEnhancement = LteCoverageEnhancement.LEVEL0
    "Coverage enhancement."

    @property
    def signalQuality(self):
        """
        Signal quality.
        """
        return self.__signalQuality

    @signalQuality.setter
    def signalQuality(self, value):
        self.__signalQuality = value

    @property
    def signalLevel(self):
        """
        Signal level.
        """
        return self.__signalLevel

    @signalLevel.setter
    def signalLevel(self, value):
        self.__signalLevel = value

    @property
    def signalToNoiseRatio(self):
        """
        Signal to noise ratio.
        """
        return self.__signalToNoiseRatio

    @signalToNoiseRatio.setter
    def signalToNoiseRatio(self, value):
        self.__signalToNoiseRatio = value

    @property
    def coverageEnhancement(self):
        """
        Coverage enhancement.
        """
        return self.__coverageEnhancement

    @coverageEnhancement.setter
    def coverageEnhancement(self, value):
        self.__coverageEnhancement = value

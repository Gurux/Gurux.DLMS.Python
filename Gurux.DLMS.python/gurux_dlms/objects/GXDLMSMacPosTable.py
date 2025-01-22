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
class GXDLMSMacPosTable:
    __shortAddress = None
    "The 16-bit address the device is using to communicate through the PAN."

    __lQI = 0
    "Link Quality Indicator."

    __validTime = None
    "Valid time."

    @property
    def shortAddress(self):
        """
        The 16-bit address the device is using to communicate through the PAN.
        """
        return self.__shortAddress

    @shortAddress.setter
    def shortAddress(self, value):
        self.__shortAddress = value

    @property
    def lQI(self):
        """
        Link Quality Indicator.
        """
        return self.__lQI

    @lQI.setter
    def lQI(self, value):
        self.__lQI = value

    @property
    def validTime(self):
        """
        Valid time,
        """
        return self.__validTime

    @validTime.setter
    def validTime(self, value):
        self.__validTime = value

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

class GXPushConfirmationParameter:
    """
    Push confirmation parameters.
    """

    def __init__(self):
        self.__startDate = None
        self.__interval = None

    @property
    def startDate(self):
        """
        Confirmation start date. Fields of date-time not specified are not used.
        """
        return self.__startDate

    @startDate.setter
    def startDate(self, value):
        self.__startDate = value

    @property
    def interval(self):
        """
        Confirmation time interval in seconds. Disabled, if zero.
        """
        return self.__interval

    @interval.setter
    def interval(self, value):
        self.__interval = value

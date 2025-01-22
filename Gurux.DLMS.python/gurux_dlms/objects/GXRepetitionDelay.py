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
class GXRepetitionDelay:
    """
    This class is used to count repetition delay for the next push message.
    """

    def __init__(self):
        self.__min = 0
        self.__exponent = 0
        self.__max = 0

    @property
    def min(self):
        """
        The minimum delay until a next push attempt is started in seconds.
        """
        return self.__min

    @min.setter
    def min(self, value):
        self.__min = value

    @property
    def exponent(self):
        """
        Calculating the next delay.
        """
        return self.__exponent

    @exponent.setter
    def exponent(self, value):
        self.__exponent = value

    @property
    def max(self):
        """
        The maximum delay until a next push attempt is started in seconds.
        """
        return self.__max

    @max.setter
    def max(self, value):
        self.__max = value

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
from gurux_dlms.objects.enums.RestrictionType import RestrictionType


class GXDLMSRestriction:
    """
    Compact data and push object restriction values.
    """

    def __init__(self):
        self.__type = RestrictionType.NONE
        self.__from = None
        self.__to = None

    @property
    def type(self):
        """
        Restriction type.
        """
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def from_(self):
        """
        From date or entry.
        """
        return self.__from

    @from_.setter
    def from_(self, value):
        self.__from = value

    @property
    def to(self):
        """
        To date or entry.
        """
        return self.__to

    @to.setter
    def to(self, value):
        self.__to = value

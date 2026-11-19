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
#  More information of Gurux products: http://www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http://www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------


class GXMappingTable:
    """Reference status table ID and its mapping value."""

    def __init__(self):
        self.__refefence_table_id = 0
        self.__refefence_table_mapping = None

    @property
    def refefence_table_id(self):
        """Reference status table ID (unsigned 8-bit integer)."""
        return self.__refefence_table_id

    @refefence_table_id.setter
    def refefence_table_id(self, value):
        self.__refefence_table_id = value

    @property
    def refefence_table_mapping(self):
        """Reference table mapping value; None when no mapping is assigned."""
        return self.__refefence_table_mapping

    @refefence_table_mapping.setter
    def refefence_table_mapping(self, value):
        self.__refefence_table_mapping = value

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
#
#  * OBIS Code class is used to find out default description to OBIS Code.
#
class GXStandardObisCode:
    #
    # Constructor.
    #
    def __init__(self, forObis, desc=None, forInterfaces=None, forDataType=""):
        # OBIS code.
        if forObis is None:
            self.obis = [0, 0, 0, 0, 0, 0]
        else:
            self.obis = forObis
        # OBIS code description.
        self.description = desc
        # Interfaces that are using this OBIS code.
        self.interfaces = forInterfaces
        # Standard data types.
        self.dataType = forDataType
        #Standard UI data types.
        self.uiDataType = None

    #
    # Convert to string.
    #
    # @return
    #
    def __str__(self):
        str_ = ""
        for s in self.obis:
            if str_:
                str_ += '.'
            str_ += s
        return str_ + " " + self.description

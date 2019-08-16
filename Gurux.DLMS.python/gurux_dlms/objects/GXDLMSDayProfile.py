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
class GXDLMSDayProfile:
    """
    Activity Calendar's Day profile is defined on the standard.
    """
    #pylint: disable=bad-option-value,old-style-class,too-few-public-methods

    def __init__(self, day=0, schedules=None):
        """
        # Constructor.

        day: value of the day.
        schedules: Collection of schedules.
        """
        self.dayId = day
        self.daySchedules = schedules

    def __str__(self):
        str_ = str(self.dayId)
        if self.daySchedules:
            for it in self.daySchedules:
                str_ += " " + it.__str__()
        return str_

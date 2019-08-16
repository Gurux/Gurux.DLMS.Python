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

###Python 2 requires this
#pylint: disable=bad-option-value,old-style-class
class GXDLMSScheduleEntry:
    """Executed scripts."""
    #pylint: disable=too-few-public-methods,too-many-instance-attributes

    def __init__(self):
        """#Constructor."""
        # Schedule entry index.
        self.index = 0
        # Is Schedule entry enabled.
        self.enable = False
        # Logical name of the Script table object.
        self.logicalName = None
        # Script identifier of the script to be executed.
        self.scriptSelector = 0
        self.switchTime = None
        # Defines a period in minutes, in which an entry shall be processed
        # after power fail.
        self.validityWindow = 0
        # Days of the week on which the entry is valid.
        self.execWeekdays = None
        # Perform the link to the IC Special days table, day_id.
        self.execSpecDays = None
        # Date starting period in which the entry is valid.
        self.beginDate = None
        # Date starting period in which the entry is valid.
        self.endDate = None

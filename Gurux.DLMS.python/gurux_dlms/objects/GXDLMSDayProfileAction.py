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
class GXDLMSDayProfileAction:
    """
    Activity Calendar's Day Profile Action is defined on the standard.
    """

    # pylint: disable=bad-option-value,old-style-class,too-few-public-methods

    def __init__(self, startTime=None, scriptLogicalName=None, scriptSelector=0):
        """
        Constructor.

         startTime: Start time.
         scriptLogicalName: Logical name.
         scriptSelector: Script selector.
        """
        self.startTime = startTime
        self.scriptLogicalName = scriptLogicalName
        self.scriptSelector = scriptSelector

    def __str__(self):
        return (
            str(self.startTime)
            + " "
            + self.scriptLogicalName
            + ":"
            + str(self.scriptSelector)
        )

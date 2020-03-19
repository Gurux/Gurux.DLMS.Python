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

from ..GXByteBuffer import GXByteBuffer

###Python 2 requires this
#pylint: disable=bad-option-value,old-style-class,too-few-public-methods
class GXDLMSSeasonProfile:
    # Constructor.
    #
    # @param forName
    # name of season profile.
    # @param forStart
    # Start time.
    # @param forWeekName
    # Week name.
    def __init__(self, forName=None, forStart=None, forWeekName=None):
        self.name = forName
        self.start = forStart
        self.weekName = forWeekName

    def __str__(self):
        if GXByteBuffer.isAsciiString(self.name):
            tmp = self.name.decode("utf-8")
        else:
            tmp = GXByteBuffer.hex(self.name)
        return tmp + " " + str(self.start)

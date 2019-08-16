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
# pylint: disable=bad-option-value,old-style-class,too-few-public-methods
class GXServerReply:
    #
    # Constructor.
    #
    # @param value
    #            Received data.
    #
    def __init__(self, value):
        # Connection info.
        self.connectionInfo = None
        # Server reply message.
        self.reply = []
        # Message count to send.
        self.count = 0
        # Server received data.
        self.data = value

    #
    # Is GBT streaming in progress.
    #
    def isStreaming(self):
        return self.count != 0

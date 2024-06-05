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
from .GXByteBuffer import GXByteBuffer


# Long get or set information is saved here.
#
class GXDLMSLongTransaction:
    # pylint: disable=too-few-public-methods
    #
    # Constructor.
    #
    # @param forTargets
    #            Targets.
    # @param forCommand
    #            Command.
    # @param forData
    #            Data.
    #
    def __init__(self, forTargets, forCommand, forData=None):
        # Targets.
        self.targets = forTargets
        # Executed command.
        self.command = forCommand
        # Extra data from PDU.
        self.data = GXByteBuffer()
        if forData:
            self.data.set(forData)

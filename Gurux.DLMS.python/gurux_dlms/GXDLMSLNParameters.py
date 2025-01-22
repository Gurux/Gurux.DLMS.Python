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

from .enums.Command import Command
from .GetCommandType import GetCommandType


#
#  LN Parameters
# pylint: disable=too-many-instance-attributes, too-many-arguments, too-few-public-methods
class GXDLMSLNParameters:
    #
    # Constructor.
    #
    # forSettings: DLMS settings.
    # forInvokeId: Invoke ID.
    # forCommand: Command.
    # forCommandType: Command type.
    # forAttributeDescriptor: Attribute descriptor.
    # forData: Data.
    def __init__(
        self,
        forSettings,
        forInvokeId,
        forCommand,
        forCommandType,
        forAttributeDescriptor,
        forData,
        forStatus,
    ):
        # DLMS settings.
        self.settings = forSettings
        self.invokeId = forInvokeId
        self.blockIndex = self.settings.blockIndex
        self.blockNumberAck = self.settings.blockNumberAck
        # DLMS Command.
        self.command = forCommand
        # Request type.
        self.requestType = forCommandType
        # Attribute descriptor.
        self.attributeDescriptor = forAttributeDescriptor
        # Data.
        self.data = forData
        # Send date and time.  This is used in Data notification messages.
        self.time = None
        # Reply status.
        self.status = forStatus
        # Are there more data to send or more data to receive.
        self.multipleBlocks = forSettings.count != forSettings.index
        # Is this last block in send.
        self.lastBlock = forSettings.count == forSettings.index
        self.gbtWindowSize = 1
        # Is GBT streaming used.
        self.streaming = False
        if self.settings:
            self.settings.command = forCommand
            if (
                forCommand == Command.GET_REQUEST
                and forCommandType != GetCommandType.NEXT_DATA_BLOCK
            ):
                self.settings.commandType = forCommandType

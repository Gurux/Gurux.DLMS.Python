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

# SN Parameters
#
# pylint: disable=too-many-instance-attributes,too-many-arguments
class GXDLMSSNParameters:
    #
    # Constructor.
    #
    # @param forSettings
    #            DLMS settings.
    # @param forCommand
    #            Command.
    # @param forCommandType
    #            Command type.
    # @param forAttributeDescriptor
    # @param forData
    #            Attribute descriptor
    # Generated messages.
    #
    def __init__(self, forSettings, forCommand, forCount, forCommandType, forAttributeDescriptor, forData):
        # DLMS settings.
        self.settings = forSettings
        # Block index.
        self.blockIndex = self.settings.blockIndex
        # DLMS Command.
        self.command = forCommand
        # Item Count.
        self.count = forCount
        # Request type.
        self.requestType = forCommandType
        # Attribute descriptor.
        self.attributeDescriptor = forAttributeDescriptor
        # Data.
        self.data = forData
        # Are there more data to send or more data to receive.
        self.multipleBlocks = False
        # Send date and time. This is used in Data notification messages.
        self.time = None

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
class GXDLMSTranslatorMessage:
    ##pylint: disable=too-many-instance-attributes,too-few-public-methods
    def __init__(self):
        """
        Constructor.
        """
        self.message = None
        """Message to convert to XML."""
        # Converted XML.
        self.xml = None
        # Executed Command.
        self.command = None
        # System title from AARQ or AARE messages.
        self.systemTitle = None
        # Dedicated key from AARQ messages.
        self.dedicatedKey = None
        # Interface type.
        self.interfaceType = None
        # Client address.
        self.sourceAddress = 0
        # Server address.
        self.targetAddress = 0
        # Is more data available. Return None if more data is not available or Frame or Block type.
        self.moreData = 0
        # Occurred exception.
        self.exception = None

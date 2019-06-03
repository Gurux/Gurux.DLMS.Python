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
#  GXDLMSLimits contains commands for retrieving and setting the limits of
#  field ength and window size, when communicating with the server.
#
class GXDLMSLimits:
    DEFAULT_MAX_INFO_TX = 128
    DEFAULT_MAX_INFO_RX = 128
    DEFAULT_WINDOWS_SIZE_TX = 1
    DEFAULT_WINDOWS_SIZE_RX = 1

    #
    # Constructor.
    #
    def __init__(self):
        self.maxInfoTX = self.DEFAULT_MAX_INFO_TX
        self.maxInfoRX = self.DEFAULT_MAX_INFO_RX
        self.windowSizeTX = self.DEFAULT_WINDOWS_SIZE_TX
        self.windowSizeRX = self.DEFAULT_WINDOWS_SIZE_RX

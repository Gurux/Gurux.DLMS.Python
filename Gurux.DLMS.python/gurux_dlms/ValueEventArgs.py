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
from .enums import ErrorCode, DataType
from .GXDLMSSettings import GXDLMSSettings

# pylint: disable=bad-option-value,old-style-class,too-few-public-methods,too-many-instance-attributes
class ValueEventArgs:
    #
    # Constructor.
    #
    # @param s
    #            DLMS settings.
    # @param eventTarget
    #            Event target.
    # @param eventIndex
    #            Event index.
    # @param readSelector
    #            Optional read event selector.
    # @param forParameters
    #            Optional parameters.
    # pylint: disable=too-many-arguments
    def __init__(self, s, eventTarget, eventIndex, readSelector=0, forParameters=None):
        if isinstance(s, GXDLMSSettings):
            self.settings = s
        else:
            self.settings = s.settings
        # Data type of the value.
        self.dataType = DataType.NONE
        # Target DLMS object
        self.target = eventTarget
        # Attribute index.
        self.index = eventIndex
        # Optional selector.
        self.selector = readSelector
        # Optional parameters.
        self.parameters = forParameters
        # Object value.
        self.eventValue = None
        # Is request handled.
        self.handled = False
        # Occurred error.
        self.error = ErrorCode.OK
        # Is action.  This is reserved for internal use.
        self.action = False
        # Is value max PDU size skipped when converting data to bytes.
        self.skipMaxPduSize = False
        # Is reply handled as byte array or octect string.
        self.byteArray = False
        # Row to PDU is used with Profile Generic to tell how many rows are fit
        # to
        # one PDU.
        self.rowToPdu = 0
        # Rows begin index.
        self.rowBeginIndex = 0
        # Rows end index.
        self.rowEndIndex = 0
        # DLMS server.
        self.server = None
        # Invoke ID.
        self.invokeId = 0
        self.rowEndIndex = 0
        self.rowBeginIndex = 0

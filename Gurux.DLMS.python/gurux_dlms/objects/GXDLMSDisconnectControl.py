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
from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ErrorCode
from ..internal._GXCommon import _GXCommon
from ..enums import ObjectType, DataType
from .enums import ControlState, ControlMode

# pylint: disable=too-many-instance-attributes
class GXDLMSDisconnectControl(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSDisconnectControl
    """

    def __init__(self, ln=None, sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.DISCONNECT_CONTROL, ln, sn)
        self.controlState = ControlState.DISCONNECTED
        self.controlMode = ControlMode.NONE
        self.outputState = False

    #
    # Forces the disconnect control object into 'disconnected' state if
    #      remote
    # disconnection is enabled.
    #
    def remoteDisconnect(self, client):
        return client.method(self, 1, int(0), DataType.INT8)

    #
    # Forces the disconnect control object into the
    #      'ready_for_reconnection'
    # state if a direct remote reconnection is disabled.
    #
    def remoteReconnect(self, client):
        return client.method(self, 2, int(0), DataType.INT8)

    def getValues(self):
        return [self.logicalName,
                self.outputState,
                self.controlState,
                self.controlMode]

    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  OutputState
        if all_ or self.canRead(2):
            attributes.append(2)
        #  ControlState
        if all_ or self.canRead(3):
            attributes.append(3)
        #  ControlMode
        if all_ or self.canRead(4):
            attributes.append(4)
        return attributes

    def getAttributeCount(self):
        return 4

    def getMethodCount(self):
        return 2

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.BOOLEAN
        elif index == 3:
            ret = DataType.ENUM
        elif index == 4:
            ret = DataType.ENUM
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret

    def getValue(self, settings, e):
        if e.index == 1:
            return _GXCommon.logicalNameToBytes(self.logicalName)
        if e.index == 2:
            return self.outputState
        if e.index == 3:
            return self.controlState
        if e.index == 4:
            return self.controlMode
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            if e.value is None:
                self.outputState = False
            else:
                self.outputState = e.value
        elif e.index == 3:
            #pylint: disable=bad-option-value,redefined-variable-type
            if e.value is None:
                self.controlState = ControlState.DISCONNECTED
            else:
                self.controlState = e.value
        elif e.index == 4:
            #pylint: disable=bad-option-value,redefined-variable-type
            if e.value is None:
                self.controlMode = ControlMode.NONE
            else:
                self.controlMode = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.outputState = reader.readElementContentAsInt("OutputState") != 0
        self.controlState = reader.readElementContentAsInt("ControlState")
        self.controlMode = reader.readElementContentAsInt("ControlMode")

    def save(self, writer):
        writer.writeElementString("OutputState", self.outputState)
        writer.writeElementString("ControlState", int(self.controlState))
        writer.writeElementString("ControlMode", int(self.controlMode))

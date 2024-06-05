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
from ..enums import ErrorCode, ObjectType, DataType
from ..internal._GXCommon import _GXCommon
from .enums import BaudRate

# pylint: disable=too-many-instance-attributes
class GXDLMSHdlcSetup(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSHdlcSetup
    """

    def __init__(self, ln="0.0.22.0.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.IEC_HDLC_SETUP, ln, sn)
        self.communicationSpeed = BaudRate.BAUDRATE_9600
        self.windowSizeTransmit = 1
        self.windowSizeReceive = 1
        self.maximumInfoLengthReceive = 128
        self.maximumInfoLengthTransmit = 128
        self.inactivityTimeout = 120
        self.version = 1
        self.interCharachterTimeout = 0
        self.deviceAddress = 0

    def getValues(self):
        return [self.logicalName,
                self.communicationSpeed,
                self.windowSizeTransmit,
                self.windowSizeReceive,
                self.maximumInfoLengthTransmit,
                self.maximumInfoLengthReceive,
                self.interCharachterTimeout,
                self.inactivityTimeout,
                self.deviceAddress]

    #
    # Returns collection of attributes to read.  If attribute is static and
    # already read or device is returned HW error it is not returned.
    def getAttributeIndexToRead(self, all_):
        attributes = []
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  Communication speed
        if all_ or not self.isRead(2):
            attributes.append(2)
        #  Window size transmit
        if all_ or not self.isRead(3):
            attributes.append(3)
        #  Window size receive
        if all_ or not self.isRead(4):
            attributes.append(4)
        #  maximum info length transmit
        if all_ or not self.isRead(5):
            attributes.append(5)
        #  MaximumInfoLengthReceive
        if all_ or not self.isRead(6):
            attributes.append(6)
        #  InterCharachterTimeout
        if all_ or not self.isRead(7):
            attributes.append(7)
        #  Inactivity timeout
        if all_ or not self.isRead(8):
            attributes.append(8)
        #  Device address
        if all_ or not self.isRead(9):
            attributes.append(9)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 9

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 0

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.ENUM
        elif index == 3:
            ret = DataType.UINT8
        elif index == 4:
            ret = DataType.UINT8
        elif index == 5:
            if self.version == 0:
                ret = DataType.UINT8
            else:
                ret = DataType.UINT16
        elif index == 6:
            if self.version == 0:
                ret = DataType.UINT8
            else:
                ret = DataType.UINT16
        elif index == 7:
            ret = DataType.UINT16
        elif index == 8:
            ret = DataType.UINT16
        elif index == 9:
            ret = DataType.UINT16
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret
    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        #pylint: disable=bad-option-value,redefined-variable-type
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.communicationSpeed
        elif e.index == 3:
            ret = self.windowSizeTransmit
        elif e.index == 4:
            ret = self.windowSizeReceive
        elif e.index == 5:
            ret = self.maximumInfoLengthTransmit
        elif e.index == 6:
            ret = self.maximumInfoLengthReceive
        elif e.index == 7:
            ret = self.interCharachterTimeout
        elif e.index == 8:
            ret = self.inactivityTimeout
        elif e.index == 9:
            ret = self.deviceAddress
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.communicationSpeed = e.value
        elif e.index == 3:
            self.windowSizeTransmit = e.value
        elif e.index == 4:
            self.windowSizeReceive = e.value
        elif e.index == 5:
            self.maximumInfoLengthTransmit = e.value
        elif e.index == 6:
            self.maximumInfoLengthReceive = e.value
        elif e.index == 7:
            self.interCharachterTimeout = e.value
        elif e.index == 8:
            self.inactivityTimeout = e.value
        elif e.index == 9:
            self.deviceAddress = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.communicationSpeed = reader.readElementContentAsInt("Speed")
        self.windowSizeTransmit = reader.readElementContentAsInt("WindowSizeTx")
        self.windowSizeReceive = reader.readElementContentAsInt("WindowSizeRx")
        self.maximumInfoLengthTransmit = reader.readElementContentAsInt("MaximumInfoLengthTx")
        self.maximumInfoLengthReceive = reader.readElementContentAsInt("MaximumInfoLengthRx")
        self.interCharachterTimeout = reader.readElementContentAsInt("InterCharachterTimeout")
        self.inactivityTimeout = reader.readElementContentAsInt("InactivityTimeout")
        self.deviceAddress = reader.readElementContentAsInt("DeviceAddress")

    def save(self, writer):
        writer.writeElementString("Speed", int(self.communicationSpeed))
        writer.writeElementString("WindowSizeTx", self.windowSizeTransmit)
        writer.writeElementString("WindowSizeRx", self.windowSizeReceive)
        writer.writeElementString("MaximumInfoLengthTx", self.maximumInfoLengthTransmit)
        writer.writeElementString("MaximumInfoLengthRx", self.maximumInfoLengthReceive)
        writer.writeElementString("InterCharachterTimeout", self.interCharachterTimeout)
        writer.writeElementString("InactivityTimeout", self.inactivityTimeout)
        writer.writeElementString("DeviceAddress", self.deviceAddress)

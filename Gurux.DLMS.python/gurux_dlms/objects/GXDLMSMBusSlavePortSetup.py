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
from .enums import BaudRate, AddressState

# pylint: disable=too-many-instance-attributes
class GXDLMSMBusSlavePortSetup(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSMBusSlavePortSetup
    """

    #
    # Constructor.
    #
    # @param ln
    # Logical Name of the object.
    # @param sn
    # Short Name of the object.
    #
    def __init__(self, ln=None, sn=0):
        super(GXDLMSMBusSlavePortSetup, self).__init__(ObjectType.MBUS_SLAVE_PORT_SETUP, ln, sn)
        # Defines the baud rate for the opening sequence.
        self.defaultBaud = BaudRate.BAUDRATE_300
        # Defines the baud rate for the opening sequence.
        self.availableBaud = BaudRate.BAUDRATE_300
        # Defines whether or not the device has been assigned an
        # address since last power up of the device.
        self.addressState = AddressState.NONE
        # Defines the baud rate for the opening sequence.
        self.busAddress = 0

    def getValues(self):
        return [self.logicalName,
                self.defaultBaud,
                self.availableBaud,
                self.addressState,
                self.busAddress]

    #
    # Returns collection of attributes to read.  If attribute is static and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  DefaultBaud
        if all_ or not self.isRead(2):
            attributes.append(2)
        #  AvailableBaud
        if all_ or not self.isRead(3):
            attributes.append(3)
        #  AddressState
        if all_ or not self.isRead(4):
            attributes.append(4)
        #  BusAddress
        if all_ or not self.isRead(5):
            attributes.append(5)
        return attributes

    def getAttributeCount(self):
        return 5

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
            ret = DataType.ENUM
        elif index == 4:
            ret = DataType.ENUM
        elif index == 5:
            ret = DataType.UINT16
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret
    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            return _GXCommon.logicalNameToBytes(self.logicalName)
        if e.index == 2:
            return self.defaultBaud
        if e.index == 3:
            return self.availableBaud
        if e.index == 4:
            return self.addressState
        if e.index == 5:
            return self.busAddress
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        #pylint: disable=bad-option-value,redefined-variable-type
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            if e.value is None:
                self.defaultBaud = BaudRate.BAUDRATE_300
            else:
                self.defaultBaud = BaudRate(e.value)
        elif e.index == 3:
            if e.value is None:
                self.availableBaud = BaudRate.BAUDRATE_300
            else:
                self.availableBaud = BaudRate(e.value)
        elif e.index == 4:
            if e.value is None:
                self.addressState = AddressState.NONE
            else:
                self.addressState = AddressState(e.value)
        elif e.index == 5:
            if e.value is None:
                self.busAddress = 0
            else:
                self.busAddress = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.defaultBaud = reader.readElementContentAsInt("DefaultBaud")
        self.availableBaud = reader.readElementContentAsInt("AvailableBaud")
        self.addressState = reader.readElementContentAsInt("AddressState")
        self.busAddress = reader.readElementContentAsInt("BusAddress")

    def save(self, writer):
        writer.writeElementString("DefaultBaud", int(self.defaultBaud))
        writer.writeElementString("AvailableBaud", int(self.availableBaud))
        writer.writeElementString("AddressState", int(self.addressState))
        writer.writeElementString("BusAddress", self.busAddress)

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
from .enums import OpticalProtocolMode, BaudRate, LocalPortResponseTime

# pylint: disable=too-many-instance-attributes
class GXDLMSIECLocalPortSetup(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSIECLocalPortSetup
    """

    def __init__(self, ln="0.0.20.0.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.IEC_LOCAL_PORT_SETUP, ln, sn)
        self.defaultMode = OpticalProtocolMode.DEFAULT
        self.defaultBaudrate = BaudRate.BAUDRATE_300
        self.proposedBaudrate = BaudRate.BAUDRATE_300
        self.responseTime = LocalPortResponseTime.ms20
        self.password1 = None
        self.password2 = None
        self.password5 = None
        self.deviceAddress = None
        self.version = 1

    def getValues(self):
        return [self.logicalName,
                self.defaultMode,
                self.defaultBaudrate,
                self.proposedBaudrate,
                self.responseTime,
                self.deviceAddress,
                self.password1,
                self.password2,
                self.password5]

    #
    # Returns collection of attributes to read.  If attribute is static and
    # already read or device is returned HW error it is not returned.
    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  DefaultMode
        if all_ or not self.isRead(2):
            attributes.append(2)
        #  DefaultBaudrate
        if all_ or not self.isRead(3):
            attributes.append(3)
        #  ProposedBaudrate
        if all_ or not self.isRead(4):
            attributes.append(4)
        #  ResponseTime
        if all_ or not self.isRead(5):
            attributes.append(5)
        #  DeviceAddress
        if all_ or not self.isRead(6):
            attributes.append(6)
        #  Password1
        if all_ or not self.isRead(7):
            attributes.append(7)
        #  Password2
        if all_ or not self.isRead(8):
            attributes.append(8)
        #  Password5
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
            ret = DataType.ENUM
        elif index == 4:
            ret = DataType.ENUM
        elif index == 5:
            ret = DataType.ENUM
        elif index == 6:
            ret = DataType.OCTET_STRING
        elif index == 7:
            ret = DataType.OCTET_STRING
        elif index == 8:
            ret = DataType.OCTET_STRING
        elif index == 9:
            ret = DataType.OCTET_STRING
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret
    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.defaultMode
        elif e.index == 3:
            ret = self.defaultBaudrate
        elif e.index == 4:
            ret = self.proposedBaudrate
        elif e.index == 5:
            ret = self.responseTime
        elif e.index == 6:
            ret = _GXCommon.getBytes(self.deviceAddress)
        elif e.index == 7:
            ret = _GXCommon.getBytes(self.password1)
        elif e.index == 8:
            ret = _GXCommon.getBytes(self.password2)
        elif e.index == 9:
            ret = _GXCommon.getBytes(self.password5)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.defaultMode = e.value
        elif e.index == 3:
            self.defaultBaudrate = e.value
        elif e.index == 4:
            self.proposedBaudrate = e.value
        elif e.index == 5:
            self.responseTime = e.value
        elif e.index == 6:
            self.deviceAddress = _GXCommon.changeType(settings, e.value, DataType.STRING)
        elif e.index == 7:
            self.password1 = _GXCommon.changeType(settings, e.value, DataType.STRING)
        elif e.index == 8:
            self.password2 = _GXCommon.changeType(settings, e.value, DataType.STRING)
        elif e.index == 9:
            self.password5 = _GXCommon.changeType(settings, e.value, DataType.STRING)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.defaultMode = reader.readElementContentAsInt("DefaultMode")
        self.defaultBaudrate = reader.readElementContentAsInt("DefaultBaudrate")
        self.proposedBaudrate = reader.readElementContentAsInt("ProposedBaudrate")
        self.responseTime = reader.readElementContentAsInt("ResponseTime")
        self.deviceAddress = reader.readElementContentAsString("DeviceAddress")
        self.password1 = reader.readElementContentAsString("Password1")
        self.password2 = reader.readElementContentAsString("Password2")
        self.password5 = reader.readElementContentAsString("Password5")

    def save(self, writer):
        writer.writeElementString("DefaultMode", int(self.defaultMode))
        writer.writeElementString("DefaultBaudrate", int(self.defaultBaudrate))
        writer.writeElementString("ProposedBaudrate", int(self.proposedBaudrate))
        writer.writeElementString("ResponseTime", int(self.responseTime))
        writer.writeElementString("DeviceAddress", self.deviceAddress)
        writer.writeElementString("Password1", self.password1)
        writer.writeElementString("Password2", self.password2)
        writer.writeElementString("Password5", self.password5)

class GXDLMSIECOpticalPortSetup(GXDLMSIECLocalPortSetup):
    """Obsolete. Use GXDLMSIECLocalPortSetup instead."""

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

# pylint: disable=too-many-instance-attributes
class GXDLMSTcpUdpSetup(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSTcpUdpSetup
    """
    def __init__(self, ln="0.0.25.0.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        super(GXDLMSTcpUdpSetup, self).__init__(ObjectType.TCP_UDP_SETUP, ln, sn)
        self.port = 4059
        self.inactivityTimeout = 180
        self.maximumSegmentSize = 576
        self.ipReference = None
        self.maximumSimultaneousConnections = 0

    def getValues(self):
        return [self.logicalName,
                self.port,
                self.ipReference,
                self.maximumSegmentSize,
                self.maximumSimultaneousConnections,
                self.inactivityTimeout]

    #
    # Returns collection of attributes to read.  If attribute is static
    #      and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  Port
        if all_ or not self.isRead(2):
            attributes.append(2)
        #  IPReference
        if all_ or not self.isRead(3):
            attributes.append(3)
        #  MaximumSegmentSize
        if all_ or not self.isRead(4):
            attributes.append(4)
        #  MaximumSimultaneousConnections
        if all_ or not self.isRead(5):
            attributes.append(5)
        #  InactivityTimeout
        if all_ or not self.isRead(6):
            attributes.append(6)
        return attributes

    def getAttributeCount(self):
        return 6

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 0

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.UINT16
        elif index == 3:
            ret = DataType.OCTET_STRING
        elif index == 4:
            ret = DataType.UINT16
        elif index == 5:
            ret = DataType.UINT8
        elif index == 6:
            ret = DataType.UINT16
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
            ret = self.port
        elif e.index == 3:
            ret = _GXCommon.logicalNameToBytes(self.ipReference)
        elif e.index == 4:
            ret = self.maximumSegmentSize
        elif e.index == 5:
            ret = self.maximumSimultaneousConnections
        elif e.index == 6:
            ret = self.inactivityTimeout
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
            if e.value is None:
                self.port = 4059
            else:
                self.port = e.value
        elif e.index == 3:
            if e.value is None:
                self.ipReference = None
            else:
                if isinstance(e.value, bytearray):
                    self.ipReference = _GXCommon.toLogicalName(e.value)
                else:
                    self.ipReference(e.value)
        elif e.index == 4:
            if e.value is None:
                self.maximumSegmentSize = 576
            else:
                self.maximumSegmentSize = e.value
        elif e.index == 5:
            if e.value is None:
                self.maximumSimultaneousConnections = 1
            else:
                self.maximumSimultaneousConnections = e.value
        elif e.index == 6:
            if e.value is None:
                self.inactivityTimeout = 180
            else:
                self.inactivityTimeout = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.port = reader.readElementContentAsInt("Port")
        self.ipReference = reader.readElementContentAsString("IPReference")
        self.maximumSegmentSize = reader.readElementContentAsInt("MaximumSegmentSize")
        self.maximumSimultaneousConnections = reader.readElementContentAsInt("MaximumSimultaneousConnections")
        self.inactivityTimeout = reader.readElementContentAsInt("InactivityTimeout")

    def save(self, writer):
        writer.writeElementString("Port", self.port)
        writer.writeElementString("IPReference", self.ipReference)
        writer.writeElementString("MaximumSegmentSize", self.maximumSegmentSize)
        writer.writeElementString("MaximumSimultaneousConnections", self.maximumSimultaneousConnections)
        writer.writeElementString("InactivityTimeout", self.inactivityTimeout)

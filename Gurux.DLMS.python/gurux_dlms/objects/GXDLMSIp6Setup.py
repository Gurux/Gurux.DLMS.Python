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
import socket
from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ErrorCode
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from ..enums import ObjectType, DataType
from .enums import AddressConfigMode
from .GXNeighborDiscoverySetup import GXNeighborDiscoverySetup

# pylint: disable=too-many-instance-attributes
class GXDLMSIp6Setup(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSIp6Setup
    """
    def __init__(self, ln="0.0.25.7.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        super(GXDLMSIp6Setup, self).__init__(ObjectType.IP6_SETUP, ln, sn)
        self.addressConfigMode = AddressConfigMode.AUTO
        self.dataLinkLayerReference = None
        self.unicastIPAddress = list()
        self.multicastIPAddress = list()
        self.gatewayIPAddress = list()
        self.primaryDNSAddress = ""
        self.secondaryDNSAddress = ""
        self.trafficClass = 0
        self.neighborDiscoverySetup = list()

    def getValues(self):
        return [self.logicalName,
                self.dataLinkLayerReference,
                self.addressConfigMode,
                self.unicastIPAddress,
                self.multicastIPAddress,
                self.gatewayIPAddress,
                self.primaryDNSAddress,
                self.secondaryDNSAddress,
                self.trafficClass,
                self.neighborDiscoverySetup]

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
        #  DataLinkLayerReference
        if all_ or not self.isRead(2):
            attributes.append(2)
        #  AddressConfigMode
        if all_ or self.canRead(3):
            attributes.append(3)
        #  UnicastIPAddress
        if all_ or self.canRead(4):
            attributes.append(4)
        #  MulticastIPAddress
        if all_ or self.canRead(5):
            attributes.append(5)
        #  GatewayIPAddress
        if all_ or self.canRead(6):
            attributes.append(6)
        #  PrimaryDNSAddress
        if all_ or self.canRead(7):
            attributes.append(7)
        #  SecondaryDNSAddress
        if all_ or not self.isRead(8):
            attributes.append(8)
        #  TrafficClass
        if all_ or self.canRead(9):
            attributes.append(9)
        #  NeighborDiscoverySetup
        if all_ or self.canRead(10):
            attributes.append(10)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 10

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 2

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.OCTET_STRING
        elif index == 3:
            ret = DataType.ENUM
        elif index == 4:
            ret = DataType.ARRAY
        elif index == 5:
            ret = DataType.ARRAY
        elif index == 6:
            ret = DataType.ARRAY
        elif index == 7:
            ret = DataType.OCTET_STRING
        elif index == 8:
            ret = DataType.OCTET_STRING
        elif index == 9:
            ret = DataType.UINT8
        elif index == 10:
            ret = DataType.ARRAY
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
            ret = _GXCommon.logicalNameToBytes(self.dataLinkLayerReference)
        elif e.index == 3:
            ret = self.addressConfigMode
        elif e.index == 4:
            data = GXByteBuffer()
            data.setUInt8(DataType.ARRAY)
            if not self.unicastIPAddress:
                _GXCommon.setObjectCount(0, data)
            else:
                _GXCommon.setObjectCount(len(self.unicastIPAddress), data)
                for it in self.unicastIPAddress:
                    _GXCommon.setData(settings, data, DataType.OCTET_STRING, socket.inet_pton(socket.AF_INET6, it))
            ret = data
        elif e.index == 5:
            data = GXByteBuffer()
            data.setUInt8(DataType.ARRAY)
            if not self.multicastIPAddress:
                _GXCommon.setObjectCount(0, data)
            else:
                _GXCommon.setObjectCount(len(self.multicastIPAddress), data)
                for it in self.multicastIPAddress:
                    _GXCommon.setData(settings, data, DataType.OCTET_STRING, socket.inet_pton(socket.AF_INET6, it))
            ret = data
        elif e.index == 6:
            data = GXByteBuffer()
            data.setUInt8(DataType.ARRAY)
            if not self.gatewayIPAddress:
                _GXCommon.setObjectCount(0, data)
            else:
                _GXCommon.setObjectCount(len(self.gatewayIPAddress), data)
                for it in self.gatewayIPAddress:
                    _GXCommon.setData(settings, data, DataType.OCTET_STRING, socket.inet_pton(socket.AF_INET6, it))
            ret = data
        elif e.index == 7:
            if not self.primaryDNSAddress:
                ret = None
            else:
                ret = socket.inet_pton(socket.AF_INET6, self.primaryDNSAddress)
        elif e.index == 8:
            if not self.secondaryDNSAddress:
                ret = None
            else:
                ret = socket.inet_pton(socket.AF_INET6, self.secondaryDNSAddress)
        elif e.index == 9:
            ret = self.trafficClass
        elif e.index == 10:
            data = GXByteBuffer()
            data.setUInt8(DataType.ARRAY)
            if self.neighborDiscoverySetup is None:
                #  Object count is zero.
                data.setUInt8(0)
            else:
                _GXCommon.setObjectCount(len(self.neighborDiscoverySetup), data)
                for it in self.neighborDiscoverySetup:
                    data.setUInt8(DataType.STRUCTURE)
                    data.setUInt8(3)
                    _GXCommon.setData(settings, data, DataType.UINT8, it.maxRetry)
                    _GXCommon.setData(settings, data, DataType.UINT16, it.retryWaitTime)
                    _GXCommon.setData(settings, data, DataType.UINT32, it.sendPeriod)
            ret = data
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
            if isinstance(e.value, str):
                self.dataLinkLayerReference = e.value.__str__()
            else:
                self.dataLinkLayerReference = _GXCommon.toLogicalName(e.value)
        elif e.index == 3:
            self.addressConfigMode = AddressConfigMode(e.value)
        elif e.index == 4:
            self.unicastIPAddress = []
            if e.value:
                # This fails in Python 2.7.4. Update to 2.7.6
                # https://bugs.python.org/issue10212
                for it in e.value:
                    self.unicastIPAddress.append(socket.inet_ntop(socket.AF_INET6, it))
        elif e.index == 5:
            self.multicastIPAddress = []
            if e.value:
                # This fails in Python 2.7.4. Update to 2.7.6
                # https://bugs.python.org/issue10212
                for it in e.value:
                    self.multicastIPAddress.append(socket.inet_ntop(socket.AF_INET6, it))
        elif e.index == 6:
            self.gatewayIPAddress = []
            if e.value:
                # This fails in Python 2.7.4. Update to 2.7.6
                # https://bugs.python.org/issue10212
                for it in e.value:
                    self.gatewayIPAddress.append(socket.inet_ntop(socket.AF_INET6, it))
        elif e.index == 7:
            if not e.value:
                self.primaryDNSAddress = None
            else:
                self.primaryDNSAddress = socket.inet_ntop(socket.AF_INET6, e.value)
        elif e.index == 8:
            if not e.value:
                self.secondaryDNSAddress = None
            else:
                # This fails in Python 2.7.4. Update to 2.7.6
                # https://bugs.python.org/issue10212
                self.secondaryDNSAddress = socket.inet_ntop(socket.AF_INET6, e.value)
        elif e.index == 9:
            self.trafficClass = e.value
        elif e.index == 10:
            self.neighborDiscoverySetup = []
            if e.value:
                for it in e.value:
                    v = GXNeighborDiscoverySetup()
                    v.maxRetry = it[0]
                    v.retryWaitTime = it[1]
                    v.sendPeriod = it[2]
                    self.neighborDiscoverySetup.append(v)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    @classmethod
    def loadIPAddress(cls, reader, name):
        list_ = list()
        if reader.isStartElement(name, True):
            while reader.isStartElement("Value", False):
                list_.append(reader.readElementContentAsString("Value"))
            reader.readEndElement(name)
        return list_

    @classmethod
    def loadNeighborDiscoverySetup(cls, reader, name):
        list_ = list()
        if reader.isStartElement(name, True):
            while reader.isStartElement("Item", True):
                it = GXNeighborDiscoverySetup()
                list_.append(it)
                it.maxRetry = reader.readElementContentAsInt("MaxRetry")
                it.retryWaitTime = reader.readElementContentAsInt("RetryWaitTime")
                it.sendPeriod = reader.readElementContentAsInt("SendPeriod")
            reader.readEndElement(name)
        return list_

    def load(self, reader):
        self.dataLinkLayerReference = reader.readElementContentAsString("DataLinkLayerReference")
        self.addressConfigMode = reader.readElementContentAsInt("AddressConfigMode")
        self.unicastIPAddress = self.loadIPAddress(reader, "UnicastIPAddress")
        self.multicastIPAddress = self.loadIPAddress(reader, "MulticastIPAddress")
        self.gatewayIPAddress = self.loadIPAddress(reader, "GatewayIPAddress")
        self.primaryDNSAddress = reader.readElementContentAsString("PrimaryDNSAddress")
        self.secondaryDNSAddress = reader.readElementContentAsString("SecondaryDNSAddress")
        self.trafficClass = reader.readElementContentAsInt("TrafficClass")
        self.neighborDiscoverySetup = self.loadNeighborDiscoverySetup(reader, "NeighborDiscoverySetup")

    @classmethod
    def saveIPAddress(cls, writer, list_, name):
        writer.writeStartElement(name)
        if list_:
            for it in list_:
                writer.writeElementString("Value", it)
        writer.writeEndElement()

    @classmethod
    def saveNeighborDiscoverySetup(cls, writer, list_, name):
        writer.writeStartElement(name)
        if list_:
            for it in list_:
                writer.writeStartElement("Item")
                writer.writeElementString("MaxRetry", it.maxRetry)
                writer.writeElementString("RetryWaitTime", it.retryWaitTime)
                writer.writeElementString("SendPeriod", it.sendPeriod)
                writer.writeEndElement()
        writer.writeEndElement()

    def save(self, writer):
        writer.writeElementString("DataLinkLayerReference", self.dataLinkLayerReference)
        writer.writeElementString("AddressConfigMode", int(self.addressConfigMode))
        self.saveIPAddress(writer, self.unicastIPAddress, "UnicastIPAddress")
        self.saveIPAddress(writer, self.multicastIPAddress, "MulticastIPAddress")
        self.saveIPAddress(writer, self.gatewayIPAddress, "GatewayIPAddress")
        writer.writeElementString("PrimaryDNSAddress", self.primaryDNSAddress)
        writer.writeElementString("SecondaryDNSAddress", self.secondaryDNSAddress)
        writer.writeElementString("TrafficClass", self.trafficClass)
        self.saveNeighborDiscoverySetup(writer, self.neighborDiscoverySetup, "NeighborDiscoverySetup")

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
#  Gurux Device Framework is Open Source software you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http:#www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http:#www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ObjectType, ErrorCode, DataType
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from .enums.DeviceType import DeviceType
from .GXDLMSRoutingConfiguration import GXDLMSRoutingConfiguration
from .GXDLMSRoutingTable import GXDLMSRoutingTable
from .GXDLMSContextInformationTable import GXDLMSContextInformationTable
from .GXDLMSBroadcastLogTable import GXDLMSBroadcastLogTable


class GXDLMSG3Plc6LoWPan(GXDLMSObject, IGXDLMSBase):
    """
    G3-PLC 6LoWPAN adaptation layer setup.

        Online help:
            https://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSG3Plc6LoWPan
    """

    def __init__(self, ln="0.0.29.2.0.255", sn=0):
        """
        Constructor.

            Parameters:
                ln: Logical Name of the object.
                sn: Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.G3_PLC6_LO_WPAN, ln, sn)
        self.__version = 3
        self.__blacklistTable = []
        self.__contextInformationTable = []
        self.__prefixTable = bytearray()
        self.__routingConfiguration = []
        self.__routingTable = []
        self.__broadcastLogTable = []
        self.__groupTable = []
        self.__maxHops = 8
        self.__weakLqiValue = 52
        self.__securityLevel = 5
        self.__broadcastLogTableEntryTtl = 2
        self.__maxJoinWaitTime = 20
        self.__pathDiscoveryTime = 40
        self.__activeKeyIndex = 0
        self.__metricType = 0xF
        self.__coordShortAddress = 0
        self.__disableDefaultRouting = False
        self.__deviceType = DeviceType.NOT_DEFINED
        self.__defaultCoordRouteEnabled = 0
        self.__destinationAddress = []
        self.__lowLQI = 0
        self.__highLQI = 0

    @property
    def maxHops(self):
        """
        Defines the maximum number of hops to be used by the routing algorithm.
        """
        return self.__maxHops

    @maxHops.setter
    def maxHops(self, value):
        self.__maxHops = value

    @property
    def weakLqiValue(self):
        """
        The weak link value defines the LQI value below which a link to a neighbour is considered as a weak link.
        """
        return self.__weakLqiValue

    @weakLqiValue.setter
    def weakLqiValue(self, value):
        self.__weakLqiValue = value

    @property
    def securityLevel(self):
        """
        The minimum security level to be used for incoming and outgoing adaptation frames.
        """
        return self.__securityLevel

    @securityLevel.setter
    def securityLevel(self, value):
        self.__securityLevel = value

    @property
    def prefixTable(self):
        """
        Contains the list of prefixes defined on this PAN
        """
        return self.__prefixTable

    @prefixTable.setter
    def prefixTable(self, value):
        self.__prefixTable = value

    @property
    def routingConfiguration(self):
        """
        The routing configuration element specifies all parameters linked to the routing mechanism described in ITU-T G.9903:2014.
        """
        return self.__routingConfiguration

    @routingConfiguration.setter
    def routingConfiguration(self, value):
        self.__routingConfiguration = value

    @property
    def broadcastLogTableEntryTtl(self):
        """
        Maximum time to live of an adpBroadcastLogTable entry (in minutes).
        """
        return self.__broadcastLogTableEntryTtl

    @broadcastLogTableEntryTtl.setter
    def broadcastLogTableEntryTtl(self, value):
        self.__broadcastLogTableEntryTtl = value

    @property
    def routingTable(self):
        """
        Routing table.
        """
        return self.__routingTable

    @routingTable.setter
    def routingTable(self, value):
        self.__routingTable = value

    @property
    def contextInformationTable(self):
        """
        Contains the context information associated to each CID extension field.
        """
        return self.__contextInformationTable

    @contextInformationTable.setter
    def contextInformationTable(self, value):
        self.__contextInformationTable = value

    @property
    def blacklistTable(self):
        """
               Contains the list of the blacklisted neighbours.Key is 16-bit address of the blacklisted neighbour.

        Value is Remaining time in minutes until which this entry in the blacklisted neighbour table is considered valid.
        """
        return self.__blacklistTable

    @blacklistTable.setter
    def blacklistTable(self, value):
        self.__blacklistTable = value

    @property
    def broadcastLogTable(self):
        """
        Broadcast log table
        """
        return self.__broadcastLogTable

    @broadcastLogTable.setter
    def broadcastLogTable(self, value):
        self.__broadcastLogTable = value

    @property
    def groupTable(self):
        """
        Contains the group addresses to which the device belongs. array
        """
        return self.__groupTable

    @groupTable.setter
    def groupTable(self, value):
        self.__groupTable = value

    @property
    def maxJoinWaitTime(self):
        """
        Network join timeout in seconds for LBD
        """
        return self.__maxJoinWaitTime

    @maxJoinWaitTime.setter
    def maxJoinWaitTime(self, value):
        self.__maxJoinWaitTime = value

    @property
    def pathDiscoveryTime(self):
        """
        Timeout for path discovery in seconds.
        """
        return self.__pathDiscoveryTime

    @pathDiscoveryTime.setter
    def pathDiscoveryTime(self, value):
        self.__pathDiscoveryTime = value

    @property
    def activeKeyIndex(self):
        """
        Index of the active GMK to be used for data transmission.
        """
        return self.__activeKeyIndex

    @activeKeyIndex.setter
    def activeKeyIndex(self, value):
        self.__activeKeyIndex = value

    @property
    def metricType(self):
        """
        Metric Type to be used for routing purposes.
        """
        return self.__metricType

    @metricType.setter
    def metricType(self, value):
        self.__metricType = value

    @property
    def coordShortAddress(self):
        """
        Defines the short address of the coordinator.
        """
        return self.__coordShortAddress

    @coordShortAddress.setter
    def coordShortAddress(self, value):
        self.__coordShortAddress = value

    @property
    def disableDefaultRouting(self):
        """
        Is default routing (LOADng) disabled.
        """
        return self.__disableDefaultRouting

    @disableDefaultRouting.setter
    def disableDefaultRouting(self, value):
        self.__disableDefaultRouting = value

    @property
    def deviceType(self):
        """
        Defines the type of the device connected to the modem
        """
        return self.__deviceType

    @deviceType.setter
    def deviceType(self, value):
        self.__deviceType = value

    @property
    def defaultCoordRouteEnabled(self):
        """
        If true, the default route will be created.
        """
        return self.__defaultCoordRouteEnabled

    @defaultCoordRouteEnabled.setter
    def defaultCoordRouteEnabled(self, value):
        self.__defaultCoordRouteEnabled = value

    @property
    def destinationAddress(self):
        """
               List of the addresses of the devices for which this LOADng

        router is providing connectivity.
        """
        return self.__destinationAddress

    @destinationAddress.setter
    def destinationAddress(self, value):
        self.__destinationAddress = value

    @property
    def lowLQI(self):
        """
        PIB attribute 0x04.
        """
        return self.__lowLQI

    @lowLQI.setter
    def lowLQI(self, value):
        self.__lowLQI = value

    @property
    def highLQI(self):
        """
        PIB attribute 0x05.
        """
        return self.__highLQI

    @highLQI.setter
    def highLQI(self, value):
        self.__highLQI = value

    def getAttributeIndexToRead(self, all_):
        attributes = []
        # LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        # MaxHops
        if all_ or self.canRead(2):
            attributes.append(2)
        # WeakLqiValue
        if all_ or self.canRead(3):
            attributes.append(3)
        # SecurityLevel
        if all_ or self.canRead(4):
            attributes.append(4)
        # PrefixTable
        if all_ or self.canRead(5):
            attributes.append(5)
        # RoutingConfiguration
        if all_ or self.canRead(6):
            attributes.append(6)
        # BroadcastLogTableEntryTtl
        if all_ or self.canRead(7):
            attributes.append(7)
        # RoutingTable
        if all_ or self.canRead(8):
            attributes.append(8)
        # ContextInformationTable
        if all_ or self.canRead(9):
            attributes.append(9)
        # BlacklistTable
        if all_ or self.canRead(10):
            attributes.append(10)
        # BroadcastLogTable
        if all_ or self.canRead(11):
            attributes.append(11)
        # GroupTable
        if all_ or self.canRead(12):
            attributes.append(12)
        # MaxJoinWaitTime
        if all_ or self.canRead(13):
            attributes.append(13)
        # PathDiscoveryTime
        if all_ or self.canRead(14):
            attributes.append(14)
        # ActiveKeyIndex
        if all_ or self.canRead(15):
            attributes.append(15)
        # MetricType
        if all_ or self.canRead(16):
            attributes.append(16)
        if self.__version > 0:
            # CoordShortAddress
            if all_ or self.canRead(17):
                attributes.append(17)
            # DisableDefaultRouting
            if all_ or self.canRead(18):
                attributes.append(18)
            # DeviceType
            if all_ or self.canRead(19):
                attributes.append(19)
            if self.__version > 1:
                # DefaultCoordRouteEnabled
                if all_ or self.canRead(20):
                    attributes.append(20)
                # DestinationAddress
                if all_ or self.canRead(21):
                    attributes.append(21)
                if self.__version > 2:
                    # LowLQI
                    if all_ or self.canRead(22):
                        attributes.append(22)
                    # HighLQI
                    if all_ or self.canRead(23):
                        attributes.append(23)
        return attributes

    def getNames(self):
        return (
            "Logical Name",
            "MaxHops",
            "WeakLqiValue",
            "SecurityLevel",
            "PrefixTable",
            "RoutingConfiguration",
            "BroadcastLogTableEntryTtl",
            "RoutingTable",
            "ContextInformationTable",
            "BlacklistTable",
            "BroadcastLogTable",
            "GroupTable",
            "MaxJoinWaitTime",
            " PathDiscoveryTime",
            "ActiveKeyIndex",
            "MetricType",
            "CoordShortAddress",
            "DisableDefaultRouting",
            "DeviceType",
            "Default coord route enabled",
            "Destination address",
            "Low LQI",
            "High LQI",
        )

    def getAttributeCount(self):
        if self.__version == 0:
            return 16
        if self.__version == 1:
            return 19
        if self.__version == 2:
            return 21
        return 23

    def getMethodCount(self):
        return 0

    def getValue(self, settings, e):
        """
        Returns value of given attribute.

            Parameters:
                settings: DLMS settings.
                e: Get parameters.

            Returns:
                Value of the attribute index.
        """
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        if e.index == 2:
            return self.__maxHops
        if e.index == 3:
            return self.__weakLqiValue
        if e.index == 4:
            return self.__securityLevel
        if e.index == 5:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.ARRAY)
            if self.__prefixTable is None:
                bb.setUInt8(0)
            else:
                _GXCommon.setObjectCount(len(self.__prefixTable), bb)
                for it in self.__prefixTable:
                    _GXCommon.setData(settings, bb, DataType.UINT8, it)
            return bb.array()
        if e.index == 6:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.ARRAY)
            if self.__routingConfiguration is None:
                bb.setUInt8(0)
            else:
                _GXCommon.setObjectCount(len(self.routingConfiguration), bb)
                for it in self.__routingConfiguration:
                    bb.setUInt8(DataType.STRUCTURE)
                    bb.setUInt8(14)
                    _GXCommon.setData(settings, bb, DataType.UINT8, it.netTraversalTime)
                    _GXCommon.setData(
                        settings, bb, DataType.UINT16, it.routingTableEntryTtl
                    )
                    _GXCommon.setData(settings, bb, DataType.UINT8, it.kr)
                    _GXCommon.setData(settings, bb, DataType.UINT8, it.km)
                    _GXCommon.setData(settings, bb, DataType.UINT8, it.kc)
                    _GXCommon.setData(settings, bb, DataType.UINT8, it.kq)
                    _GXCommon.setData(settings, bb, DataType.UINT8, it.kh)
                    _GXCommon.setData(settings, bb, DataType.UINT8, it.krt)
                    _GXCommon.setData(settings, bb, DataType.UINT8, it.rreqRetries)
                    _GXCommon.setData(settings, bb, DataType.UINT8, it.rreqReqWait)
                    _GXCommon.setData(
                        settings, bb, DataType.UINT16, it.blacklistTableEntryTtl
                    )
                    _GXCommon.setData(
                        settings, bb, DataType.BOOLEAN, it.unicastRreqGenEnable
                    )
                    _GXCommon.setData(settings, bb, DataType.BOOLEAN, it.rlcEnabled)
                    _GXCommon.setData(settings, bb, DataType.UINT8, it.addRevLinkCost)
            return bb.array()
        if e.index == 7:
            return self.__broadcastLogTableEntryTtl
        if e.index == 8:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.ARRAY)
            if self.__routingTable is None:
                bb.setUInt8(0)
            else:
                _GXCommon.setObjectCount(len(self.__routingTable), bb)
                for it in self.__routingTable:
                    bb.setUInt8(DataType.STRUCTURE)
                    bb.setUInt8(6)
                    _GXCommon.setData(
                        settings, bb, DataType.UINT16, it.destinationAddress
                    )
                    _GXCommon.setData(settings, bb, DataType.UINT16, it.nextHopAddress)
                    _GXCommon.setData(settings, bb, DataType.UINT16, it.routeCost)
                    _GXCommon.setData(settings, bb, DataType.UINT8, it.hopCount)
                    _GXCommon.setData(settings, bb, DataType.UINT8, it.weakLinkCount)
                    _GXCommon.setData(settings, bb, DataType.UINT16, it.validTime)
            return bb.array()
        if e.index == 9:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.ARRAY)
            if self.__contextInformationTable is None:
                bb.setUInt8(0)
            else:
                _GXCommon.setObjectCount(len(self.__contextInformationTable), bb)
                for it in self.__contextInformationTable:
                    bb.setUInt8(DataType.STRUCTURE)
                    bb.setUInt8(5)
                    _GXCommon.setData(settings, bb, DataType.BITSTRING, it.cid)
                    if it.context:
                        _GXCommon.setData(settings, bb, DataType.UINT8, len(it.context))
                    else:
                        _GXCommon.setData(settings, bb, DataType.UINT8, 0)
                    _GXCommon.setData(settings, bb, DataType.OCTET_STRING, it.context)
                    _GXCommon.setData(settings, bb, DataType.BOOLEAN, it.compression)
                    _GXCommon.setData(settings, bb, DataType.UINT16, it.validLifetime)
            return bb.array()
        if e.index == 10:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.ARRAY)
            if self.__blacklistTable is None:
                bb.setUInt8(0)
            else:
                _GXCommon.setObjectCount(len(self.__blacklistTable), bb)
                for k, v in self.__blacklistTable:
                    bb.setUInt8(DataType.STRUCTURE)
                    bb.setUInt8(2)
                    _GXCommon.setData(settings, bb, DataType.UINT16, k)
                    _GXCommon.setData(settings, bb, DataType.UINT16, v)
            return bb.array()
        if e.index == 11:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.ARRAY)
            if self.__broadcastLogTable is None:
                bb.setUInt8(0)
            else:
                _GXCommon.setObjectCount(len(self.__broadcastLogTable), bb)
                for it in self.__broadcastLogTable:
                    bb.setUInt8(DataType.STRUCTURE)
                    bb.setUInt8(3)
                    _GXCommon.setData(settings, bb, DataType.UINT16, it.sourceAddress)
                    _GXCommon.setData(settings, bb, DataType.UINT8, it.sequenceNumber)
                    _GXCommon.setData(settings, bb, DataType.UINT16, it.validTime)
            return bb.array()
        if e.index == 12:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.ARRAY)
            if self.__groupTable is None:
                bb.setUInt8(0)
            else:
                _GXCommon.setObjectCount(len(self.__groupTable), bb)
                for it in self.__groupTable:
                    _GXCommon.setData(settings, bb, DataType.UINT16, it)
            return bb.array()
        if e.index == 13:
            return self.__maxJoinWaitTime
        if e.index == 14:
            return self.__pathDiscoveryTime
        if e.index == 15:
            return self.__activeKeyIndex
        if e.index == 16:
            return self.__metricType
        if e.index == 17:
            return self.__coordShortAddress
        if e.index == 18:
            return self.__disableDefaultRouting
        if e.index == 19:
            return self.__deviceType
        if e.index == 20:
            return self.__defaultCoordRouteEnabled
        if e.index == 21:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.ARRAY)
            if self.__destinationAddress is None:
                bb.setUInt8(0)
            else:
                _GXCommon.setObjectCount(len(self.__destinationAddress), bb)
                for it in self.__destinationAddress:
                    _GXCommon.setData(settings, bb, DataType.UINT16, it)
            return bb.array()
        if e.index == 22:
            return self.__lowLQI
        if e.index == 23:
            return self.__highLQI
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.__maxHops = e.value
        elif e.index == 3:
            self.__weakLqiValue = e.value
        elif e.index == 4:
            self.__securityLevel = e.value
        elif e.index == 5:
            self.__prefixTable.clear()
            if e.value:
                for it in e.value:
                    self.__prefixTable.append(it)
        elif e.index == 6:
            self.__routingConfiguration.clear()
            if e.value:
                for arr in e.value:
                    it = GXDLMSRoutingConfiguration()
                    it.netTraversalTime = arr[0]
                    it.routingTableEntryTtl = arr[1]
                    it.kr = arr[2]
                    it.km = arr[3]
                    it.kc = arr[4]
                    it.kq = arr[5]
                    it.kh = arr[6]
                    it.krt = arr[7]
                    it.rreqRetries = arr[8]
                    it.rreqReqWait = arr[9]
                    it.blacklistTableEntryTtl = arr[10]
                    it.unicastRreqGenEnable = arr[11]
                    it.rlcEnabled = arr[12]
                    it.addRevLinkCost = arr[13]
                    self.__routingConfiguration.append(it)
        elif e.index == 7:
            self.__broadcastLogTableEntryTtl = e.value
        elif e.index == 8:
            self.__routingTable.clear()
            if e.value:
                for arr in e.value:
                    it = GXDLMSRoutingTable()
                    it.destinationAddress = arr[0]
                    it.nextHopAddress = arr[1]
                    it.routeCost = arr[2]
                    it.hopCount = arr[3]
                    it.weakLinkCount = arr[4]
                    it.validTime = arr[5]
                    self.__routingTable.append(it)
        elif e.index == 9:
            self.__contextInformationTable.clear()
            if e.value:
                for arr in e.value:
                    it = GXDLMSContextInformationTable()
                    it.cid = arr[0]
                    it.context = arr[2]
                    it.compression = arr[3]
                    it.validLifetime = arr[4]
                    self.__contextInformationTable.append(it)
        elif e.index == 10:
            self.__blacklistTable.clear()
            if e.value:
                for arr in e.value:
                    self.__blacklistTable.append((arr[0], arr[1]))
        elif e.index == 11:
            self.__broadcastLogTable.clear()
            if e.value:
                for arr in e.value:
                    it = GXDLMSBroadcastLogTable()
                    it.sourceAddress = arr[0]
                    it.sequenceNumber = arr[1]
                    it.validTime = arr[2]
                    self.__broadcastLogTable.append(it)
        elif e.index == 12:
            self.__groupTable.clear()
            if e.value:
                for it in e.value:
                    self.__groupTable.append(it)
        elif e.index == 13:
            self.__maxJoinWaitTime = e.value
        elif e.index == 14:
            self.__pathDiscoveryTime = e.value
        elif e.index == 15:
            self.__activeKeyIndex = e.value
        elif e.index == 16:
            self.__metricType = e.value
        elif e.index == 17:
            self.__coordShortAddress = e.value
        elif e.index == 18:
            self.__disableDefaultRouting = e.value
        elif e.index == 19:
            self.__deviceType = DeviceType(e.value)
        elif e.index == 20:
            self.__defaultCoordRouteEnabled = e.value
        elif e.index == 21:
            self.__destinationAddress.clear()
            if e.value:
                for it in e.value:
                    self.__destinationAddress.append(it)
        elif e.index == 22:
            self.__lowLQI = e.value
        elif e.index == 23:
            self.__highLQI = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def getValues(self):
        """
        Returns attributes as an array.

            Returns:
                Collection of COSEM object values.
        """
        return (
            self.logicalName,
            self.__maxHops,
            self.__weakLqiValue,
            self.__securityLevel,
            self.__prefixTable,
            self.__routingConfiguration,
            self.__broadcastLogTableEntryTtl,
            self.__routingTable,
            self.__contextInformationTable,
            self.__blacklistTable,
            self.__broadcastLogTable,
            self.__groupTable,
            self.__maxJoinWaitTime,
            self.__pathDiscoveryTime,
            self.__activeKeyIndex,
            self.__metricType,
            self.__coordShortAddress,
            self.__disableDefaultRouting,
            self.__deviceType,
            self.__defaultCoordRouteEnabled,
            self.__destinationAddress,
            self.__lowLQI,
            self.__highLQI,
        )

    def getDataType(self, index):
        """
        Returns device data type of selected attribute index.

            Parameters:
                index: Attribute index of the object.

            Returns:
                Device data type of the object.
        """
        # LN.
        if index == 1:
            return DataType.OCTET_STRING
        # MaxHops
        if index == 2:
            return DataType.UINT8
        # WeakLqiValue
        if index == 3:
            return DataType.UINT8
        # SecurityLevel
        if index == 4:
            return DataType.UINT8
        # PrefixTable
        if index == 5:
            return DataType.ARRAY
        # RoutingConfiguration
        if index == 6:
            return DataType.ARRAY
        # BroadcastLogTableEntryTtl
        if index == 7:
            return DataType.UINT16
        # RoutingTable
        if index == 8:
            return DataType.ARRAY
        # ContextInformationTable
        if index == 9:
            return DataType.ARRAY
        # BlacklistTable
        if index == 10:
            return DataType.ARRAY
        # BroadcastLogTable
        if index == 11:
            return DataType.ARRAY
        # GroupTable
        if index == 12:
            return DataType.ARRAY
        # MaxJoinWaitTime
        if index == 13:
            return DataType.UINT16
        # PathDiscoveryTime
        if index == 14:
            return DataType.UINT8
        # ActiveKeyIndex
        if index == 15:
            return DataType.UINT8
        # MetricType
        if index == 16:
            return DataType.UINT8
        if self.__version > 0:
            # CoordShortAddress
            if index == 17:
                return DataType.UINT16
            # DisableDefaultRouting
            if index == 18:
                return DataType.BOOLEAN
            # DeviceType
            if index == 19:
                return DataType.ENUM
            if self.__version > 1:
                # DefaultCoordRouteEnabled
                if index == 20:
                    return DataType.BOOLEAN
                # DestinationAddress
                if index == 21:
                    return DataType.ARRAY
                # LowLQI
                if index == 22:
                    return DataType.UINT8
                # HighLQI
                if index == 23:
                    return DataType.UINT8
        raise ValueError("GetDataType failed. Invalid attribute index.")

    def __loadPrefixTable(self, reader):
        self.__prefixTable.clear()
        if reader.isStartElement("PrefixTable", True):
            while reader.isStartElement("Value", False):
                self.__prefixTable.append(reader.readElementContentAsInt("Value"))
            reader.readEndElement("PrefixTable")

    def __loadRoutingConfiguration(self, reader):
        self.__routingConfiguration.clear()
        if reader.isStartElement("RoutingConfiguration", True):
            while reader.isStartElement("Item", True):
                it = GXDLMSRoutingConfiguration()
                self.__routingConfiguration.append(it)
                it.netTraversalTime = reader.readElementContentAsInt("NetTraversalTime")
                it.routingTableEntryTtl = reader.readElementContentAsInt(
                    "RoutingTableEntryTtl"
                )
                it.kr = reader.readElementContentAsInt("Kr")
                it.km = reader.readElementContentAsInt("Km")
                it.kc = reader.readElementContentAsInt("Kc")
                it.kq = reader.readElementContentAsInt("Kq")
                it.kh = reader.readElementContentAsInt("Kh")
                it.krt = reader.readElementContentAsInt("Krt")
                it.rreqRetries = reader.readElementContentAsInt("RreqRetries")
                it.rreqReqWait = reader.readElementContentAsInt("RreqReqWait")
                it.blacklistTableEntryTtl = reader.readElementContentAsInt(
                    "BlacklistTableEntryTtl"
                )
                it.unicastRreqGenEnable = (
                    reader.readElementContentAsInt("UnicastRreqGenEnable") != 0
                )
                it.rlcEnabled = reader.readElementContentAsInt("RlcEnabled") != 0
                it.addRevLinkCost = reader.readElementContentAsInt("AddRevLinkCost")
            reader.readEndElement("RoutingConfiguration")

    def __loadRoutingTable(self, reader):
        self.__routingTable.clear()
        if reader.isStartElement("RoutingTable", True):
            while reader.isStartElement("Item", True):
                it = GXDLMSRoutingTable()
                self.__routingTable.Add(it)
                it.destinationAddress = reader.readElementContentAsInt(
                    "DestinationAddress"
                )
                it.nextHopAddress = reader.readElementContentAsInt("NextHopAddress")
                it.routeCost = reader.readElementContentAsInt("RouteCost")
                it.hopCount = reader.readElementContentAsInt("HopCount")
                it.weakLinkCount = reader.readElementContentAsInt("WeakLinkCount")
                it.validTime = reader.readElementContentAsInt("ValidTime")
            reader.readEndElement("RoutingTable")

    def __loadContextInformationTable(self, reader):
        self.__contextInformationTable.clear()
        if reader.isStartElement("ContextInformationTable", True):
            while reader.isStartElement("Item", True):
                it = GXDLMSContextInformationTable()
                self.__contextInformationTable.Add(it)
                it.cid = reader.readElementContentAsString("CID")
                it.context = _GXCommon.hexToBytes(
                    reader.readElementContentAsString("Context")
                )
                it.compression = reader.readElementContentAsInt("Compression") != 0
                it.validLifetime = reader.readElementContentAsInt("ValidLifetime")
            reader.readEndElement("ContextInformationTable")

    def __loadBlacklistTable(self, reader):
        self.__blacklistTable.clear()
        if reader.isStartElement("BlacklistTable", True):
            while reader.isStartElement("Item", True):
                k = reader.readElementContentAsInt("Key")
                v = reader.readElementContentAsInt("Value")
                self.__blacklistTable.append((k, v))
            reader.readEndElement("BlacklistTable")

    def __loadBroadcastLogTable(self, reader):
        self.__broadcastLogTable.clear()
        if reader.isStartElement("BroadcastLogTable", True):
            while reader.isStartElement("Item", True):
                it = GXDLMSBroadcastLogTable()
                self.__broadcastLogTable.append(it)
                it.sourceAddress = reader.readElementContentAsInt("SourceAddress")
                it.sequenceNumber = reader.readElementContentAsInt("SequenceNumber")
                it.validTime = reader.readElementContentAsInt("ValidTime")
            reader.readEndElement("BroadcastLogTable")

    def __loadGroupTable(self, reader):
        self.__groupTable.clear()
        if reader.isStartElement("GroupTable", True):
            while reader.isStartElement("Value", False):
                self.__groupTable.append(reader.readElementContentAsInt("Value"))
            reader.readEndElement("GroupTable")

    def __loadDestinationAddress(self, reader):
        self.__destinationAddress.clear()
        if reader.isStartElement("DestinationAddress", True):
            while reader.isStartElement("Value", False):
                self.__destinationAddress.append(
                    reader.readElementContentAsInt("Value")
                )
            reader.readEndElement("DestinationAddress")

    def load(self, reader):
        self.__maxHops = reader.readElementContentAsInt("MaxHops")
        self.__weakLqiValue = reader.readElementContentAsInt("WeakLqiValue")
        self.__securityLevel = reader.readElementContentAsInt("SecurityLevel")
        self.__loadPrefixTable(reader)
        self.__loadRoutingConfiguration(reader)
        self.__broadcastLogTableEntryTtl = reader.readElementContentAsInt(
            "BroadcastLogTableEntryTtl"
        )
        self.__loadRoutingTable(reader)
        self.__loadContextInformationTable(reader)
        self.__loadBlacklistTable(reader)
        self.__loadBroadcastLogTable(reader)
        self.__loadGroupTable(reader)
        self.__maxJoinWaitTime = reader.readElementContentAsInt("MaxJoinWaitTime")
        self.__pathDiscoveryTime = reader.readElementContentAsInt("PathDiscoveryTime")
        self.__activeKeyIndex = reader.readElementContentAsInt("ActiveKeyIndex")
        self.__metricType = reader.readElementContentAsInt("MetricType")
        self.__coordShortAddress = reader.readElementContentAsInt("CoordShortAddress")
        self.__disableDefaultRouting = (
            reader.readElementContentAsInt("DisableDefaultRouting") != 0
        )
        self.__deviceType = DeviceType(reader.readElementContentAsInt("DeviceType"))
        self.__defaultCoordRouteEnabled = (
            reader.readElementContentAsInt("DefaultCoordRouteEnabled") != 0
        )
        self.__loadDestinationAddress(reader)
        self.__lowLQI = reader.readElementContentAsInt("LowLQI")
        self.__highLQI = reader.readElementContentAsInt("HighLQI")

    def __savePrefixTable(self, writer):
        if self.__prefixTable:
            writer.writeStartElement("PrefixTable")
            for it in self.__prefixTable:
                writer.writeElementObject("Value", it)
            writer.writeEndElement()

    def __saveRoutingConfiguration(self, writer):
        if self.__routingConfiguration:
            writer.writeStartElement("RoutingConfiguration")
            for it in self.__routingConfiguration:
                writer.writeStartElement("Item")
                writer.writeElementString("NetTraversalTime", it.netTraversalTime)
                writer.writeElementString(
                    "RoutingTableEntryTtl", it.routingTableEntryTtl
                )
                writer.writeElementString("Kr", it.kr)
                writer.writeElementString("Km", it.km)
                writer.writeElementString("Kc", it.kc)
                writer.writeElementString("Kq", it.kq)
                writer.writeElementString("Kh", it.kh)
                writer.writeElementString("Krt", it.krt)
                writer.writeElementString("RreqRetries", it.rreqRetries)
                writer.writeElementString("RreqReqWait", it.rreqReqWait)
                writer.writeElementString(
                    "BlacklistTableEntryTtl", it.blacklistTableEntryTtl
                )
                writer.writeElementString(
                    "UnicastRreqGenEnable", it.unicastRreqGenEnable
                )
                writer.writeElementString("RlcEnabled", it.rlcEnabled)
                writer.writeElementString("AddRevLinkCost", it.addRevLinkCost)
                writer.writeEndElement()
            writer.writeEndElement()

    def __saveRoutingTable(self, writer):
        if self.__routingTable:
            writer.writeStartElement("RoutingTable")
            for it in self.__routingTable:
                writer.writeStartElement("Item")
                writer.writeElementString("DestinationAddress", it.destinationAddress)
                writer.writeElementString("NextHopAddress", it.nextHopAddress)
                writer.writeElementString("RouteCost", it.routeCost)
                writer.writeElementString("HopCount", it.hopCount)
                writer.writeElementString("WeakLinkCount", it.weakLinkCount)
                writer.writeElementString("ValidTime", it.validTime)
                writer.writeEndElement()
            writer.writeEndElement()

    def __saveContextInformationTable(self, writer):
        if self.__contextInformationTable:
            writer.writeStartElement("ContextInformationTable")
            for it in self.__contextInformationTable:
                writer.writeStartElement("Item")
                writer.writeElementString("CID", it.CID)
                writer.writeElementString("Context", _GXCommon.toHex(it.context))
                writer.writeElementString("Compression", it.compression)
                writer.writeElementString("ValidLifetime", it.validLifetime)
                writer.writeEndElement()
            writer.writeEndElement()

    def __saveBlacklistTable(self, writer):
        if self.__blacklistTable:
            writer.writeStartElement("BlacklistTable")
            for k, v in self.__blacklistTable:
                writer.writeStartElement("Item")
                writer.writeElementObject("Key", k)
                writer.writeElementObject("Value", v)
                writer.writeEndElement()
            writer.writeEndElement()

    def __saveBroadcastLogTable(self, writer):
        if self.__broadcastLogTable:
            writer.writeStartElement("BroadcastLogTable")
            for it in self.__broadcastLogTable:
                writer.writeStartElement("Item")
                writer.writeElementObject("SourceAddress", it.sourceAddress)
                writer.writeElementObject("SequenceNumber", it.sequenceNumber)
                writer.writeElementObject("ValidTime", it.validTime)
                writer.writeEndElement()
            writer.writeEndElement()

    def __saveGroupTable(self, writer):
        if self.__groupTable:
            writer.writeStartElement("GroupTable")
            for it in self.__groupTable:
                writer.writeElementObject("Value", it)
            writer.writeEndElement()

    def __saveDestinationAddress(self, writer):
        if self.__destinationAddress:
            writer.writeStartElement("DestinationAddress")
            for it in self.__destinationAddress:
                writer.writeElementObject("Value", it)
            writer.writeEndElement()

    def save(self, writer):
        writer.writeElementString("MaxHops", self.__maxHops)
        writer.writeElementString("WeakLqiValue", self.__weakLqiValue)
        writer.writeElementString("SecurityLevel", self.__securityLevel)
        self.__savePrefixTable(writer)
        self.__saveRoutingConfiguration(writer)
        writer.writeElementString(
            "BroadcastLogTableEntryTtl", self.__broadcastLogTableEntryTtl
        )
        self.__saveRoutingTable(writer)
        self.__saveContextInformationTable(writer)
        self.__saveBlacklistTable(writer)
        self.__saveBroadcastLogTable(writer)
        self.__saveGroupTable(writer)
        writer.writeElementString("MaxJoinWaitTime", self.__maxJoinWaitTime)
        writer.writeElementString("PathDiscoveryTime", self.__pathDiscoveryTime)
        writer.writeElementString("ActiveKeyIndex", self.__activeKeyIndex)
        writer.writeElementString("MetricType", self.__metricType)
        writer.writeElementString("CoordShortAddress", self.__coordShortAddress)
        writer.writeElementString("DisableDefaultRouting", self.__disableDefaultRouting)
        writer.writeElementString("DeviceType", self.__deviceType)
        writer.writeElementString(
            "DefaultCoordRouteEnabled", self.__defaultCoordRouteEnabled
        )
        self.__saveDestinationAddress(writer)
        writer.writeElementString("LowLQI", self.__lowLQI)
        writer.writeElementString("HighLQI", self.__highLQI)

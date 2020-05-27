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
from ..GXByteBuffer import GXByteBuffer
from ..enums import ObjectType, DataType
from .enums.MacState import MacState

# pylint: disable=too-many-instance-attributes
class GXDLMSPrimeNbOfdmPlcMacFunctionalParameters(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSPrimeNbOfdmPlcMacFunctionalParameters
    """

    def __init__(self, ln="0.0.28.3.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.PRIME_NB_OFDM_PLC_MAC_FUNCTIONAL_PARAMETERS, ln, sn)
        #LNID allocated to this node at time of its registration.
        self.lnId = 0
        #LSID allocated to this node at the time of its promotion.
        self.lsId = 0
        #SID of the switch node through which this node is connected to the
        #subnetwork.
        self.sId = 0
        #Subnetwork address to which this node is registered.
        self.sna = None
        #Present functional state of the node.
        self.state = MacState.DISCONNECTED
        #The SCP length, in symbols, in present frame.
        self.scpLength = 0
        #Level of this node in subnetwork hierarchy.
        self.nodeHierarchyLevel = 0
        #Number of beacon slots provisioned in present frame structure.
        self.beaconSlotCount = 0
        #Beacon slot in which this device's switch node transmits its
        #beacon.
        self.beaconRxSlot = 0
        #Beacon slot in which this device transmits its beacon.
        self.beaconTxSlot = 0
        #Number of frames between receptions of two successive beacons.
        self.beaconRxFrequency = 0
        #Number of frames between transmissions of two successive beacons.
        self.beaconTxFrequency = 0
        #This attribute defines the capabilities of the node.
        self.capabilities = list()

    def getValues(self):
        return [self.logicalName,
                self.lnId,
                self.lsId,
                self.sId,
                self.sna,
                self.state,
                self.scpLength,
                self.nodeHierarchyLevel,
                self.beaconSlotCount,
                self.beaconRxSlot,
                self.beaconTxSlot,
                self.beaconRxFrequency,
                self.beaconTxFrequency,
                self.capabilities]

    #
    # Returns collection of attributes to read.  If attribute is static and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        # LnId
        if all_ or self.canRead(2):
            attributes.append(2)
        # LsId
        if all_ or self.canRead(3):
            attributes.append(3)
        # SId
        if all_ or self.canRead(4):
            attributes.append(4)
        # SNa
        if all_ or self.canRead(5):
            attributes.append(5)
        # State
        if all_ or self.canRead(6):
            attributes.append(6)
        # ScpLength
        if all_ or self.canRead(7):
            attributes.append(7)
        # NodeHierarchyLevel
        if all_ or self.canRead(8):
            attributes.append(8)
        # BeaconSlotCount
        if all_ or self.canRead(9):
            attributes.append(9)
        # BeaconRxSlot
        if all_ or self.canRead(10):
            attributes.append(10)
        # BeaconTxSlot
        if all_ or self.canRead(11):
            attributes.append(11)
        # BeaconRxFrequency
        if all_ or self.canRead(12):
            attributes.append(12)
        # BeaconTxFrequency
        if all_ or self.canRead(13):
            attributes.append(13)
        # Capabilities
        if all_ or self.canRead(14):
            attributes.append(14)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 14

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 0

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.INT16
        elif index in (3, 4):
            ret = DataType.UINT8
        elif index == 5:
            ret = DataType.OCTET_STRING
        elif index == 6:
            ret = DataType.ENUM
        elif index == 7:
            ret = DataType.INT16
        elif index in (8, 9, 10, 11, 12, 13):
            ret = DataType.UINT8
        elif index == 14:
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
            ret = self.lnId
        elif e.index == 3:
            ret = self.lsId
        elif e.index == 4:
            ret = self.sId
        elif e.index == 5:
            ret = self.sna
        elif e.index == 6:
            ret = self.state
        elif e.index == 7:
            ret = self.scpLength
        elif e.index == 8:
            ret = self.nodeHierarchyLevel
        elif e.index == 9:
            ret = self.beaconSlotCount
        elif e.index == 10:
            ret = self.beaconRxSlot
        elif e.index == 11:
            ret = self.beaconTxSlot
        elif e.index == 12:
            ret = self.beaconRxFrequency
        elif e.index == 13:
            ret = self.beaconTxFrequency
        elif e.index == 14:
            ret = self.capabilities
        else:
            ret = None
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.lnId = e.value
        elif e.index == 3:
            self.lsId = e.value
        elif e.index == 4:
            self.sId = e.value
        elif e.index == 5:
            self.sna = e.value
        elif e.index == 6:
            self.state = e.value
        elif e.index == 7:
            self.scpLength = e.value
        elif e.index == 8:
            self.nodeHierarchyLevel = e.value
        elif e.index == 9:
            self.beaconSlotCount = e.value
        elif e.index == 10:
            self.beaconRxSlot = e.value
        elif e.index == 11:
            self.beaconTxSlot = e.value
        elif e.index == 12:
            self.beaconRxFrequency = e.value
        elif e.index == 13:
            self.beaconTxFrequency = e.value
        elif e.index == 14:
            self.capabilities = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.lnId = reader.readElementContentAsInt("LnId")
        self.lsId = reader.readElementContentAsInt("LsId")
        self.sId = reader.readElementContentAsInt("SId")
        self.sna = GXByteBuffer.hexToBytes(reader.readElementContentAsString("SNa"))
        self.state = reader.readElementContentAsInt("State")
        self.scpLength = reader.readElementContentAsInt("ScpLength")
        self.nodeHierarchyLevel = reader.readElementContentAsInt("NodeHierarchyLevel")
        self.beaconSlotCount = reader.readElementContentAsInt("BeaconSlotCount")
        self.beaconRxSlot = reader.readElementContentAsInt("BeaconRxSlot")
        self.beaconTxSlot = reader.readElementContentAsInt("BeaconTxSlot")
        self.beaconRxFrequency = reader.readElementContentAsInt("BeaconRxFrequency")
        self.beaconTxFrequency = reader.readElementContentAsInt("BeaconTxFrequency")
        self.capabilities = reader.readElementContentAsInt("Capabilities")

    def save(self, writer):
        writer.writeElementString("LnId", self.lnId)
        writer.writeElementString("LsId", self.lsId)
        writer.writeElementString("SId", self.sId)
        writer.writeElementString("SNa", self.sna)
        writer.writeElementString("State", self.state)
        writer.writeElementString("ScpLength", self.scpLength)
        writer.writeElementString("NodeHierarchyLevel", self.nodeHierarchyLevel)
        writer.writeElementString("BeaconSlotCount", self.beaconSlotCount)
        writer.writeElementString("BeaconRxSlot", self.beaconRxSlot)
        writer.writeElementString("BeaconTxSlot", self.beaconTxSlot)
        writer.writeElementString("BeaconRxFrequency", self.beaconRxFrequency)
        writer.writeElementString("BeaconTxFrequency", self.beaconTxFrequency)
        writer.writeElementString("Capabilities", self.capabilities)

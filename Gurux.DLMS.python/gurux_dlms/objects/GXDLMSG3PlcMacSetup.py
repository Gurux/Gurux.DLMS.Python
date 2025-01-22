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
#  self file is a part of Gurux Device Framework.
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
#  self code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http:#www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ErrorCode
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from ..GXDateTime import GXDateTime
from ..enums import ObjectType, DataType, ClockStatus
from .enums.GainResolution import GainResolution
from .enums.Modulation import Modulation
from ..internal._GXDataInfo import _GXDataInfo
from .GXDLMSMacPosTable import GXDLMSMacPosTable
from .GXDLMSNeighbourTable import GXDLMSNeighbourTable


class GXDLMSG3PlcMacSetup(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    https://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSG3PlcMacSetup
    """

    def __init__(self, ln="0.0.29.1.0.255", sn=0):
        GXDLMSObject.__init__(self, ObjectType.G3_PLC_MAC_SETUP, ln, sn)
        self.__version = 3
        self.__keyTable = []
        self.__shortAddress = 0xFFFF
        self.__rcCoord = 0xFFFF
        self.__panId = 0xFFFF
        self.__frameCounter = 0
        self.__tmrTtl = 2
        self.__maxFrameRetries = 5
        self.__neighbourTable = []
        self.__neighbourTableEntryTtl = 255
        self.__highPriorityWindowSize = 7
        self.__cscmFairnessLimit = 25
        self.__beaconRandomizationWindowLength = 12
        self.__a = 8
        self.__k = 5
        self.__minCwAttempts = 10
        self.__cenelecLegacyMode = 1
        self.__fccLegacyMode = 1
        self.__maxBe = 8
        self.__maxCsmaBackoffs = 50
        self.__minBe = 3
        self.__toneMask = ""
        self.__macBroadcastMaxCwEnabled = False
        self.__macTransmitAtten = 0
        self.__macPosTable = []
        self.__macDuplicateDetectionTtl = 0

    @classmethod
    def __getNeighbourTables(cls, tables):
        bb = GXByteBuffer()
        bb.setUInt8(DataType.ARRAY)
        if tables is None:
            bb.setUInt8(0)
        else:
            _GXCommon.setObjectCount(len(tables), bb)
            for it in tables:
                bb.setUInt8(DataType.STRUCTURE)
                bb.setUInt8(11)
                _GXCommon.setData(None, bb, DataType.UINT16, it.shortAddress)
                _GXCommon.setData(None, bb, DataType.BOOLEAN, it.enabled)
                _GXCommon.setData(None, bb, DataType.BITSTRING, it.toneMap)
                _GXCommon.setData(None, bb, DataType.ENUM, it.modulation)
                _GXCommon.setData(None, bb, DataType.INT8, it.txGain)
                _GXCommon.setData(None, bb, DataType.ENUM, it.txRes)
                _GXCommon.setData(None, bb, DataType.BITSTRING, it.txCoeff)
                _GXCommon.setData(None, bb, DataType.UINT8, it.lqi)
                _GXCommon.setData(None, bb, DataType.INT8, it.phaseDifferential)
                _GXCommon.setData(None, bb, DataType.UINT8, it.tmrValidTime)
                _GXCommon.setData(None, bb, DataType.UINT8, it.neighbourValidTime)
        return bb.array()

    @classmethod
    def __getPosTables(cls, tables):
        bb = GXByteBuffer()
        bb.setUInt8(DataType.ARRAY)
        if tables is None:
            bb.setUInt8(0)
        else:
            _GXCommon.setObjectCount(len(tables), bb)
            for it in tables:
                bb.setUInt8(DataType.STRUCTURE)
                bb.setUInt8(3)
                _GXCommon.setData(None, bb, DataType.UINT16, it.shortAddress)
                _GXCommon.setData(None, bb, DataType.UINT8, it.lQI)
                _GXCommon.setData(None, bb, DataType.UINT8, it.validTime)
        return bb.array()

    def invoke(self, settings, e):
        list_ = []
        if e.index == 1:
            index = e.value
            for it in self.__neighbourTable:
                if it.shortAddress == index:
                    list_.append(it)
            return self.__getNeighbourTables(list_)
        elif e.index == 2:
            index = e.value
            for it in self.__macPosTable:
                if it.shortAddress == index:
                    list_.append(it)
            return self.__getPosTables(list_.ToArray())
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    def getAttributeIndexToRead(self, all_):
        attributes = []
        # LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        # MacShortAddress
        if all_ or self.canRead(2):
            attributes.append(2)
        # MacRcCoord
        if all_ or self.canRead(3):
            attributes.append(3)
        # MacPANId
        if all_ or self.canRead(4):
            attributes.append(4)
        # MackeyTable
        if all_ or self.canRead(5):
            attributes.append(5)
        # MacFrameCounter
        if all_ or self.canRead(6):
            attributes.append(6)
        # MacToneMask
        if all_ or self.canRead(7):
            attributes.append(7)
        # MacTmrTtl
        if all_ or self.canRead(8):
            attributes.append(8)
        # MacMaxFrameRetries
        if all_ or self.canRead(9):
            attributes.append(9)
        # MacneighbourTableEntryTtl
        if all_ or self.canRead(10):
            attributes.append(10)
        # MacNeighbourTable
        if all_ or self.canRead(11):
            attributes.append(11)
        # MachighPriorityWindowSize
        if all_ or self.canRead(12):
            attributes.append(12)
        # MacCscmFairnessLimit
        if all_ or self.canRead(13):
            attributes.append(13)
        # MacBeaconRandomizationWindowLength
        if all_ or self.canRead(14):
            attributes.append(14)
        # MacA
        if all_ or self.canRead(15):
            attributes.append(15)
        # MacK
        if all_ or self.canRead(16):
            attributes.append(16)
        # MacMinCwAttempts
        if all_ or self.canRead(17):
            attributes.append(17)
        # MacCenelecLegacyMode
        if all_ or self.canRead(18):
            attributes.append(18)
        # MacFCCLegacyMode
        if all_ or self.canRead(19):
            attributes.append(19)
        # MacMaxBe
        if all_ or self.canRead(20):
            attributes.append(20)
        # MacMaxCsmaBackoffs,
        if all_ or self.canRead(21):
            attributes.append(21)
        # MacMinBe
        if all_ or self.canRead(22):
            attributes.append(22)
        # MacBroadcastMaxCwEnabled
        if all_ or self.canRead(23):
            attributes.append(23)
        # MacTransmitAtten
        if all_ or self.canRead(24):
            attributes.append(24)
        # MacPosTable
        if all_ or self.canRead(25):
            attributes.append(25)
        # MacDuplicateDetectionTtl
        if self.__version > 2:
            if all_ or self.canRead(26):
                attributes.append(26)
        return attributes

    @classmethod
    def __parseNeighbourTableEntry(cls, value):
        list_ = []
        if value:
            for tmp in value:
                it = GXDLMSNeighbourTable()
                it.shortAddress = tmp[0]
                it.enabled = tmp[1]
                it.toneMap = str(tmp[2])
                it.modulation = Modulation(tmp[3])
                it.txGain = tmp[4]
                it.txRes = GainResolution(tmp[5])
                it.txCoeff = str(tmp[6])
                it.lqi = tmp[7]
                it.phaseDifferential = tmp[8]
                it.tmrValidTime = tmp[9]
                it.neighbourValidTime = tmp[10]
                list_.append(it)
        return list_

    @classmethod
    def __parsePosTableEntry(cls, value):
        list_ = []
        if value:
            for arr in value:
                it = GXDLMSMacPosTable()
                it.shortAddress = arr[0]
                it.lQI = arr[1]
                it.validTime = arr[2]
                list_.append(it)
        return list_

    def getNames(self):
        """
        Returns names of attribute indexes.

            Returns:
        """
        return (
            "Logical name",
            "MacShortAddress",
            "MacRcCoord",
            "MacPANId",
            "MackeyTable ",
            "MacFrameCounter",
            "MacToneMask",
            "MacTmrTtl",
            "MacMaxFrameRetries",
            "MacneighbourTableEntryTtl",
            "MacNeighbourTable",
            "MachighPriorityWindowSize",
            "MacCscmFairnessLimit",
            "MacBeaconRandomizationWindowLength",
            "MacA",
            "MacK",
            "MacMinCwAttempts",
            "MacCenelecLegacyMode",
            "MacFCCLegacyMode",
            "MacMaxBe",
            "MacMaxCsmaBackoffs",
            "MacMinBe",
            "MacBroadcastMaxCwEnabled",
            "MacTransmitAtten",
            "MacPosTable",
            "MacDuplicateDetectionTtl",
        )

    def getMethodNames(self):
        """
        Returns names of method indexes.
        """
        return ("MAC get neighbour table entry", "MAC get POS tableentry")

    def getAttributeCount(self):
        if self.__version == 3:
            return 26
        if self.__version == 2:
            return 25
        return 22

    def getMethodCount(self):
        if self.__version == 3:
            return 2
        return 1

    def getValue(self, settings, e):
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.__shortAddress
        elif e.index == 3:
            ret = self.__rcCoord
        elif e.index == 4:
            ret = self.__panId
        elif e.index == 5:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.ARRAY)
            if self.__keyTable is None:
                bb.setUInt8(0)
            else:
                _GXCommon.setObjectCount(len(self.__keyTable), bb)
                for k, v in self.__keyTable:
                    bb.setUInt8(DataType.STRUCTURE)
                    bb.setUInt8(2)
                    _GXCommon.setData(settings, bb, DataType.UINT8, k)
                    _GXCommon.setData(settings, bb, DataType.OCTET_STRING, v)
            ret = bb.array()
        elif e.index == 6:
            ret = self.__frameCounter
        elif e.index == 7:
            ret = self.__toneMask
        elif e.index == 8:
            ret = self.__tmrTtl
        elif e.index == 9:
            ret = self.__maxFrameRetries
        elif e.index == 10:
            ret = self.__neighbourTableEntryTtl
        elif e.index == 11:
            ret = self.__getNeighbourTables(self.__neighbourTable)
        elif e.index == 12:
            ret = self.__highPriorityWindowSize
        elif e.index == 13:
            ret = self.__cscmFairnessLimit
        elif e.index == 14:
            ret = self.__beaconRandomizationWindowLength
        elif e.index == 15:
            ret = self.__a
        elif e.index == 16:
            ret = self.__k
        elif e.index == 17:
            ret = self.__minCwAttempts
        elif e.index == 18:
            ret = self.__cenelecLegacyMode
        elif e.index == 19:
            ret = self.__fccLegacyMode
        elif e.index == 20:
            ret = self.__maxBe
        elif e.index == 21:
            ret = self.__maxCsmaBackoffs
        elif e.index == 22:
            ret = self.__minBe
        elif e.index == 23:
            ret = self.__macBroadcastMaxCwEnabled
        elif e.index == 24:
            ret = self.__macTransmitAtten
        elif e.index == 25:
            ret = self.__getPosTables(self.__macPosTable)
        elif e.index == 26:
            ret = self.__macDuplicateDetectionTtl
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
            ret = None
        return ret

    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.__shortAddress = e.value
        elif e.index == 3:
            self.__rcCoord = e.value
        elif e.index == 4:
            self.__panId = e.value
        elif e.index == 5:
            self.__keyTable.clear()
            if e.value:
                for arr in e.value:
                    self.__keyTable.append((arr[0], arr[1]))
        elif e.index == 6:
            self.frameCounter = e.value
        elif e.index == 7:
            self.toneMask = e.value
        elif e.index == 8:
            self.tmrTtl = e.value
        elif e.index == 9:
            self.maxFrameRetries = e.value
        elif e.index == 10:
            self.neighbourTableEntryTtl = e.value
        elif e.index == 11:
            self.__neighbourTable = self.__parseNeighbourTableEntry(e.value)
        elif e.index == 12:
            self.highPriorityWindowSize = e.value
        elif e.index == 13:
            self.cscmFairnessLimit = e.value
        elif e.index == 14:
            self.beaconRandomizationWindowLength = e.value
        elif e.index == 15:
            self.a = e.value
        elif e.index == 16:
            self.k = e.value
        elif e.index == 17:
            self.minCwAttempts = e.value
        elif e.index == 18:
            self.cenelecLegacyMode = e.value
        elif e.index == 19:
            self.fccLegacyMode = e.value
        elif e.index == 20:
            self.maxBe = e.value
        elif e.index == 21:
            self.maxCsmaBackoffs = e.value
        elif e.index == 22:
            self.minBe = e.value
        elif e.index == 23:
            self.macBroadcastMaxCwEnabled = e.value
        elif e.index == 24:
            self.macTransmitAtten = e.value
        elif e.index == 25:
            self.__macPosTable = self.__parsePosTableEntry(e.value)
        elif e.index == 26:
            self.macDuplicateDetectionTtl = e.value
        else:
            e.error = ErrorCode.ReadWriteDenied

    @property
    def shortAddress(self):
        """
        The 16-bit address the device is using to communicate through the PAN.
        """
        return self.__shortAddress

    @shortAddress.setter
    def shortAddress(self, value):
        self.__shortAddress = value

    @property
    def rcCoord(self):
        """
        Route cost to coordinator.
        """
        return self.__rcCoord

    @rcCoord.setter
    def rcCoord(self, value):
        self.__rcCoord = value

    @property
    def pANId(self):
        """
        The 16-bit identifier of the PAN through which the device is operating.
        """
        return self.__panId

    @pANId.setter
    def pANId(self, value):
        self.__panId = value

    @property
    def keyTable(self):
        """
        self attribute holds GMK keys required for MAC layer ciphering.
        """
        return self.__keyTable

    @keyTable.setter
    def keyTable(self, value):
        self.__keyTable = value

    @property
    def frameCounter(self):
        """
        The outgoing frame counter for self device, used when ciphering frames at MAC layer.
        """
        return self.__frameCounter

    @frameCounter.setter
    def frameCounter(self, value):
        self.__frameCounter = value

    @property
    def toneMask(self):
        """
        Defines the tone mask to use during symbol formation.
        """
        return self.__toneMask

    @toneMask.setter
    def toneMask(self, value):
        self.__toneMask = value

    @property
    def tmrTtl(self):
        """
        Maximum time to live of tone map parameters entry in the neighbour table in minutes.
        """
        return self.__tmrTtl

    @tmrTtl.setter
    def tmrTtl(self, value):
        self.__tmrTtl = value

    @property
    def maxFrameRetries(self):
        """
        Maximum number of retransmissions.
        """
        return self.__maxFrameRetries

    @maxFrameRetries.setter
    def maxFrameRetries(self, value):
        self.__maxFrameRetries = value

    @property
    def neighbourTableEntryTtl(self):
        """
        Maximum time to live for an entry in the neighbour table in minutes
        """
        return self.__neighbourTableEntryTtl

    @neighbourTableEntryTtl.setter
    def neighbourTableEntryTtl(self, value):
        self.__neighbourTableEntryTtl = value

    @property
    def neighbourTable(self):
        """
        The neighbour table contains information about all the devices within the POS of the device
        """
        return self.__neighbourTable

    @neighbourTable.setter
    def neighbourTable(self, value):
        self.__neighbourTable = value

    @property
    def highPriorityWindowSize(self):
        """
        The high priority contention window size in number of slots.
        """
        return self.__highPriorityWindowSize

    @highPriorityWindowSize.setter
    def highPriorityWindowSize(self, value):
        self.__highPriorityWindowSize = value

    @property
    def cscmFairnessLimit(self):
        """
        Channel access fairness limit.
        """
        return self.__cscmFairnessLimit

    @cscmFairnessLimit.setter
    def cscmFairnessLimit(self, value):
        self.__cscmFairnessLimit = value

    @property
    def beaconRandomizationWindowLength(self):
        """
        Duration time in seconds for the beacon randomization.
        """
        return self.__beaconRandomizationWindowLength

    @beaconRandomizationWindowLength.setter
    def beaconRandomizationWindowLength(self, value):
        self.__beaconRandomizationWindowLength = value

    @property
    def a(self):
        """
        self parameter controls the adaptive CW linear decrease.
        """
        return self.__a

    @a.setter
    def a(self, value):
        self.__a = value

    @property
    def k(self):
        """
        Rate adaptation factor for channel access fairness limit.
        """
        return self.__k

    @k.setter
    def k(self, value):
        self.__k = value

    @property
    def minCwAttempts(self):
        """
        Number of consecutive attempts while using minimum CW.
        """
        return self.__minCwAttempts

    @minCwAttempts.setter
    def minCwAttempts(self, value):
        self.__minCwAttempts = value

    @property
    def cenelecLegacyMode(self):
        """
        self read only attribute indicates the capability of the node.
        """
        return self.__cenelecLegacyMode

    @cenelecLegacyMode.setter
    def cenelecLegacyMode(self, value):
        self.__cenelecLegacyMode = value

    @property
    def fccLegacyMode(self):
        """
        self read only attribute indicates the capability of the node.
        """
        return self.__fccLegacyMode

    @fccLegacyMode.setter
    def fccLegacyMode(self, value):
        self.__fccLegacyMode = value

    @property
    def maxBe(self):
        """
        Maximum value of backoff exponent.
        """
        return self.__maxBe

    @maxBe.setter
    def maxBe(self, value):
        self.__maxBe = value

    @property
    def maxCsmaBackoffs(self):
        """
        Maximum number of backoff attempts.
        """
        return self.__maxCsmaBackoffs

    @maxCsmaBackoffs.setter
    def maxCsmaBackoffs(self, value):
        self.__maxCsmaBackoffs = value

    @property
    def minBe(self):
        """
        Minimum value of backoff exponent.
        """
        return self.__minBe

    @minBe.setter
    def minBe(self, value):
        self.__minBe = value

    @property
    def macBroadcastMaxCwEnabled(self):
        """
        If True, MAC uses maximum contention window.
        """
        return self.__macBroadcastMaxCwEnabled

    @macBroadcastMaxCwEnabled.setter
    def macBroadcastMaxCwEnabled(self, value):
        self.__macBroadcastMaxCwEnabled = value

    @property
    def macTransmitAtten(self):
        """
        Attenuation of the output level in dB.
        """
        return self.__macTransmitAtten

    @macTransmitAtten.setter
    def macTransmitAtten(self, value):
        self.__macTransmitAtten = value

    @property
    def macPosTable(self):
        """
               The neighbour table contains some information

        about all the devices within the POS of the device.
        """
        return self.__macPosTable

    @macPosTable.setter
    def macPosTable(self, value):
        self.__macPosTable = value

    @property
    def macDuplicateDetectionTtl(self):
        """
        Duplicate frame detection time in seconds.
        """
        return self.__macDuplicateDetectionTtl

    @macDuplicateDetectionTtl.setter
    def macDuplicateDetectionTtl(self, value):
        self.__macDuplicateDetectionTtl = value

    def getValues(self):
        """
        Returns attributes as an array.

            Returns:
                Collection of COSEM object values.
        """
        return (
            self.logicalName,
            self.__shortAddress,
            self.__rcCoord,
            self.__panId,
            self.__keyTable,
            self.__frameCounter,
            self.__toneMask,
            self.__tmrTtl,
            self.__maxFrameRetries,
            self.__neighbourTableEntryTtl,
            self.__neighbourTable,
            self.__highPriorityWindowSize,
            self.__cscmFairnessLimit,
            self.__beaconRandomizationWindowLength,
            self.__a,
            self.__k,
            self.__minCwAttempts,
            self.__cenelecLegacyMode,
            self.__fccLegacyMode,
            self.__maxBe,
            self.__maxCsmaBackoffs,
            self.__minBe,
            self.__macBroadcastMaxCwEnabled,
            self.__macTransmitAtten,
            self.__macPosTable,
            self.__macDuplicateDetectionTtl,
        )

    def getNeighbourTableEntry(self, client, address):
        """
        Retrieves the MAC neighbour table.

            Parameters:
                client: DLMS client.
                address: MAC short address

            Returns:
                Generated bytes.
        """
        return client.method(self, 1, address)

    def parseNeighbourTableEntry(self, reply):
        """
        Parse neighbour table entry.

            Parameters:
                reply: Received reply

            Returns:
        """
        info = _GXDataInfo()
        value = _GXCommon.getData(None, reply, info)
        return self.__parseNeighbourTableEntry(value)

    def getPosTableEntry(self, client, address):
        """
        Retrieves the mac POS table.

            Parameters:
                client: DLMS client.
                address: MAC short address

            Returns:
                Generated bytes.
        """
        return client.method(self, 2, address)

    def parsePosTableEntry(self, reply):
        """
        Parse MAC POS tables.

            Parameters:
                reply: Received reply

            Returns:
        """
        info = _GXDataInfo()
        value = _GXCommon.getData(None, reply, info)
        return self.__parsePosTableEntry(value)

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.UINT16
        elif index == 3:
            ret = DataType.UINT16
        elif index == 4:
            ret = DataType.UINT16
        elif index == 5:
            ret = DataType.ARRAY
        elif index == 6:
            ret = DataType.UINT32
        elif index == 7:
            ret = DataType.BITSTRING
        elif index == 8:
            ret = DataType.UINT8
        elif index == 9:
            ret = DataType.UINT8
        elif index == 10:
            ret = DataType.UINT8
        elif index == 11:
            ret = DataType.ARRAY
        elif index == 12:
            ret = DataType.UINT8
        elif index == 13:
            ret = DataType.UINT8
        elif index == 14:
            ret = DataType.UINT8
        elif index == 15:
            ret = DataType.UINT8
        elif index == 16:
            ret = DataType.UINT8
        elif index == 17:
            ret = DataType.UINT8
        elif index == 18:
            ret = DataType.UINT8
        elif index == 19:
            ret = DataType.UINT8
        elif index == 20:
            ret = DataType.UINT8
        elif index == 21:
            ret = DataType.UINT8
        elif index == 22:
            ret = DataType.UINT8
        elif index == 23:
            ret = DataType.BOOLEAN
        elif index == 24:
            ret = DataType.UINT8
        elif index == 25:
            ret = DataType.ARRAY
        elif index == 26:
            ret = DataType.UINT8
        else:
            raise ValueError("GetDataType failed. Invalid attribute index.")
        return ret

    def __loadKeyTable(self, reader):
        self.__keyTable.clear()
        if reader.isStartElement("KeyTable", True):
            while reader.isStartElement("Item", True):
                k = reader.readElementContentAsInt("Key")
                d = _GXCommon.hexToBytes(reader.readElementContentAsString("Data"))
                self.__keyTable.append((k, d))
            reader.readEndElement("KeyTable")

    def __loadNeighbourTable(self, reader):
        self.__neighbourTable.clear()
        if reader.isStartElement("NeighbourTable", True):
            while reader.isStartElement("Item", True):
                it = GXDLMSNeighbourTable()
                it.shortAddress = reader.readElementContentAsInt("ShortAddress")
                it.enabled = reader.readElementContentAsInt("Enabled") != 0
                it.toneMap = reader.readElementContentAsString("ToneMap")
                it.modulation = Modulation(reader.readElementContentAsInt("Modulation"))
                it.txGain = reader.readElementContentAsInt("TxGain")
                it.txRes = GainResolution(reader.readElementContentAsInt("TxRes"))
                it.txCoeff = reader.readElementContentAsString("TxCoeff")
                it.lqi = reader.readElementContentAsInt("Lqi")
                it.phaseDifferential = reader.readElementContentAsInt(
                    "PhaseDifferential"
                )
                it.tmrValidTime = reader.readElementContentAsInt("TMRValidTime")
                it.NeighbourValidTime = reader.readElementContentAsInt(
                    "NeighbourValidTime"
                )
                self.__neighbourTable.Add(it)
            reader.readEndElement("NeighbourTable")

    def __loadMacPosTable(self, reader):
        self.__macPosTable.clear()
        if reader.isStartElement("MacPosTable", True):
            while reader.isStartElement("Item", True):
                it = GXDLMSMacPosTable()
                it.shortAddress = reader.readElementContentAsInt("ShortAddress")
                it.lqi = reader.readElementContentAsInt("LQI")
                it.validTime = reader.readElementContentAsInt("ValidTime")
                self.__macPosTable.Add(it)
            reader.readEndElement("MacPosTable")

    def load(self, reader):
        self.__shortAddress = reader.readElementContentAsInt("ShortAddress")
        self.__rcCoord = reader.readElementContentAsInt("RcCoord")
        self.__panId = reader.readElementContentAsInt("PANId")
        self.__loadKeyTable(reader)
        self.__frameCounter = reader.readElementContentAsInt("FrameCounter")
        self.__toneMask = reader.readElementContentAsString("ToneMask")
        self.__tmrTtl = reader.readElementContentAsInt("TmrTtl")
        self.__maxFrameRetries = reader.readElementContentAsInt("MaxFrameRetries")
        self.__neighbourTableEntryTtl = reader.readElementContentAsInt(
            "NeighbourTableEntryTtl"
        )
        self.__loadNeighbourTable(reader)
        self.__highPriorityWindowSize = reader.readElementContentAsInt(
            "HighPriorityWindowSize"
        )
        self.__cscmFairnessLimit = reader.readElementContentAsInt("CscmFairnessLimit")
        self.__beaconRandomizationWindowLength = reader.readElementContentAsInt(
            "BeaconRandomizationWindowLength"
        )
        self.__a = reader.readElementContentAsInt("A")
        self.__k = reader.readElementContentAsInt("K")
        self.__minCwAttempts = reader.readElementContentAsInt("MinCwAttempts")
        self.__cenelecLegacyMode = reader.readElementContentAsInt("CenelecLegacyMode")
        self.__fccLegacyMode = reader.readElementContentAsInt("FccLegacyMode")
        self.__maxBe = reader.readElementContentAsInt("MaxBe")
        self.__maxCsmaBackoffs = reader.readElementContentAsInt("MaxCsmaBackoffs")
        self.__minBe = reader.readElementContentAsInt("MinBe")
        self.__macBroadcastMaxCwEnabled = (
            reader.readElementContentAsInt("MacBroadcastMaxCwEnabled") != 0
        )
        self.__macTransmitAtten = reader.readElementContentAsInt("MacTransmitAtten")
        self.__loadMacPosTable(reader)
        self.__macDuplicateDetectionTtl = reader.readElementContentAsInt(
            "MacDuplicateDetectionTtl"
        )

    def __saveKeyTable(self, writer, index):
        writer.writeStartElement("KeyTable", index)
        if self.__keyTable:
            for k, v in self.__keyTable:
                writer.writeStartElement("Item", index)
                writer.writeElementString("Key", k, index)
                writer.writeElementString("Data", _GXCommon.toHex(v), index)
                writer.writeEndElement()
        writer.writeEndElement()  # KeyTable

    def __saveNeighbourTable(self, writer):
        writer.writeStartElement("NeighbourTable")
        if self.__neighbourTable:
            for it in self.__neighbourTable:
                writer.writeStartElement("Item")
                writer.writeElementString("ShortAddress", it.shortAddress)
                writer.writeElementString("Enabled", it.enabled)
                writer.writeElementString("ToneMap", it.toneMap)
                writer.writeElementString("Modulation", it.modulation)
                writer.writeElementString("TxGain", it.txGain)
                writer.writeElementString("TxRes", it.txRes)
                writer.writeElementString("TxCoeff", it.txCoeff)
                writer.writeElementString("Lqi", it.Lqi)
                writer.writeElementString("PhaseDifferential", it.phaseDifferential)
                writer.writeElementString("TMRValidTime", it.tmrValidTime)
                writer.writeElementString("NeighbourValidTime", it.neighbourValidTime)
                writer.writeEndElement()
        writer.writeEndElement()  # NeighbourTable

    def __saveMacPosTable(self, writer):
        writer.writeStartElement("MacPosTable")
        if self.__macPosTable:
            for it in self.__macPosTable:
                writer.writeStartElement("Item")
                writer.writeElementString("ShortAddress", it.shortAddress)
                writer.writeElementString("LQI", it.lqi)
                writer.writeElementString("ValidTime", it.validTime)
                writer.writeEndElement()
        writer.writeEndElement()  # MacPosTable

    def save(self, writer):
        writer.writeElementString("ShortAddress", self.__shortAddress)
        writer.writeElementString("RcCoord", self.__rcCoord)
        writer.writeElementString("PANId", self.__panId)
        self.__saveKeyTable(writer)
        writer.writeElementString("FrameCounter", self.__frameCounter)
        writer.writeElementString("ToneMask", self.__toneMask)
        writer.writeElementString("TmrTtl", self.__tmrTtl)
        writer.writeElementString("MaxFrameRetries", self.__maxFrameRetries)
        writer.writeElementString(
            "NeighbourTableEntryTtl", self.__neighbourTableEntryTtl
        )
        self.__saveNeighbourTable(writer)
        writer.writeElementString(
            "HighPriorityWindowSize", self.__highPriorityWindowSize
        )
        writer.writeElementString("CscmFairnessLimit", self.__cscmFairnessLimit)
        writer.writeElementString(
            "BeaconRandomizationWindowLength", self.__beaconRandomizationWindowLength
        )
        writer.writeElementString("A", self.__a)
        writer.writeElementString("K", self.__k)
        writer.writeElementString("MinCwAttempts", self.__minCwAttempts)
        writer.writeElementString("CenelecLegacyMode", self.__cenelecLegacyMode)
        writer.writeElementString("FccLegacyMode", self.__fccLegacyMode)
        writer.writeElementString("MaxBe", self.__maxBe)
        writer.writeElementString("MaxCsmaBackoffs", self.__maxCsmaBackoffs)
        writer.writeElementString("MinBe", self.__minBe)
        writer.writeElementString(
            "MacBroadcastMaxCwEnabled", self.__macBroadcastMaxCwEnabled
        )
        writer.writeElementString("MacTransmitAtten", self.__macTransmitAtten)
        self.__saveMacPosTable(writer)
        writer.writeElementString(
            "MacDuplicateDetectionTtl", self.__macDuplicateDetectionTtl
        )

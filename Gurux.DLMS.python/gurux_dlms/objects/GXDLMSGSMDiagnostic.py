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
from .enums import GsmStatus, GsmCircuitSwitchStatus, GsmPacketSwitchStatus
from .GXDLMSGSMCellInfo import GXDLMSGSMCellInfo
from .GXAdjacentCell import GXAdjacentCell

# pylint: disable=too-many-instance-attributes
class GXDLMSGSMDiagnostic(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSGSMDiagnostic
    """

    def __init__(self, ln="0.0.25.6.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.GSM_DIAGNOSTIC, ln, sn)
        self.version = 1
        self.cellInfo = GXDLMSGSMCellInfo()
        self.adjacentCells = list()
        self.operator = ""
        self.status = GsmStatus.NONE
        self.circuitSwitchStatus = GsmCircuitSwitchStatus.INACTIVE
        self.packetSwitchStatus = GsmPacketSwitchStatus.INACTIVE
        self.captureTime = None

    #
    # Returns collection of attributes to read.  If attribute is static and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  Operator
        if all_ or self.canRead(2):
            attributes.append(2)
        #  Status
        if all_ or self.canRead(3):
            attributes.append(3)
        #  CircuitSwitchStatus
        if all_ or self.canRead(4):
            attributes.append(4)
        #  PacketSwitchStatus
        if all_ or self.canRead(5):
            attributes.append(5)
        #  CellInfo
        if all_ or self.canRead(6):
            attributes.append(6)
        #  AdjacentCells
        if all_ or self.canRead(7):
            attributes.append(7)
        #  CaptureTime
        if all_ or self.canRead(8):
            attributes.append(8)
        return attributes

    def getValues(self):
        return [self.logicalName,
                self.operator,
                self.status,
                self.circuitSwitchStatus,
                self.packetSwitchStatus,
                self.cellInfo,
                self.adjacentCells,
                self.captureTime]

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 8

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 0

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.STRING
        elif index == 3:
            ret = DataType.ENUM
        elif index == 4:
            ret = DataType.ENUM
        elif index == 5:
            ret = DataType.ENUM
        elif index == 6:
            ret = DataType.STRUCTURE
        elif index == 7:
            ret = DataType.ARRAY
        elif index == 8:
            ret = DataType.DATETIME
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret
    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        bb = None
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            #pylint: disable=bad-option-value,redefined-variable-type
            if self.operator is None:
                ret = None
            else:
                ret = self.operator.encode()
        elif e.index == 3:
            if not self.status:
                ret = 0
            else:
                ret = self.status
        elif e.index == 4:
            ret = self.circuitSwitchStatus
        elif e.index == 5:
            ret = self.packetSwitchStatus
        elif e.index == 6:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.STRUCTURE)
            if self.version == 0:
                bb.setUInt8(4)
                _GXCommon.setData(settings, bb, DataType.UINT16, self.cellInfo.cellId)
            else:
                bb.setUInt8(7)
                _GXCommon.setData(settings, bb, DataType.UINT32, self.cellInfo.cellId)
            _GXCommon.setData(settings, bb, DataType.UINT16, self.cellInfo.locationId)
            _GXCommon.setData(settings, bb, DataType.UINT8, self.cellInfo.signalQuality)
            _GXCommon.setData(settings, bb, DataType.UINT8, self.cellInfo.ber)
            if self.version > 0:
                _GXCommon.setData(settings, bb, DataType.UINT16, self.cellInfo.mobileCountryCode)
                _GXCommon.setData(settings, bb, DataType.UINT16, self.cellInfo.mobileNetworkCode)
                _GXCommon.setData(settings, bb, DataType.UINT32, self.cellInfo.channelNumber)
            ret = bb
        elif e.index == 7:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.ARRAY)
            if self.adjacentCells is None:
                bb.setUInt8(0)
            else:
                bb.setUInt8(len(self.adjacentCells))
            for it in self.adjacentCells:
                bb.setUInt8(DataType.STRUCTURE)
                bb.setUInt8(2)
                if self.version == 0:
                    _GXCommon.setData(settings, bb, DataType.UINT16, it.cellId)
                else:
                    _GXCommon.setData(settings, bb, DataType.UINT32, it.cellId)
                _GXCommon.setData(settings, bb, DataType.UINT8, it.signalQuality)
            ret = bb
        elif e.index == 8:
            ret = self.captureTime
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
            if isinstance(e.value, bytearray):
                self.operator = str(e.value)
            elif isinstance(self.operator, (str,)):
                self.operator = str(e.value)
            elif self.operator is None:
                self.operator = None
            else:
                e.error = ErrorCode.READ_WRITE_DENIED
        elif e.index == 3:
            self.status = GsmStatus(e.value)
        elif e.index == 4:
            self.circuitSwitchStatus = GsmCircuitSwitchStatus(e.value)
        elif e.index == 5:
            self.packetSwitchStatus = GsmPacketSwitchStatus(e.value)
        elif e.index == 6:
            if e.value:
                self.cellInfo.cellId = e.value[0]
                self.cellInfo.locationId = e.value[1]
                self.cellInfo.signalQuality = e.value[2]
                self.cellInfo.ber = e.value[3]
                if self.version > 0:
                    self.cellInfo.mobileCountryCode = e.value[4]
                    self.cellInfo.mobileNetworkCode = e.value[5]
                    self.cellInfo.channelNumber = e.value[6]
        elif e.index == 7:
            self.adjacentCells = []
            if e.value:
                for it in e.value:
                    ac = GXAdjacentCell()
                    ac.cellId = it[0]
                    ac.signalQuality = it[1]
                    self.adjacentCells.append(ac)
        elif e.index == 8:
            if isinstance(e.value, bytearray):
                self.captureTime = _GXCommon.changeType(settings, e.value, DataType.DATETIME)
            else:
                self.captureTime = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.operator = reader.readElementContentAsString("Operator")
        self.status = reader.readElementContentAsInt("Status")
        self.circuitSwitchStatus = reader.readElementContentAsInt("CircuitSwitchStatus")
        self.packetSwitchStatus = reader.readElementContentAsInt("PacketSwitchStatus")
        if reader.isStartElement("CellInfo", True):
            self.cellInfo.cellId = reader.readElementContentAsLong("CellId")
            self.cellInfo.locationId = reader.readElementContentAsInt("LocationId")
            self.cellInfo.signalQuality = reader.readElementContentAsInt("SignalQuality")
            self.cellInfo.ber = reader.readElementContentAsInt("Ber")
            reader.readEndElement("CellInfo")
        self.adjacentCells = []
        if reader.isStartElement("AdjacentCells", True):
            while reader.isStartElement("Item", True):
                it = GXAdjacentCell()
                it.cellId = reader.readElementContentAsLong("CellId")
                it.signalQuality = reader.readElementContentAsInt("SignalQuality")
                self.adjacentCells.append(it)
            reader.readEndElement("AdjacentCells")
        self.captureTime = reader.readElementContentAsDateTime("CaptureTime")

    def save(self, writer):
        writer.writeElementObject("Operator", self.operator)
        writer.writeElementString("Status", int(self.status))
        writer.writeElementString("CircuitSwitchStatus", int(self.circuitSwitchStatus))
        writer.writeElementString("PacketSwitchStatus", int(self.packetSwitchStatus))
        if self.cellInfo:
            writer.writeStartElement("CellInfo")
            writer.writeElementString("CellId", self.cellInfo.cellId)
            writer.writeElementString("LocationId", self.cellInfo.locationId)
            writer.writeElementString("SignalQuality", self.cellInfo.signalQuality)
            writer.writeElementString("Ber", self.cellInfo.ber)
            writer.writeEndElement()
        if self.adjacentCells:
            writer.writeStartElement("AdjacentCells")
            for it in self.adjacentCells:
                writer.writeStartElement("Item")
                writer.writeElementString("CellId", it.cellId)
                writer.writeElementString("SignalQuality", it.signalQuality)
                writer.writeEndElement()
            writer.writeEndElement()
        writer.writeElementString("CaptureTime", self.captureTime)

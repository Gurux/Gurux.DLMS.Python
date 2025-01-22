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
class GXDLMSG3PlcMacLayerCounters(GXDLMSObject, IGXDLMSBase):

    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSData
    """

    def __init__(self, ln="0.0.29.0.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.G3_PLC_MAC_LAYER_COUNTERS, ln, sn)
        self.version = 1
        self.txDataPacketCount = 0
        self.rxDataPacketCount = 0
        self.txCmdPacketCount = 0
        self.rxCmdPacketCount = 0
        self.csmaFailCount = 0
        self.csmaNoAckCount = 0
        self.badCrcCount = 0
        self.txDataBroadcastCount = 0
        self.rxDataBroadcastCount = 0

    def getValues(self):
        return [
            self.logicalName,
            self.txDataPacketCount,
            self.rxDataPacketCount,
            self.txCmdPacketCount,
            self.rxCmdPacketCount,
            self.csmaFailCount,
            self.csmaNoAckCount,
            self.badCrcCount,
            self.txDataBroadcastCount,
            self.rxDataBroadcastCount,
        ]

    #
    # Returns collection of attributes to read.  If attribute is static and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = []
        # LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        if all or self.canRead(2):
            attributes.append(2)
        if all or self.canRead(3):
            attributes.append(3)
        if all or self.canRead(4):
            attributes.append(4)
        if all or self.canRead(5):
            attributes.append(5)
        if all or self.canRead(6):
            attributes.append(6)
        if all or self.canRead(7):
            attributes.append(7)
        if all or self.canRead(8):
            attributes.append(8)
        if all or self.canRead(9):
            attributes.append(9)
        if all or self.canRead(10):
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
        return 1

    def getDataType(self, index):
        if index == 1:
            return DataType.OCTET_STRING
        elif index in range(2, 11):
            # pylint: disable=super-with-arguments
            return DataType.UINT32
        raise ValueError("getDataType failed. Invalid attribute index.")

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.txDataPacketCount
        elif e.index == 3:
            ret = self.rxDataPacketCount
        elif e.index == 4:
            ret = self.txCmdPacketCount
        elif e.index == 5:
            ret = self.rxCmdPacketCount
        elif e.index == 6:
            ret = self.csmaFailCount
        elif e.index == 7:
            ret = self.csmaNoAckCount
        elif e.index == 8:
            ret = self.badCrcCount
        elif e.index == 9:
            ret = self.txDataBroadcastCount
        elif e.index == 10:
            ret = self.rxDataBroadcastCount
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
            self.txDataPacketCount = int(e.value)
        elif e.index == 3:
            self.rxDataPacketCount = int(e.value)
        elif e.index == 4:
            self.txCmdPacketCount = int(e.value)
        elif e.index == 5:
            self.rxCmdPacketCount = int(e.value)
        elif e.index == 6:
            self.csmaFailCount = int(e.value)
        elif e.index == 7:
            self.csmaNoAckCount = int(e.value)
        elif e.index == 8:
            self.badCrcCount = int(e.value)
        elif e.index == 9:
            self.txDataBroadcastCount = int(e.value)
        elif e.index == 10:
            self.rxDataBroadcastCount = int(e.value)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.txDataPacketCount = reader.readElementContentAsInt("TxDataPacketCount")
        self.rxDataPacketCount = reader.readElementContentAsInt("RxDataPacketCount")
        self.txCmdPacketCount = reader.readElementContentAsInt("TxCmdPacketCount")
        self.rxCmdPacketCount = reader.readElementContentAsInt("RxCmdPacketCount")
        self.csmaFailCount = reader.readElementContentAsInt("CSMAFailCount")
        self.csmaNoAckCount = reader.readElementContentAsInt("CSMANoAckCount")
        self.badCrcCount = reader.readElementContentAsInt("BadCrcCount")
        self.txDataBroadcastCount = reader.readElementContentAsInt(
            "TxDataBroadcastCount"
        )
        self.rxDataBroadcastCount = reader.readElementContentAsInt(
            "RxDataBroadcastCount"
        )

    def save(self, writer):
        writer.writeElementString("TxDataPacketCount", self.txDataPacketCount)
        writer.writeElementString("RxDataPacketCount", self.rxDataPacketCount)
        writer.writeElementString("TxCmdPacketCount", self.txCmdPacketCount)
        writer.writeElementString("RxCmdPacketCount", self.rxCmdPacketCount)
        writer.writeElementString("CSMAFailCount", self.csmaFailCount)
        writer.writeElementString("CSMANoAckCount", self.csmaNoAckCount)
        writer.writeElementString("BadCrcCount", self.badCrcCount)
        writer.writeElementString("TxDataBroadcastCount", self.txDataBroadcastCount)
        writer.writeElementString("RxDataBroadcastCount", self.rxDataBroadcastCount)

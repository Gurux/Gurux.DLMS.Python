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
class GXDLMSPrimeNbOfdmPlcMacCounters(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSPrimeNbOfdmPlcMacCounters
    """

    def __init__(self, ln="0.0.28.4.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.PRIME_NB_OFDM_PLC_MAC_COUNTERS, ln, sn)
        # Count of successfully transmitted MSDUs.
        self.txDataPktCount = 0
        # Count of successfully received MSDUs whose destination address
        # was this node.
        self.rxDataPktCount = 0
        # Count of successfully transmitted MAC control packets.
        self.txCtrlPktCount = 0
        # Count of successfully received MAC control packets whose
        # destination was this node.
        self.rxCtrlPktCount = 0
        # Count of failed CSMA transmit attempts.
        self.csmaFailCount = 0
        # Count of number of times this node has to back off SCP
        # transmission due to channel busy state.
        self.csmaChBusyCount = 0

    def getValues(self):
        return [self.logicalName,
                self.txDataPktCount,
                self.rxDataPktCount,
                self.txCtrlPktCount,
                self.rxCtrlPktCount,
                self.csmaFailCount,
                self.csmaChBusyCount]

    def reset(self, client):
        """Reset all counters."""
        return client.method(self.getName(), self.objectType, 1, 0, DataType.INT8)

    def invoke(self, settings, e):
        #  Resets the value to the default value.
        #  The default value is an instance specific constant.
        if e.index == 1:
            self.txDataPktCount = self.rxDataPktCount = self.txCtrlPktCount = self.rxCtrlPktCount = self.csmaFailCount = self.csmaChBusyCount = 0
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    #
    # Returns collection of attributes to read.  If attribute is static and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  TxDataPktCount
        if all_ or self.canRead(2):
            attributes.append(2)
        #  RxDataPktCount
        if all_ or self.canRead(3):
            attributes.append(3)
        #  TxCtrlPktCount
        if all_ or self.canRead(4):
            attributes.append(4)
        #  RxCtrlPktCount
        if all_ or self.canRead(5):
            attributes.append(5)
        #  CsmaFailCount
        if all_ or self.canRead(6):
            attributes.append(6)
        #  CsmaChBusyCount
        if all_ or self.canRead(7):
            attributes.append(7)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 7

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 1

    def getDataType(self, index):
        if index == 1:
            return DataType.OCTET_STRING
        if index in (2, 3, 4, 5, 6, 7):
            return DataType.UINT32
        raise ValueError("getDataType failed. Invalid attribute index.")

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.txDataPktCount
        elif e.index == 3:
            ret = self.rxDataPktCount
        elif e.index == 4:
            ret = self.txCtrlPktCount
        elif e.index == 5:
            ret = self.rxCtrlPktCount
        elif e.index == 6:
            ret = self.csmaFailCount
        elif e.index == 7:
            ret = self.csmaChBusyCount
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
            self.txDataPktCount = e.value
        elif e.index == 3:
            self.rxDataPktCount = e.value
        elif e.index == 4:
            self.txCtrlPktCount = e.value
        elif e.index == 5:
            self.rxCtrlPktCount = e.value
        elif e.index == 6:
            self.csmaFailCount = e.value
        elif e.index == 7:
            self.csmaChBusyCount = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.txDataPktCount = reader.readElementContentAsLong("TxDataPktCount")
        self.rxDataPktCount = reader.readElementContentAsLong("RxDataPktCount")
        self.txCtrlPktCount = reader.readElementContentAsLong("TxCtrlPktCount")
        self.rxCtrlPktCount = reader.readElementContentAsLong("RxCtrlPktCount")
        self.csmaFailCount = reader.readElementContentAsLong("CsmaFailCount")
        self.csmaChBusyCount = reader.readElementContentAsLong("CsmaChBusyCount")

    def save(self, writer):
        writer.writeElementString("TxDataPktCount", self.txDataPktCount)
        writer.writeElementString("RxDataPktCount", self.rxDataPktCount)
        writer.writeElementString("TxCtrlPktCount", self.txCtrlPktCount)
        writer.writeElementString("RxCtrlPktCount", self.rxCtrlPktCount)
        writer.writeElementString("CsmaFailCount", self.csmaFailCount)
        writer.writeElementString("CsmaChBusyCount", self.csmaChBusyCount)

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
class GXDLMSPrimeNbOfdmPlcPhysicalLayerCounters(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSPrimeNbOfdmPlcPhysicalLayerCounters
    """

    def __init__(self, ln="0.0.28.1.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.PRIME_NB_OFDM_PLC_PHYSICAL_LAYER_COUNTERS, ln, sn)
        # Number of bursts received on the physical layer for which the CRC was incorrect.
        self.crcIncorrectCount = 0
        # Number of bursts received on the physical layer for which the CRC
        # was
        # correct, but the Protocol field of PHY header had invalid value.
        self.crcFailedCount = 0

        # Number of times when PHY layer received new data to transmit.
        self.txDropCount = 0
        # Number of times when the PHY layer received new data on the
        # channel.
        self.rxDropCount = 0

    def getValues(self):
        return [self.logicalName,
                self.crcIncorrectCount,
                self.crcFailedCount,
                self.txDropCount,
                self.rxDropCount]

    def reset(self, client):
        """Reset value."""
        return client.method(self.getName(), self.objectType, 1, 0, DataType.INT8)

    def invoke(self, settings, e):
        #  Resets the value to the default value.
        #  The default value is an instance specific constant.
        if e.index == 1:
            self.crcIncorrectCount = self.crcFailedCount = self.txDropCount = self.rxDropCount = 0
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
        #  CrcIncorrectCount
        if all_ or self.canRead(2):
            attributes.append(2)
        #  CrcFailedCount
        if all_ or self.canRead(3):
            attributes.append(3)
        #  TxDropCount
        if all_ or self.canRead(4):
            attributes.append(4)
        #  RxDropCount
        if all_ or self.canRead(5):
            attributes.append(5)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 5

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 1

    def getDataType(self, index):
        if index == 1:
            return DataType.OCTET_STRING
        if index in (2, 3, 4, 5):
            return DataType.UINT16
        raise ValueError("getDataType failed. Invalid attribute index.")

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            return _GXCommon.logicalNameToBytes(self.logicalName)
        if e.index == 2:
            return self.crcIncorrectCount
        if e.index == 3:
            return self.crcFailedCount
        if e.index == 4:
            return self.txDropCount
        if e.index == 5:
            return self.rxDropCount
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.crcIncorrectCount = e.value
        elif e.index == 3:
            self.crcFailedCount = e.value
        elif e.index == 4:
            self.txDropCount = e.value
        elif e.index == 5:
            self.rxDropCount = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.crcIncorrectCount = reader.readElementContentAsInt("CrcIncorrectCount")
        self.crcFailedCount = reader.readElementContentAsInt("CrcFailedCount")
        self.txDropCount = reader.readElementContentAsInt("TxDropCount")
        self.rxDropCount = reader.readElementContentAsInt("RxDropCount")

    def save(self, writer):
        writer.writeElementString("CrcIncorrectCount", self.crcIncorrectCount)
        writer.writeElementString("CrcFailedCount", self.crcFailedCount)
        writer.writeElementString("TxDropCount", self.txDropCount)
        writer.writeElementString("RxDropCount", self.rxDropCount)

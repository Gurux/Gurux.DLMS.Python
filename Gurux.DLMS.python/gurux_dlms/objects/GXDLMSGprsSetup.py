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
from .GXDLMSQualityOfService import GXDLMSQualityOfService

# pylint: disable=too-many-instance-attributes
class GXDLMSGprsSetup(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSGprsSetup
    """

    def __init__(self, ln="0.0.25.4.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.GPRS_SETUP, ln, sn)
        self.apn = ""
        self.pinCode = 0
        self.defaultQualityOfService = GXDLMSQualityOfService()
        self.requestedQualityOfService = GXDLMSQualityOfService()

    def getValues(self):
        return [self.logicalName,
                self.apn,
                self.pinCode,
                self.defaultQualityOfService,
                self.requestedQualityOfService]

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
        #  APN
        if all_ or not self.isRead(2):
            attributes.append(2)
        #  PINCode
        if all_ or not self.isRead(3):
            attributes.append(3)
        #  DefaultQualityOfService + RequestedQualityOfService
        if all_ or not self.isRead(4):
            attributes.append(4)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 4

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 0

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.OCTET_STRING
        elif index == 3:
            ret = DataType.UINT16
        elif index == 4:
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
            if not self.apn:
                ret = None
            else:
                ret = self.apn.encode()
        elif e.index == 3:
            ret = self.pinCode
        elif e.index == 4:
            data = GXByteBuffer()
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(2)
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(5)
            _GXCommon.setData(settings, data, DataType.UINT8, self.defaultQualityOfService.precedence)
            _GXCommon.setData(settings, data, DataType.UINT8, self.defaultQualityOfService.delay)
            _GXCommon.setData(settings, data, DataType.UINT8, self.defaultQualityOfService.reliability)
            _GXCommon.setData(settings, data, DataType.UINT8, self.defaultQualityOfService.peakThroughput)
            _GXCommon.setData(settings, data, DataType.UINT8, self.defaultQualityOfService.meanThroughput)
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(5)
            _GXCommon.setData(settings, data, DataType.UINT8, self.requestedQualityOfService.precedence)
            _GXCommon.setData(settings, data, DataType.UINT8, self.requestedQualityOfService.delay)
            _GXCommon.setData(settings, data, DataType.UINT8, self.requestedQualityOfService.reliability)
            _GXCommon.setData(settings, data, DataType.UINT8, self.requestedQualityOfService.peakThroughput)
            _GXCommon.setData(settings, data, DataType.UINT8, self.requestedQualityOfService.meanThroughput)
            ret = data.array()
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
                self.apn = e.value
            else:
                self.apn = _GXCommon.changeType(settings, e.value, DataType.STRING)
        elif e.index == 3:
            self.pinCode = e.value
        elif e.index == 4:
            arr = (e.value)[0]
            self.defaultQualityOfService.precedence = arr[0]
            self.defaultQualityOfService.delay = arr[1]
            self.defaultQualityOfService.reliability = arr[2]
            self.defaultQualityOfService.peakThroughput = arr[3]
            self.defaultQualityOfService.meanThroughput = arr[4]
            arr = (e.value)[1]
            self.requestedQualityOfService.precedence = arr[0]
            self.requestedQualityOfService.delay = arr[1]
            self.requestedQualityOfService.reliability = arr[2]
            self.requestedQualityOfService.peakThroughput = arr[3]
            self.requestedQualityOfService.meanThroughput = arr[4]
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.apn = reader.readElementContentAsString("APN")
        self.pinCode = reader.readElementContentAsInt("PINCode")
        if reader.isStartElement("DefaultQualityOfService", True):
            self.defaultQualityOfService.precedence = reader.readElementContentAsInt("Precedence")
            self.defaultQualityOfService.delay = reader.readElementContentAsInt("Delay")
            self.defaultQualityOfService.reliability = reader.readElementContentAsInt("Reliability")
            self.defaultQualityOfService.peakThroughput = reader.readElementContentAsInt("PeakThroughput")
            self.defaultQualityOfService.meanThroughput = reader.readElementContentAsInt("MeanThroughput")
            reader.readEndElement("DefaultQualityOfService")
        if reader.isStartElement("RequestedQualityOfService", True):
            self.requestedQualityOfService.precedence = reader.readElementContentAsInt("Precedence")
            self.requestedQualityOfService.delay = reader.readElementContentAsInt("Delay")
            self.requestedQualityOfService.reliability = reader.readElementContentAsInt("Reliability")
            self.requestedQualityOfService.peakThroughput = reader.readElementContentAsInt("PeakThroughput")
            self.requestedQualityOfService.meanThroughput = reader.readElementContentAsInt("MeanThroughput")
            reader.readEndElement("DefaultQualityOfService")

    def save(self, writer):
        writer.writeElementString("APN", self.apn)
        writer.writeElementString("PINCode", self.pinCode)
        if self.defaultQualityOfService:
            writer.writeStartElement("DefaultQualityOfService")
            writer.writeElementString("Precedence", self.defaultQualityOfService.precedence)
            writer.writeElementString("Delay", self.defaultQualityOfService.delay)
            writer.writeElementString("Reliability", self.defaultQualityOfService.reliability)
            writer.writeElementString("PeakThroughput", self.defaultQualityOfService.peakThroughput)
            writer.writeElementString("MeanThroughput", self.defaultQualityOfService.meanThroughput)
            writer.writeEndElement()
        if self.requestedQualityOfService:
            writer.writeStartElement("RequestedQualityOfService")
            writer.writeElementString("Precedence", self.requestedQualityOfService.precedence)
            writer.writeElementString("Delay", self.requestedQualityOfService.delay)
            writer.writeElementString("Reliability", self.requestedQualityOfService.reliability)
            writer.writeElementString("PeakThroughput", self.requestedQualityOfService.peakThroughput)
            writer.writeElementString("MeanThroughput", self.requestedQualityOfService.meanThroughput)
            writer.writeEndElement()

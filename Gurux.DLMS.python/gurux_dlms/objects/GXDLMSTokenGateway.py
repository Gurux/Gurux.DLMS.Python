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
from .enums import TokenDelivery, TokenStatusCode

# pylint: disable=too-many-instance-attributes
class GXDLMSTokenGateway(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSTokenGateway
    """

    def __init__(self, ln="0.0.19.40.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        super(GXDLMSTokenGateway, self).__init__(ObjectType.TOKEN_GATEWAY, ln, sn)
        # Descriptions.
        self.descriptions = list()
        # Token Delivery method.
        self.deliveryMethod = TokenDelivery.LOCAL
        # Token status code.
        self.statusCode = TokenStatusCode.FORMAT_OK
        # Token.
        self.token = list()
        # Time.
        self.time = None
        # Token data value.
        self.dataValue = None

    def getValues(self):
        return [self.logicalName,
                self.token,
                self.time,
                self.descriptions,
                self.deliveryMethod,
                [self.statusCode, self.dataValue]]

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
        #  Token
        if all_ or self.canRead(2):
            attributes.append(2)
        #  Time
        if all_ or self.canRead(3):
            attributes.append(3)
        #  Description
        if all_ or self.canRead(4):
            attributes.append(4)
        #  DeliveryMethod
        if all_ or self.canRead(5):
            attributes.append(5)
        #  Status
        if all_ or self.canRead(6):
            attributes.append(6)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):

        return 6

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):

        return 1

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.OCTET_STRING
        elif index == 3:
            ret = DataType.OCTET_STRING
        elif index == 4:
            ret = DataType.ARRAY
        elif index == 5:
            ret = DataType.ENUM
        elif index == 6:
            ret = DataType.STRUCTURE
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret
    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        #pylint: disable=bad-option-value,redefined-variable-type
        bb = None
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.token
        elif e.index == 3:
            ret = self.time
        elif e.index == 4:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.ARRAY)
            if not self.descriptions:
                bb.setUInt8(0)
            else:
                bb.setUInt8(len(self.descriptions))
                for it in self.descriptions:
                    bb.setUInt8(DataType.OCTET_STRING)
                    bb.setUInt8(int(len(it)))
                    bb.set(it)
            ret = bb
        elif e.index == 5:
            ret = self.deliveryMethod
        elif e.index == 6:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.STRUCTURE)
            bb.setUInt8(2)
            _GXCommon.setData(settings, bb, DataType.ENUM, self.statusCode)
            _GXCommon.setData(settings, bb, DataType.BITSTRING, self.dataValue)
            ret = bb
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
            self.token = e.value
        elif e.index == 3:
            self.time = _GXCommon.changeType(settings, e.value, DataType.DATETIME)
        elif e.index == 4:
            self.descriptions = []
            if e.value:
                for it in e.value:
                    self.descriptions.append(it)
        elif e.index == 5:
            self.deliveryMethod = e.value
        elif e.index == 6:
            self.statusCode = e.value[0]
            self.dataValue = str(e.value[1])
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.token = GXByteBuffer.hexToBytes(reader.readElementContentAsString("Token"))
        self.time = reader.readElementContentAsDateTime("Time")
        self.descriptions = []
        if reader.isStartElement("Descriptions", True):
            while reader.isStartElement("Item", True):
                self.descriptions.append(reader.readElementContentAsString("Name"))
            reader.readEndElement("Descriptions")
        self.deliveryMethod = reader.readElementContentAsInt("DeliveryMethod")
        self.statusCode = reader.readElementContentAsInt("Status")
        self.dataValue = reader.readElementContentAsString("Data")

    def save(self, writer):
        writer.writeElementString("Token", GXByteBuffer.hex(self.token, False))
        writer.writeElementString("Time", self.time)
        if self.descriptions:
            writer.writeStartElement("Descriptions")
            for it in self.descriptions:
                writer.writeStartElement("Item")
                writer.writeElementString("Name", it)
                writer.writeEndElement()
            writer.writeEndElement()
        writer.writeElementString("DeliveryMethod", int(self.deliveryMethod))
        writer.writeElementString("Status", int(self.statusCode))
        writer.writeElementString("Data", self.dataValue)

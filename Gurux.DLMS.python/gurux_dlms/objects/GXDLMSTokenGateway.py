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
from ..GXDateTime import GXDateTime
from ..enums import ObjectType, DataType
from .enums import TokenDelivery, TokenStatusCode

#
#  * Online help:
#  * http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSTokenGateway
#
# pylint: disable=too-many-instance-attributes
class GXDLMSTokenGateway(GXDLMSObject, IGXDLMSBase):

    #
    # Constructor.
    #
    # @param ln
    # Logical Name of the object.
    # @param sn
    # Short Name of the object.
    #
    def __init__(self, ln="0.0.19.40.0.255", sn=0):
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
        bb = None
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.token
        elif e.index == 3:
            ret = self.time
        elif e.index == 4:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.ARRAY.value)
            if not self.descriptions:
                bb.setUInt8(0)
            else:
                bb.setUInt8(len(self.descriptions))
                for it in self.descriptions:
                    bb.setUInt8(DataType.OCTET_STRING.value)
                    bb.setUInt8(int(len(it)))
                    bb.set(it.encode())
            ret = bb
        elif e.index == 5:
            ret = self.deliveryMethod.value
        elif e.index == 6:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.STRUCTURE.value)
            bb.setUInt8(2)
            _GXCommon.setData(bb, DataType.ENUM, self.statusCode.value)
            _GXCommon.setData(bb, DataType.BITSTRING, self.dataValue)
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
            self.time = _GXCommon.changeType(e.value, DataType.DATETIME)
        elif e.index == 4:
            self.descriptions.clear()
            if e.value:
                for it in e.value:
                    self.descriptions.append(it)
        elif e.index == 5:
            self.deliveryMethod = TokenDelivery(e.value)
        elif e.index == 6:
            self.statusCode = TokenStatusCode(e.value[0])
            self.dataValue = str(e.value[1])
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.token = GXByteBuffer.hexToBytes(reader.readElementContentAsString("Token"))
        tmp = reader.readElementContentAsString("Time")
        if tmp:
            self.time = GXDateTime(tmp)
        self.descriptions.clear()
        if reader.isStartElement("Descriptions", True):
            while reader.isStartElement("Item", True):
                self.descriptions.append(reader.readElementContentAsString("Name"))
            reader.readEndElement("Descriptions")
        self.deliveryMethod = TokenDelivery(reader.readElementContentAsInt("DeliveryMethod"))
        self.statusCode = TokenStatusCode(reader.readElementContentAsInt("Status"))
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
        writer.writeElementString("DeliveryMethod", self.deliveryMethod.value)
        writer.writeElementString("Status", self.statusCode.value)
        writer.writeElementString("Data", self.dataValue)

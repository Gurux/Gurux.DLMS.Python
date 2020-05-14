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
from .enums import ImageTransferStatus
from .GXDLMSImageActivateInfo import GXDLMSImageActivateInfo

# pylint: disable=too-many-instance-attributes
class GXDLMSImageTransfer(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSImageTransfer
    """

    def __init__(self, ln="0.0.44.0.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.IMAGE_TRANSFER, ln, sn)
        self.imageBlockSize = 200
        self.imageTransferredBlocksStatus = ""
        self.imageFirstNotTransferredBlockNumber = 0
        self.imageTransferEnabled = True
        self.imageActivateInfo = list()
        self.imageTransferStatus = ImageTransferStatus.IMAGE_TRANSFER_NOT_INITIATED
        self.imageSize = 0
        self.imageData = None

    def getValues(self):
        return [self.logicalName,
                self.imageBlockSize,
                self.imageTransferredBlocksStatus,
                self.imageFirstNotTransferredBlockNumber,
                self.imageTransferEnabled,
                self.imageTransferStatus,
                self.imageActivateInfo]

    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  ImageBlockSize
        if all_ or not self.isRead(2):
            attributes.append(2)
        #  ImageTransferredBlocksStatus
        if all_ or not self.isRead(3):
            attributes.append(3)
        #  ImageFirstNotTransferredBlockNumber
        if all_ or not self.isRead(4):
            attributes.append(4)
        #  ImageTransferEnabled
        if all_ or not self.isRead(5):
            attributes.append(5)
        #  ImageTransferStatus
        if all_ or not self.isRead(6):
            attributes.append(6)
        #  ImageActivateInfo
        if all_ or not self.isRead(7):
            attributes.append(7)
        return attributes

    def getAttributeCount(self):
        return 7

    def getMethodCount(self):
        return 4

    def invoke(self, settings, e):
        #  Image transfer initiate
        if e.index == 1:
            self.imageFirstNotTransferredBlockNumber = 0
            self.imageTransferredBlocksStatus = ""
            value = e.parameters
            imageIdentifier = value[0]
            self.imageSize = value[1]
            self.imageTransferStatus = ImageTransferStatus.IMAGE_TRANSFER_INITIATED
            list_ = list()
            list_.append(self.imageActivateInfo)
            item = None
            for it in self.imageActivateInfo:
                if it.identification == imageIdentifier:
                    item = it
                    break
            if item is None:
                item = GXDLMSImageActivateInfo()
                list_.append(item)
            item.size = self.imageSize
            item.identification = imageIdentifier
            self.imageActivateInfo = list_
            cnt = int((self.imageSize / self.imageBlockSize))
            if self.imageSize % self.imageBlockSize != 0:
                cnt += 1
            sb = ""
            pos = 0
            while pos < cnt:
                sb += '0'
                pos += 1
            self.imageTransferredBlocksStatus = sb
            return None
        if e.index == 2:
            #  Image block transfer
            value = e.parameters
            imageIndex = (value[0]).longValue()
            tmp = self.imageTransferredBlocksStatus.encode()
            tmp[int(imageIndex)] = '1'
            self.imageTransferredBlocksStatus = str(tmp)
            self.imageFirstNotTransferredBlockNumber = imageIndex + 1
            self.imageData.put(imageIndex, value[1])
            self.imageTransferStatus = ImageTransferStatus.IMAGE_TRANSFER_INITIATED
            return None
        if e.index == 3:
            #  Image verify.
            return None
        if e.index == 4:
            return None
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.UINT32
        elif index == 3:
            ret = DataType.BITSTRING
        elif index == 4:
            ret = DataType.UINT32
        elif index == 5:
            ret = DataType.BOOLEAN
        elif index == 6:
            ret = DataType.ENUM
        elif index == 7:
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
            ret = self.imageBlockSize
        elif e.index == 3:
            ret = self.imageTransferredBlocksStatus
        elif e.index == 4:
            ret = self.imageFirstNotTransferredBlockNumber
        elif e.index == 5:
            ret = self.imageTransferEnabled
        elif e.index == 6:
            ret = self.imageTransferStatus
        elif e.index == 7:
            data = GXByteBuffer()
            data.setUInt8(DataType.ARRAY)
            #  Count
            data.setUInt8(len(self.imageActivateInfo))
            for it in self.imageActivateInfo:
                data.setUInt8(DataType.STRUCTURE)
                #  Item count.
                data.setUInt8(int(3))
                _GXCommon.setData(settings, data, DataType.UINT32, it.size)
                _GXCommon.setData(settings, data, DataType.OCTET_STRING, it.identification)
                _GXCommon.setData(settings, data, DataType.OCTET_STRING, it.signature)
            ret = data
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
            if e.value is None:
                self.imageBlockSize = 0
            else:
                self.imageBlockSize = e.value
        elif e.index == 3:
            self.imageTransferredBlocksStatus = str(e.value)
        elif e.index == 4:
            if e.value is None:
                self.imageFirstNotTransferredBlockNumber = 0
            else:
                self.imageFirstNotTransferredBlockNumber = e.value
        elif e.index == 5:
            if e.value is None:
                self.imageTransferEnabled = False
            else:
                self.imageTransferEnabled = e.value
        elif e.index == 6:
            #pylint: disable=bad-option-value,redefined-variable-type
            if e.value is None:
                self.imageTransferStatus = ImageTransferStatus.IMAGE_TRANSFER_NOT_INITIATED
            else:
                self.imageTransferStatus = e.value
        elif e.index == 7:
            self.imageActivateInfo = []
            if e.value:
                for it in e.value:
                    item = GXDLMSImageActivateInfo()
                    item.size = it[0]
                    item.identification = it[1]
                    item.signature = it[2]
                    self.imageActivateInfo.append(item)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def imageTransferInitiate(self, client, imageIdentifier, forImageSize):
        if self.imageBlockSize == 0:
            raise ValueError("Invalid image block size.")
        if self.imageBlockSize > client.maxReceivePDUSize:
            raise ValueError("Image block size is bigger than max PDU size.")
        data = GXByteBuffer()
        data.setUInt8(DataType.STRUCTURE)
        data.setUInt8(2)
        _GXCommon.setData(None, data, DataType.OCTET_STRING, _GXCommon.getBytes(imageIdentifier))
        _GXCommon.setData(None, data, DataType.UINT32, forImageSize)
        return client.method(self, 1, data, DataType.ARRAY)

    def imageBlockTransfer(self, client, imageBlockValue, imageBlockCount):
        cnt = len(imageBlockValue)
        if (cnt % self.imageBlockSize) != 0:
            cnt += 1
        if imageBlockCount:
            imageBlockCount[0] = cnt
        packets = list()
        pos = 0
        while pos != cnt:
            data = GXByteBuffer()
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(2)
            _GXCommon.setData(None, data, DataType.UINT32, pos)
            tmp = None
            len_ = len(imageBlockValue) - ((pos + 1) * self.imageBlockSize)
            #  If last packet
            if len_ < 0:
                tmp = imageBlockValue[pos * self.imageBlockSize:]
            else:
                tmp = imageBlockValue[pos * self.imageBlockSize: pos * self.imageBlockSize + self.imageBlockSize]
            _GXCommon.setData(None, data, DataType.OCTET_STRING, tmp)
            packets.append(client.method(self, 2, data, DataType.ARRAY))
            pos += 1
        return packets

    def imageVerify(self, client):
        return client.method(self, 3, int(0), DataType.INT8)

    def imageActivate(self, client):
        return client.method(self, 4, int(0), DataType.INT8)

    def load(self, reader):
        self.imageBlockSize = reader.readElementContentAsInt("ImageBlockSize")
        self.imageTransferredBlocksStatus = reader.readElementContentAsString("ImageTransferredBlocksStatus")
        self.imageFirstNotTransferredBlockNumber = reader.readElementContentAsLong("ImageFirstNotTransferredBlockNumber")
        self.imageTransferEnabled = reader.readElementContentAsInt("ImageTransferEnabled") != 0
        self.imageTransferStatus = reader.readElementContentAsInt("ImageTransferStatus")
        self.imageActivateInfo = []
        if reader.isStartElement("ImageActivateInfo", True):
            while reader.isStartElement("Item", True):
                it = GXDLMSImageActivateInfo()
                it.size = reader.readElementContentAsULong("Size")
                it.identification = GXByteBuffer.hexToBytes(reader.readElementContentAsString("Identification"))
                it.signature = GXByteBuffer.hexToBytes(reader.readElementContentAsString("Signature"))
                self.imageActivateInfo.append(it)
            reader.readEndElement("ImageActivateInfo")

    def save(self, writer):
        writer.writeElementString("ImageBlockSize", self.imageBlockSize)
        writer.writeElementString("ImageTransferredBlocksStatus", self.imageTransferredBlocksStatus)
        writer.writeElementString("ImageFirstNotTransferredBlockNumber", self.imageFirstNotTransferredBlockNumber)
        writer.writeElementString("ImageTransferEnabled", self.imageTransferEnabled)
        writer.writeElementString("ImageTransferStatus", int(self.imageTransferStatus))
        writer.writeStartElement("ImageActivateInfo")
        if self.imageActivateInfo:
            for it in self.imageActivateInfo:
                writer.writeStartElement("Item")
                writer.writeElementString("Size", it.size)
                writer.writeElementString("Identification", GXByteBuffer.hex(it.identification, False))
                writer.writeElementString("Signature", GXByteBuffer.hex(it.signature, False))
                writer.writeEndElement()
        writer.writeEndElement()

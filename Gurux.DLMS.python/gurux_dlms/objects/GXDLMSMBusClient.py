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
from .enums import MBusEncryptionKeyStatus

# pylint: disable=too-many-instance-attributes
class GXDLMSMBusClient(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSMBusClient
    """

    def __init__(self, ln=None, sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        super(GXDLMSMBusClient, self).__init__(ObjectType.MBUS_CLIENT, ln, sn)
        self.captureDefinition = list()
        self.mBusPortReference = None
        self.capturePeriod = None
        self.primaryAddress = None
        self.identificationNumber = None
        self.manufacturerID = None
        self.dataHeaderVersion = None
        self.deviceType = None
        self.accessNumber = None
        self.status = None
        self.alarm = None
        self.configuration = 0
        self.encryptionKeyStatus = MBusEncryptionKeyStatus.NO_ENCRYPTION_KEY
        self.version = 1

    def getValues(self):
        if self.version == 0:
            return [self.logicalName,
                    self.mBusPortReference,
                    self.captureDefinition,
                    self.capturePeriod,
                    self.primaryAddress,
                    self.identificationNumber,
                    self.manufacturerID,
                    self.dataHeaderVersion,
                    self.deviceType,
                    self.accessNumber,
                    self.status,
                    self.alarm]
        return [self.logicalName,
                self.mBusPortReference,
                self.captureDefinition,
                self.capturePeriod,
                self.primaryAddress,
                self.identificationNumber,
                self.manufacturerID,
                self.dataHeaderVersion,
                self.deviceType,
                self.accessNumber,
                self.status,
                self.alarm,
                self.configuration,
                self.encryptionKeyStatus]

    # Returns collection of attributes to read.  If attribute is static
    #      and
    # already read or device is returned HW error it is not returned.
    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  MBusPortReference
        if all_ or self.canRead(2):
            attributes.append(2)
        #  CaptureDefinition
        if all_ or self.canRead(3):
            attributes.append(3)
        #  CapturePeriod
        if all_ or self.canRead(4):
            attributes.append(4)
        #  PrimaryAddress
        if all_ or self.canRead(5):
            attributes.append(5)
        #  IdentificationNumber
        if all_ or self.canRead(6):
            attributes.append(6)
        #  ManufacturerID
        if all_ or self.canRead(7):
            attributes.append(7)
        #  Version
        if all_ or self.canRead(8):
            attributes.append(8)
        #  DeviceType
        if all_ or self.canRead(9):
            attributes.append(9)
        #  AccessNumber
        if all_ or self.canRead(10):
            attributes.append(10)
        #  Status
        if all_ or self.canRead(11):
            attributes.append(11)
        #  Alarm
        if all_ or self.canRead(12):
            attributes.append(12)
        if self.version != 0:
            #  Alarm
            if all_ or self.canRead(13):
                attributes.append(13)
            #  Alarm
            if all_ or self.canRead(14):
                attributes.append(14)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        if self.version != 0:
            return 14
        return 12

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 8

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.OCTET_STRING
        elif index == 3:
            ret = DataType.ARRAY
        elif index == 4:
            ret = DataType.UINT32
        elif index == 5:
            ret = DataType.UINT8
        elif index == 6:
            ret = DataType.UINT32
        elif index == 7:
            ret = DataType.UINT16
        elif index == 8:
            ret = DataType.UINT8
        elif index == 9:
            ret = DataType.UINT8
        elif index == 10:
            ret = DataType.UINT8
        elif index == 11:
            ret = DataType.UINT8
        elif index == 12:
            ret = DataType.UINT8
        elif index == 13:
            ret = DataType.UINT16
        elif index == 14:
            ret = DataType.ENUM
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
            ret = _GXCommon.logicalNameToBytes(self.mBusPortReference)
        elif e.index == 3:
            buff = GXByteBuffer()
            buff.setUInt8(DataType.ARRAY)
            _GXCommon.setObjectCount(len(self.captureDefinition), buff)
            for k, v in self.captureDefinition:
                buff.setUInt8(DataType.STRUCTURE)
                buff.setUInt8(2)
                _GXCommon.setData(settings, buff, DataType.UINT8, k)
                if not v:
                    _GXCommon.setData(settings, buff, DataType.OCTET_STRING, None)
                else:
                    _GXCommon.setData(settings, buff, DataType.OCTET_STRING, v.encode())
            ret = buff
        elif e.index == 4:
            ret = self.capturePeriod
        elif e.index == 5:
            ret = self.primaryAddress
        elif e.index == 6:
            ret = self.identificationNumber
        elif e.index == 7:
            ret = self.manufacturerID
        elif e.index == 8:
            ret = self.dataHeaderVersion
        elif e.index == 9:
            ret = self.deviceType
        elif e.index == 10:
            ret = self.accessNumber
        elif e.index == 11:
            ret = self.status
        elif e.index == 12:
            ret = self.alarm
        elif e.index == 13:
            ret = self.configuration
        elif e.index == 14:
            ret = self.encryptionKeyStatus
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
            self.mBusPortReference = _GXCommon.toLogicalName(e.value)
        elif e.index == 3:
            self.captureDefinition = []
            if e.value:
                for it in e.value:
                    self.captureDefinition.append((_GXCommon.changeType(settings, it[0], DataType.OCTET_STRING), _GXCommon.changeType(settings, it[1], DataType.OCTET_STRING)))
        elif e.index == 4:
            self.capturePeriod = e.value
        elif e.index == 5:
            self.primaryAddress = e.value
        elif e.index == 6:
            self.identificationNumber = e.value
        elif e.index == 7:
            self.manufacturerID = e.value
        elif e.index == 8:
            self.dataHeaderVersion = e.value
        elif e.index == 9:
            self.deviceType = e.value
        elif e.index == 10:
            self.accessNumber = e.value
        elif e.index == 11:
            self.status = e.value
        elif e.index == 12:
            self.alarm = e.value
        elif e.index == 13:
            self.configuration = e.value
        elif e.index == 14:
            self.encryptionKeyStatus = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.mBusPortReference = reader.readElementContentAsString("MBusPortReference")
        self.captureDefinition = []
        if reader.isStartElement("CaptureDefinition", True):
            while reader.isStartElement("Item", True):
                d = reader.readElementContentAsString("Data")
                v = reader.readElementContentAsString("Value")
                self.captureDefinition.append((d, v))
            reader.readEndElement("CaptureDefinition")
        self.capturePeriod = reader.readElementContentAsInt("CapturePeriod")
        self.primaryAddress = reader.readElementContentAsInt("PrimaryAddress")
        self.identificationNumber = reader.readElementContentAsInt("IdentificationNumber")
        self.manufacturerID = reader.readElementContentAsInt("ManufacturerID")
        self.dataHeaderVersion = reader.readElementContentAsInt("DataHeaderVersion")
        self.deviceType = reader.readElementContentAsInt("DeviceType")
        self.accessNumber = reader.readElementContentAsInt("AccessNumber")
        self.status = reader.readElementContentAsInt("Status")
        self.alarm = reader.readElementContentAsInt("Alarm")
        if self.version != 0:
            self.configuration = reader.readElementContentAsInt("Configuration")
            self.encryptionKeyStatus = MBusEncryptionKeyStatus(reader.readElementContentAsInt("EncryptionKeyStatus"))

    def save(self, writer):
        writer.writeElementString("MBusPortReference", self.mBusPortReference)
        writer.writeStartElement("CaptureDefinition")
        if self.captureDefinition:
            for k, v in self.captureDefinition:
                writer.writeStartElement("Item")
                writer.writeElementString("Data", k)
                writer.writeElementString("Value", v)
                writer.writeEndElement()
        writer.writeEndElement()
        writer.writeElementString("CapturePeriod", self.capturePeriod)
        writer.writeElementString("PrimaryAddress", self.primaryAddress)
        writer.writeElementString("IdentificationNumber", self.identificationNumber)
        writer.writeElementString("ManufacturerID", self.manufacturerID)
        writer.writeElementString("DataHeaderVersion", self.dataHeaderVersion)
        writer.writeElementString("DeviceType", self.deviceType)
        writer.writeElementString("AccessNumber", self.accessNumber)
        writer.writeElementString("Status", self.status)
        writer.writeElementString("Alarm", self.alarm)
        if self.version != 0:
            writer.writeElementString("Configuration", self.configuration)
            writer.writeElementString("EncryptionKeyStatus", self.encryptionKeyStatus)

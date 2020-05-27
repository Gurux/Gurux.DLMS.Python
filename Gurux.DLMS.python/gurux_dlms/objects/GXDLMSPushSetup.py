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
from .enums import ServiceType, MessageType
from .GXDLMSCaptureObject import GXDLMSCaptureObject

# pylint: disable=too-many-instance-attributes
class GXDLMSPushSetup(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSPushSetup
    """

    def __init__(self, ln="0.7.25.9.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        super(GXDLMSPushSetup, self).__init__(ObjectType.PUSH_SETUP, ln, sn)
        self.pushObjectList = list()
        self.communicationWindow = list()
        self.service = ServiceType.TCP
        self.message = MessageType.COSEM_APDU
        self.destination = None
        self.randomisationStartInterval = 0
        self.numberOfRetries = 0
        self.repetitionDelay = 0

    def getValues(self):
        return [self.logicalName,
                self.pushObjectList,
                (self.service, self.destination, self.message),
                self.communicationWindow,
                self.randomisationStartInterval,
                self.numberOfRetries,
                self.repetitionDelay]

    def invoke(self, settings, e):
        if e.index != 1:
            e.error = ErrorCode.READ_WRITE_DENIED

    #
    # Activates the push process.
    #
    def activate(self, client):
        return client.method(self.getName(), self.objectType, 1, 0, DataType.INT8)

    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  PushObjectList
        if all_ or self.canRead(2):
            attributes.append(2)
        #  SendDestinationAndMethod
        if all_ or self.canRead(3):
            attributes.append(3)
        #  CommunicationWindow
        if all_ or self.canRead(4):
            attributes.append(4)
        #  RandomisationStartInterval
        if all_ or self.canRead(5):
            attributes.append(5)
        #  NumberOfRetries
        if all_ or self.canRead(6):
            attributes.append(6)
        #  RepetitionDelay
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
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.ARRAY
        elif index == 3:
            ret = DataType.STRUCTURE
        elif index == 4:
            ret = DataType.ARRAY
        elif index == 5:
            ret = DataType.UINT16
        elif index == 6:
            ret = DataType.UINT8
        elif index == 7:
            ret = DataType.UINT16
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret
    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        #pylint: disable=bad-option-value,redefined-variable-type
        buff = GXByteBuffer()
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            buff.setUInt8(DataType.ARRAY)
            _GXCommon.setObjectCount(len(self.pushObjectList), buff)
            for k, v in self.pushObjectList:
                buff.setUInt8(DataType.STRUCTURE)
                buff.setUInt8(4)
                _GXCommon.setData(settings, buff, DataType.UINT16, k.objectType)
                _GXCommon.setData(settings, buff, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(k.logicalName))
                _GXCommon.setData(settings, buff, DataType.INT8, v.attributeIndex)
                _GXCommon.setData(settings, buff, DataType.UINT16, v.dataIndex)
            ret = buff
        elif e.index == 3:
            buff.setUInt8(DataType.STRUCTURE)
            buff.setUInt8(3)
            _GXCommon.setData(settings, buff, DataType.ENUM, self.service)
            if self.destination:
                _GXCommon.setData(settings, buff, DataType.OCTET_STRING, self.destination.encode())
            else:
                _GXCommon.setData(settings, buff, DataType.OCTET_STRING, None)
            _GXCommon.setData(settings, buff, DataType.ENUM, self.message)
            ret = buff
        elif e.index == 4:
            buff.setUInt8(DataType.ARRAY)
            _GXCommon.setObjectCount(len(self.communicationWindow), buff)
            for k, v in self.communicationWindow:
                buff.setUInt8(DataType.STRUCTURE)
                buff.setUInt8(2)
                _GXCommon.setData(settings, buff, DataType.OCTET_STRING, k)
                _GXCommon.setData(settings, buff, DataType.OCTET_STRING, v)
            return buff
        elif e.index == 5:
            ret = self.randomisationStartInterval
        elif e.index == 6:
            ret = self.numberOfRetries
        elif e.index == 7:
            ret = self.repetitionDelay
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.pushObjectList = []
            #pylint: disable=import-outside-toplevel
            from .._GXObjectFactory import _GXObjectFactory
            if e.value:
                for it in e.value:
                    type_ = it[0]
                    ln = _GXCommon.toLogicalName(it[1])
                    obj = settings.objects.findByLN(type_, ln)
                    if not obj:
                        obj = _GXObjectFactory.createObject(type_)
                        obj.logicalName = ln
                    co = GXDLMSCaptureObject()
                    co.attributeIndex = it[2]
                    co.dataIndex = it[3]
                    self.pushObjectList.append((obj, co))
        elif e.index == 3:
            #pylint: disable=broad-except
            if e.value:
                self.service = ServiceType(e.value[0])
                try:
                    if self.service == ServiceType.HDLC:
                        self.destination = _GXCommon.toLogicalName(e.value[1])
                    else:
                        self.destination = e.value[1].decode()
                except Exception:
                    self.destination = GXByteBuffer.toHex(e.value[1])
                self.message = e.value[2]
        elif e.index == 4:
            self.communicationWindow = []
            if e.value:
                for it in e.value:
                    start = _GXCommon.changeType(settings, it[0], DataType.DATETIME)
                    end = _GXCommon.changeType(settings, it[1], DataType.DATETIME)
                    self.communicationWindow.append((start, end))
        elif e.index == 5:
            self.randomisationStartInterval = e.value
        elif e.index == 6:
            self.numberOfRetries = e.value
        elif e.index == 7:
            self.repetitionDelay = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.pushObjectList = []
        if reader.isStartElement("ObjectList", True):
            while reader.isStartElement("Item", True):
                ot = ObjectType(reader.readElementContentAsInt("ObjectType"))
                ln = reader.readElementContentAsString("LN")
                ai = reader.readElementContentAsInt("AI")
                di = reader.readElementContentAsInt("DI")
                reader.readEndElement("ObjectList")
                co = GXDLMSCaptureObject(ai, di)
                obj = reader.objects.findByLN(ot, ln)
                self.pushObjectList.append((obj, co))
            reader.readEndElement("ObjectList")
        self.service = ServiceType(reader.readElementContentAsInt("Service"))
        self.destination = reader.readElementContentAsString("Destination")
        self.message = MessageType(reader.readElementContentAsInt("Message"))
        self.communicationWindow = []
        if reader.isStartElement("CommunicationWindow", True):
            while reader.isStartElement("Item", True):
                start = reader.readElementContentAsDateTime("Start")
                end = reader.readElementContentAsDateTime("End")
                self.communicationWindow.append((start, end))
            reader.readEndElement("CommunicationWindow")
        self.randomisationStartInterval = reader.readElementContentAsInt("RandomisationStartInterval")
        self.numberOfRetries = reader.readElementContentAsInt("NumberOfRetries")
        self.repetitionDelay = reader.readElementContentAsInt("RepetitionDelay")

    def save(self, writer):
        if self.pushObjectList:
            writer.writeStartElement("ObjectList")
            for k, v in self.pushObjectList:
                writer.writeStartElement("Item")
                writer.writeElementString("ObjectType", int(k.objectType))
                writer.writeElementString("LN", k.logicalName)
                writer.writeElementString("AI", v.attributeIndex)
                writer.writeElementString("DI", v.dataIndex)
                writer.writeEndElement()
            writer.writeEndElement()
        writer.writeElementString("Service", int(self.service))
        writer.writeElementString("Destination", self.destination)
        writer.writeElementString("Message", int(self.message))
        writer.writeStartElement("CommunicationWindow")
        if self.communicationWindow:
            for k, v in self.communicationWindow:
                writer.writeStartElement("Item")
                writer.writeElementString("Start", k)
                writer.writeElementString("End", v)
                writer.writeEndElement()
        writer.writeEndElement()
        writer.writeElementString("RandomisationStartInterval", self.randomisationStartInterval)
        writer.writeElementString("NumberOfRetries", self.numberOfRetries)
        writer.writeElementString("RepetitionDelay", self.repetitionDelay)

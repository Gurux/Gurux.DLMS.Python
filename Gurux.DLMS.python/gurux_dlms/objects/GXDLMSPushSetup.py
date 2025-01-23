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
#  Gurux Device Framework is Open Source software you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
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
from .GXRepetitionDelay import GXRepetitionDelay
from .GXPushConfirmationParameter import GXPushConfirmationParameter
from .GXPushProtectionParameters import GXPushProtectionParameters

from .enums.PushOperationMethod import PushOperationMethod
from .enums.DataProtectionKeyType import DataProtectionKeyType
from .enums.RestrictionType import RestrictionType
from .enums.ProtectionType import ProtectionType
from .enums.DataProtectionIdentifiedKeyType import DataProtectionIdentifiedKeyType
from .enums.DataProtectionWrappedKeyType import DataProtectionWrappedKeyType


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
        # pylint: disable=super-with-arguments
        super(GXDLMSPushSetup, self).__init__(ObjectType.PUSH_SETUP, ln, sn)
        self.version = 2
        self.pushObjectList = []
        self.communicationWindow = []
        self.repetitionDelay2 = GXRepetitionDelay()
        self.confirmationParameters = GXPushConfirmationParameter()
        self.service = ServiceType.TCP
        self.message = MessageType.COSEM_APDU
        self.destination = None
        self.randomisationStartInterval = 0
        self.numberOfRetries = 0
        self.repetitionDelay = 0
        self.portReference = None
        self.pushClientSAP = 0
        self.pushProtectionParameters = []
        self.pushOperationMethod = PushOperationMethod.UNCONFIRMED_FAILURE
        self.confirmationParameters = GXPushConfirmationParameter()
        self.lastConfirmationDateTime = None

    def getValues(self):
        if self.version == 0:
            return [
                self.logicalName,
                self.pushObjectList,
                (self.service, self.destination, self.message),
                self.communicationWindow,
                self.randomisationStartInterval,
                self.numberOfRetries,
                self.repetitionDelay,
            ]
        if self.version == 0:
            return [
                self.logicalName,
                self.pushObjectList,
                (self.service, self.destination, self.message),
                self.communicationWindow,
                self.randomisationStartInterval,
                self.numberOfRetries,
                self.repetitionDelay,
                self.portReference,
                self.pushClientSAP,
                self.pushProtectionParameters,
                self.pushOperationMethod,
                self.confirmationParameters,
                self.lastConfirmationDateTime,
            ]
        return [
            self.logicalName,
            self.pushObjectList,
            (self.service, self.destination, self.message),
            self.communicationWindow,
            self.randomisationStartInterval,
            self.numberOfRetries,
            self.repetitionDelay2,
            self.portReference,
            self.pushClientSAP,
            self.pushProtectionParameters,
            self.pushOperationMethod,
            self.confirmationParameters,
            self.lastConfirmationDateTime,
        ]

    def getPushValues(self, client, values):
        """
        Get received objects from push message.

        values: Received values.
        Returns clone of captured COSEM objects.
        """
        if len(values) != len(self.pushObjectList):
            raise ValueError("Size of the push object list is different than values.")
        pos = 0
        objects = []
        for k, v in self.pushObjectList:
            co = GXDLMSCaptureObject(v.attributeIndex, v.dataIndex)
            objects.append((k, co))
            if v.attributeIndex == 0:
                tmp = values[pos]
                index = 1
                while index <= k.getAttributeCount():
                    client.updateValue(k, index, tmp[index - 1])
                    index = 1 + index
            else:
                client.updateValue(k, v.attributeIndex, values[pos])
            pos = 1 + pos

    def invoke(self, settings, e):
        if e.index != 1:
            e.error = ErrorCode.READ_WRITE_DENIED

    #
    # Activates the push process.
    #
    def activate(self, client):
        return client.method(self, 1, 0, DataType.INT8)

    #
    # Reset the push process.
    #
    def reset(self, client):
        return client.method(self, 2, 0, DataType.INT8)

    def getAttributeIndexToRead(self, all_):
        attributes = []
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
        # RepetitionDelay
        if all_ or self.canRead(7):
            attributes.append(7)
        if self.version > 0:
            # PortReference
            if all_ or self.canRead(8):
                attributes.append(8)
            # PushClientSAP
            if all_ or self.canRead(9):
                attributes.append(9)
            # PushProtectionParameters
            if all_ or self.canRead(10):
                attributes.append(10)
            if self.version > 0:
                # PushOperationMethod
                if all_ or self.canRead(11):
                    attributes.append(11)
                # ConfirmationParameters
                if all_ or self.canRead(12):
                    attributes.append(12)
                # LastConfirmationDateTime
                if all_ or self.canRead(13):
                    attributes.append(13)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        if self.version == 0:
            return 7
        if self.version == 1:
            return 10
        return 13

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        if self.version < 2:
            return 1
        return 2

    def getDataType(self, index):
        ret = None
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
            if self.version < 2:
                ret = DataType.UINT16
            else:
                ret = DataType.STRUCTURE
        elif self.version > 0:
            # PortReference
            if index == 8:
                ret = DataType.OCTET_STRING
            # PushClientSAP
            elif index == 9:
                ret = DataType.INT8
            # PushProtectionParameters
            elif index == 10:
                return DataType.ARRAY
            elif self.version > 1:
                # PushOperationMethod
                if index == 11:
                    ret = DataType.ENUM
                # ConfirmationParameters
                if index == 12:
                    ret = DataType.STRUCTURE
                # LastConfirmationDateTime
                if index == 13:
                    ret = DataType.DATETIME
        if ret == None:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret

    def __getPushObjectList(self, settings):
        buff = GXByteBuffer()
        buff.setUInt8(DataType.ARRAY)
        _GXCommon.setObjectCount(len(self.pushObjectList), buff)
        for k, v in self.pushObjectList:
            buff.setUInt8(DataType.STRUCTURE)
            if self.version < 1:
                buff.setUInt8(4)
                _GXCommon.setData(None, buff, DataType.UINT16, k.objectType)
                _GXCommon.setData(
                    None,
                    buff,
                    DataType.OCTET_STRING,
                    _GXCommon.logicalNameToBytes(k.logicalName),
                )
                _GXCommon.setData(settings, buff, DataType.INT8, v.attributeIndex)
                _GXCommon.setData(settings, buff, DataType.UINT16, v.dataIndex)
            else:
                buff.setUInt8(5 if self.version == 1 else 6)
                _GXCommon.setData(settings, buff, DataType.UINT16, k.objectType)
                _GXCommon.setData(
                    settings,
                    buff,
                    DataType.OCTET_STRING,
                    _GXCommon.logicalNameToBytes(k.logicalName),
                )
                _GXCommon.setData(settings, buff, DataType.INT8, v.attributeIndex)
                _GXCommon.setData(settings, buff, DataType.UINT16, v.dataIndex)
                # restriction_element
                buff.setUInt8(DataType.STRUCTURE)
                buff.setUInt8(2)
                _GXCommon.setData(settings, buff, DataType.ENUM, v.restriction.type)
                if v.restriction.type == RestrictionType.NONE:
                    _GXCommon.setData(settings, buff, DataType.NONE, None)
                elif v.restriction.type == RestrictionType.DATE:
                    buff.setUInt8(DataType.STRUCTURE)
                    buff.setUInt8(2)
                    _GXCommon.setData(
                        settings, buff, DataType.OCTET_STRING, v.restriction.from_
                    )
                    _GXCommon.setData(
                        settings, buff, DataType.OCTET_STRING, v.restriction.to
                    )
                elif v.restriction.type == RestrictionType.ENTRY:
                    buff.setUInt8(DataType.STRUCTURE)
                    buff.setUInt8(2)
                    _GXCommon.setData(
                        settings, buff, DataType.UINT16, v.restriction.from_
                    )
                    _GXCommon.setData(settings, buff, DataType.UINT16, v.restriction.to)
                if self.version > 1:
                    if v.columns:
                        buff.setUInt8(DataType.ARRAY)
                        _GXCommon.setObjectCount(len(v.columns), buff)
                        for k2, v2 in v.columns:
                            buff.setUInt8(DataType.STRUCTURE)
                            buff.setUInt8(4)
                            _GXCommon.setData(
                                settings, buff, DataType.UINT16, k2.objectType
                            )
                            _GXCommon.setData(
                                settings,
                                buff,
                                DataType.OCTET_STRING,
                                _GXCommon.logicalNameToBytes(k2.logicalName),
                            )
                            _GXCommon.setData(
                                settings, buff, DataType.INT8, v2.attributeIndex
                            )
                            _GXCommon.setData(
                                settings, buff, DataType.UINT16, v2.dataIndex
                            )
                    else:
                        buff.setUInt8(DataType.ARRAY)
                        buff.setUInt8(0)

        return buff

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        # pylint: disable=bad-option-value,redefined-variable-type
        buff = GXByteBuffer()
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.__getPushObjectList(settings)
        elif e.index == 3:
            buff.setUInt8(DataType.STRUCTURE)
            buff.setUInt8(3)
            _GXCommon.setData(settings, buff, DataType.ENUM, self.service)
            if self.destination:
                _GXCommon.setData(
                    settings, buff, DataType.OCTET_STRING, self.destination.encode()
                )
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
            if self.version < 2:
                ret = self.repetitionDelay
            else:
                buff.setUInt8(DataType.STRUCTURE)
                _GXCommon.setObjectCount(3, buff)
                _GXCommon.setData(
                    None, buff, DataType.UINT16, self.repetitionDelay2.min
                )
                _GXCommon.setData(
                    None, buff, DataType.UINT16, self.repetitionDelay2.exponent
                )
                _GXCommon.setData(
                    None, buff, DataType.UINT16, self.repetitionDelay2.max
                )
                ret = buff.array()
        elif e.index == 8:
            if self.portReference:
                ret = _GXCommon.logicalNameToBytes(self.portReference.LogicalName)
            else:
                ret = None
        elif e.index == 9:
            ret = self.pushClientSAP
        elif e.index == 10:
            buff.setUInt8(DataType.ARRAY)
            _GXCommon.setObjectCount(len(self.pushProtectionParameters), buff)
            for it in self.pushProtectionParameters:
                buff.setUInt8(DataType.STRUCTURE)
                buff.setUInt8(2)
                _GXCommon.setData(None, buff, DataType.ENUM, it.protectionType)
                buff.setUInt8(DataType.STRUCTURE)
                buff.setUInt8(5)
                _GXCommon.setData(
                    settings, buff, DataType.OCTET_STRING, it.transactionId
                )
                _GXCommon.setData(
                    settings, buff, DataType.OCTET_STRING, it.originatorSystemTitle
                )
                _GXCommon.setData(
                    settings, buff, DataType.OCTET_STRING, it.recipientSystemTitle
                )
                _GXCommon.setData(
                    settings, buff, DataType.OCTET_STRING, it.otherInformation
                )
                buff.setUInt8(DataType.STRUCTURE)
                buff.setUInt8(2)
                _GXCommon.setData(
                    settings, buff, DataType.ENUM, it.keyInfo.dataProtectionKeyType
                )
                buff.setUInt8(DataType.STRUCTURE)
                if it.keyInfo.dataProtectionKeyType == DataProtectionKeyType.IDENTIFIED:
                    buff.setUInt8(1)
                    _GXCommon.setData(
                        settings, buff, DataType.ENUM, it.keyInfo.identifiedKey.keyType
                    )
                elif it.keyInfo.dataProtectionKeyType == DataProtectionKeyType.WRAPPED:
                    buff.setUInt8(2)
                    _GXCommon.setData(
                        settings, buff, DataType.Enum, it.keyInfo.wrappedKey.keyType
                    )
                    _GXCommon.setData(
                        settings, buff, DataType.OCTET_STRING, it.keyInfo.wrappedKey.key
                    )
                elif it.keyInfo.dataProtectionKeyType == DataProtectionKeyType.AGREED:
                    buff.setUInt8(2)
                    _GXCommon.setData(
                        settings,
                        buff,
                        DataType.OCTET_STRING,
                        it.keyInfo.agreedKey.parameters,
                    )
                    _GXCommon.setData(
                        settings, buff, DataType.OCTET_STRING, it.keyInfo.agreedKey.data
                    )
            ret = buff
        elif e.index == 11:
            ret = self.pushOperationMethod
        elif e.index == 12:
            buff.setUInt8(DataType.STRUCTURE)
            _GXCommon.setObjectCount(2, buff)
            _GXCommon.setData(
                settings, buff, DataType.DATETIME, self.confirmationParameters.startDate
            )
            _GXCommon.setData(
                settings, buff, DataType.UINT32, self.confirmationParameters.interval
            )
            ret = buff.array()
        elif e.index == 13:
            ret = self.lastConfirmationDateTime
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    def __setPushObject(self, settings, e):
        # pylint: disable=import-outside-toplevel
        from .._GXObjectFactory import _GXObjectFactory

        self.pushObjectList = []
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
            if self.version > 1:
                restriction = it[4]
                co.restriction.type = RestrictionType(restriction[0])
                if co.restriction.type == RestrictionType.NONE:
                    pass
                elif (
                    co.restriction.type == RestrictionType.DATE
                    or co.restriction.type == RestrictionType.ENTRY
                ):
                    co.Restriction.From = restriction[1]
                    co.Restriction.To = restriction[2]
                else:
                    raise ValueError("Invalid restriction type.")
                for c in it[5]:
                    tp = ObjectType(c[0])
                    ln = _GXCommon.toLogicalName(c[1])
                    obj = settings.objects.findByLN(tp, ln)
                    if obj is None:
                        obj = _GXObjectFactory.CreateObject(tp)
                        obj.logicalName = ln
                    co.columns.append((obj, co))

    def __getPushProtectionParameters(self, e):
        self.pushProtectionParameters.clear()
        if e.value:
            for it in e.value:
                p = GXPushProtectionParameters()
                p.protectionType = ProtectionType(int(it[0]))
                options = it[1]
                p.transactionId = options[0]
                p.originatorSystemTitle = options[1]
                p.recipientSystemTitle = options[2]
                p.otherInformation = options[3]
                keyInfo = options[4]
                p.keyInfo.dataProtectionKeyType = DataProtectionKeyType(int(keyInfo[0]))
                data = keyInfo[1]
                if p.keyInfo.dataProtectionKeyType == DataProtectionKeyType.IDENTIFIED:
                    p.keyInfo.identifiedKey.keyType = DataProtectionIdentifiedKeyType(
                        int(data[0])
                    )
                elif p.keyInfo.dataProtectionKeyType == DataProtectionKeyType.WRAPPED:
                    p.keyInfo.wrappedKey.keyType = DataProtectionWrappedKeyType(
                        int(data[0])
                    )
                    p.keyInfo.wrappedKey.key = data[1]
                elif p.keyInfo.dataProtectionKeyType == DataProtectionKeyType.AGREED:
                    p.keyInfo.agreedKey.parameters = data[0]
                    p.keyInfo.agreedKey.data = data[1]
                self.pushProtectionParameters.append(p)

    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.__setPushObject(settings, e)
        elif e.index == 3:
            # pylint: disable=broad-except
            if e.value:
                self.service = ServiceType(e.value[0])
                try:
                    if self.service == ServiceType.HDLC:
                        self.destination = _GXCommon.toLogicalName(e.value[1])
                    else:
                        # If destination is not ASCII string.
                        if e.value[1] and not GXByteBuffer.isAsciiString(e.value[1]):
                            self.destination = GXByteBuffer.toHex(self.destination)
                        else:
                            self.destination = e.value[1].decode()
                except Exception:
                    self.destination = GXByteBuffer.hex(e.value[1])
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
            if self.version < 2:
                self.repetitionDelay = e.value
            else:
                if e.value:
                    self.repetitionDelay2.min = e.value[0]
                    self.repetitionDelay2.exponent = e.value[1]
                    self.repetitionDelay2.max = e.value[2]
        elif self.version > 0 and e.index == 8:
            self.portReference = None
            if e.value:
                ln = _GXCommon.toLogicalName(e.value)
                self.portReference = settings.objects.findByLN(ObjectType.NONE, ln)
        elif self.version > 0 and e.index == 9:
            self.pushClientSAP = e.value
        elif self.version > 0 and e.index == 10:
            self.__getPushProtectionParameters(e)
        elif self.version > 0 and e.index == 11:
            self.pushOperationMethod = PushOperationMethod(e.value)
        elif self.version > 0 and e.index == 12:
            if e.value:
                self.confirmationParameters.startDate = e.value[0]
                self.confirmationParameters.interval = e.value[1]
            else:
                e.Error = ErrorCode.ReadWriteDenied
        elif self.version > 0 and e.index == 13:
            LastConfirmationDateTime = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        from .._GXObjectFactory import _GXObjectFactory

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
                if not obj:
                    obj = _GXObjectFactory.createObject(ot)
                    obj.LogicalName = ln
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
        self.randomisationStartInterval = reader.readElementContentAsInt(
            "RandomisationStartInterval"
        )
        self.numberOfRetries = reader.readElementContentAsInt("NumberOfRetries")
        if self.version < 2:
            self.repetitionDelay = reader.readElementContentAsInt("RepetitionDelay")
        else:
            if reader.isStartElement("RepetitionDelay", True):
                self.repetitionDelay2.min = reader.readElementContentAsInt("Min")
                self.repetitionDelay2.exponent = reader.readElementContentAsInt(
                    "Exponent"
                )
                self.repetitionDelay2.max = reader.readElementContentAsInt("Max")
            reader.readEndElement("RepetitionDelay")
        if self.version > 0:
            ln = reader.readElementContentAsString("PortReference")
            self.portReference = reader.objects.findByLN(ObjectType.NONE, ln)
            if self.portReference is None:
                self.portReference = _GXObjectFactory.createObject(
                    ObjectType.IEC_HDLC_SETUP
                )
                self.portReference.logicalName = ln
            self.pushClientSAP = reader.readElementContentAsInt("PushClientSAP")
            if reader.isStartElement("PushProtectionParameters", True):
                self.pushProtectionParameters.clear()
                while reader.isStartElement("Item", True):
                    it = GXPushProtectionParameters()
                    it.protectionType = ProtectionType(
                        reader.readElementContentAsInt("ProtectionType")
                    )
                    it.transactionId = _GXCommon.HexToBytes(
                        reader.readElementContentAsString("TransactionId")
                    )
                    it.originatorSystemTitle = _GXCommon.HexToBytes(
                        reader.readElementContentAsString("OriginatorSystemTitle")
                    )
                    it.recipientSystemTitle = _GXCommon.HexToBytes(
                        reader.readElementContentAsString("RecipientSystemTitle")
                    )
                    it.otherInformation = _GXCommon.HexToBytes(
                        reader.readElementContentAsString("OtherInformation")
                    )
                    it.keyInfo.dataProtectionKeyType = DataProtectionKeyType(
                        reader.readElementContentAsInt("DataProtectionKeyType")
                    )
                    it.keyInfo.identifiedKey.keyType = DataProtectionIdentifiedKeyType(
                        reader.readElementContentAsInt("IdentifiedKey")
                    )
                    it.keyInfo.wrappedKey.keyType = DataProtectionWrappedKeyType(
                        reader.readElementContentAsInt("WrappedKeyType")
                    )
                    it.keyInfo.wrappedKey.key = _GXCommon.HexToBytes(
                        reader.readElementContentAsString("WrappedKey")
                    )
                    it.keyInfo.agreedKey.parameters = _GXCommon.HexToBytes(
                        reader.readElementContentAsString("WrappedKeyParameters")
                    )
                    it.keyInfo.agreedKey.data = _GXCommon.HexToBytes(
                        reader.readElementContentAsString("AgreedKeyData")
                    )
                    self.pushProtectionParameters.append(it)
                reader.readEndElement("PushProtectionParameters")
            if self.version > 1:
                self.pushOperationMethod = PushOperationMethod(
                    reader.readElementContentAsInt("PushOperationMethod")
                )
                self.confirmationParameters.startDate = (
                    reader.readElementContentAsDateTime(
                        "ConfirmationParametersStartDate"
                    )
                )
                self.confirmationParameters.interval = reader.readElementContentAsInt(
                    "ConfirmationParametersInterval"
                )
                self.lastConfirmationDateTime = reader.readElementContentAsDateTime(
                    "LastConfirmationDateTime"
                )

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
        writer.writeElementString(
            "RandomisationStartInterval", self.randomisationStartInterval
        )
        writer.writeElementString("NumberOfRetries", self.numberOfRetries)
        if self.version < 2:
            writer.writeElementString("RepetitionDelay", self.repetitionDelay)
        else:
            writer.writeStartElement("RepetitionDelay")
            writer.writeElementString("Min", self.repetitionDelay2.min)
            writer.writeElementString("Exponent", self.repetitionDelay2.exponent)
            writer.writeElementString("Max", self.repetitionDelay2.max)
            writer.writeEndElement()
        if self.version > 0:
            if self.portReference:
                writer.writeElementString(
                    "PortReference", self.portReference.logicalName
                )
            writer.writeElementString("PushClientSAP", self.pushClientSAP)
            if self.pushProtectionParameters:
                writer.writeStartElement("PushProtectionParameters")
                for it in self.pushProtectionParameters:
                    writer.writeStartElement("Item")
                    writer.writeElementString("ProtectionType", int(it.protectionType))
                    writer.writeElementString(
                        "TransactionId", _GXCommon.toHex(it.transactionId, False)
                    )
                    writer.writeElementString(
                        "OriginatorSystemTitle",
                        _GXCommon.toHex(it.originatorSystemTitle, False),
                    )
                    writer.writeElementString(
                        "RecipientSystemTitle",
                        _GXCommon.toHex(it.recipientSystemTitle, False),
                    )
                    writer.writeElementString(
                        "OtherInformation", _GXCommon.toHex(it.otherInformation, False)
                    )
                    writer.writeElementString(
                        "DataProtectionKeyType", int(it.keyInfo.dataProtectionKeyType)
                    )
                    writer.writeStartElement("IdentifiedKey")
                    writer.writeElementString(
                        "KeyType", int(it.keyInfo.identifiedKey.keyType)
                    )
                    writer.writeEndElement()
                    writer.writeStartElement("WrappedKey")
                    writer.writeElementString(
                        "KeyType", int(it.keyInfo.wrappedKey.keyType)
                    )
                    writer.writeElementString(
                        "Key", _GXCommon.toHex(it.keyInfo.wrappedKey.key, False)
                    )
                    writer.writeEndElement()
                    writer.writeStartElement("AgreedKey")
                    writer.writeElementString(
                        "Parameters",
                        _GXCommon.toHex(it.keyInfo.agreedKey.parameters, False),
                    )
                    writer.writeElementString(
                        "Data", _GXCommon.toHex(it.keyInfo.agreedKey.data, False)
                    )
                    writer.writeEndElement()
                    writer.writeEndElement()
                writer.writeEndElement()
            if self.version > 1:
                writer.writeElementString(
                    "PushOperationMethod", int(self.pushOperationMethod)
                )
                writer.writeElementString(
                    "ConfirmationParametersStartDate",
                    self.confirmationParameters.startDate,
                )
                writer.writeElementString(
                    "ConfirmationParametersInterval",
                    self.confirmationParameters.interval,
                )
                writer.writeElementString(
                    "LastConfirmationDateTime", self.lastConfirmationDateTime
                )

    def postLoad(self, reader):
        target = None
        # Update port reference.
        if self.portReference:
            target = reader.objects.findByLN(
                ObjectType.NONE, self.portReference.logicalName
            )
        if target and target != self.portReference:
            self.portReference = target
        # Upload object list after load.
        if self.pushObjectList and len(self.pushObjectList) != 0:
            self.pushObjectList.clear()
            for obj, co in self.pushObjectList:
                target = reader.objects.findByLN(obj.objectType, obj.logicalName)
                if target and target != obj:
                    obj = target
                self.pushObjectList.append((obj, co))

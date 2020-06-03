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
from ..enums import ObjectType, DataType
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from ..GXDateTime import GXDateTime
from .enums import PaymentMode, AccountStatus, AccountCreditStatus, CreditCollectionConfiguration
from .GXCurrency import GXCurrency
from .GXTokenGatewayConfiguration import GXTokenGatewayConfiguration
from .GXCreditChargeConfiguration import GXCreditChargeConfiguration
from ..GXBitString import GXBitString

# pylint: disable=too-many-instance-attributes
class GXDLMSAccount(GXDLMSObject, IGXDLMSBase):

    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSAccount
    """
    def __init__(self, ln="0.0.19.0.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.ACCOUNT, ln, sn)
        self.paymentMode = PaymentMode.CREDIT
        self.accountStatus = AccountStatus.NEW_INACTIVE_ACCOUNT
        self.creditReferences = list()
        self.chargeReferences = list()
        self.creditChargeConfigurations = list()
        self.tokenGatewayConfigurations = list()
        self.currency = GXCurrency()
        self.currentCreditInUse = 0
        self.currentCreditStatus = AccountCreditStatus.IN_CREDIT
        self.availableCredit = 0
        self.amountToClear = 0
        self.clearanceThreshold = 0
        self.aggregatedDebt = 0
        self.accountActivationTime = None
        self.accountClosureTime = None
        self.lowCreditThreshold = 0
        self.nextCreditAvailableThreshold = 0
        self.maxProvision = 0
        self.maxProvisionPeriod = 0

    def getValues(self):
        return [self.logicalName,
                [self.paymentMode, self.accountStatus],
                self.currentCreditInUse,
                self.currentCreditStatus,
                self.availableCredit,
                self.amountToClear,
                self.clearanceThreshold,
                self.aggregatedDebt,
                self.creditReferences,
                self.chargeReferences,
                self.creditChargeConfigurations,
                self.tokenGatewayConfigurations,
                self.accountActivationTime,
                self.accountClosureTime,
                self.currency,
                self.lowCreditThreshold,
                self.nextCreditAvailableThreshold,
                self.maxProvision,
                self.maxProvisionPeriod]

    def activate(self, client):
        """Activate account."""
        return client.method(self.getName(), self.objectType, 1, 0, DataType.INT8)

    def close(self, client):
        """Close account."""
        return client.method(self.getName(), self.objectType, 2, 0, DataType.INT8)

    def reset(self, client):
        """Reset account."""
        return client.method(self.getName(), self.objectType, 3, 0, DataType.INT8)

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
        #  PaymentMode, AccountStatus
        if all_ or self.canRead(2):
            attributes.append(2)
        #  CurrentCreditInUse
        if all_ or self.canRead(3):
            attributes.append(3)
        #  CurrentCreditStatus
        if all_ or self.canRead(4):
            attributes.append(4)
        #  AvailableCredit
        if all_ or self.canRead(5):
            attributes.append(5)
        #  AmountToClear
        if all_ or self.canRead(6):
            attributes.append(6)
        #  ClearanceThreshold
        if all_ or self.canRead(7):
            attributes.append(7)
        #  AggregatedDebt
        if all_ or self.canRead(8):
            attributes.append(8)
        #  CreditReferences
        if all_ or self.canRead(9):
            attributes.append(9)
        #  ChargeReferences
        if all_ or self.canRead(10):
            attributes.append(10)
        #  CreditChargeConfigurations
        if all_ or self.canRead(11):
            attributes.append(11)
        #  TokenGatewayConfigurations
        if all_ or self.canRead(12):
            attributes.append(12)
        #  AccountActivationTime
        if all_ or self.canRead(13):
            attributes.append(13)
        #  AccountClosureTime
        if all_ or self.canRead(14):
            attributes.append(14)
        #  Currency
        if all_ or self.canRead(15):
            attributes.append(15)
        #  LowCreditThreshold
        if all_ or self.canRead(16):
            attributes.append(16)
        #  NextCreditAvailableThreshold
        if all_ or self.canRead(17):
            attributes.append(17)
        #  MaxProvision
        if all_ or self.canRead(18):
            attributes.append(18)
        #  MaxProvisionPeriod
        if all_ or self.canRead(19):
            attributes.append(19)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 19

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 3

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.STRUCTURE
        elif index == 3:
            ret = DataType.UINT8
        elif index == 4:
            ret = DataType.BITSTRING
        elif index == 5:
            ret = DataType.INT32
        elif index == 6:
            ret = DataType.INT32
        elif index == 7:
            ret = DataType.INT32
        elif index == 8:
            ret = DataType.INT32
        elif index == 9:
            ret = DataType.ARRAY
        elif index == 10:
            ret = DataType.ARRAY
        elif index == 11:
            ret = DataType.ARRAY
        elif index == 12:
            ret = DataType.ARRAY
        elif index == 13:
            ret = DataType.OCTET_STRING
        elif index == 14:
            ret = DataType.OCTET_STRING
        elif index == 15:
            ret = DataType.STRUCTURE
        elif index == 16:
            ret = DataType.INT32
        elif index == 17:
            ret = DataType.INT32
        elif index == 18:
            ret = DataType.UINT16
        elif index == 19:
            ret = DataType.INT32
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
            bb = GXByteBuffer()
            bb.setUInt8(DataType.STRUCTURE)
            bb.setUInt8(2)
            bb.setUInt8(DataType.ENUM)
            bb.setUInt8(self.accountStatus)
            bb.setUInt8(DataType.ENUM)
            bb.setUInt8(self.paymentMode)
            ret = bb.array()
        elif e.index == 3:
            ret = self.currentCreditInUse
        elif e.index == 4:
            ret = GXBitString.toBitString(self.currentCreditStatus, 8)
        elif e.index == 5:
            ret = self.availableCredit
        elif e.index == 6:
            ret = self.amountToClear
        elif e.index == 7:
            ret = self.clearanceThreshold
        elif e.index == 8:
            ret = self.aggregatedDebt
        elif e.index == 9:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.ARRAY)
            if not self.creditReferences:
                bb.setUInt8(0)
            else:
                _GXCommon.setObjectCount(len(self.creditReferences), bb)
                for it in self.creditReferences:
                    bb.setUInt8(DataType.OCTET_STRING)
                    bb.setUInt8(6)
                    bb.set(_GXCommon.logicalNameToBytes(it))
            ret = bb.array()
        elif e.index == 10:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.ARRAY)
            if not self.chargeReferences:
                bb.setUInt8(0)
            else:
                _GXCommon.setObjectCount(len(self.chargeReferences), bb)
                for it in self.chargeReferences:
                    bb.setUInt8(DataType.OCTET_STRING)
                    bb.setUInt8(6)
                    bb.set(_GXCommon.logicalNameToBytes(it))
            ret = bb.array()
        elif e.index == 11:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.ARRAY)
            if not self.creditChargeConfigurations:
                bb.setUInt8(0)
            else:
                _GXCommon.setObjectCount(len(self.creditChargeConfigurations), bb)
                for it in self.creditChargeConfigurations:
                    bb.setUInt8(DataType.STRUCTURE)
                    bb.setUInt8(3)
                    bb.setUInt8(DataType.OCTET_STRING)
                    bb.setUInt8(6)
                    bb.set(_GXCommon.logicalNameToBytes(it.creditReference))
                    bb.setUInt8(DataType.OCTET_STRING)
                    bb.setUInt8(6)
                    bb.set(_GXCommon.logicalNameToBytes(it.chargeReference))
                    _GXCommon.setData(settings, bb, DataType.BITSTRING, GXBitString.toBitString(it.collectionConfiguration, 3))
            ret = bb.array()
        elif e.index == 12:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.ARRAY)
            if not self.tokenGatewayConfigurations:
                bb.setUInt8(0)
            else:
                _GXCommon.setObjectCount(len(self.tokenGatewayConfigurations), bb)
                for it in self.tokenGatewayConfigurations:
                    bb.setUInt8(DataType.STRUCTURE)
                    bb.setUInt8(2)
                    bb.setUInt8(DataType.OCTET_STRING)
                    bb.setUInt8(6)
                    bb.set(_GXCommon.logicalNameToBytes(it.creditReference))
                    bb.setUInt8(DataType.UINT8)
                    bb.setUInt8(it.tokenProportion)
            ret = bb.array()
        elif e.index == 13:
            ret = self.accountActivationTime
        elif e.index == 14:
            ret = self.accountClosureTime
        elif e.index == 15:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.STRUCTURE)
            bb.setUInt8(3)
            _GXCommon.setData(settings, bb, DataType.STRING_UTF8, self.currency.name)
            _GXCommon.setData(settings, bb, DataType.INT8, self.currency.scale)
            _GXCommon.setData(settings, bb, DataType.ENUM, self.currency.unit)
            ret = bb.array()
        elif e.index == 16:
            ret = self.lowCreditThreshold
        elif e.index == 17:
            ret = self.nextCreditAvailableThreshold
        elif e.index == 18:
            ret = self.maxProvision
        elif e.index == 19:
            ret = self.maxProvisionPeriod
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
            self.accountStatus = e.value[0]
            self.paymentMode = e.value[1]
        elif e.index == 3:
            self.currentCreditInUse = e.value
        elif e.index == 4:
            self.currentCreditStatus = AccountCreditStatus(e.value.toInteger())
        elif e.index == 5:
            self.availableCredit = e.value
        elif e.index == 6:
            self.amountToClear = e.value
        elif e.index == 7:
            self.clearanceThreshold = e.value
        elif e.index == 8:
            self.aggregatedDebt = e.value
        elif e.index == 9:
            self.creditReferences = []
            if e.value:
                for it in e.value:
                    self.creditReferences.append(_GXCommon.toLogicalName(it))
        elif e.index == 10:
            self.chargeReferences = []
            if e.value:
                for it in e.value:
                    self.chargeReferences.append(_GXCommon.toLogicalName(it))
        elif e.index == 11:
            #pylint: disable=bad-option-value,redefined-variable-type
            self.creditChargeConfigurations = []
            if e.value:
                for it in e.value:
                    item = GXCreditChargeConfiguration()
                    item.creditReference = _GXCommon.toLogicalName(it[0])
                    item.chargeReference = _GXCommon.toLogicalName(it[1])
                    item.collectionConfiguration = CreditCollectionConfiguration(it[2].toInteger())
                    self.creditChargeConfigurations.append(item)
        elif e.index == 12:
            #pylint: disable=bad-option-value,redefined-variable-type
            self.tokenGatewayConfigurations = []
            if e.value:
                for it in e.value:
                    item = GXTokenGatewayConfiguration()
                    item.creditReference = _GXCommon.toLogicalName(it[0])
                    item.tokenProportion = it[1]
                    self.tokenGatewayConfigurations.append(item)
        elif e.index == 13:
            if not e.value:
                self.accountActivationTime = GXDateTime()
            else:
                tmp = None
                if isinstance(e.value, bytearray):
                    tmp = _GXCommon.changeType(settings, e.value, DataType.DATETIME)
                else:
                    tmp = e.value
                self.accountActivationTime = tmp
        elif e.index == 14:
            if not e.value:
                self.accountClosureTime = GXDateTime()
            else:
                tmp = None
                if isinstance(e.value, bytearray):
                    tmp = _GXCommon.changeType(settings, e.value, DataType.DATETIME)
                else:
                    tmp = e.value
                self.accountClosureTime = tmp
        elif e.index == 15:
            tmp = e.value
            self.currency.name = str(tmp[0])
            self.currency.scale = tmp[1]
            self.currency.unit = tmp[2]
        elif e.index == 16:
            self.lowCreditThreshold = e.value
        elif e.index == 17:
            self.nextCreditAvailableThreshold = e.value
        elif e.index == 18:
            self.maxProvision = e.value
        elif e.index == 19:
            self.maxProvisionPeriod = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    @classmethod
    def loadReferences(cls, reader, name, list_):
        list_ = []
        if reader.isStartElement(name, True):
            while reader.isStartElement("Item", True):
                list_.append(reader.readElementContentAsString("Name"))
            reader.readEndElement(name)

    @classmethod
    def loadCreditChargeConfigurations(cls, reader, list_):
        list_ = []
        if reader.isStartElement("CreditChargeConfigurations", True):
            while reader.isStartElement("Item", True):
                it = GXCreditChargeConfiguration()
                it.creditReference = reader.readElementContentAsString("Credit")
                it.chargeReference = reader.readElementContentAsString("Charge")
                it.collectionConfiguration = CreditCollectionConfiguration(reader.readElementContentAsInt("Configuration"))
                list_.append(it)
            reader.readEndElement("CreditChargeConfigurations")

    @classmethod
    def loadTokenGatewayConfigurations(cls, reader, list_):
        list_ = []
        if reader.isStartElement("TokenGatewayConfigurations", True):
            while reader.isStartElement("Item", True):
                it = GXTokenGatewayConfiguration()
                it.creditReference = reader.readElementContentAsString("Credit")
                it.tokenProportion = reader.readElementContentAsInt("Token")
                list_.append(it)
            reader.readEndElement("TokenGatewayConfigurations")

    def load(self, reader):
        self.paymentMode = reader.readElementContentAsInt("PaymentMode")
        self.accountStatus = reader.readElementContentAsInt("AccountStatus")
        self.currentCreditInUse = reader.readElementContentAsInt("CurrentCreditInUse")
        self.currentCreditStatus = AccountCreditStatus(reader.readElementContentAsInt("CurrentCreditStatus"))
        self.availableCredit = reader.readElementContentAsInt("AvailableCredit")
        self.amountToClear = reader.readElementContentAsInt("AmountToClear")
        self.clearanceThreshold = reader.readElementContentAsInt("ClearanceThreshold")
        self.aggregatedDebt = reader.readElementContentAsInt("AggregatedDebt")
        self.loadReferences(reader, "CreditReferences", self.creditReferences)
        self.loadReferences(reader, "ChargeReferences", self.chargeReferences)
        self.loadCreditChargeConfigurations(reader, self.creditChargeConfigurations)
        self.loadTokenGatewayConfigurations(reader, self.tokenGatewayConfigurations)
        self.accountActivationTime = reader.readElementContentAsDateTime("AccountActivationTime")
        self.accountClosureTime = reader.readElementContentAsDateTime("AccountClosureTime")
        self.currency.name = reader.readElementContentAsString("CurrencyName")
        self.currency.scale = reader.readElementContentAsInt("CurrencyScale")
        self.currency.unit = reader.readElementContentAsInt("CurrencyUnit")
        self.lowCreditThreshold = reader.readElementContentAsInt("LowCreditThreshold")
        self.nextCreditAvailableThreshold = reader.readElementContentAsInt("NextCreditAvailableThreshold")
        self.maxProvision = reader.readElementContentAsInt("MaxProvision")
        self.maxProvisionPeriod = reader.readElementContentAsInt("MaxProvisionPeriod")

    @classmethod
    def saveReferences(cls, writer, list_, name):
        if list_:
            writer.writeStartElement(name)
            for it in list_:
                writer.writeStartElement("Item")
                writer.writeElementString("Name", it)
                writer.writeEndElement()
            writer.writeEndElement()

    @classmethod
    def saveCreditChargeConfigurations(cls, writer, list_):
        if list_:
            writer.writeStartElement("CreditChargeConfigurations")
            for it in list_:
                writer.writeStartElement("Item")
                writer.writeElementString("Credit", it.creditReference)
                writer.writeElementString("Charge", it.chargeReference)
                writer.writeElementString("Configuration", int(it.collectionConfiguration))
                writer.writeEndElement()
            writer.writeEndElement()

    @classmethod
    def saveTokenGatewayConfigurations(cls, writer, list_):
        if list_:
            writer.writeStartElement("TokenGatewayConfigurations")
            for it in list_:
                writer.writeStartElement("Item")
                writer.writeElementString("Credit", it.creditReference)
                writer.writeElementString("Token", it.tokenProportion)
                writer.writeEndElement()
            writer.writeEndElement()

    def save(self, writer):
        writer.writeElementString("PaymentMode", int(self.paymentMode))
        writer.writeElementString("AccountStatus", int(self.accountStatus))
        writer.writeElementString("CurrentCreditInUse", self.currentCreditInUse)
        writer.writeElementString("CurrentCreditStatus", int(self.currentCreditStatus))
        writer.writeElementString("AvailableCredit", self.availableCredit)
        writer.writeElementString("AmountToClear", self.amountToClear)
        writer.writeElementString("ClearanceThreshold", self.clearanceThreshold)
        writer.writeElementString("AggregatedDebt", self.aggregatedDebt)
        self.saveReferences(writer, self.creditReferences, "CreditReferences")
        self.saveReferences(writer, self.chargeReferences, "ChargeReferences")
        self.saveCreditChargeConfigurations(writer, self.creditChargeConfigurations)
        self.saveTokenGatewayConfigurations(writer, self.tokenGatewayConfigurations)
        writer.writeElementString("AccountActivationTime", self.accountActivationTime)
        writer.writeElementString("AccountClosureTime", self.accountClosureTime)
        writer.writeElementString("CurrencyName", self.currency.name)
        writer.writeElementString("CurrencyScale", self.currency.scale)
        writer.writeElementString("CurrencyUnit", int(self.currency.unit))
        writer.writeElementString("LowCreditThreshold", self.lowCreditThreshold)
        writer.writeElementString("NextCreditAvailableThreshold", self.nextCreditAvailableThreshold)
        writer.writeElementString("MaxProvision", self.maxProvision)
        writer.writeElementString("MaxProvisionPeriod", self.maxProvisionPeriod)

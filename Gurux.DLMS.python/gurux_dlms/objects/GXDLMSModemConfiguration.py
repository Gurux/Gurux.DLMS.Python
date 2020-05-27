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
from .enums import BaudRate
from .GXDLMSModemInitialisation import GXDLMSModemInitialisation

# pylint: disable=too-many-instance-attributes
class GXDLMSModemConfiguration(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSModemConfiguration
    """

    #
    # Constructor.
    #
    # @param ln
    # Logical Name of the object.
    # @param sn
    # Short Name of the object.
    #
    def __init__(self, ln=None, sn=0):
        super(GXDLMSModemConfiguration, self).__init__(ObjectType.MODEM_CONFIGURATION, ln, sn)
        self.initialisationStrings = list()
        self.communicationSpeed = BaudRate.BAUDRATE_300
        self.modemProfile = self.defultProfiles()

    @classmethod
    def defultProfiles(cls):
        return ["OK", "CONNECT", "RING", "NO CARRIER", "ERROR",
                "CONNECT 1200", "NO DIAL TONE", "BUSY", "NO ANSWER",
                "CONNECT 600", "CONNECT 2400", "CONNECT 4800", "CONNECT 9600",
                "CONNECT 14 400", "CONNECT 28 800", "CONNECT 33 600",
                "CONNECT 56 000"]

    def getValues(self):
        return [self.logicalName,
                self.communicationSpeed,
                self.initialisationStrings,
                self.modemProfile]

    #
    # Returns collection of attributes to read.  If attribute is static
    # and already read or device is returned HW error it is not returned.
    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  CommunicationSpeed
        if all_ or not self.isRead(2):
            attributes.append(2)
        #  InitialisationStrings
        if all_ or not self.isRead(3):
            attributes.append(3)
        #  ModemProfile
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
            return DataType.OCTET_STRING
        if index == 2:
            return DataType.ENUM
        if index == 3:
            return DataType.ARRAY
        if index == 4:
            return DataType.ARRAY
        raise ValueError("getDataType failed. Invalid attribute index.")

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            return _GXCommon.logicalNameToBytes(self.logicalName)
        if e.index == 2:
            return self.communicationSpeed
        if e.index == 3:
            data = GXByteBuffer()
            data.setUInt8(DataType.ARRAY)
            #  Add count
            cnt = 0
            if self.initialisationStrings:
                cnt = len(self.initialisationStrings)
            _GXCommon.setObjectCount(cnt, data)
            if cnt != 0:
                for it in self.initialisationStrings:
                    data.setUInt8(DataType.STRUCTURE)
                    data.setUInt8(3)
                    #  Count
                    _GXCommon.setData(settings, data, DataType.OCTET_STRING, _GXCommon.getBytes(it.request))
                    _GXCommon.setData(settings, data, DataType.OCTET_STRING, _GXCommon.getBytes(it.response))
                    _GXCommon.setData(settings, data, DataType.UINT16, it.delay)
            return data
        if e.index == 4:
            data = GXByteBuffer()
            data.setUInt8(DataType.ARRAY)
            #  Add count
            cnt = len(self.modemProfile)
            _GXCommon.setObjectCount(cnt, data)
            if cnt != 0:
                for it in self.modemProfile:
                    _GXCommon.setData(settings, data, DataType.OCTET_STRING, _GXCommon.getBytes(it))
            return data
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.communicationSpeed = e.value
        elif e.index == 3:
            self.initialisationStrings = []
            if e.value:
                for it in e.value:
                    item = GXDLMSModemInitialisation()
                    item.request = it[0].decode("utf-8")
                    item.response = it[1].decode("utf-8")
                    if len(it) == 3:
                        item.delay = it[2]
                    self.initialisationStrings.append(item)
        elif e.index == 4:
            self.modemProfile = []
            if e.value:
                for it in e.value:
                    self.modemProfile.append(it.decode("utf-8"))
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.communicationSpeed = BaudRate(reader.readElementContentAsInt("CommunicationSpeed"))
        if reader.isStartElement("InitialisationStrings", True):
            while reader.isStartElement("Initialisation", True):
                it = GXDLMSModemInitialisation()
                it.request = reader.readElementContentAsString("Request")
                it.response = reader.readElementContentAsString("Response")
                it.delay = reader.readElementContentAsInt("Delay")
            reader.readEndElement("InitialisationStrings")
        self.modemProfile = reader.readElementContentAsString("ModemProfile", "").split(';')

    def save(self, writer):
        writer.writeElementString("CommunicationSpeed", int(self.communicationSpeed))
        writer.writeStartElement("InitialisationStrings")
        if self.initialisationStrings:
            for it in self.initialisationStrings:
                writer.writeStartElement("Initialisation")
                writer.writeElementString("Request", it.request)
                writer.writeElementString("Response", it.response)
                writer.writeElementString("Delay", it.delay)
                writer.writeEndElement()
        writer.writeEndElement()
        if self.modemProfile:
            writer.writeElementString("ModemProfile", ';'.join(self.modemProfile))

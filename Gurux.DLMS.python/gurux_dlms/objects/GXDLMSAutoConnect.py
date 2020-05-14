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
from .enums import AutoConnectMode

# pylint: disable=too-many-instance-attributes
class GXDLMSAutoConnect(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSAutoConnect
    """

    def __init__(self, ln="0.0.2.1.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.AUTO_CONNECT, ln, sn)
        self.mode = AutoConnectMode.NO_AUTO_DIALLING
        self.repetitions = 0
        self.repetitionDelay = 0
        self.callingWindow = list()
        self.destinations = list()
        self.version = 2

    #
    # Initiates the connection process.
    #
    # @param client
    #            DLMS client.
    # Action bytes.
    #
    def connect(self, client):
        return client.method(self.name(), self.objectType, 1, 0, DataType.INT8)

    def getValues(self):
        return [self.logicalName,
                self.mode,
                self.repetitions,
                self.repetitionDelay,
                self.callingWindow,
                self.destinations]

    def invoke(self, settings, e):
        if e.index != 1:
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
        #  Mode
        if all_ or self.canRead(2):
            attributes.append(2)
        #  Repetitions
        if all_ or self.canRead(3):
            attributes.append(3)
        #  RepetitionDelay
        if all_ or self.canRead(4):
            attributes.append(4)
        #  CallingWindow
        if all_ or self.canRead(5):
            attributes.append(5)
        #  Destinations
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
            ret = DataType.ENUM
        elif index == 3:
            ret = DataType.UINT8
        elif index == 4:
            ret = DataType.UINT16
        elif index == 5:
            ret = DataType.ARRAY
        elif index == 6:
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
            ret = self.mode
        elif e.index == 3:
            ret = self.repetitions
        elif e.index == 4:
            ret = self.repetitionDelay
        elif e.index == 5:
            data = GXByteBuffer()
            data.setUInt8(DataType.ARRAY)
            #  Add count
            _GXCommon.setObjectCount(len(self.callingWindow), data)
            for k, v in self.callingWindow:
                data.setUInt8(DataType.STRUCTURE)
                #  Count
                data.setUInt8(2)
                #  Start time
                _GXCommon.setData(settings, data, DataType.OCTET_STRING, k)
                #  End time
                _GXCommon.setData(settings, data, DataType.OCTET_STRING, v)
            ret = data.array()
        elif e.index == 6:
            data = GXByteBuffer()
            data.setUInt8(DataType.ARRAY)
            if not self.destinations:
                #  Add count
                _GXCommon.setObjectCount(0, data)
            else:
                #  Add count
                _GXCommon.setObjectCount(len(self.destinations), data)
                #  destination
                for it in self.destinations:
                    _GXCommon.setData(settings, data, DataType.OCTET_STRING, _GXCommon.getBytes(it))
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
            self.mode = e.value
        elif e.index == 3:
            self.repetitions = e.value
        elif e.index == 4:
            self.repetitionDelay = e.value
        elif e.index == 5:
            self.callingWindow = []
            if e.value:
                for item in e.value:
                    start = _GXCommon.changeType(settings, item[0], DataType.DATETIME)
                    end = _GXCommon.changeType(settings, item[1], DataType.DATETIME)
                    self.callingWindow.append((start, end))
        elif e.index == 6:
            self.destinations = []
            if e.value:
                for item in e.value:
                    it = _GXCommon.changeType(settings, item, DataType.STRING)
                    self.destinations.append(it)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.mode = reader.readElementContentAsInt("Mode")
        self.repetitions = reader.readElementContentAsInt("Repetitions")
        self.repetitionDelay = reader.readElementContentAsInt("RepetitionDelay")
        self.callingWindow = []
        if reader.isStartElement("CallingWindow", True):
            while reader.isStartElement("Item", True):
                start = reader.readElementContentAsDateTime("Start")
                end = reader.readElementContentAsDateTime("End")
                self.callingWindow.append((start, end))
            reader.readEndElement("CallingWindow")
        str_ = reader.readElementContentAsString("Destinations", "")
        if str_:
            self.destinations = str_.split(';')

    def save(self, writer):
        writer.writeElementString("Mode", int(self.mode))
        writer.writeElementString("Repetitions", self.repetitions)
        writer.writeElementString("RepetitionDelay", self.repetitionDelay)
        if self.callingWindow:
            writer.writeStartElement("CallingWindow")
            for k, v in self.callingWindow:
                writer.writeStartElement("Item")
                writer.writeElementString("Start", k)
                writer.writeElementString("End", v)
                writer.writeEndElement()
            writer.writeEndElement()
        if self.destinations:
            writer.writeElementString("Destinations", ';'.join(self.destinations))

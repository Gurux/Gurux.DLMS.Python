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
from .enums import AutoAnswerMode, AutoAnswerStatus

# pylint: disable=too-many-instance-attributes
class GXDLMSAutoAnswer(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSAutoAnswer
    """

    def __init__(self, ln="0.0.2.2.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.AUTO_ANSWER, ln, sn)
        self.listeningWindow = list()
        self.mode = AutoAnswerMode.NONE
        self.status = AutoAnswerStatus.INACTIVE
        self.numberOfCalls = 0
        self.numberOfRingsInListeningWindow = 0
        self.numberOfRingsOutListeningWindow = 0

    def getValues(self):
        return [self.logicalName,
                self.mode,
                self.listeningWindow,
                self.status,
                self.numberOfCalls,
                [self.numberOfRingsInListeningWindow,
                 self.numberOfRingsOutListeningWindow]]
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
        #  Mode is static and read only once.
        if all_ or not self.isRead(2):
            attributes.append(2)
        #  ListeningWindow is static and read only once.
        if all_ or not self.isRead(3):
            attributes.append(3)
        #  Status is not static.
        if all_ or self.canRead(4):
            attributes.append(4)
        #  NumberOfCalls is static and read only once.
        if all_ or not self.isRead(5):
            attributes.append(5)
        #  NumberOfRingsInListeningWindow is static and read only once.
        if all_ or not self.isRead(6):
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
        return 0

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.ENUM
        elif index == 3:
            ret = DataType.ARRAY
        elif index == 4:
            ret = DataType.ENUM
        elif index == 5:
            ret = DataType.UINT8
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
            cnt = len(self.listeningWindow)
            buff = GXByteBuffer()
            buff.setUInt8(DataType.ARRAY)
            #  Add count
            _GXCommon.setObjectCount(cnt, buff)
            if cnt != 0:
                for it in self.listeningWindow:
                    buff.setUInt8(DataType.STRUCTURE)
                    #  Count
                    buff.setUInt8(2)
                    #  Start time
                    _GXCommon.setData(settings, buff, DataType.OCTET_STRING, it.getKey())
                    #  End time
                    _GXCommon.setData(settings, buff, DataType.OCTET_STRING, it.value)
            ret = buff.array()
        elif e.index == 4:
            ret = self.status
        elif e.index == 5:
            ret = self.numberOfCalls
        elif e.index == 6:
            buff = GXByteBuffer()
            buff.setUInt8(DataType.STRUCTURE)
            _GXCommon.setObjectCount(2, buff)
            _GXCommon.setData(settings, buff, DataType.UINT8, self.numberOfRingsInListeningWindow)
            _GXCommon.setData(settings, buff, DataType.UINT8, self.numberOfRingsOutListeningWindow)
            ret = buff.array()
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
            self.listeningWindow = []
            if e.value:
                for item in e.value:
                    start = _GXCommon.changeType(settings, item[0], DataType.DATETIME)
                    end = _GXCommon.changeType(settings, item[1], DataType.DATETIME)
                    self.listeningWindow.append((start, end))
        elif e.index == 4:
            self.status = e.value
        elif e.index == 5:
            self.numberOfCalls = e.value
        elif e.index == 6:
            self.numberOfRingsInListeningWindow = 0
            self.numberOfRingsOutListeningWindow = 0
            if e.value:
                self.numberOfRingsInListeningWindow = e.value[0]
                self.numberOfRingsOutListeningWindow = e.value[1]
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.mode = reader.readElementContentAsInt("Mode")
        self.listeningWindow = []
        if reader.isStartElement("ListeningWindow", True):
            while reader.isStartElement("Item", True):
                start = reader.readElementContentAsDateTime("Start")
                end = reader.readElementContentAsDateTime("End")
                self.listeningWindow.append((start, end))
            reader.readEndElement("ListeningWindow")
        self.status = reader.readElementContentAsInt("Status")
        self.numberOfCalls = reader.readElementContentAsInt("NumberOfCalls")
        self.numberOfRingsInListeningWindow = reader.readElementContentAsInt("NumberOfRingsInListeningWindow")
        self.numberOfRingsOutListeningWindow = reader.readElementContentAsInt("NumberOfRingsOutListeningWindow")

    def save(self, writer):
        writer.writeElementString("Mode", int(self.mode))
        writer.writeStartElement("ListeningWindow")
        if self.listeningWindow:
            for k, v in self.listeningWindow:
                writer.writeStartElement("Item")
                writer.writeElementString("Start", k)
                writer.writeElementString("End", v)
                writer.writeEndElement()
        writer.writeEndElement()
        writer.writeElementString("Status", int(self.status))
        writer.writeElementString("NumberOfCalls", self.numberOfCalls)
        writer.writeElementString("NumberOfRingsInListeningWindow", self.numberOfRingsInListeningWindow)
        writer.writeElementString("NumberOfRingsOutListeningWindow", self.numberOfRingsOutListeningWindow)

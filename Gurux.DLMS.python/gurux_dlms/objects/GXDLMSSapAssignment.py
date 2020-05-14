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

# pylint: disable=too-many-instance-attributes
class GXDLMSSapAssignment(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSSapAssignment
    """
    def __init__(self, ln=None, sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        super(GXDLMSSapAssignment, self).__init__(ObjectType.SAP_ASSIGNMENT, ln, sn)
        self.sapAssignmentList = list()

    def getValues(self):
        return [self.logicalName,
                self.sapAssignmentList]

    #
    # Returns collection of attributes to read.  If attribute is static and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  SapAssignmentList
        if all_ or not self.isRead(2):
            attributes.append(2)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 2

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 1

    def getDataType(self, index):
        if index == 1:
            return DataType.OCTET_STRING
        if index == 2:
            return DataType.ARRAY
        raise ValueError("getDataType failed. Invalid attribute index.")

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            return _GXCommon.logicalNameToBytes(self.logicalName)
        if e.index == 2:
            cnt = len(self.sapAssignmentList)
            data = GXByteBuffer()
            data.setUInt8(DataType.ARRAY)
            #  Add count
            _GXCommon.setObjectCount(cnt, data)
            if cnt != 0:
                for k, v in self.sapAssignmentList:
                    data.setUInt8(DataType.STRUCTURE)
                    data.setUInt8(2)
                    #  Count
                    _GXCommon.setData(settings, data, DataType.UINT16, k)
                    _GXCommon.setData(settings, data, DataType.OCTET_STRING, _GXCommon.getBytes(v))
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
            self.sapAssignmentList = []
            if e.value:
                for item in e.value:
                    str_ = None
                    if isinstance(item[1], bytearray):
                        str_ = _GXCommon.changeType(settings, item[1], DataType.STRING)
                    else:
                        str_ = str(item[1])
                    self.sapAssignmentList.append((item[0], str_))
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.sapAssignmentList = []
        if reader.isStartElement("SapAssignmentList", True):
            while reader.isStartElement("Item", True):
                sap = reader.readElementContentAsInt("SAP")
                ldn = reader.readElementContentAsString("LDN")
                self.sapAssignmentList.append((sap, ldn))
            reader.readEndElement("SapAssignmentList")

    def save(self, writer):
        if self.sapAssignmentList:
            writer.writeStartElement("SapAssignmentList")
            for k, v in self.sapAssignmentList:
                writer.writeStartElement("Item")
                writer.writeElementString("SAP", k)
                writer.writeElementString("LDN", v)
                writer.writeEndElement()
            writer.writeEndElement()

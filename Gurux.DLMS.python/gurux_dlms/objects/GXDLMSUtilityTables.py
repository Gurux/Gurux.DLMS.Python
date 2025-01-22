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
from ..internal._GXCommon import _GXCommon
from ..enums import ObjectType, DataType, ErrorCode
from ..GXByteBuffer import GXByteBuffer


# pylint: disable=too-many-instance-attributes
class GXDLMSUtilityTables(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSUtilityTables
    """

    def __init__(self, ln="0.0.65.0.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.UTILITY_TABLES, ln, sn)
        # Table Id.
        self.tableId = 0
        # Contents of the table.
        self.buffer = None

    def getValues(self):
        tmp = 0
        if self.buffer:
            tmp = len(self.buffer)
        return [self.logicalName, self.tableId, tmp, self.buffer]

    #
    # Returns collection of attributes to read.  If attribute is static and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = []
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  Table Id.
        if all_ or self.canRead(2):
            attributes.append(2)
        # Length
        if all_ or self.canRead(3):
            attributes.append(3)
        # Buffer
        if all_ or self.canRead(4):
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
            return DataType.UINT16
        if index == 3:
            return DataType.UINT32
        if index == 4:
            return DataType.OCTET_STRING
        raise ValueError("getDataType failed. Invalid attribute index.")

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            return _GXCommon.logicalNameToBytes(self.logicalName)
        if e.index == 2:
            return self.tableId
        if e.index == 3:
            if self.buffer:
                return len(self.buffer)
            return 0
        if e.index == 4:
            return self.buffer
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.tableId = e.value
        elif e.index == 3:
            pass
        elif e.index == 4:
            self.buffer = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.tableId = reader.readElementContentAsInt("Id", None)
        self.buffer = GXByteBuffer.hexToBytes(
            reader.readElementContentAsString("Buffer")
        )

    def save(self, writer):
        writer.writeElementString("Id", self.tableId)
        writer.writeElementString("Buffer", GXByteBuffer.hex(self.buffer))

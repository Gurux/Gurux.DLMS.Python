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
from .GXMappingTable import GXMappingTable
from ..enums import DataType, ErrorCode, ObjectType
from ..GXByteBuffer import GXByteBuffer
from ..GXStructure import GXStructure
from ..internal._GXCommon import _GXCommon
from ..internal._GXLocalizer import _GXLocalizer


class GXDLMSStatusMapping(GXDLMSObject, IGXDLMSBase):
    """COSEM status word and reference status mapping table."""

    def __init__(self, ln="0.0.96.5.0.255", sn=0):
        GXDLMSObject.__init__(self, ObjectType.STATUS_MAPPING, ln, sn)
        self.status_word = None
        self.mapping_table = GXMappingTable()

    def getValues(self):
        return [self.logicalName, self.status_word, self.mapping_table]

    def invoke(self, settings, e):
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    def getAttributeIndexToRead(self, all_):
        attributes = []
        if all_ or not self.logicalName:
            attributes.append(1)
        if all_ or self.canRead(2):
            attributes.append(2)
        if all_ or self.canRead(3):
            attributes.append(3)
        return attributes

    def getNames(self):
        return (
            _GXLocalizer.gettext("Logical name"),
            _GXLocalizer.gettext("Status word"),
            _GXLocalizer.gettext("Mapping table"),
        )

    def getMethodNames(self):
        return []

    def getMaxSupportedVersion(self):
        return 0

    def getAttributeCount(self):
        return 3

    def getMethodCount(self):
        return 0

    def getDataType(self, index):
        if index == 1:
            return DataType.OCTET_STRING
        if index == 2:
            dt = super(GXDLMSStatusMapping, self).getDataType(index)
            if dt == DataType.NONE and self.status_word is not None:
                dt = _GXCommon.getDLMSDataType(self.status_word)
                if dt == DataType.STRING:
                    dt = DataType.NONE
            return dt
        if index == 3:
            return DataType.STRUCTURE
        raise ValueError("getDataType failed. Invalid attribute index.")

    def getUIDataType(self, index):
        return self.getDataType(index)

    def getValue(self, settings, e):
        if e.index == 1:
            return _GXCommon.logicalNameToBytes(self.logicalName)
        if e.index == 2:
            return self.status_word
        if e.index == 3:
            data = GXByteBuffer()
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(2)
            _GXCommon.setData(
                settings, data, DataType.UINT8, self.mapping_table.refefence_table_id
            )
            value = self.mapping_table.refefence_table_mapping
            _GXCommon.setData(settings, data, _GXCommon.getDLMSDataType(value), value)
            return data.array()
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.status_word = e.value
        elif e.index == 3:
            if isinstance(e.value, GXStructure) and len(e.value) == 2:
                self.mapping_table.refefence_table_id = e.value[0]
                self.mapping_table.refefence_table_mapping = e.value[1]
            else:
                e.error = ErrorCode.READ_WRITE_DENIED
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.status_word = reader.readElementContentAsObject(
            "StatusWord", None, self, 2
        )
        self.mapping_table.refefence_table_id = (
            reader.readElementContentAsInt("TableId") & 0xFF
        )
        self.mapping_table.refefence_table_mapping = reader.readElementContentAsObject(
            "RefefenceTableMapping", None, self, 3
        )

    def save(self, writer):
        writer.writeElementObject(
            "StatusWord", self.status_word, self.getDataType(2), self.getUIDataType(2)
        )
        writer.writeElementString("TableId", self.mapping_table.refefence_table_id)
        value = self.mapping_table.refefence_table_mapping
        dt = _GXCommon.getDLMSDataType(value) if value is not None else DataType.NONE
        writer.writeElementObject("RefefenceTableMapping", value, dt, DataType.NONE)

    def postLoad(self, reader):
        pass

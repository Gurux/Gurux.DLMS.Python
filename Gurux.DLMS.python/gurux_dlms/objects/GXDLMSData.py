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
from ..enums import ObjectType, DataType
from ..internal._GXLocalizer import _GXLocalizer


# pylint: disable=too-many-instance-attributes
class GXDLMSData(GXDLMSObject, IGXDLMSBase):
    """
    Represents a COSEM Data object that holds a value and provides access to its logical name and data attributes.
    
    
    The GXDLMSData class is used to model a COSEM Data object as defined in the DLMS/COSEM
    specification. It allows reading and writing of the data value and supports both logical name (LN) and short
    name (SN) referencing. This class is typically used in DLMS/COSEM server or client implementations to represent
    simple data points, such as configuration parameters or measurement values.
    
    
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSData
    """

    def __init__(self, ln=None, sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.DATA, ln, sn)
        self.value = None

    def getValues(self):
        return [self.logicalName, self.value]

    def getAttributeIndexToRead(self, all_):
        """See IGXDLMSBase.getAttributeIndexToRead."""
        attributes = []
        # LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        # Value
        if all_ or self.canRead(2):
            attributes.append(2)
        return attributes

    def getAttributeCount(self):
        """See IGXDLMSBase.getAttributeCount."""
        return 2

    def getMethodCount(self):
        """See IGXDLMSBase.getMethodCount."""
        return 0

    def getNames(self):
        """See IGXDLMSBase.getNames."""
        return (_GXLocalizer.gettext("Logical name"), _GXLocalizer.gettext("Value"))

    def getDataType(self, index):
        """See IGXDLMSBase.getDataType."""
        if index == 1:
            dt = DataType.OCTET_STRING
        elif index == 2:
            # pylint: disable=super-with-arguments
            dt = super(GXDLMSData, self).getDataType(index)
            if dt == DataType.NONE:
                dt = _GXCommon.getDLMSDataType(self.value)
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return dt

    def getValue(self, settings, e):
        """See IGXDLMSBase.getValue."""
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
            ret = None
        return ret

    def setValue(self, settings, e):
        """See IGXDLMSBase.setValue."""
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.value = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        """See IGXDLMSBase.load."""
        self.value = reader.readElementContentAsObject("Value", None, self, 2)

    def save(self, writer):
        """See IGXDLMSBase.save."""
        writer.writeElementObject(
            "Value", self.value, self.getDataType(2), self.getUIDataType(2)
        )

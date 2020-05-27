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
import math
from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ErrorCode
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from ..enums import ObjectType, DataType, Unit

# pylint: disable=too-many-instance-attributes
class GXDLMSRegister(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSRegister
    """
    def __init__(self, ln=None, sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        super(GXDLMSRegister, self).__init__(ObjectType.REGISTER, ln, sn)
        self.value = None
        self.scaler = 1
        self.unit = Unit.NONE

    def reset(self, client):
        """Reset value."""
        return client.method(self.getName(), self.objectType, 1, 0, DataType.INT8)

    def getValues(self):
        return [self.logicalName,
                self.value,
                [self.scaler, self.unit]]


    def invoke(self, settings, e):
        #  Resets the value to the default value.
        #  The default value is an instance specific constant.
        if e.index == 1:
            self.value = None
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def isRead(self, index):
        if index == 3:
            return self.unit != 0
        return super(GXDLMSRegister, self).isRead(index)

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
        #  ScalerUnit
        if all_ or not self.isRead(3):
            attributes.append(3)
        #  Value
        if all_ or self.canRead(2):
            attributes.append(2)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 3


    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 1


    def getDataType(self, index):
        if index == 1:
            return DataType.OCTET_STRING
        if index == 2:
            return super(GXDLMSRegister, self).getDataType(index)
        if index == 3:
            return DataType.STRUCTURE
        raise ValueError("getDataType failed. Invalid attribute index.")

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            return _GXCommon.logicalNameToBytes(self.logicalName)
        if e.index == 2:
            return self.value
        if e.index == 3:
            data = GXByteBuffer()
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(2)
            _GXCommon.setData(settings, data, DataType.INT8, math.floor(math.log(self.scaler, 10)))
            _GXCommon.setData(settings, data, DataType.ENUM, int(self.unit))
            return data.array()
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    #
    # Set value of given attribute.
    #
    #pylint: disable=broad-except
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            if self.scaler != 1 and e.value is not None:
                try:
                    if settings.isServer:
                        self.value = e.value
                    else:
                        self.value = e.value * self.scaler
                except Exception:
                    #  Sometimes scaler is set for wrong Object type.
                    self.value = e.value
            else:
                self.value = e.value
        elif e.index == 3:
            #  Set default values.
            if not e.value:
                self.scaler = 1
                self.unit = Unit.NONE
            else:
                self.scaler = math.pow(10, e.value[0])
                self.unit = Unit(e.value[1])
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.unit = Unit(reader.readElementContentAsInt("Unit", 0))
        self.scaler = reader.readElementContentAsDouble("Scaler", 1)
        self.value = reader.readElementContentAsObject("Value", None, self, 2)

    def save(self, writer):
        writer.writeElementString("Unit", int(self.unit))
        writer.writeElementString("Scaler", self.scaler, 1)
        writer.writeElementObject("Value", self.value, self.getDataType(2), self.getUIDataType(2))

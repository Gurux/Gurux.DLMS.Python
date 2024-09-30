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
import datetime
from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ErrorCode
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from ..GXDateTime import GXDateTime
from ..enums import ObjectType, DataType, Unit
from .GXDLMSRegister import GXDLMSRegister

# pylint: disable=too-many-instance-attributes
class GXDLMSExtendedRegister(GXDLMSRegister, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSExtendedRegister
    """

    def __init__(self, ln=None, sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        # pylint: disable=non-parent-init-called
        GXDLMSObject.__init__(self, ObjectType.EXTENDED_REGISTER, ln, sn)
        self.value = None
        self.scaler = 1
        self.unit = Unit.NONE
        self.status = None
        self.captureTime = None

    def getUIDataType(self, index):
        if index == 5:
            return DataType.DATETIME
        #pylint: disable=super-with-arguments
        return super(GXDLMSExtendedRegister, self).getUIDataType(index)

    def getValues(self):
        return [self.logicalName,
                self.value,
                [self.scaler, self.unit],
                self.status,
                self.captureTime]

    def reset(self, client):
        """Reset value."""
        return client.method(self, 1, 0, DataType.INT8)

    def invoke(self, settings, e):
        #  Resets the value to the default value.
        #  The default value is an instance specific constant.
        if e.index == 1:
            self.value = None
            self.captureTime = datetime.datetime.now()
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    #
    #      Returns collection of attributes to read.  If attribute is static
    #      and
    #      already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = []
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  ScalerUnit
        if all_ or not self.isRead(3):
            attributes.append(3)
        #  Value
        if all_ or self.canRead(2):
            attributes.append(2)
        #  Status
        if all_ or self.canRead(4):
            attributes.append(4)
        #  CaptureTime
        if all_ or self.canRead(5):
            attributes.append(5)
        return attributes

    #
    #      Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 5

    def getMethodCount(self):
        return 0

    def getDataType(self, index):
        #pylint: disable=super-with-arguments
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = super(GXDLMSExtendedRegister, self).getDataType(index)
        elif index == 3:
            ret = DataType.ARRAY
        elif index == 4:
            ret = super(GXDLMSRegister, self).getDataType(index)
        elif index == 5:
            ret = DataType.OCTET_STRING
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret
    #
    #      Returns value of given attribute.
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
        if e.index == 4:
            return self.status
        if e.index == 5:
            return self.captureTime
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    #
    #      Set value of given attribute.
    #
    def setValue(self, settings, e):
        #pylint: disable=broad-except
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            if self.scaler != 1 and e.value:
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
                self.scaler = 0
                self.unit = Unit.NONE
            else:
                if not e.value:
                    self.scaler = 0
                    self.unit = Unit.NONE
                else:
                    self.scaler = math.pow(10, e.value[0])
                    self.unit = Unit(e.value[1])
        elif e.index == 4:
            self.status = e.value
        elif e.index == 5:
            if e.value is None:
                self.captureTime = GXDateTime()
            else:
                if isinstance(e.value, bytearray):
                    self.captureTime = _GXCommon.changeType(settings, e.value, DataType.DATETIME)
                else:
                    self.captureTime = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.unit = Unit(reader.readElementContentAsInt("Unit", 0))
        self.scaler = reader.readElementContentAsDouble("Scaler", 1)
        self.value = reader.readElementContentAsObject("Value", None, self, 2)
        self.status = reader.readElementContentAsObject("Status", None, self, 4)
        self.captureTime = reader.readElementContentAsDateTime("CaptureTime")

    def save(self, writer):
        writer.writeElementString("Unit", int(self.unit))
        writer.writeElementString("Scaler", self.scaler, 1)
        writer.writeElementObject("Value", self.value, self.getDataType(2), self.getUIDataType(2))
        writer.writeElementObject("Status", self.status, self.getDataType(4), self.getUIDataType(4))
        writer.writeElementString("CaptureTime", self.captureTime)

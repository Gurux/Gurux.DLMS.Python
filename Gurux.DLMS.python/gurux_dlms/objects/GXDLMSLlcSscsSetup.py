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

# pylint: disable=too-many-instance-attributes
class GXDLMSLlcSscsSetup(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSLlcSscsSetup
    """

    def __init__(self, ln="0.0.28.0.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.LLC_SSCS_SETUP, ln, sn)
        self.serviceNodeAddress = 0
        self.baseNodeAddress = 0

    def getValues(self):
        return [self.logicalName,
                self.serviceNodeAddress,
                self.baseNodeAddress]

    def reset(self, client):
        """Reset value."""
        return client.method(self.getName(), self.objectType, 1, 0, DataType.INT8)

    #
    # Returns collection of attributes to read.  If attribute is static and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  ServiceNodeAddress
        if all_ or self.canRead(2):
            attributes.append(2)
        #  BaseNodeAddress
        if all_ or self.canRead(3):
            attributes.append(3)
        return attributes

    def invoke(self, settings, e):
        #  Resets the value to the default value.
        #  The default value is an instance specific constant.
        if e.index == 1:
            self.serviceNodeAddress = 0xFFE
            self.baseNodeAddress = 0
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
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
        if index in (2, 3):
            return DataType.UINT16
        raise ValueError("getDataType failed. Invalid attribute index.")

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            return _GXCommon.logicalNameToBytes(self.logicalName)
        if e.index == 2:
            return self.serviceNodeAddress
        if e.index == 3:
            return self.baseNodeAddress
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.serviceNodeAddress = e.value
        elif e.index == 3:
            self.baseNodeAddress = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.serviceNodeAddress = reader.readElementContentAsInt("ServiceNodeAddress")
        self.baseNodeAddress = reader.readElementContentAsInt("BaseNodeAddress")

    def save(self, writer):
        writer.writeElementString("ServiceNodeAddress", self.serviceNodeAddress)
        writer.writeElementString("BaseNodeAddress", self.baseNodeAddress)

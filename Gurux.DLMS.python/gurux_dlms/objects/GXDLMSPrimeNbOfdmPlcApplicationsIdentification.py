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
class GXDLMSPrimeNbOfdmPlcApplicationsIdentification(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSPrimeNbOfdmPlcApplicationsIdentification
    """

    def __init__(self, ln="0.0.28.7.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.PRIME_NB_OFDM_PLC_APPLICATIONS_IDENTIFICATION, ln, sn)
        # Textual description of the firmware version running on the device.
        self.firmwareVersion = None
        # Unique vendor identifier assigned by PRIME Alliance.
        self.vendorId = 0
        # Vendor assigned unique identifier for specific product.
        self.productId = 0

    def getValues(self):
        return [self.logicalName,
                self.firmwareVersion,
                self.vendorId,
                self.productId]

    #
    # Returns collection of attributes to read.  If attribute is static and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  FirmwareVersion
        if all_ or self.canRead(2):
            attributes.append(2)
        #  VendorId
        if all_ or self.canRead(3):
            attributes.append(3)
        #  ProductId
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
        if index in (1, 2):
            return DataType.OCTET_STRING
        if index in (3, 4):
            return DataType.UINT16
        raise ValueError("getDataType failed. Invalid attribute index.")

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            if isinstance(self.firmwareVersion, str):
                ret = self.firmwareVersion.encode()
            else:
                ret = self.firmwareVersion
        elif e.index == 3:
            ret = self.vendorId
        elif e.index == 4:
            ret = self.productId
        else:
            ret = None
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            if e.value is None:
                self.firmwareVersion = None
            else:
                self.firmwareVersion = e.value.decode("utf-8").rstrip('\x00')
        elif e.index == 3:
            self.vendorId = e.value
        elif e.index == 4:
            self.productId = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.firmwareVersion = reader.readElementContentAsString("FirmwareVersion")
        self.vendorId = reader.readElementContentAsInt("VendorId")
        self.productId = reader.readElementContentAsInt("ProductId")

    def save(self, writer):
        writer.writeElementString("FirmwareVersion", self.firmwareVersion)
        writer.writeElementString("VendorId", self.vendorId)
        writer.writeElementString("ProductId", self.productId)

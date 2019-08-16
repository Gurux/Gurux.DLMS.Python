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
#
from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ErrorCode
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from ..enums import ObjectType, DataType
from .enums import IecTwistedPairSetupMode, BaudRate

# pylint: disable=too-many-instance-attributes
class GXDLMSIecTwistedPairSetup(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSIecTwistedPairSetup
    """

    def __init__(self, ln=None, sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.IEC_HDLC_SETUP, ln, sn)
        # Working mode.
        self.mode = IecTwistedPairSetupMode.INACTIVE
        # Communication speed.
        self.speed = BaudRate.BAUDRATE_9600
        # List of Primary Station Addresses.
        self.primaryAddresses = list()
        # List of the TAB(i) for which the real equipment has been programmed
        # in the case of forgotten station call.
        self.tabis = list()

    def getValues(self):
        return [self.logicalName,
                self.mode,
                self.speed,
                self.primaryAddresses,
                self.tabis]

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
        #  Speed
        if all_ or self.canRead(3):
            attributes.append(3)
        #  PrimaryAddresses
        if all_ or self.canRead(4):
            attributes.append(4)
        #  Tabis
        if all_ or self.canRead(5):
            attributes.append(5)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 5

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 0

    def getDataType(self, index):
        if index == 1:
            return DataType.OCTET_STRING
        if index == 2:
            return DataType.ENUM
        if index == 3:
            return DataType.ENUM
        if index == 4:
            return DataType.ARRAY
        if index == 5:
            return DataType.ARRAY
        raise ValueError("getDataType failed. Invalid attribute index.")

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            return _GXCommon.logicalNameToBytes(self.logicalName)
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.mode = IecTwistedPairSetupMode(e.value)
        elif e.index == 3:
            self.speed = BaudRate(e.value)
        elif e.index == 4:
            self.primaryAddresses = []
            for it in e.value:
                self.primaryAddresses.append(it)
        elif e.index == 5:
            self.tabis = []
            for it in e.value:
                self.tabis.append(it)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.mode = IecTwistedPairSetupMode(reader.readElementContentAsInt("Mode"))
        self.speed = BaudRate(reader.readElementContentAsInt("Speed"))
        self.primaryAddresses = GXByteBuffer.hexToBytes(reader.readElementContentAsString("PrimaryAddresses"))
        self.tabis = GXByteBuffer.hexToBytes(reader.readElementContentAsString("Tabis"))

    def save(self, writer):
        writer.writeElementString("Mode", self.mode)
        writer.writeElementString("Speed", self.speed)
        writer.writeElementString("LN", GXByteBuffer.hex(self.primaryAddresses))
        if self.tabis:
            writer.writeElementString("LN", GXByteBuffer.hex(self.tabis))

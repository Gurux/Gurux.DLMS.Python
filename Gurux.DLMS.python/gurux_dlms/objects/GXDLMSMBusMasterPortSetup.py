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
from .enums import BaudRate

# pylint: disable=too-many-instance-attributes
class GXDLMSMBusMasterPortSetup(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSMBusMasterPortSetup
    """

    def __init__(self, ln=None, sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        super(GXDLMSMBusMasterPortSetup, self).__init__(ObjectType.MBUS_MASTER_PORT_SETUP, ln, sn)
        # The communication speed supported by the port.
        self.commSpeed = BaudRate.BAUDRATE_2400

    def getValues(self):
        return [self.logicalName,
                self.commSpeed]

    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  CommSpeed
        if all_ or self.canRead(2):
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
        return 0

    def getDataType(self, index):
        if index == 1:
            return DataType.OCTET_STRING
        if index == 2:
            return DataType.ENUM
        raise ValueError("getDataType failed. Invalid attribute index.")

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            return self.logicalName
        if e.index == 2:
            return self.commSpeed
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.commSpeed = BaudRate(e.value)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.commSpeed = BaudRate(reader.readElementContentAsInt("CommSpeed"))

    def save(self, writer):
        writer.writeElementString("CommSpeed", int(self.commSpeed))

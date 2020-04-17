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
#  Gurux Device Framework is Open Source software you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
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
class GXDLMSPrimeNbOfdmPlcMacSetup(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSPrimeNbOfdmPlcMacSetup
    """

    def __init__(self, ln="0.0.28.2.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.PRIME_NB_OFDM_PLC_MAC_SETUP, ln, sn)
        # PIB attribute 0x0010.
        self.macMinSwitchSearchTime = 0
        # PIB attribute 0x0011.
        self.macMaxPromotionPdu = 0
        # PIB attribute 0x0012.
        self.macPromotionPduTxPeriod = 0
        # PIB attribute 0x0013.
        self.macBeaconsPerFrame = 0
        # PIB attribute 0x0014.
        self.macScpMaxTxAttempts = 0
        # PIB attribute 0x0015.
        self.macCtlReTxTimer = 0
        # PIB attribute 0x0018.
        self.macMaxCtlReTx = 0

    def getValues(self):
        return [self.logicalName,
                self.macMinSwitchSearchTime,
                self.macMaxPromotionPdu,
                self.macPromotionPduTxPeriod,
                self.macBeaconsPerFrame,
                self.macScpMaxTxAttempts,
                self.macCtlReTxTimer,
                self.macMaxCtlReTx]

    #
    # Returns collection of attributes to read.  If attribute is static and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  MacMinSwitchSearchTime
        if all_ or self.canRead(2):
            attributes.append(2)
        #  MacMaxPromotionPdu
        if all_ or self.canRead(3):
            attributes.append(3)
        #  MacPromotionPduTxPeriod
        if all_ or self.canRead(4):
            attributes.append(4)
        #  MacBeaconsPerFrame
        if all_ or self.canRead(5):
            attributes.append(5)
        #  MacScpMaxTxAttempts
        if all_ or self.canRead(6):
            attributes.append(6)
        #  MacCtlReTxTimer
        if all_ or self.canRead(7):
            attributes.append(7)
        #  MacMaxCtlReTx
        if all_ or self.canRead(8):
            attributes.append(8)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 8

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 0

    def getDataType(self, index):
        if index == 1:
            return DataType.OCTET_STRING
        if index in (2, 3, 4, 5, 6, 7, 8):
            return DataType.UINT8
        raise ValueError("getDataType failed. Invalid attribute index.")

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.macMinSwitchSearchTime
        elif e.index == 3:
            ret = self.macMaxPromotionPdu
        elif e.index == 4:
            ret = self.macPromotionPduTxPeriod
        elif e.index == 5:
            ret = self.macBeaconsPerFrame
        elif e.index == 6:
            ret = self.macScpMaxTxAttempts
        elif e.index == 7:
            ret = self.macCtlReTxTimer
        elif e.index == 8:
            ret = self.macMaxCtlReTx
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
            self.macMinSwitchSearchTime = e.value
        elif e.index == 3:
            self.macMaxPromotionPdu = e.value
        elif e.index == 4:
            self.macPromotionPduTxPeriod = e.value
        elif e.index == 5:
            self.macBeaconsPerFrame = e.value
        elif e.index == 6:
            self.macScpMaxTxAttempts = e.value
        elif e.index == 7:
            self.macCtlReTxTimer = e.value
        elif e.index == 8:
            self.macMaxCtlReTx = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.macMinSwitchSearchTime = reader.readElementContentAsInt("MacMinSwitchSearchTime")
        self.macMaxPromotionPdu = reader.readElementContentAsInt("MacMaxPromotionPdu")
        self.macPromotionPduTxPeriod = reader.readElementContentAsInt("MacPromotionPduTxPeriod")
        self.macBeaconsPerFrame = reader.readElementContentAsInt("MacBeaconsPerFrame")
        self.macScpMaxTxAttempts = reader.readElementContentAsInt("MacScpMaxTxAttempts")
        self.macCtlReTxTimer = reader.readElementContentAsInt("MacCtlReTxTimer")
        self.macMaxCtlReTx = reader.readElementContentAsInt("MacMaxCtlReTx")

    def save(self, writer):
        writer.writeElementString("MacMinSwitchSearchTime", self.macMinSwitchSearchTime)
        writer.writeElementString("MacMaxPromotionPdu", self.macMaxPromotionPdu)
        writer.writeElementString("MacPromotionPduTxPeriod", self.macPromotionPduTxPeriod)
        writer.writeElementString("MacBeaconsPerFrame", self.macBeaconsPerFrame)
        writer.writeElementString("MacScpMaxTxAttempts", self.macScpMaxTxAttempts)
        writer.writeElementString("MacCtlReTxTimer", self.macCtlReTxTimer)
        writer.writeElementString("MacMaxCtlReTx", self.macMaxCtlReTx)

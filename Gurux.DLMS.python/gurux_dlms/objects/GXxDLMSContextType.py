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
from ..enums  import Conformance
from ..GXByteBuffer import GXByteBuffer

#pylint: disable=too-many-instance-attributes,too-few-public-methods, useless-object-inheritance
class GXxDLMSContextType(object):
    #
    # Constructor.
    #
    def __init__(self):
        # Server settings.
        self.__settings = None
        # Conformance.
        self.__conformance = Conformance.NONE
        # Maximum receive PDU size.
        self.__maxReceivePduSize = 0
        # Maximum Send PDU size.
        self.__maxSendPduSize = 0
        # DLMS Version Number.
        self.__dlmsVersionNumber = 0
        # Quality Of Service.
        self.qualityOfService = 0
        # CypheringInfo.
        self.cypheringInfo = []

    def __getConformance(self):
        if self.__settings:
            return self.__settings.proposedConformance
        return self.__conformance

    def __setConformance(self, value):
        if self.__settings:
            self.__settings.proposedConformance = value
        self.__conformance = value

    def __getMaxReceivePduSize(self):
        if self.__settings:
            return self.__settings.maxServerPDUSize
        return self.__maxReceivePduSize

    def __setMaxReceivePduSize(self, value):
        if self.__settings:
            self.__settings.maxServerPDUSize = value
        self.__maxReceivePduSize = value

    def __getMaxSendPduSize(self):
        if self.__settings:
            return self.__settings.maxServerPDUSize
        return self.__maxSendPduSize

    def __setMaxSendPduSize(self, value):
        if self.__settings:
            self.__settings.maxServerPDUSize = value
        self.__maxSendPduSize = value

    def __getDlmsVersionNumber(self):
        if self.__settings:
            return self.__settings.dlmsVersionNumber
        return self.__dlmsVersionNumber

    def __setDlmsVersionNumber(self, value):
        if self.__settings:
            self.__settings.dlmsVersionNumber = value
        self.__dlmsVersionNumber = value

    #Conformance
    conformance = property(__getConformance, __setConformance)

    maxReceivePduSize = property(__getMaxReceivePduSize, __setMaxReceivePduSize)

    maxSendPduSize = property(__getMaxSendPduSize, __setMaxSendPduSize)

    dlmsVersionNumber = property(__getDlmsVersionNumber, __setDlmsVersionNumber)

    def __str__(self):
        str_ = str(self.conformance) + " " + str(self.maxReceivePduSize) + " "
        str_ += str(self.maxSendPduSize) + " " + str(self.dlmsVersionNumber) + " "
        str_ += str(self.qualityOfService) + " " + GXByteBuffer.hex(self.cypheringInfo, True)
        return str_

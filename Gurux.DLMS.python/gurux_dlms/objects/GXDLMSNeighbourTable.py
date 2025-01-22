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
#  More information of Gurux products: http:#www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http:#www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
from gurux_dlms.objects.enums.GainResolution import GainResolution
from gurux_dlms.objects.enums.Modulation import Modulation


class GXDLMSNeighbourTable:
    """
    The neighbour table contains information about all the devices within the POS of the device
    """

    __shortAddress = None
    "MAC Short Address of the node."

    __enabled = None
    "Is Payload Modulation scheme used."

    __toneMap = ""
    "Frequency sub-band can be used for communication with the device."

    __modulation = Modulation.ROBUST_MODE
    "Modulation type."

    __txGain = None
    "Tx Gain."

    __txRes = GainResolution.D_B6
    "Tx Gain resolution."

    __txCoeff = ""
    "Transmitter gain for each group of tones represented by one valid bit of the tone map."

    __lqi = 0
    "Link Quality Indicator."

    __phaseDifferential = None
    "Phase difference in multiples of 60 degrees between the mains phase of the local node and the neighbour node."

    __tMRValidTime = 0
    "Remaining time in minutes until which the tone map response parameters in the neighbour table are considered valid."

    __neighbourValidTime = 0
    "Remaining time in minutes until which this entry in the neighbour table is considered valid."

    @property
    def shortAddress(self):
        """
        MAC Short Address of the node.
        """
        return self.__shortAddress

    @shortAddress.setter
    def shortAddress(self, value):
        self.__shortAddress = value

    @property
    def enabled(self):
        """
        Is Payload Modulation scheme used.
        """
        return self.__enabled

    @enabled.setter
    def enabled(self, value):
        self.__enabled = value

    @property
    def toneMap(self):
        """
        Frequency sub-band can be used for communication with the device.
        """
        return self.__toneMap

    @toneMap.setter
    def toneMap(self, value):
        self.__toneMap = value

    @property
    def modulation(self):
        """
        Modulation type.
        """
        return self.__modulation

    @modulation.setter
    def modulation(self, value):
        self.__modulation = value

    @property
    def txGain(self):
        """
        Tx Gain.
        """
        return self.__txGain

    @txGain.setter
    def txGain(self, value):
        self.__txGain = value

    @property
    def txRes(self):
        """
        Tx Gain resolution.
        """
        return self.__txRes

    @txRes.setter
    def txRes(self, value):
        self.__txRes = value

    @property
    def txCoeff(self):
        """
        Transmitter gain for each group of tones represented by one valid bit of the tone map.
        """
        return self.__txCoeff

    @txCoeff.setter
    def txCoeff(self, value):
        self.__txCoeff = value

    @property
    def lqi(self):
        """
        Link Quality Indicator.
        """
        return self.__lqi

    @lqi.setter
    def lqi(self, value):
        self.__lqi = value

    @property
    def phaseDifferential(self):
        """
        Phase difference in multiples of 60 degrees between the mains phase of the local node and the neighbour node.
        """
        return self.__phaseDifferential

    @phaseDifferential.setter
    def phaseDifferential(self, value):
        self.__phaseDifferential = value

    @property
    def tMRValidTime(self):
        """
        Remaining time in minutes until which the tone map response parameters in the neighbour table are considered valid.
        """
        return self.__tMRValidTime

    @tMRValidTime.setter
    def tMRValidTime(self, value):
        self.__tMRValidTime = value

    @property
    def neighbourValidTime(self):
        """
        Remaining time in minutes until which this entry in the neighbour table is considered valid.
        """
        return self.__neighbourValidTime

    @neighbourValidTime.setter
    def neighbourValidTime(self, value):
        self.__neighbourValidTime = value

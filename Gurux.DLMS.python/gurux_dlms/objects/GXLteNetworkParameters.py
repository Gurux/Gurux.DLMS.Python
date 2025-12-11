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
class GXLteNetworkParameters:
    """
    Network parameters for the LTE network
    """

    __t3402 = 0
    "T3402 timer in seconds."

    __t3412 = 0
    "T3412 timer in seconds."

    __t3412ext2 = 0
    "T3412ext2 timer in seconds."

    __t3324 = 0
    "Power saving mode active timer timer in 0,01 seconds."

    __teDRX = 0
    "Extended idle mode DRX cycle timer in 0,01 seconds."

    __tPTW = 0
    "DRX paging time window timer in seconds."

    __qRxlevMin = 0
    "The minimum required Rx level in the cell in dBm."

    __qRxlevMinCE = 0
    "The minimum required Rx level in enhanced coverage CE Mode A."

    __qRxLevMinCE1 = 0
    "The minimum required Rx level in enhanced coverage CE Mode B."

    @property
    def t3402(self):
        """
        T3402 timer in seconds.
        """
        return self.__t3402

    @t3402.setter
    def t3402(self, value):
        self.__t3402 = value

    @property
    def t3412(self):
        """
        T3412 timer in seconds.
        """
        return self.__t3412

    @t3412.setter
    def t3412(self, value):
        self.__t3412 = value

    @property
    def t3412ext2(self):
        """
        T3412ext2 timer in seconds.
        """
        return self.__t3412ext2

    @t3412ext2.setter
    def t3412ext2(self, value):
        self.__t3412ext2 = value

    @property
    def t3324(self):
        """
        Power saving mode active timer timer in 0,01 seconds.
        """
        return self.__t3324

    @t3324.setter
    def t3324(self, value):
        self.__t3324 = value

    @property
    def teDRX(self):
        """
        Extended idle mode DRX cycle timer in 0,01 seconds.
        """
        return self.__teDRX

    @teDRX.setter
    def teDRX(self, value):
        self.__teDRX = value

    @property
    def tPTW(self):
        """
        DRX paging time window timer in seconds.
        """
        return self.__tPTW

    @tPTW.setter
    def tPTW(self, value):
        self.__tPTW = value

    @property
    def qRxlevMin(self):
        """
        The minimum required Rx level in the cell in dBm.
        """
        return self.__qRxlevMin

    @qRxlevMin.setter
    def qRxlevMin(self, value):
        self.__qRxlevMin = value

    @property
    def qRxlevMinCE(self):
        """
        The minimum required Rx level in enhanced coverage CE Mode A.
        """
        return self.__qRxlevMinCE

    @qRxlevMinCE.setter
    def qRxlevMinCE(self, value):
        self.__qRxlevMinCE = value

    @property
    def qRxLevMinCE1(self):
        """
        The minimum required Rx level in enhanced coverage CE Mode B.
        """
        return self.__qRxLevMinCE1

    @qRxLevMinCE1.setter
    def qRxLevMinCE1(self, value):
        self.__qRxLevMinCE1 = value

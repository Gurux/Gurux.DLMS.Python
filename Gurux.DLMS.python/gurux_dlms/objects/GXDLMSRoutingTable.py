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
class GXDLMSRoutingTable:
    """
    G3-PLC 6LoWPAN routing table.
    """

    __destinationAddress = None
    __nextHopAddress = None
    __routeCost = None
    __hopCount = 0
    __weakLinkCount = 0
    __validTime = None

    @property
    def destinationAddress(self):
        """
        Address of the destination.
        """
        return self.__destinationAddress

    @destinationAddress.setter
    def destinationAddress(self, value):
        self.__destinationAddress = value

    @property
    def nextHopAddress(self):
        """
        Address of the next hop on the route towards the destination.
        """
        return self.__nextHopAddress

    @nextHopAddress.setter
    def nextHopAddress(self, value):
        self.__nextHopAddress = value

    @property
    def routeCost(self):
        """
        Cumulative link cost along the route towards the destination.
        """
        return self.__routeCost

    @routeCost.setter
    def routeCost(self, value):
        self.__routeCost = value

    @property
    def hopCount(self):
        """
        Number of hops of the selected route to the destination.
        """
        return self.__hopCount

    @hopCount.setter
    def hopCount(self, value):
        self.__hopCount = value

    @property
    def weakLinkCount(self):
        """
        Number of weak links to destination.
        """
        return self.__weakLinkCount

    @weakLinkCount.setter
    def weakLinkCount(self, value):
        self.__weakLinkCount = value

    @property
    def validTime(self):
        """
        Remaining time in minutes until when this entry in the routing table is considered valid.
        """
        return self.__validTime

    @validTime.setter
    def validTime(self, value):
        self.__validTime = value

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
class GXDLMSRoutingConfiguration:
    """
    The routing configuration element specifies all parameters linked to the routing mechanism described in ITU-T G.9903:2014.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.__netTraversalTime = 0
        self.__routingTableEntryTtl = 0
        self.__kr = 0
        self.__km = 0
        self.__kc = 0
        self.__kq = 0
        self.__kh = 0
        self.__krt = 0
        self.__rreqRetries = 0
        self.__rreqReqWait = 0
        self.__blacklistTableEntryTtl = 0
        self.__unicastRreqGenEnable = False
        self.__rlcEnabled = False
        self.__addRevLinkCost = 0

    @property
    def netTraversalTime(self):
        """
        Maximum time that a packet is expected to take to reach any node from any node in seconds.
        """
        return self.__netTraversalTime

    @netTraversalTime.setter
    def netTraversalTime(self, value):
        self.__netTraversalTime = value

    @property
    def routingTableEntryTtl(self):
        """
        Maximum time-to-live of a routing table entry (in minutes).
        """
        return self.__routingTableEntryTtl

    @routingTableEntryTtl.setter
    def routingTableEntryTtl(self, value):
        self.__routingTableEntryTtl = value

    @property
    def kr(self):
        """
        A weight factor for the Robust Mode to calculate link cost.
        """
        return self.__kr

    @kr.setter
    def kr(self, value):
        self.__kr = value

    @property
    def km(self):
        """
        A weight factor for modulation to calculate link cost.
        """
        return self.__km

    @km.setter
    def km(self, value):
        self.__km = value

    @property
    def kc(self):
        """
        A weight factor for number of active tones to calculate link cost.
        """
        return self.__kc

    @kc.setter
    def kc(self, value):
        self.__kc = value

    @property
    def kq(self):
        """
        A weight factor for LQI to calculate route cost.
        """
        return self.__kq

    @kq.setter
    def kq(self, value):
        self.__kq = value

    @property
    def kh(self):
        """
        A weight factor for hop to calculate link cost.
        """
        return self.__kh

    @kh.setter
    def kh(self, value):
        self.__kh = value

    @property
    def krt(self):
        """
        A weight factor for the number of active routes in the routing table to calculate link cost.
        """
        return self.__krt

    @krt.setter
    def krt(self, value):
        self.__krt = value

    @property
    def rreqRetries(self):
        """
        The number of RREQ retransmission in case of RREP reception time out.
        """
        return self.__rreqRetries

    @rreqRetries.setter
    def rreqRetries(self, value):
        self.__rreqRetries = value

    @property
    def rreqReqWait(self):
        """
        The number of seconds to wait between two consecutive RREQ � RERR generations.
        """
        return self.__rreqReqWait

    @rreqReqWait.setter
    def rreqReqWait(self, value):
        self.__rreqReqWait = value

    @property
    def blacklistTableEntryTtl(self):
        """
        Maximum time-to-live of a blacklisted neighbour entry (in minutes).
        """
        return self.__blacklistTableEntryTtl

    @blacklistTableEntryTtl.setter
    def blacklistTableEntryTtl(self, value):
        self.__blacklistTableEntryTtl = value

    @property
    def unicastRreqGenEnable(self):
        """
        If TRUE, the RREQ shall be generated with its 'unicast RREQ'.
        """
        return self.__unicastRreqGenEnable

    @unicastRreqGenEnable.setter
    def unicastRreqGenEnable(self, value):
        self.__unicastRreqGenEnable = value

    @property
    def rlcEnabled(self):
        """
        Enable the sending of RLCREQ frame by the device.
        """
        return self.__rlcEnabled

    @rlcEnabled.setter
    def rlcEnabled(self, value):
        self.__rlcEnabled = value

    @property
    def addRevLinkCost(self):
        """
        It represents an additional cost to take into account a possible asymmetry in the link.
        """
        return self.__addRevLinkCost

    @addRevLinkCost.setter
    def addRevLinkCost(self, value):
        self.__addRevLinkCost = value

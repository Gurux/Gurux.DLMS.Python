#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename:        $HeadURL$
#
#  Version:         $Revision$,
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
from ..GXIntEnum import GXIntEnum

class InterfaceType(GXIntEnum):
    """InterfaceType enumerates the usable types of connection in GuruxDLMS."""
    #pylint: disable=too-few-public-methods

    # General interface type is used for meters that support IEC 62056-46 Data link layer using HDLC protocol.
    HDLC = 0
    # Network interface type is used for meters that support IEC 62056-47 COSEM transport layers for IPv4 networks.
    WRAPPER = 1
    # Plain PDU is returned.
    PDU = 2
    # EN 13757-4/-5 Wireless M-Bus profile is used.
    WIRELESS_MBUS = 3
    # IEC 62056-21 E-Mode is used to initialize communication before moving to HDLC protocol.
    HDLC_WITH_MODE_E = 4
    #PLC Logical link control (LLC) profile is used with IEC 61334-4-32 connectionless LLC sublayer.
    PLC = 5
    # PLC Logical link control (LLC) profile is used with HDLC.
    PLC_HDLC = 6
    # LowPower Wide Area Networks (LPWAN) profile is used.
    LPWAN = 7
    # Wi-SUN FAN mesh network is used.
    WI_SUN = 8
    # OFDM PLC PRIME is defined in IEC 62056-8-4.
    PLC_PRIME = 9
    # EN 13757-2 wired (twisted pair based) M-Bus scheme is used.
    WIRED_MBUS = 10

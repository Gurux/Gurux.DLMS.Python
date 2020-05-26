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
from gurux_dlms.GXIntEnum import GXIntEnum

class ServiceType(GXIntEnum):
    """
    Type of service used to push the data.
    """
    #pylint: disable=too-few-public-methods

    #
    # Transport service type is TCP/IP.
    #
    TCP = 0
    #
    # Transport service type is UDP.
    #
    UDP = 1
    #
    # Transport service type is FTP.
    #
    FTP = 2
    #
    # Transport service type is SMTP.
    #
    SMTP = 3
    #
    # Transport service type is SMS.
    #
    SMS = 4
    #
    # Transport service type is HDLC.
    #
    HDLC = 5
    #
    # Transport service type is MBUS.
    #
    M_BUS = 6
    #
    # Transport service type is ZigBee.
    #
    ZIGBEE = 7

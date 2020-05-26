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

class BaudRate(GXIntEnum):
    """
    Defines the baud rates.
    """
    #pylint: disable=too-few-public-methods

    #
    # Baudrate is 300.
    #
    BAUDRATE_300 = 0

    #
    # Baudrate is 600.
    #
    BAUDRATE_600 = 1

    #
    # Baudrate is 1200.
    #
    BAUDRATE_1200 = 2

    #
    # Baudrate is 2400.
    #
    BAUDRATE_2400 = 3

    #
    # Baudrate is 4800.
    #
    BAUDRATE_4800 = 4

    #
    # Baudrate is 9600.
    #
    BAUDRATE_9600 = 5

    #
    # Baudrate is 19200.
    #
    BAUDRATE_19200 = 6

    #
    # Baudrate is 38400.
    #
    BAUDRATE_38400 = 7

    #
    # Baudrate is 57600.
    #
    BAUDRATE_57600 = 8

    #
    # Baudrate is 115200.
    #
    BAUDRATE_115200 = 9

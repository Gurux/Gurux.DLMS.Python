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

class ControlMode(GXIntEnum):
    """
    Configures the behaviour of the disconnect control object for all
    triggers, i.e.  the possible state transitions.
    """
    #pylint: disable=too-few-public-methods

    #
    # The disconnect control object is always in 'connected' state,
    #
    NONE = 0
    #
    # Disconnection: Remote =b, c manual =f local =g) Reconnection: Remote
    #  =d manual =e).
    #
    MODE_1 = 1
    #
    # Disconnection: Remote =b, c manual =f local =g) Reconnection: Remote
    #  =a manual =e).
    #
    MODE_2 = 2
    #
    # Disconnection: Remote =b, c manual =- local =g) Reconnection: Remote
    #  =d manual =e).
    #
    MODE_3 = 3
    #
    # Disconnection: Remote =b, c manual =- local =g) Reconnection: Remote
    #  =a manual =e)
    #
    MODE_4 = 4
    #
    # Disconnection: Remote =b, c manual =f local =g) Reconnection: Remote
    #  =d manual =e local =h
    #
    MODE_5 = 5
    #
    # Disconnection: Remote =b, c manual =- local =g) Reconnection: Remote
    #  =d manual =e local =h)
    #
    MODE_6 = 6

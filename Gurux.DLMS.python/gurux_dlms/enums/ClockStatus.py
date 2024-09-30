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
#  Copyright =c) Gurux Ltd
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
from ..GXIntFlag import GXIntFlag

class ClockStatus(GXIntFlag):
    """Defines Clock status."""
    #pylint: disable=too-few-public-methods

    # OK.
    OK = 0

    # Invalid value.
    INVALID_VALUE = 0x1

    # Doubtful b value.
    DOUBTFUL_VALUE = 0x2

    # Different clock base c.
    DIFFERENT_CLOCK_BASE = 0X4

    # Invalid clock status d.
    INVALID_CLOCK_STATUS = 0x8

    # Reserved.
    RESERVED2 = 0x10

    # Reserved.
    RESERVED3 = 0x20

    # Reserved.
    RESERVED4 = 0x40

    # Daylight saving active.
    DAYLIGHT_SAVE_ACTIVE = 0x80

    # Clock status is skipped.
    #pylint: disable=W0213
    SKIPPED = 0xFF

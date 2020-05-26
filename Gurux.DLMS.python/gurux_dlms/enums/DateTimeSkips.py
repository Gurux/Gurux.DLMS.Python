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
#  Copyright =c Gurux Ltd
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

class DateTimeSkips(GXIntFlag):
    """Enumerated date time skipped fields."""
    #pylint: disable=too-few-public-methods

     # Nothing is skipped from date time.
    NONE = 0

     # Year part of date time is skipped.
    YEAR = 1

     # Month part of date time is skipped.
    MONTH = 2

     # Day part is skipped.
    DAY = 4

     # Day of week part of date time is skipped.
    DAY_OF_WEEK = 8

     # Hours part of date time is skipped.
    HOUR = 0x10

     # Minute part of date time is skipped.
    MINUTE = 0x20

     # Second part of date time is skipped.
    SECOND = 0x40

     # Hundreds of seconds part of date time is skipped.
    MILLISECOND = 0x80

     # Devitation is not used.
    DEVITATION = 0x100

     # Status is not used.
    STATUS = 0x200

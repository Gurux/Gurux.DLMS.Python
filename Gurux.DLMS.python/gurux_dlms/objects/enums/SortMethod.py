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

class SortMethod(GXIntEnum):
    """
    Sort methods.
    """
    #pylint: disable=too-few-public-methods

    #
    # First in first out When circle buffer is full first item is removed.
    #
    FIFO = 1

    #
    # Last in first out.  When circle buffer is full last item is removed.
    #
    LIFO = 2

    #
    # Largest is first.
    #
    LARGEST = 3

    #
    # Smallest is first.
    #
    SMALLEST = 4

    #
    # Nearest to zero is first.
    #
    NEAREST_TO_ZERO = 5

    #
    # Farest from zero is first.
    #
    FAREST_FROM_ZERO = 6

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

class ErrorCode(GXIntEnum):
    """Enumerates all DLMS error codes.
    https://www.gurux.fi/Gurux.DLMS.ErrorCodes
    """
    #pylint: disable=too-few-public-methods

    DISCONNECT_MODE = -4

    RECEIVE_NOT_READY = -3

    REJECTED = -2

    UNACCEPTABLE_FRAME = -1

    OK = 0

    HARDWARE_FAULT = 1

    TEMPORARY_FAILURE = 2

    READ_WRITE_DENIED = 3

    UNDEFINED_OBJECT = 4

    INCONSISTENT_CLASS = 9

    UNAVAILABLE_OBJECT = 11

    UNMATCHED_TYPE = 12

    ACCESS_VIOLATED = 13

    DATA_BLOCK_UNAVAILABLE = 14

    LONG_GET_OR_READ_ABORTED = 15

    NO_LONG_GET_OR_READ_IN_PROGRESS = 16

    LONG_SET_OR_WRITE_ABORTED = 17

    NO_LONG_SET_OR_WRITE_IN_PROGRESS = 18

    DATA_BLOCK_NUMBER_INVALID = 19

    OTHER_REASON = 250

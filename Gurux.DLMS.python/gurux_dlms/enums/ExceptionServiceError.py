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
from ..GXIntEnum import GXIntEnum

class ExceptionServiceError(GXIntEnum):
    """DLMS service errors."""
    #pylint: disable=too-few-public-methods
    # Operation is not possible.
    OPERATION_NOT_POSSIBLE = 1
    # Service is not supported.
    SERVICE_NOT_SUPPORTED = 2
    # Other reason.
    OTHER_REASON = 3
    # PDU is too long.
    PDU_TOO_LONG = 4
    # Ciphering failed.
    DECIPHERING_ERROR = 5
    # Invocation counter is invalid.
    INVOCATION_COUNTER_ERROR = 6

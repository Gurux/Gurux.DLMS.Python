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

class SourceDiagnostic(GXIntEnum):
    """SourceDiagnostic enumerates the error codes for reasons that can
    cause the server to reject the client."""
    #pylint: disable=too-few-public-methods

    NONE = 0

    NO_REASON_GIVEN = 1

    NOT_SUPPORTED = 2

    CALLING_AP_TITLE_NOT_RECOGNIZED = 3

    CALLING_AP_INVOCATION_IDENTIFIER_NOT_RECOGNIZED = 4

    CALLING_AE_QUALIFIER_NOT_RECOGNIZED = 5

    CALLING_AE_INVOCATION_IDENTIFIER_NOT_RECOGNIZED = 6

    CALLED_AP_TITLE_NOT_RECOGNIZED = 7

    CALLED_AP_INVOCATION_IDENTIFIER_NOT_RECOGNIZED = 8

    CALLED_AE_QUALIFIER_NOT_RECOGNIZED = 9

    CALLED_AE_INVOCATION_IDENTIFIER_NOT_RECOGNIZED = 10

    NOT_RECOGNISED = 11

    MECHANISM_NAME_REGUIRED = 12

    AUTHENTICATION_FAILURE = 13

    AUTHENTICATION_REQUIRED = 14

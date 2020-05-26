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

class PduType(GXIntEnum):
    """APDU types."""
    #pylint: disable=too-few-public-methods

    # IMPLICIT BIT STRING {version1 = 0)} DEFAULT {version1}
    PROTOCOL_VERSION = 0

    # Application-context-name
    APPLICATION_CONTEXT_NAME = 1

    # AP-title OPTIONAL
    CALLED_AP_TITLE = 2

    # AE-qualifier OPTIONAL.
    CALLED_AE_QUALIFIER = 3

    # AP-invocation-identifier OPTIONAL.
    CALLED_AP_INVOCATION_ID = 4

    # AE-invocation-identifier OPTIONAL
    CALLED_AE_INVOCATION_ID = 5

    # AP-title OPTIONAL
    CALLING_AP_TITLE = 6

    # AE-qualifier OPTIONAL
    CALLING_AE_QUALIFIER = 7

    # AP-invocation-identifier OPTIONAL
    CALLING_AP_INVOCATION_ID = 8

    # AE-invocation-identifier OPTIONAL
    CALLING_AE_INVOCATION_ID = 9

    # The following field shall not be present if only the kernel is used.
    SENDER_ACSE_REQUIREMENTS = 10

    # The following field shall only be present if the authentication
    # functional unit is selected.
    MECHANISM_NAME = 11

    # The following field shall only be present if the authentication
    # functional unit is selected.
    CALLING_AUTHENTICATION_VALUE = 12

    # Implementation-data.
    IMPLEMENTATION_INFORMATION = 29

    # Association-information OPTIONAL.
    USER_INFORMATION = 30

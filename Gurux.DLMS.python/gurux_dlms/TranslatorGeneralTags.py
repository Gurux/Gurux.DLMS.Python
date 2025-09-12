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


class TranslatorGeneralTags(GXIntEnum):
    APPLICATION_CONTEXT_NAME = 0xA1
    NEGOTIATED_QUALITY_OF_SERVICE = 0xBE00
    PROPOSED_DLMS_VERSION_NUMBER = 0xBE01
    PROPOSED_MAX_PDU_SIZE = 0xBE02
    PROPOSED_CONFORMANCE = 0xBE03
    VAA_NAME = 0xBE04
    NEGOTIATED_CONFORMANCE = 0xBE05
    NEGOTIATED_DLMS_VERSION_NUMBER = 0xBE06
    NEGOTIATED_MAX_PDU_SIZE = 0xBE07
    CONFORMANCE_BIT = 0xBE08
    PROPOSED_QUALITY_OF_SERVICE = 0xBE09
    SENDER_ACSE_REQUIREMENTS = 0x8A
    RESPONDER_ACSE_REQUIREMENT = 0x88
    RESPONDING_MECHANISM_NAME = 0x89
    CALLING_MECHANISM_NAME = 0x8B
    CALLING_AUTHENTICATION = 0xAC
    RESPONDING_AUTHENTICATION = 0x80
    ASSOCIATION_RESULT = 0xA2
    RESULT_SOURCE_DIAGNOSTIC = 0xA3
    ACSE_SERVICE_USER = 0xA301
    RESPONDING_AP_TITLE = 0xA4
    DEDICATED_KEY = 0xA8
    CALLING_AP_TITLE = 0xA6
    CALLING_AE_INVOCATION_ID = 0xA9
    CALLED_AE_INVOCATION_ID = 0xA5
    RESPONDING_AE_INVOCATION_ID = 0xA7
    CHAR_STRING = 0xAA
    USER_INFORMATION = 0xAB
    RESPONDING_AE_INVOCATION_ID = 0xAD
    PRIME_NEW_DEVICE_NOTIFICATION = 0xAE
    PRIME_REMOVE_DEVICE_NOTIFICATION = 0xAF
    PRIME_START_REPORTING_METERS = 0xB0
    PRIME_DELETE_METERS = 0xB1
    PRIME_ENABLE_AUTO_CLOSE = 0xB2
    PRIME_DISABLE_AUTO_CLOSE = 0xB3

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

class TranslatorTags(GXIntEnum):
    WRAPPER = 0xFF01
    HDLC = 0xFF02
    PDU_DLMS = 0xFF03
    TARGET_ADDRESS = 0xFF04
    SOURCE_ADDRESS = 0xFF05
    LIST_OF_VARIABLE_ACCESS_SPECIFICATION = 0xFF06
    LIST_OF_DATA = 0xFF07
    SUCCESS = 0xFF08
    DATA_ACCESS_ERROR = 0xFF09
    ATTRIBUTE_DESCRIPTOR = 0xFF0A
    CLASS_ID = 0xFF0B
    INSTANCE_ID = 0xFF0C
    ATTRIBUTE_ID = 0xFF0D
    METHOD_INVOCATION_PARAMETERS = 0xFF0E
    SELECTOR = 0xFF0F
    PARAMETER = 0xFF10
    LAST_BLOCK = 0xFF11
    BLOCK_NUMBER = 0xFF12
    RAW_DATA = 0xFF13
    METHOD_DESCRIPTOR = 0xFF14
    METHOD_ID = 0xFF15
    RESULT = 0xFF16
    RETURN_PARAMETERS = 0xFF17
    ACCESS_SELECTION = 0xFF18
    VALUE = 0xFF19
    ACCESS_SELECTOR = 0xFF1A
    ACCESS_PARAMETERS = 0xFF1B
    ATTRIBUTE_DESCRIPTOR_LIST = 0xFF1C
    ATTRIBUTE_DESCRIPTOR_WITH_SELECTION = 0xFF1D
    READ_DATA_BLOCK_ACCESS = 0xFF1E
    WRITE_DATA_BLOCK_ACCESS = 0xFF1F
    DATA = 0xFF20
    INVOKE_ID = 0xFF21
    DATE_TIME = 0xFF22
    REASON = 0xFF23
    VARIABLE_ACCESS_SPECIFICATION = 0xFF24
    PDU_CSE = 0xFF26
    CHOICE = 0xFF27
    LONG_INVOKE_ID = 0xFF28
    NOTIFICATION_BODY = 0xFF29
    DATA_VALUE = 0xFF30
    ACCESS_REQUEST_BODY = 0xFF31
    LIST_OF_ACCESS_REQUEST_SPECIFICATION = 0xFF32
    ACCESS_REQUEST_SPECIFICATION = 0xFF33
    ACCESS_REQUEST_LIST_OF_DATA = 0xFF34
    ACCESS_RESPONSE_BODY = 0xFF35
    LIST_OF_ACCESS_RESPONSE_SPECIFICATION = 0xFF36
    ACCESS_RESPONSE_SPECIFICATION = 0xFF37
    ACCESS_RESPONSE_LIST_OF_DATA = 0xFF38
    SINGLE_RESPONSE = 0xFF39
    SERVICE = 0xFF40
    SERVICE_ERROR = 0xFF41
    INITIATE_ERROR = 0xFF42
    CIPHERED_SERVICE = 0xFF43
    SYSTEM_TITLE = 0xFF44
    DATA_BLOCK = 0xFF45
    TRANSACTION_ID = 0xFF46
    ORIGINATOR_SYSTEM_TITLE = 0xFF47
    RECIPIENT_SYSTEM_TITLE = 0xFF48
    OTHER_INFORMATION = 0xFF49
    KEY_INFO = 0xFF50
    AGREED_KEY = 0xFF51
    KEY_PARAMETERS = 0xFF52
    KEY_CIPHERED_DATA = 0xFF53
    CIPHERED_CONTENT = 0xFF54
    ATTRIBUTE_VALUE = 0xFF55
    CURRENT_TIME = 0xFF56
    TIME = 0xFF57
    MAX_INFO_RX = 0xFF58
    MAX_INFO_TX = 0xFF59
    WINDOW_SIZE_RX = 0xFF60
    WINDOW_SIZE_TX = 0xFF61
    VALUE_LIST = 0xFF62
    DATA_ACCESS_RESULT = 0xFF63
    FRAME_TYPE = 0xFF64
    BLOCK_CONTROL = 0xFF65
    BLOCK_NUMBER_ACK = 0xFF66
    BLOCK_DATA = 0xFF67
    CONTENTS_DESCRIPTION = 0xFF68
    ARRAY_CONTENTS = 0xFF69
    NETWORK_ID = 0xFF7A
    PHYSICAL_DEVICE_ADDRESS = 0xFF7B
    PROTOCOL_VERSION = 0xFF7C
    CALLED_AP_TITLE = 0xFF7D
    CALLED_AP_INVOCATION_ID = 0xFF7E
    CALLED_AE_INVOCATION_ID = 0xFF7F
    CALLING_AP_INVOCATION_ID = 0xFF80
    CALLED_AE_QUALIFIER = 0xFF81
    RESPONSE_ALLOWED = 0xFF82
    EXCEPTION_RESPONSE = 0xFF83
    STATE_ERROR = 0xFF84
    P_BLOCK = 0xFF85
    CONTENT = 0xFF86
    SIGNATURE = 0xFF87

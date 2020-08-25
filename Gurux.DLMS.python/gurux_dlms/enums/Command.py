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

class Command(GXIntEnum):
    """DLMS commands."""

    #
    # No command to execute.
    #
    NONE = 0

    #
    # Initiate request.
    #
    INITIATE_REQUEST = 0x1

    #
    # Initiate response.
    #
    INITIATE_RESPONSE = 0x8

    #
    # Read request.
    #
    READ_REQUEST = 0x5

    #
    # Read response.
    #
    READ_RESPONSE = 0xC

    #
    # Write request.
    #
    WRITE_REQUEST = 0x6

    #
    # Write response.
    #
    WRITE_RESPONSE = 0xD

    #
    # Get request.
    #
    GET_REQUEST = 0xC0

    #
    # Get response.
    #
    GET_RESPONSE = 0xC4

    #
    # Set request.
    #
    SET_REQUEST = 0xC1

    #
    # Set response.
    #
    SET_RESPONSE = 0xC5

    #
    # Action request.
    #
    METHOD_REQUEST = 0xC3

    #
    # Action response.
    #
    METHOD_RESPONSE = 0xC7

    #
    # HDLC Disconnect Mode.
    #
    DISCONNECT_MODE = 0x1F

    #
    # HDLC Unacceptable frame.
    #
    UNACCEPTABLE_FRAME = 0x97

    #
    # HDLC SNRM request.
    #
    SNRM = 0x93

    #
    # HDLC UA request.
    #
    UA = 0x73

    #
    # AARQ request.
    #
    AARQ = 0x60

    #
    # AARE request.
    #
    AARE = 0x61

    #
    # Disconnect request for HDLC framing.
    #
    DISCONNECT_REQUEST = 0x53

    #
    # Release request.
    #
    RELEASE_REQUEST = 0x62

    #
    # Disconnect response.
    #
    RELEASE_RESPONSE = 0x63

    #
    # Confirmed Service Error.
    #
    CONFIRMED_SERVICE_ERROR = 0x0E

    #
    # Exception Response.
    #
    EXCEPTION_RESPONSE = 0xD8

    #
    # General Block Transfer.
    #
    GENERAL_BLOCK_TRANSFER = 0xE0

    #
    # Access Request.
    #
    ACCESS_REQUEST = 0xD9

    #
    # Access Response.
    #
    ACCESS_RESPONSE = 0xDA

    #
    # Data Notification request.
    #
    DATA_NOTIFICATION = 0x0F

    #
    # Glo get request.
    #
    GLO_GET_REQUEST = 0xC8

    #
    # Glo get response.
    #
    GLO_GET_RESPONSE = 0xCC

    #
    # Glo set request.
    #
    GLO_SET_REQUEST = 0xC9

    #
    # Glo set response.
    #
    GLO_SET_RESPONSE = 0xCD

    #
    # Glo event notification.
    #
    GLO_EVENT_NOTIFICATION = 0xCA

    #
    # Glo method request.
    #
    GLO_METHOD_REQUEST = 0xCB

    #
    # Glo method response.
    #
    GLO_METHOD_RESPONSE = 0xCF

    #
    # Glo Initiate request.
    #
    GLO_INITIATE_REQUEST = 0x21

    #
    # Glo read request.
    #
    GLO_READ_REQUEST = 37

    #
    # Glo write request.
    #
    GLO_WRITE_REQUEST = 38

    #
    # Glo Initiate response.
    #
    GLO_INITIATE_RESPONSE = 40

    #
    # Glo read response.
    #
    GLO_READ_RESPONSE = 44

    #
    # Glo write response.
    #
    GLO_WRITE_RESPONSE = 45

    #
    # Ded confirmed service error.
    #
    GLO_CONFIRMED_SERVICE_ERROR = 46

    #
    # General GLO ciphering.
    #
    GENERAL_GLO_CIPHERING = 0xDB

    #
    # General DED ciphering.
    #
    GENERAL_DED_CIPHERING = 0xDC

    #
    # General ciphering.
    #
    GENERAL_CIPHERING = 0xDD

    #
    # Information Report request.
    #
    INFORMATION_REPORT = 0x18

    #
    # Event Notification request.
    #
    EVENT_NOTIFICATION = 0xC2

    #
    # Ded initiate request.
    #
    DED_INITIATE_REQUEST = 65

    #
    # Ded read request.
    #
    DED_READ_REQUEST = 69

    #
    # Ded write request.
    #
    DED_WRITE_REQUEST = 70

    #
    # Ded initiate response.
    #
    DED_INITIATE_RESPONSE = 72

    #
    # Ded read response.
    #
    DED_READ_RESPONSE = 76

    #
    # Ded write response.
    #
    DED_WRITE_RESPONSE = 77

    #
    # Ded confirmed service error.
    #
    DED_CONFIRMED_SERVICE_ERROR = 78

    #
    # Ded confirmed write request.
    #
    DED_UNCONFIRMED_WRITE_REQUEST = 86

    #
    # Ded information report request.
    #
    DED_INFORMATION_REPORT_REQUEST = 88

    #
    # Ded get request.
    #
    DED_GET_REQUEST = 0xD0

    #
    # Ded get response.
    #
    DED_GET_RESPONSE = 0xD4

    #
    # Ded set request.
    #
    DED_SET_REQUEST = 0xD1

    #
    # Ded set response.
    #
    DED_SET_RESPONSE = 0xD5

    #
    # Ded event notification request.
    #
    DED_EVENT_NOTIFICATION = 0xD2

    #
    # Ded method request.
    #
    DED_METHOD_REQUEST = 0xD3

    #
    # Ded method response.
    #
    DED_METHOD_RESPONSE = 0xD7

    #
    # Request message from client to gateway.
    #
    GATEWAY_REQUEST = 0xE6

    #
    # Response message from gateway to client.
    #
    GATEWAY_RESPONSE = 0xE7

    @classmethod
    def toString(cls, value):
        str_ = None
        if value == Command.NONE:
            str_ = "None"
        elif value == Command.INITIATE_REQUEST:
            str_ = "InitiateRequest"
        elif value == Command.INITIATE_RESPONSE:
            str_ = "InitiateResponse"
        elif value == Command.READ_REQUEST:
            str_ = "ReadRequest"
        elif value == Command.READ_RESPONSE:
            str_ = "ReadResponse"
        elif value == Command.WRITE_REQUEST:
            str_ = "WriteRequest"
        elif value == Command.WRITE_RESPONSE:
            str_ = "WriteResponse"
        elif value == Command.GET_REQUEST:
            str_ = "GetRequest"
        elif value == Command.GET_RESPONSE:
            str_ = "GetResponse"
        elif value == Command.SET_REQUEST:
            str_ = "SetRequest"
        elif value == Command.SET_RESPONSE:
            str_ = "SetResponse"
        elif value == Command.METHOD_REQUEST:
            str_ = "MethodRequest"
        elif value == Command.METHOD_RESPONSE:
            str_ = "MethodResponse"
        elif value == Command.UNACCEPTABLE_FRAME:
            str_ = "UnacceptableFrame"
        elif value == Command.SNRM:
            str_ = "Snrm"
        elif value == Command.UA:
            str_ = "Ua"
        elif value == Command.AARQ:
            str_ = "Aarq"
        elif value == Command.AARE:
            str_ = "Aare"
        elif value == Command.DISCONNECT_REQUEST:
            str_ = "Disc"
        elif value == Command.RELEASE_REQUEST:
            str_ = "DisconnectRequest"
        elif value == Command.RELEASE_RESPONSE:
            str_ = "DisconnectResponse"
        elif value == Command.CONFIRMED_SERVICE_ERROR:
            str_ = "ConfirmedServiceError"
        elif value == Command.EXCEPTION_RESPONSE:
            str_ = "ExceptionResponse"
        elif value == Command.GENERAL_BLOCK_TRANSFER:
            str_ = "GeneralBlockTransfer"
        elif value == Command.ACCESS_REQUEST:
            str_ = "AccessRequest"
        elif value == Command.ACCESS_RESPONSE:
            str_ = "AccessResponse"
        elif value == Command.DATA_NOTIFICATION:
            str_ = "DataNotification"
        elif value == Command.GLO_GET_REQUEST:
            str_ = "GloGetRequest"
        elif value == Command.GLO_GET_RESPONSE:
            str_ = "GloGetResponse"
        elif value == Command.GLO_SET_REQUEST:
            str_ = "GloSetRequest"
        elif value == Command.GLO_SET_RESPONSE:
            str_ = "GloSetResponse"
        elif value == Command.GLO_EVENT_NOTIFICATION:
            str_ = "GloEventNotification"
        elif value == Command.GLO_METHOD_REQUEST:
            str_ = "GloMethodRequest"
        elif value == Command.GLO_METHOD_RESPONSE:
            str_ = "GloMethodResponse"
        elif value == Command.GLO_INITIATE_REQUEST:
            str_ = "GloInitiateRequest"
        elif value == Command.GLO_READ_REQUEST:
            str_ = "GloReadRequest"
        elif value == Command.GLO_WRITE_REQUEST:
            str_ = "GloWriteRequest"
        elif value == Command.GLO_INITIATE_RESPONSE:
            str_ = "GloInitiateResponse"
        elif value == Command.GLO_READ_RESPONSE:
            str_ = "GloReadResponse"
        elif value == Command.GLO_WRITE_RESPONSE:
            str_ = "GloWriteResponse"
        elif value == Command.GENERAL_GLO_CIPHERING:
            str_ = "GeneralGloCiphering"
        elif value == Command.GENERAL_DED_CIPHERING:
            str_ = "GeneralDedCiphering"
        elif value == Command.GENERAL_CIPHERING:
            str_ = "GeneralCiphering"
        elif value == Command.INFORMATION_REPORT:
            str_ = "InformationReport"
        elif value == Command.EVENT_NOTIFICATION:
            str_ = "EventNotification"
        elif value == Command.DED_GET_REQUEST:
            str_ = "DedGetRequest"
        elif value == Command.DED_GET_RESPONSE:
            str_ = "DedGetResponse"
        elif value == Command.DED_SET_REQUEST:
            str_ = "DedSetRequest"
        elif value == Command.DED_SET_RESPONSE:
            str_ = "DedSetResponse"
        elif value == Command.DED_EVENT_NOTIFICATION:
            str_ = "DedEventNotification"
        elif value == Command.DED_METHOD_REQUEST:
            str_ = "DedMethodRequest"
        elif value == Command.GATEWAY_REQUEST:
            str_ = "GatewayRequest "
        elif value == Command.GATEWAY_RESPONSE:
            str_ = "GatewayResponse "
        else:
            raise ValueError(str(value))
        return str_

    @classmethod
    def value_of(cls, value):
        if "None".lower() == value.lower():
            ret = Command.NONE
        elif "InitiateRequest".lower() == value.lower():
            ret = Command.INITIATE_REQUEST
        elif "InitiateResponse".lower() == value.lower():
            ret = Command.INITIATE_RESPONSE
        elif "ReadRequest".lower() == value.lower():
            ret = Command.READ_REQUEST
        elif "ReadResponse".lower() == value.lower():
            ret = Command.READ_RESPONSE
        elif "WriteRequest".lower() == value.lower():
            ret = Command.WRITE_REQUEST
        elif "WriteRequest".lower() == value.lower():
            ret = Command.WRITE_RESPONSE
        elif "WriteResponse".lower() == value.lower():
            ret = Command.WRITE_RESPONSE
        elif "GetRequest".lower() == value.lower():
            ret = Command.GET_REQUEST
        elif "GetResponse".lower() == value.lower():
            ret = Command.GET_RESPONSE
        elif "SetRequest".lower() == value.lower():
            ret = Command.SET_REQUEST
        elif "SetResponse".lower() == value.lower():
            ret = Command.SET_RESPONSE
        elif "MethodRequest".lower() == value.lower():
            ret = Command.METHOD_REQUEST
        elif "MethodResponse".lower() == value.lower():
            ret = Command.METHOD_RESPONSE
        elif "UnacceptableFrame".lower() == value.lower():
            ret = Command.UNACCEPTABLE_FRAME
        elif "Snrm".lower() == value.lower():
            ret = Command.SNRM
        elif "Ua".lower() == value.lower():
            ret = Command.UA
        elif "Aarq".lower() == value.lower():
            ret = Command.AARQ
        elif "Aare".lower() == value.lower():
            ret = Command.AARE
        elif "Disc".lower() == value.lower():
            ret = Command.DISCONNECT_REQUEST
        elif "DisconnectRequest".lower() == value.lower():
            ret = Command.RELEASE_REQUEST
        elif "DisconnectResponse".lower() == value.lower():
            ret = Command.RELEASE_RESPONSE
        elif "ConfirmedServiceError".lower() == value.lower():
            ret = Command.CONFIRMED_SERVICE_ERROR
        elif "ExceptionResponse".lower() == value.lower():
            ret = Command.EXCEPTION_RESPONSE
        elif "GeneralBlockTransfer".lower() == value.lower():
            ret = Command.GENERAL_BLOCK_TRANSFER
        elif "AccessRequest".lower() == value.lower():
            ret = Command.ACCESS_REQUEST
        elif "AccessResponse".lower() == value.lower():
            ret = Command.ACCESS_RESPONSE
        elif "DataNotification".lower() == value.lower():
            ret = Command.DATA_NOTIFICATION
        elif "GloGetRequest".lower() == value.lower():
            ret = Command.GLO_GET_REQUEST
        elif "GloGetResponse".lower() == value.lower():
            ret = Command.GLO_GET_RESPONSE
        elif "GloSetRequest".lower() == value.lower():
            ret = Command.GLO_SET_REQUEST
        elif "GloSetResponse".lower() == value.lower():
            ret = Command.GLO_SET_RESPONSE
        elif "GloEventNotification".lower() == value.lower():
            ret = Command.GLO_EVENT_NOTIFICATION
        elif "GloMethodRequest".lower() == value.lower():
            ret = Command.GLO_METHOD_REQUEST
        elif "GloMethodResponse".lower() == value.lower():
            ret = Command.GLO_METHOD_RESPONSE
        elif "GloInitiateRequest".lower() == value.lower():
            ret = Command.GLO_INITIATE_REQUEST
        elif "GloReadRequest".lower() == value.lower():
            ret = Command.GLO_READ_REQUEST
        elif "GloWriteRequest".lower() == value.lower():
            ret = Command.GLO_WRITE_REQUEST
        elif "GloInitiateResponse".lower() == value.lower():
            ret = Command.GLO_INITIATE_RESPONSE
        elif "GloReadResponse".lower() == value.lower():
            ret = Command.GLO_READ_RESPONSE
        elif "GloWriteResponse".lower() == value.lower():
            ret = Command.GLO_WRITE_RESPONSE
        elif "GeneralGloCiphering".lower() == value.lower():
            ret = Command.GENERAL_GLO_CIPHERING
        elif "GeneralDedCiphering".lower() == value.lower():
            ret = Command.GENERAL_DED_CIPHERING
        elif "GeneralCiphering".lower() == value.lower():
            ret = Command.GENERAL_CIPHERING
        elif "InformationReport".lower() == value.lower():
            ret = Command.INFORMATION_REPORT
        elif "EventNotification".lower() == value.lower():
            ret = Command.EVENT_NOTIFICATION
        elif "GatewayRequest".lower() == value.lower():
            ret = Command.GATEWAY_REQUEST
        elif "GatewayResponse".lower() == value.lower():
            ret = Command.GATEWAY_RESPONSE
        else:
            raise ValueError(value)
        return ret

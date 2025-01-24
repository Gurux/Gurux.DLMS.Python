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
from __future__ import print_function
from .GXByteBuffer import GXByteBuffer
from .internal._GXCommon import _GXCommon
from .internal._GXDataInfo import _GXDataInfo
from ._GXFCS16 import _GXFCS16
from ._HDLCInfo import _HDLCInfo
from .enums import (
    Conformance,
    InterfaceType,
    RequestTypes,
    HdlcFrameType,
    Command,
    ErrorCode,
    Priority,
    ServiceClass,
    ObjectType,
)
from .enums import ExceptionServiceError, Security
from .TranslatorSimpleTags import TranslatorSimpleTags
from .GetCommandType import GetCommandType
from .GXDLMSLNParameters import GXDLMSLNParameters
from .GXDLMSSNParameters import GXDLMSSNParameters
from .GXReplyData import GXReplyData
from .ConfirmedServiceError import ConfirmedServiceError
from .SetResponseType import SetResponseType
from .HdlcControlFrame import HdlcControlFrame
from .enums.TranslatorOutputType import TranslatorOutputType
from .TranslatorTags import TranslatorTags
from .TranslatorStandardTags import TranslatorStandardTags
from .SingleReadResponse import SingleReadResponse
from .objects.enums import SecuritySuite
from .ConnectionState import ConnectionState
from .GXCiphering import GXCiphering
from .enums.DataType import DataType
from .VariableAccessSpecification import VariableAccessSpecification
from .AesGcmParameter import AesGcmParameter
from .GXDLMSConfirmedServiceError import GXDLMSConfirmedServiceError
from .MBusEncryptionMode import MBusEncryptionMode
from .MBusCommand import MBusCommand
from .enums.Standard import Standard
from .GXDLMSExceptionResponse import GXDLMSExceptionResponse
from .ActionRequestType import ActionRequestType
from .ActionResponseType import ActionResponseType
from .SetRequestType import SetRequestType
from .plc.enums import (
    PlcDataLinkData,
    PlcHdlcSourceAddress,
    PlcMacSubframes,
    PlcSourceAddress,
    PlcDestinationAddress,
)


# pylint: disable=too-many-public-methods,too-many-function-args
class GXDLMS:
    """
    GXDLMS implements methods to communicate with DLMS/COSEM metering devices.
    """

    @classmethod
    def useHdlc(cls, tp):
        return tp in (
            InterfaceType.HDLC,
            InterfaceType.HDLC_WITH_MODE_E,
            InterfaceType.PLC_HDLC,
        )

    __CIPHERING_HEADER_SIZE = 7 + 12 + 3
    _data_TYPE_OFFSET = 0xFF0000

    @classmethod
    def getInvokeIDPriority(cls, settings):
        value = 0
        if settings.priority == Priority.HIGH:
            value |= 0x80
        if settings.serviceClass == ServiceClass.CONFIRMED:
            value |= 0x40
        value |= settings.invokeId
        return value

    @classmethod
    def getLongInvokeIDPriority(cls, settings):
        """
        Generates Invoke ID and priority.
        @param settings
        DLMS settings.
        Invoke ID and priority.
        """

        value = 0
        if settings.priority == Priority.HIGH:
            value = 0x80000000
        if settings.serviceClass == ServiceClass.CONFIRMED:
            value |= 0x40000000
        value |= int((settings.getLongInvokeID() & 0xFFFFFF))
        settings.setLongInvokeID(settings.getLongInvokeID() + 1)
        return value

    #
    # Generates an acknowledgment message, with which the server is
    #      informed to
    # send next packets.
    #
    # @param type
    # Frame type.
    # Acknowledgment message as byte array.
    #
    @classmethod
    def receiverReady(cls, settings, reply):
        if isinstance(reply, RequestTypes):
            tmp = reply
            reply = GXReplyData()
            reply.moreData = tmp
        if reply.moreData == RequestTypes.NONE:
            raise ValueError("Invalid receiverReady RequestTypes parameter.")
        #  Get next frame.
        if (reply.moreData & RequestTypes.FRAME) != 0:
            id_ = settings.getReceiverReady()
            return GXDLMS.getHdlcFrame(settings, id_, None)
        cmd = settings.command
        if reply.moreData == RequestTypes.GBT:
            p = GXDLMSLNParameters(
                settings, 0, Command.GENERAL_BLOCK_TRANSFER, 0, None, None, 0xFF
            )
            p.gbtWindowSize = reply.gbtWindowSize
            p.blockNumberAck = reply.blockNumber
            p.blockIndex = settings.blockNumber
            reply = GXDLMS.getLnMessages(p)
        else:
            #  Get next block.
            bb = GXByteBuffer(4)
            if settings.getUseLogicalNameReferencing():
                bb.setUInt32(settings.blockIndex)
            else:
                bb.setUInt16(settings.blockIndex)
            settings.increaseBlockIndex()
            if settings.getUseLogicalNameReferencing():
                p = GXDLMSLNParameters(
                    settings, 0, cmd, GetCommandType.NEXT_DATA_BLOCK, bb, None, 0xFF
                )
                reply = GXDLMS.getLnMessages(p)
            else:
                p = GXDLMSSNParameters(
                    settings,
                    cmd,
                    1,
                    VariableAccessSpecification.BLOCK_NUMBER_ACCESS,
                    bb,
                    None,
                )
                reply = GXDLMS.getSnMessages(p)
        return reply[0]

    #
    # Reserved for internal use.
    #
    @classmethod
    def checkInit(cls, settings):
        if settings.clientAddress == 0:
            raise ValueError("Invalid Client Address.")
        if settings.serverAddress == 0:
            raise ValueError("Invalid Server Address.")

    @classmethod
    # pylint: disable=too-many-arguments
    def appendData(cls, settings, obj, index, bb, value):
        tp = obj.getDataType(index)
        if tp == DataType.ARRAY:
            if isinstance(value, bytes):
                if tp != DataType.OCTET_STRING:
                    bb.set(int(value))
                    return
        else:
            if tp == DataType.NONE and value:
                raise Exception("Invalid parameter. In python value type must give.")
            if isinstance(value, str) and tp == DataType.OCTET_STRING:
                ui = obj.getUIDataType(index)
                if ui == DataType.STRING:
                    _GXCommon.setData(settings, bb, tp, value.encode())
                    return
        _GXCommon.setData(settings, bb, tp, value)

    #
    # Get used glo message.
    #
    # @param command
    # Executed command.
    # Integer value of glo message.
    #
    @classmethod
    def getGloMessage(cls, command):
        cmd = int()
        if command == Command.READ_REQUEST:
            cmd = Command.GLO_READ_REQUEST
        elif command == Command.GET_REQUEST:
            cmd = Command.GLO_GET_REQUEST
        elif command == Command.WRITE_REQUEST:
            cmd = Command.GLO_WRITE_REQUEST
        elif command == Command.SET_REQUEST:
            cmd = Command.GLO_SET_REQUEST
        elif command == Command.METHOD_REQUEST:
            cmd = Command.GLO_METHOD_REQUEST
        elif command == Command.READ_RESPONSE:
            cmd = Command.GLO_READ_RESPONSE
        elif command == Command.GET_RESPONSE:
            cmd = Command.GLO_GET_RESPONSE
        elif command == Command.WRITE_RESPONSE:
            cmd = Command.GLO_WRITE_RESPONSE
        elif command == Command.SET_RESPONSE:
            cmd = Command.GLO_SET_RESPONSE
        elif command == Command.METHOD_RESPONSE:
            cmd = Command.GLO_METHOD_RESPONSE
        elif command == Command.DATA_NOTIFICATION:
            cmd = Command.GENERAL_GLO_CIPHERING
        elif command == Command.RELEASE_REQUEST:
            cmd = Command.RELEASE_REQUEST
        elif command == Command.RELEASE_RESPONSE:
            cmd = Command.RELEASE_RESPONSE
        else:
            raise Exception("Invalid GLO command.")
        return cmd

    #
    # Get used ded message.
    #
    # @param cmd
    # Executed command.
    # Integer value of ded message.
    #
    @classmethod
    def getDedMessage(cls, command):
        cmd = int()
        if command == Command.GET_REQUEST:
            cmd = Command.DED_GET_REQUEST
        elif command == Command.SET_REQUEST:
            cmd = Command.DED_SET_REQUEST
        elif command == Command.METHOD_REQUEST:
            cmd = Command.DED_METHOD_REQUEST
        elif command == Command.GET_RESPONSE:
            cmd = Command.DED_GET_RESPONSE
        elif command == Command.SET_RESPONSE:
            cmd = Command.DED_SET_RESPONSE
        elif command == Command.METHOD_RESPONSE:
            cmd = Command.DED_METHOD_RESPONSE
        elif command == Command.DATA_NOTIFICATION:
            cmd = Command.GENERAL_DED_CIPHERING
        elif command == Command.RELEASE_REQUEST:
            cmd = Command.RELEASE_REQUEST
        elif command == Command.RELEASE_RESPONSE:
            cmd = Command.RELEASE_RESPONSE
        else:
            raise Exception("Invalid DED command.")
        return cmd

    #
    # Add LLC bytes to generated message.
    #
    # @param settings
    # DLMS settings.
    # @param data
    # Data where bytes are added.
    #
    @classmethod
    def addLLCBytes(cls, settings, data):
        tmp = data.array()
        data.clear()
        if settings.isServer:
            data.set(_GXCommon.LLC_REPLY_BYTES)
        else:
            data.set(_GXCommon.LLC_SEND_BYTES)
        data.set(tmp)

    @classmethod
    def multipleBlocks(cls, p, reply, ciphering):
        """
        Check is all_ data fit to one data block.

        @param p
        LN parameters.
        @param reply
        Generated reply.
        """

        #  Check is all_ data fit to one message if data is given.
        len_ = 0
        if p.data:
            len_ = len(p.data) - p.data.position
        if p.attributeDescriptor:
            len_ += p.attributeDescriptor.size
        if ciphering:
            len_ += GXDLMS.__CIPHERING_HEADER_SIZE
        if not p.multipleBlocks:
            #  Add command type and invoke and priority.
            p.multipleBlocks = 2 + len(reply) + len_ > p.settings.maxPduSize
        if p.multipleBlocks:
            #  Add command type and invoke and priority.
            p.lastBlock = not 8 + len(reply) + len_ > p.settings.maxPduSize
        if p.lastBlock:
            #  Add command type and invoke and priority.
            p.lastBlock = not 8 + len(reply) + len_ > p.settings.maxPduSize

    #
    # Get next logical name PDU.
    #
    # @param p
    # LN parameters.
    # @param reply
    # Generated message.
    #
    @classmethod
    def getLNPdu(cls, p, reply):
        # pylint: disable=too-many-nested-blocks
        ciphering = (
            p.command != Command.AARQ
            and p.command != Command.AARE
            and p.settings.cipher
            and p.settings.cipher.security != Security.NONE
        )
        len_ = 0
        if p.command == Command.AARQ:
            if p.settings.gateway and p.settings.gateway.physicalDeviceAddress:
                reply.setUInt8(Command.GATEWAY_REQUEST)
                reply.setUInt8(p.settings.gateway.networkId)
                reply.setUInt8(len(p.settings.gateway.physicalDeviceAddress))
                reply.set(p.settings.gateway.physicalDeviceAddress)
            reply.set(p.attributeDescriptor)
        else:
            if p.command != Command.GENERAL_BLOCK_TRANSFER:
                reply.setUInt8(p.command)
            if p.command in (
                Command.EVENT_NOTIFICATION,
                Command.DATA_NOTIFICATION,
                Command.ACCESS_REQUEST,
                Command.ACCESS_RESPONSE,
            ):
                if p.command != Command.EVENT_NOTIFICATION:
                    if p.invokeId != 0:
                        reply.setUInt32(p.invokeId)
                    else:
                        reply.setUInt32(GXDLMS.getLongInvokeIDPriority(p.settings))
                if p.time is None:
                    reply.setUInt8(DataType.NONE)
                else:
                    pos = len(reply)
                    _GXCommon.setData(
                        p.settings, reply, DataType.OCTET_STRING, p.getTime()
                    )
                    if p.command != Command.EVENT_NOTIFICATION:
                        reply.move(pos + 1, pos, len(reply) - pos - 1)
                GXDLMS.multipleBlocks(p, reply, ciphering)
            elif p.command not in (Command.RELEASE_REQUEST, Command.EXCEPTION_RESPONSE):
                if p.command != Command.GET_REQUEST and p.data:
                    GXDLMS.multipleBlocks(p, reply, ciphering)
                if p.command == Command.SET_REQUEST:
                    if (
                        p.multipleBlocks
                        and (
                            p.settings.negotiatedConformance
                            & Conformance.GENERAL_BLOCK_TRANSFER
                        )
                        == 0
                    ):
                        if p.requestType == SetRequestType.NORMAL:
                            p.requestType = SetRequestType.FIRST_DATA_BLOCK
                        elif p.requestType == SetRequestType.FIRST_DATA_BLOCK:
                            p.requestType = SetRequestType.WITH_DATA_BLOCK
                            # Change Request type if action request and multiple
                            # blocks is needed.
                elif p.command == Command.METHOD_REQUEST:
                    if (
                        p.multipleBlocks
                        and (
                            p.settings.negotiatedConformance
                            & Conformance.GENERAL_BLOCK_TRANSFER
                        )
                        == 0
                    ):
                        if p.requestType == ActionRequestType.NORMAL:
                            # Remove Method Invocation Parameters tag.
                            p.attributeDescriptor.size = p.attributeDescriptor.size - 1
                            p.requestType = ActionRequestType.WITH_FIRST_BLOCK
                        elif p.requestType == ActionRequestType.WITH_FIRST_BLOCK:
                            p.requestType = ActionRequestType.WITH_BLOCK
                # Change Request type if action request and multiple blocks is
                # needed.
                elif p.command == Command.METHOD_RESPONSE:
                    if (
                        p.multipleBlocks
                        and (
                            p.settings.negotiatedConformance
                            & Conformance.GENERAL_BLOCK_TRANSFER
                        )
                        == 0
                    ):
                        # There is no status fiel in action resonse.
                        p.status = 0xFF
                        if p.RequestType == ActionResponseType.NORMAL:
                            # Remove Method Invocation Parameters tag.
                            p.data.position = p.data.position + 2
                            p.requestType = ActionResponseType.WITH_BLOCK
                        elif (
                            p.requestType == ActionResponseType.WITH_BLOCK
                            and p.data.available() == 0
                        ):
                            # If server asks next part of PDU.
                            p.requestType = ActionResponseType.NEXT_BLOCK
                elif p.command == Command.GET_RESPONSE:
                    if (
                        p.multipleBlocks
                        and (
                            p.settings.negotiatedConformance
                            & Conformance.GENERAL_BLOCK_TRANSFER
                        )
                        == 0
                    ):
                        if p.requestType == 1:
                            p.requestType = 2
                if p.command != Command.GENERAL_BLOCK_TRANSFER:
                    reply.setUInt8(p.requestType)
                    if p.invokeId != 0:
                        reply.setUInt8(p.invokeId)
                    else:
                        reply.setUInt8(GXDLMS.getInvokeIDPriority(p.settings))
            reply.set(p.attributeDescriptor)
            if (
                p.multipleBlocks
                and (
                    p.settings.negotiatedConformance
                    & Conformance.GENERAL_BLOCK_TRANSFER
                )
                == 0
            ):
                if p.command != Command.SET_RESPONSE:
                    if p.lastBlock:
                        reply.setUInt8(1)
                        p.settings.setCount(0)
                        p.settings.setIndex(0)
                    else:
                        reply.setUInt8(0)
                reply.setUInt32(p.blockIndex)
                p.blockIndex = p.blockIndex + 1
                if p.status != 0xFF:
                    if p.status != 0 and p.command == Command.GET_RESPONSE:
                        reply.setUInt8(1)
                    reply.setUInt8(p.status)
                if p.data:
                    len_ = p.data.size - p.data.position
                else:
                    len_ = 0
                totalLength = len_ + len(reply)
                if ciphering:
                    totalLength += GXDLMS.__CIPHERING_HEADER_SIZE
                if totalLength > p.settings.maxPduSize:
                    len_ = p.settings.maxPduSize - len(reply)
                    if ciphering:
                        len_ -= GXDLMS.__CIPHERING_HEADER_SIZE
                    len_ -= _GXCommon.getObjectCountSizeInBytes(len_)
                _GXCommon.setObjectCount(len_, reply)
                reply.set(p.data, p.data.position, len_)
            if len_ == 0:
                if p.status != 0xFF and p.command != Command.GENERAL_BLOCK_TRANSFER:
                    if p.status != 0 and p.command == Command.GET_RESPONSE:
                        reply.setUInt8(1)
                    reply.setUInt8(p.status)
                if p.data:
                    len_ = p.data.size - p.data.position
                    if p.settings.gateway and p.settings.gateway.physicalDeviceAddress:
                        if (
                            3 + len_ + len(p.settings.gateway.physicalDeviceAddress)
                            > p.settings.maxPduSize
                        ):
                            len_ -= 3 + len(p.settings.gateway.physicalDeviceAddress)
                        tmp = GXByteBuffer(reply)
                        reply.size = 0
                        reply.setUInt8(Command.GATEWAY_REQUEST)
                        reply.setUInt8(p.settings.gateway.networkId)
                        reply.setUInt8(len(p.settings.gateway.physicalDeviceAddress))
                        reply.set(p.settings.gateway.physicalDeviceAddress)
                        reply.set(tmp)
                    if (
                        p.settings.negotiatedConformance
                        & Conformance.GENERAL_BLOCK_TRANSFER
                        != Conformance.NONE
                    ):
                        if 7 + len_ + len(reply) > p.settings.maxPduSize:
                            len_ = p.settings.maxPduSize - len(reply) - 7
                        if ciphering and p.command != Command.GENERAL_BLOCK_TRANSFER:
                            reply.set(p.data)
                            tmp = []
                            if (
                                reply.size != 0
                                and p.command != Command.GENERAL_BLOCK_TRANSFER
                            ):
                                # pylint: disable=W0212
                                p.settings._onPduEventHandler(True, reply.array())
                            if p.settings.cipher.securitySuite == SecuritySuite.SUITE_0:
                                tmp = GXDLMS.cipher0(p, reply)
                            p.data.size = 0
                            p.data.set(tmp)
                            reply.size = 0
                            len_ = p.data.size
                            if 7 + len_ > p.settings.maxPduSize:
                                len_ = p.settings.maxPduSize - 7
                            ciphering = False
                    elif (
                        p.command != Command.GET_REQUEST
                        and len_ + len(reply) > p.settings.maxPduSize
                    ):
                        len_ = p.settings.maxPduSize - len(reply)
                    reply.set(p.data, p.data.position, len_)
                elif (
                    p.settings.gateway and p.settings.gateway.physicalDeviceAddress
                ) and not (
                    p.command == Command.GENERAL_BLOCK_TRANSFER
                    or (
                        p.multipleBlocks
                        and (
                            p.settings.negotiatedConformance
                            & Conformance.GENERAL_BLOCK_TRANSFER
                            != Conformance.NONE
                        )
                    )
                ):
                    if (
                        3 + len_ + len(p.settings.gateway.physicalDeviceAddress)
                        > p.settings.maxPduSize
                    ):
                        len_ -= 3 + len(p.settings.gateway.physicalDeviceAddress)
                    tmp = GXByteBuffer(reply)
                    reply.size = 0
                    reply.setUInt8(Command.GATEWAY_REQUEST)
                    reply.setUInt8(p.settings.gateway.networkId)
                    reply.setUInt8(len(p.settings.gateway.physicalDeviceAddress))
                    reply.set(p.settings.gateway.physicalDeviceAddress)
                    reply.set(tmp)
            if (
                ciphering
                and len(reply) != 0
                and p.command != Command.RELEASE_REQUEST
                and (
                    not p.multipleBlocks
                    or p.settings.negotiatedConformance
                    & Conformance.GENERAL_BLOCK_TRANSFER
                    == Conformance.NONE
                )
            ):
                tmp = []
                # pylint: disable=W0212
                p.settings._onPduEventHandler(True, reply.array())
                if p.settings.cipher.securitySuite == SecuritySuite.SUITE_0:
                    tmp = GXDLMS.cipher0(p, reply.array())
                reply.size = 0
                reply.set(tmp)
        if p.command == Command.GENERAL_BLOCK_TRANSFER or (
            p.multipleBlocks
            and p.settings.negotiatedConformance & Conformance.GENERAL_BLOCK_TRANSFER
            != Conformance.NONE
        ):
            bb = GXByteBuffer()
            bb.set(reply)
            reply.clear()
            reply.setUInt8(Command.GENERAL_BLOCK_TRANSFER)
            value = 0
            if p.lastBlock:
                value = 0x80
            elif p.streaming:
                value |= 0x40
            value |= p.gbtWindowSize
            reply.setUInt8(value)
            reply.setUInt16(p.blockIndex)
            p.blockIndex += 1
            if p.command != Command.DATA_NOTIFICATION and p.blockNumberAck != 0:
                reply.setUInt16(p.blockNumberAck)
                p.blockNumberAck += 1
            else:
                p.blockNumberAck = -1
                reply.setUInt16(0)
            _GXCommon.setObjectCount(len(bb), reply)
            reply.set(bb)
            if p.command != Command.GENERAL_BLOCK_TRANSFER:
                p.command = Command.GENERAL_BLOCK_TRANSFER
                p.blockNumberAck += 1
            if p.settings.gateway and p.settings.gateway.physicalDeviceAddress:
                if (
                    3 + len_ + len(p.settings.gateway.physicalDeviceAddress)
                    > p.settings.maxPduSize
                ):
                    len_ -= 3 + len(p.settings.gateway.physicalDeviceAddress)
                tmp = GXByteBuffer(reply)
                reply.size = 0
                reply.setUInt8(Command.GATEWAY_REQUEST)
                reply.setUInt8(p.settings.gateway.networkId)
                reply.setUInt8(len(p.settings.gateway.physicalDeviceAddress))
                reply.set(p.settings.gateway.physicalDeviceAddress)
                reply.set(tmp)
        if GXDLMS.useHdlc(p.settings.interfaceType):
            GXDLMS.addLLCBytes(p.settings, reply)

    @classmethod
    def cipher0(cls, p, data):
        cmd = 0
        key = None
        cipher = p.settings.cipher
        if (
            (p.settings.connected & ConnectionState.DLMS) == 0
            or (p.settings.negotiatedConformance & Conformance.GENERAL_PROTECTION) == 0
        ) and (
            not p.settings.preEstablishedSystemTitle
            or (p.settings.proposedConformance & Conformance.GENERAL_PROTECTION)
            == Conformance.NONE
        ):
            if (
                cipher.dedicatedKey
                and (p.settings.connected & ConnectionState.DLMS) != 0
            ):
                cmd = GXDLMS.getDedMessage(p.command)
                key = cipher.dedicatedKey
            else:
                cmd = GXDLMS.getGloMessage(p.command)
                key = cipher.blockCipherKey
        else:
            if cipher.dedicatedKey:
                cmd = Command.GENERAL_DED_CIPHERING
                key = cipher.dedicatedKey
            else:
                cmd = Command.GENERAL_GLO_CIPHERING
                key = cipher.blockCipherKey
        s = AesGcmParameter(cmd, cipher.systemTitle, key, cipher.authenticationKey)
        s.ignoreSystemTitle = p.settings.standard == Standard.ITALY
        s.security = cipher.security
        s.invocationCounter = cipher.invocationCounter
        tmp = GXCiphering.encrypt(s, data)
        cipher.invocationCounter = cipher.invocationCounter + 1
        return tmp

    @classmethod
    def getLnMessages(cls, p):
        reply = GXByteBuffer()
        messages = []
        frame_ = 0
        if p.command in (Command.DATA_NOTIFICATION, Command.EVENT_NOTIFICATION):
            frame_ = 0x13
        while True:
            GXDLMS.getLNPdu(p, reply)
            p.lastBlock = True
            if p.attributeDescriptor is None:
                p.settings.increaseBlockIndex()
            if p.command == Command.AARQ and p.command == Command.GET_REQUEST:
                assert not p.settings.maxPduSize < len(reply)
            while reply.position != len(reply):
                if p.settings.interfaceType == InterfaceType.WRAPPER:
                    messages.append(
                        GXDLMS.getWrapperFrame(p.settings, p.command, reply)
                    )
                elif p.settings.interfaceType in (
                    InterfaceType.HDLC,
                    InterfaceType.HDLC_WITH_MODE_E,
                ):
                    messages.append(GXDLMS.getHdlcFrame(p.settings, frame_, reply))
                    if reply.position != len(reply):
                        frame_ = p.settings.getNextSend(False)
                elif p.settings.interfaceType == InterfaceType.PDU:
                    messages.append(reply.array())
                    break
                else:
                    raise ValueError("InterfaceType")
            reply.clear()
            frame_ = 0
            if not p.data or p.data.position == p.data.size:
                break
        return messages

    @classmethod
    def getSnMessages(cls, p):
        reply = GXByteBuffer()
        messages = []
        frame_ = 0x0
        if p.command in (Command.INFORMATION_REPORT, Command.DATA_NOTIFICATION):
            frame_ = 0x13
        while True:
            GXDLMS.getSNPdu(p, reply)
            if p.command not in (Command.AARQ, Command.AARE):
                assert not p.settings.maxPduSize < len(reply)
            while reply.position != len(reply):
                if p.settings.interfaceType == InterfaceType.WRAPPER:
                    messages.append(
                        GXDLMS.getWrapperFrame(p.settings, p.command, reply)
                    )
                elif p.settings.interfaceType in (
                    InterfaceType.HDLC,
                    InterfaceType.HDLC_WITH_MODE_E,
                ):
                    messages.append(GXDLMS.getHdlcFrame(p.settings, frame_, reply))
                    if reply.position != len(reply):
                        frame_ = p.settings.getNextSend(False)
                elif p.settings.interfaceType == InterfaceType.PDU:
                    messages.append(reply.array())
                    break
                else:
                    raise ValueError("InterfaceType")
            reply.clear()
            frame_ = 0
            if not p.data or p.data.position == p.data.size:
                break
        return messages

    @classmethod
    def appendMultipleSNBlocks(cls, p, reply):
        ciphering = p.settings.cipher and p.settings.cipher.security != Security.NONE
        hSize = len(reply) + 3
        if p.command in (Command.WRITE_REQUEST, Command.READ_REQUEST):
            hSize += 1 + _GXCommon.getObjectCountSizeInBytes(p.count)
        maxSize = p.settings.maxPduSize - hSize
        if ciphering:
            maxSize -= GXDLMS.__CIPHERING_HEADER_SIZE
            if p.settings.interfaceType in (
                InterfaceType.HDLC,
                InterfaceType.HDLC_WITH_MODE_E,
            ):
                maxSize -= 3
        maxSize -= _GXCommon.getObjectCountSizeInBytes(maxSize)
        if reply.available() > maxSize:
            reply.setUInt8(0)
        else:
            reply.setUInt8(1)
            maxSize = reply.available()
        reply.setUInt16(p.blockIndex)
        if p.command == Command.WRITE_REQUEST:
            p.blockIndex = p.blockIndex + 1
            _GXCommon.setObjectCount(p.count, reply)
            reply.setUInt8(DataType.OCTET_STRING)
        elif p.command == Command.READ_REQUEST:
            p.blockIndex = p.blockIndex + 1
        _GXCommon.setObjectCount(maxSize, reply)
        return maxSize

    @classmethod
    def getSNPdu(cls, p, reply):
        ciphering = (
            p.settings.cipher
            and p.settings.cipher.security != Security.NONE
            and p.command != Command.AARQ
            and p.command != Command.AARE
        )
        if not ciphering and (
            p.settings.interfaceType
            in (InterfaceType.HDLC, InterfaceType.HDLC_WITH_MODE_E)
        ):
            if p.settings.isServer:
                reply.set(_GXCommon.LLC_REPLY_BYTES)
            elif not reply:
                reply.set(_GXCommon.LLC_SEND_BYTES)
        cnt = 0
        cipherSize = 0
        if ciphering:
            cipherSize = GXDLMS.__CIPHERING_HEADER_SIZE
        if p.data:
            cnt = p.data.size - p.data.position
        if p.command == Command.INFORMATION_REPORT:
            reply.setUInt8(p.command)
            if not p.time:
                reply.setUInt8(DataType.NONE)
            else:
                pos = len(reply)
                _GXCommon.setData(p.settings, reply, DataType.OCTET_STRING, p.time)
                reply.move(pos + 1, pos, len(reply) - pos - 1)
            _GXCommon.setObjectCount(p.count, reply)
            reply.set(p.attributeDescriptor)
        elif p.command not in (Command.AARQ, Command.AARE):
            reply.setUInt8(p.command)
            if p.count != 0xFF:
                _GXCommon.setObjectCount(p.count, reply)
            if p.requestType != 0xFF:
                reply.setUInt8(p.requestType)
            reply.set(p.attributeDescriptor)
            if not p.multipleBlocks:
                p.multipleBlocks = len(reply) + cipherSize + cnt > p.settings.maxPduSize
                if p.multipleBlocks:
                    reply.size = 0
                    if not ciphering and (
                        p.settings.interfaceType
                        in (InterfaceType.HDLC, InterfaceType.HDLC_WITH_MODE_E)
                    ):
                        if p.settings.isServer:
                            reply.set(_GXCommon.LLC_REPLY_BYTES)
                        elif not reply:
                            reply.set(_GXCommon.LLC_SEND_BYTES)
                    if p.command == Command.WRITE_REQUEST:
                        p.requestType = (
                            VariableAccessSpecification.WRITE_DATA_BLOCK_ACCESS
                        )
                    elif p.command == Command.READ_REQUEST:
                        p.requestType = (
                            VariableAccessSpecification.READ_DATA_BLOCK_ACCESS
                        )
                    elif p.command == Command.READ_RESPONSE:
                        p.requestType = SingleReadResponse.DATA_BLOCK_RESULT
                    else:
                        raise ValueError("Invalid command.")
                    reply.setUInt8(p.command)
                    reply.setUInt8(1)
                    if p.requestType != 0xFF:
                        reply.setUInt8(p.requestType)
                    cnt = GXDLMS.appendMultipleSNBlocks(p, reply)
            else:
                cnt = GXDLMS.appendMultipleSNBlocks(p, reply)
        if p.data:
            reply.set(p.data, p.data.position, cnt)
        if p.data and p.data.position == p.data.size:
            p.settings.index = 0
            p.settings.count = 0
        if ciphering and p.command != Command.AARQ and p.command != Command.AARE:
            cipher = p.settings.cipher
            s = AesGcmParameter(
                GXDLMS.getGloMessage(p.command),
                cipher.systemTitle,
                cipher.blockCipherKey,
                cipher.authenticationKey,
            )
            s.security = cipher.security
            s.invocationCounter = cipher.invocationCounter
            tmp = GXCiphering.encrypt(s, reply.array())
            assert not tmp
            reply.size = 0
            if p.settings.interfaceType in (
                InterfaceType.HDLC,
                InterfaceType.HDLC_WITH_MODE_E,
            ):
                if p.settings.isServer:
                    reply.set(_GXCommon.LLC_REPLY_BYTES)
                elif not reply:
                    reply.set(_GXCommon.LLC_SEND_BYTES)
            reply.set(tmp)

    @classmethod
    def getAddress(cls, value, size):
        if size < 2 and value < 0x80:
            return int((value << 1 | 1))
        if size < 4 and value < 0x4000:
            return int(((value & 0x3F80) << 2 | (value & 0x7F) << 1 | 1))
        if value < 0x10000000:
            return int(
                (
                    (value & 0xFE00000) << 4
                    | (value & 0x1FC000) << 3
                    | (value & 0x3F80) << 2
                    | (value & 0x7F) << 1
                    | 1
                )
            )
        raise ValueError("Invalid address.")

    @classmethod
    def getAddressBytes(cls, value, size):
        tmp = GXDLMS.getAddress(value, size)
        bb = GXByteBuffer()
        if size == 1 or tmp < 0x100:
            bb.setUInt8(tmp)
        elif size == 2 or tmp < 0x10000:
            bb.setUInt16(tmp)
        elif size == 4 or tmp < 0x100000000:
            bb.setUInt32(tmp)
        else:
            raise ValueError("Invalid address type.")
        return bb.array()

    @classmethod
    def getWrapperFrame(cls, settings, command, data):
        bb = GXByteBuffer()
        bb.setUInt16(1)
        if settings.isServer:
            bb.setUInt16(settings.serverAddress)
            if settings.pushClientAddress != 0 and command in (
                Command.DATA_NOTIFICATION,
                Command.EVENT_NOTIFICATION,
            ):
                bb.setUInt16(settings.pushClientAddress)
            else:
                bb.setUInt16(settings.clientAddress)
        else:
            bb.setUInt16(settings.clientAddress)
            bb.setUInt16(settings.serverAddress)
        if data is None:
            bb.setUInt16(0)
        else:
            bb.setUInt16(len(data))
            bb.set(data)
        if settings.isServer:
            if len(data) == data.position:
                data.clear()
            else:
                data.move(data.position, 0, len(data) - data.position)
                data.position = 0
        return bb.array()

    @classmethod
    def getHdlcFrame(cls, settings, frame_, data):
        # pylint: disable=protected-access
        bb = GXByteBuffer()
        frameSize = 0
        len1 = 0
        primaryAddress = None
        secondaryAddress = None
        if settings.isServer:
            if frame_ == 0x13 and settings.pushClientAddress != 0:
                primaryAddress = GXDLMS.getAddressBytes(settings.pushClientAddress, 1)
            else:
                primaryAddress = GXDLMS.getAddressBytes(settings.clientAddress, 1)
            secondaryAddress = GXDLMS.getAddressBytes(
                settings.serverAddress, settings.serverAddressSize
            )
        else:
            primaryAddress = GXDLMS.getAddressBytes(
                settings.serverAddress, settings.serverAddressSize
            )
            secondaryAddress = GXDLMS.getAddressBytes(settings.clientAddress, 1)
        bb.setUInt8(_GXCommon.HDLC_FRAME_START_END)
        frameSize = settings.hdlc.maxInfoTX
        if data and data.position == 0:
            frameSize -= 3
        if not data:
            len1 = 0
            bb.setUInt8(0xA0)
        elif len(data) - data.position <= frameSize:
            len1 = len(data) - data.position
            bb.setUInt8(
                0xA0
                | (((len(secondaryAddress) + len(primaryAddress) + len1) >> 8) & 0x7)
            )
        else:
            len1 = frameSize
            bb.setUInt8(
                0xA8
                | (((len(secondaryAddress) + len(primaryAddress) + len1) >> 8) & 0x7)
            )
        if len1 == 0:
            bb.setUInt8(5 + len(secondaryAddress) + len(primaryAddress) + len1)
        else:
            bb.setUInt8(7 + len(secondaryAddress) + len(primaryAddress) + len1)
        bb.set(primaryAddress)
        bb.set(secondaryAddress)
        if frame_ == 0:
            bb.setUInt8(settings.getNextSend(True))
        else:
            bb.setUInt8(frame_)
        crc = _GXFCS16.countFCS16(bb._data, 1, bb.size - 1)
        bb.setUInt16(crc)
        if len1 != 0:
            bb.set(data, data.position, len1)
            crc = _GXFCS16.countFCS16(bb._data, 1, len(bb) - 1)
            bb.setUInt16(crc)
        bb.setUInt8(_GXCommon.HDLC_FRAME_START_END)
        if settings.isServer:
            if data:
                if len(data) == data.position:
                    data.clear()
                else:
                    data.move(data.position, 0, len(data) - data.position)
                    data.position = 0
        return bb.array()

    @classmethod
    def getMacFrame(cls, settings, frame_, creditFields, data):
        if settings.interfaceType == InterfaceType.PLC:
            return cls.getPlcFrame(settings, creditFields, data)
        return cls.getMacHdlcFrame(settings, frame_, creditFields, data)

    @classmethod
    def getPlcFrame(cls, settings, creditFields, data):
        frameSize = data.available()
        # Max frame size is 124 bytes.
        if frameSize > 134:
            frameSize = 134
        # PAD Length.
        padLen = (36 - ((11 + frameSize) % 36)) % 36
        bb = GXByteBuffer()
        bb.capacity = 15 + frameSize + padLen
        # Add STX
        bb.setUInt8(2)
        # Length.
        bb.setUInt8((11 + frameSize))
        # Length.
        bb.setUInt8(0x50)
        # Add Credit fields.
        bb.setUInt8(creditFields)
        # Add source and target MAC addresses.
        bb.setUInt8(settings.plc.MacSourceAddress >> 4)
        val = settings.plc.MacSourceAddress << 12
        val |= settings.plc.MacDestinationAddress & 0xFFF
        bb.setUInt16(val)
        bb.setUInt8(padLen)
        # Control byte.
        bb.setUInt8(PlcDataLinkData.Request)
        bb.setUInt8(settings.serverAddress)
        bb.setUInt8(settings.clientAddress)
        bb.Set(data, frameSize)
        # Add padding.
        while padLen != 0:
            bb.setUInt8(0)
            --padLen
        # Checksum.
        crc = GXFCS16.countFCS16(bb.Data, 0, bb.Size)
        bb.setUInt16(crc)
        # Remove sent data in server side.
        if settings.isServer:
            if data.size == data.position:
                data.clear()
            else:
                data.move(data.position, 0, data.size - data.position)
                data.position = 0
        return bb.array()

    @classmethod
    def getMacHdlcFrame(cls, settings, frame_, creditFields, data):
        if settings.Hdlc.MaxInfoTX > 126:
            settings.Hdlc.MaxInfoTX = 86
        bb = GXByteBuffer()
        # Lenght is updated last.
        bb.setUInt16(0)
        # Add  Credit fields.
        bb.setUInt8(creditFields)
        # Add source and target MAC addresses.
        bb.setUInt8(settings.plc.macSourceAddress >> 4)
        val = settings.plc.macSourceAddress << 12
        val |= settings.plc.macDestinationAddress & 0xFFF
        bb.setUInt16(val)
        tmp = cls.getHdlcFrame(settings, frame_, data, True)
        padLen = (36 - ((10 + tmp.Length) % 36)) % 36
        bb.setUInt8(padLen)
        bb.Set(tmp)
        # Add padding.
        while padLen != 0:
            bb.setUInt8(0)
            --padLen

        # Checksum.
        crc = _GXFCS16.countFCS24(bb.Data, 2, bb.Size - 2 - padLen)
        bb.setUInt8(crc >> 16)
        bb.setUInt16(crc)
        # Add NC
        val = bb.Size / 36
        if bb.Size % 36 != 0:
            ++val
        if val == 1:
            val = PlcMacSubframes.ONE
        elif val == 2:
            val = PlcMacSubframes.TWO
        elif val == 3:
            val = PlcMacSubframes.THREE
        elif val == 4:
            val = PlcMacSubframes.FOUR
        elif val == 5:
            val = PlcMacSubframes.FIVE
        elif val == 6:
            val = PlcMacSubframes.SIX
        elif val == 7:
            val = PlcMacSubframes.SEVEN
        else:
            raise Exception("Data length is too high.")
        bb.setUInt16(0, val)
        return bb.array()

    @classmethod
    def getLLCBytes(cls, server, data):
        if server:
            return data.compare(_GXCommon.LLC_SEND_BYTES)
        return data.compare(_GXCommon.LLC_REPLY_BYTES)

    @classmethod
    def getHdlcData(cls, server, settings, reply, data, notify):
        # pylint:disable=too-many-arguments,too-many-locals,too-many-return-statements,
        # protected-access,broad-except
        ch = 0
        pos = reply.position
        packetStartID = reply.position
        frameLen = 0
        crc = 0
        crcRead = 0
        if reply.size - reply.position < 9:
            data.complete = False
            if notify:
                notify.complete = False
            return 0
        data.complete = True
        if notify:
            notify.complete = True
        isNotify = False
        while pos < len(reply):
            ch = reply.getUInt8()
            if ch == _GXCommon.HDLC_FRAME_START_END:
                packetStartID = pos
                break
            pos += 1
        if reply.position == len(reply):
            data.complete = False
            if notify:
                notify.complete = False
            return 0
        frame_ = reply.getUInt8()
        if (frame_ & 0xF0) != 0xA0:
            reply.position = reply.position - 1
            return GXDLMS.getHdlcData(server, settings, reply, data, notify)
        if (frame_ & 0x7) != 0:
            frameLen = (frame_ & 0x7) << 8
        ch = reply.getUInt8()
        frameLen += ch
        if len(reply) - reply.position + 1 < frameLen:
            data.complete = False
            if notify:
                notify.complete = False
            reply.position = packetStartID
            return 0
        eopPos = frameLen + packetStartID + 1
        ch = reply.getUInt8(eopPos)
        if ch != _GXCommon.HDLC_FRAME_START_END:
            reply.position = reply.position - 2
            return GXDLMS.getHdlcData(server, settings, reply, data, notify)
        addresses = [0, 0]
        try:
            # pylint: disable=broad-except
            ret = GXDLMS.checkHdlcAddress(server, settings, reply, eopPos, addresses)
        except Exception:
            ret = False
        if not ret:
            # If not notify.
            if not (
                reply.position < len(reply)
                and (
                    reply.getUInt8(reply.position) == 0x13
                    or reply.getUInt8(reply.position) == 0x3
                )
            ):
                reply.position = 1 + eopPos
                return GXDLMS.getHdlcData(server, settings, reply, data, notify)
            if notify:
                isNotify = True
                notify.targetAddress = addresses[1]
                notify.sourceAddress = addresses[0]
        # HDLC control fields
        cf = reply.getUInt8()
        if data.xml is None and not settings.checkFrame(cf, data.xml):
            reply.position = eopPos + 1
            return GXDLMS.getHdlcData(server, settings, reply, data, notify)
        if not isNotify and notify and cf in (0x13, 0x3):
            isNotify = True
            notify.clientAddress = addresses[1]
            notify.serverAddress = addresses[0]
        if (frame_ & 0x8) != 0:
            if isNotify:
                notify.moreData = notify.moreData | RequestTypes.FRAME
            else:
                data.moreData = data.moreData | RequestTypes.FRAME
        else:
            if isNotify:
                notify.moreData = notify.moreData & ~RequestTypes.FRAME
            else:
                data.moreData = data.moreData & ~RequestTypes.FRAME
        crc = _GXFCS16.countFCS16(
            reply, packetStartID + 1, reply.position - packetStartID - 1
        )
        crcRead = reply.getUInt16()
        if crc != crcRead:
            if len(reply) - reply.position > 8:
                return GXDLMS.getHdlcData(server, settings, reply, data, notify)
            raise Exception("Wrong CRC.")
        if reply.position != packetStartID + frameLen + 1:
            crc = _GXFCS16.countFCS16(reply, packetStartID + 1, frameLen - 2)
            crcRead = reply.getUInt16(packetStartID + frameLen - 1)
            if crc != crcRead:
                raise Exception("Wrong CRC.")
            if isNotify:
                notify.packetLength = eopPos - 2
            else:
                data.packetLength = eopPos - 2
        else:
            if isNotify:
                notify.packetLength = reply.position + 1
            else:
                data.packetLength = reply.position + 1
        if (
            cf != 0x13
            and cf != 0x3
            and (cf & HdlcFrameType.U_FRAME) == HdlcFrameType.U_FRAME
        ):
            if reply.position == packetStartID + frameLen + 1:
                reply.getUInt8()
            if cf == 0x97:
                data.error = ErrorCode.UNACCEPTABLE_FRAME
            elif cf == 0x1F:
                data.error = ErrorCode.DISCONNECT_MODE
            elif cf == 0x17:
                data.error = ErrorCode.DISCONNECT_MODE
            data.command = cf
        elif (
            cf != 0x13
            and cf != 0x3
            and (cf & HdlcFrameType.S_FRAME) == HdlcFrameType.S_FRAME
        ):
            tmp = (cf >> 2) & 0x3
            if tmp == HdlcControlFrame.REJECT:
                data.error = ErrorCode.REJECTED
            elif tmp == HdlcControlFrame.RECEIVE_NOT_READY:
                data.error = ErrorCode.RECEIVE_NOT_READY
            elif tmp == HdlcControlFrame.RECEIVE_READY:
                data.error = ErrorCode.OK
            if reply.position == packetStartID + frameLen + 1:
                reply.getUInt8()
        else:
            if reply.position == packetStartID + frameLen + 1:
                reply.getUInt8()
                if (cf & 0x1) == 0x1:
                    data.moreData = RequestTypes.FRAME
            else:
                if not GXDLMS.getLLCBytes(server, reply) and data.xml:
                    GXDLMS.getLLCBytes(not server, reply)
        return cf

    @classmethod
    def getServerAddress(cls, address, logical, physical):
        if address < 0x4000:
            logical[0] = address >> 7
            physical[0] = address & 0x7F
        else:
            logical[0] = address >> 14
            physical[0] = address & 0x3FFF

    @classmethod
    def checkHdlcAddress(cls, server, settings, reply, index, addresses):
        # pylint: disable=too-many-arguments
        target = _GXCommon.getHDLCAddress(reply)
        source = _GXCommon.getHDLCAddress(reply)
        addresses[0] = source
        addresses[1] = target
        if server:
            if settings.serverAddress not in (0, target):
                if reply.getUInt8(reply.position) == Command.SNRM:
                    settings.serverAddress = target
                else:
                    raise Exception(
                        "Server addresses do not match. It is "
                        + str(target)
                        + ". It should be "
                        + str(settings.serverAddress)
                        + "."
                    )
            else:
                settings.serverAddress = target
            if settings.clientAddress not in (0, source):
                if reply.getUInt8(reply.position) == Command.SNRM:
                    settings.clientAddress = source
                else:
                    raise Exception(
                        "Client addresses do not match. It is "
                        + str(source)
                        + ". It should be "
                        + str(settings.clientAddress)
                        + "."
                    )
            else:
                settings.clientAddress = source
        else:
            if settings.clientAddress != target:
                if (
                    settings.clientAddress == source
                    and settings.serverAddress == target
                ):
                    reply.position = index + 1
                return False
            # If All-station (Broadcast).
            if (
                settings.serverAddress != source
                and (settings.serverAddress and 0x7F) != 0x7F
                and (settings.serverAddress and 0x3FFF) != 0x3FFF
            ):
                readLogical = [0]
                readPhysical = [0]
                logical = [0]
                physical = [0]
                GXDLMS.getServerAddress(source, readLogical, readPhysical)
                GXDLMS.getServerAddress(settings.serverAddress, logical, physical)
                if readLogical[0] != logical[0] or readPhysical[0] != physical[0]:
                    return False
        return True

    @classmethod
    def __getTcpData(cls, settings, buff, data, notify):
        target = data
        if len(buff) - buff.position < 8:
            target.complete = False
            return True
        isData = True
        pos = buff.position
        value = int()
        while buff.position < len(buff) - 1:
            value = buff.getUInt16()
            # pylint: disable=no-else-break
            if value == 1:
                if not GXDLMS.checkWrapperAddress(settings, buff, data, notify):
                    target = notify
                    isData = False
                value = buff.getUInt16()
                compleate = not (len(buff) - buff.position) < value
                if compleate and (len(buff) - buff.position) != value:
                    print(
                        "Data length is "
                        + str(value)
                        + "and there are "
                        + str(len(buff) - buff.position)
                        + " bytes."
                    )
                target.complete = compleate
                if not compleate:
                    buff.position = pos
                else:
                    target.packetLength = buff.position + value
                break
            else:
                buff.position = buff.position - 1
        return isData

    # Validate M-Bus checksum
    @classmethod
    def __validateCheckSum(cls, bb, count):
        value = 0
        pos = 0
        while pos < count:
            value += bb.getUInt8(bb.position + pos)
            pos = pos + 1
        return value & 0xFF == bb.getUInt8(bb.position + count)

    # Get data from wired M-Bus frame.
    @classmethod
    def __getWiredMBusData(cls, settings, buff, data):
        packetStartID = buff.position
        if buff.getUInt8() != 0x68 or buff.available() < 5:
            data.complete = False
            buff.position = buff.position - 1
        else:
            # L-field.
            len_ = buff.getUInt8()
            # L-field.
            if (
                buff.getUInt8() != len_
                or buff.available() < 3 + len_
                or buff.getUInt8() != 0x68
            ):
                data.complete = False
                buff.position = packetStartID
            else:
                crc = GXDLMS.__validateCheckSum(buff, len_)
                if not crc and not data.xml:
                    data.complete = False
                    buff.position = packetStartID
                else:
                    if not crc:
                        data.xml.appendComment("Invalid checksum.")
                    # Check EOP.
                    if buff.getUInt8(buff.position + len_ + 1) != 0x16:
                        data.complete = False
                        buff.position = packetStartID
                        return
                    data.packetLength = buff.position + len_
                    data.complete = True
                    # index = data.data.position
                    # Control field (C-Field)
                    tmp = buff.getUInt8()
                    cmd_ = MBusCommand(tmp & 0xF)
                    # Address (A-field)
                    id_ = buff.getUInt8()
                    # The Control Information Field (CI-field)
                    ci = buff.getUInt8()
                    if ci == 0x0:
                        data.moreData = data.moreData or RequestTypes.FRAME
                    elif (ci >> 4) == (ci & 0xF):
                        # If this is the last telegram.
                        data.moreData &= ~RequestTypes.FRAME
                    # If M-Bus data header is present
                    if (tmp and 0x40) != 0:
                        # Message from primary(initiating) station
                        # Destination Transport Service Access Point
                        settings.clientAddress = buff.getUInt8()
                        # Source Transport Service Access Point
                        settings.serverAddress = buff.getUInt8()
                    else:
                        # Message from secondary (responding) station.
                        # Source Transport Service Access Point
                        settings.serverAddress = buff.getUInt8()
                        # Destination Transport Service Access Point
                        settings.clientAddress = buff.getUInt8()
                    if data.xml and data.xml.comments:
                        data.xml.appendComment("Command: " + str(cmd_))
                        data.xml.appendComment("A-Field: " + str(id_))
                        data.xml.appendComment("CI-Field: " + str(ci))
                        if (tmp & 0x40) != 0:
                            data.xml.appendComment(
                                "Primary station: " + str(settings.serverAddress)
                            )
                            data.xml.appendComment(
                                "Secondary station: " + str(settings.clientAddress)
                            )
                        else:
                            data.xml.appendComment(
                                "Primary station: " + str(settings.clientAddress)
                            )
                            data.xml.appendComment(
                                "Secondary station: " + str(settings.serverAddress)
                            )

    @classmethod
    def __getWirelessMBusData(cls, settings, buff, data):
        len_ = buff.getUInt8()
        # Some meters are counting length to frame size.
        if len(buff) < len_ - 1:
            data.complete = False
            buff.position = buff.position - 1
        else:
            # Some meters are counting length to frame size.
            if len(buff) < len_:
                len_ -= 1
            data.packetLength = len_
            data.complete = True
            cmd = buff.getUInt8()
            manufacturerID = buff.getUInt16()
            man = _GXCommon.decryptManufacturer(manufacturerID)
            # id =
            buff.getUInt32()
            meterVersion = buff.getUInt8()
            type_ = buff.getUInt8()
            ci = buff.getUInt8()
            # frameId =
            buff.getUInt8()
            # state =
            buff.getUInt8()
            configurationWord = buff.getUInt16()
            encryption = MBusEncryptionMode(configurationWord & 7)
            settings.clientAddress = buff.getUInt8()
            settings.serverAddress = buff.getUInt8()
            if data.xml and data.xml.comments:
                data.xml.appendComment("Command: " + cmd)
                data.xml.appendComment("Manufacturer: " + man)
                data.xml.appendComment("Meter Version: " + meterVersion)
                data.xml.appendComment("Meter Type: " + type_)
                data.xml.appendComment("Control Info: " + ci)
                data.xml.appendComment("Encryption: " + encryption)
            elif settings.mBus:
                settings.mBus.manufacturerId = _GXCommon.decryptManufacturer(
                    manufacturerID
                )
                settings.mBus.version = meterVersion
                settings.mBus.meterType = type_

    # Get data from S-FSK PLC frame.
    @classmethod
    def __getPlcData(cls, settings, buff, data):
        # pylint: disable=too-many-locals
        if buff.available() < 9:
            data.complete = False
            return
        packetStartID = buff.position
        # Find STX.
        pos = buff.position
        while pos < buff.size:
            stx = buff.getUInt8()
            if stx == 2:
                packetStartID = pos
                break
            pos = pos + 1
        # Not a PLC frame.
        if buff.position == buff.size:
            # Not enough data to parse
            data.complete = False
            buff.position = packetStartID
            return
        len_ = buff.getUInt8()
        index = buff.position
        if buff.available() < len_:
            data.complete = False
            buff.position = buff.position - 2
        else:
            buff.getUInt8()
            # Credit fields.  IC, CC, DC
            # credit =
            buff.getUInt8()
            # MAC Addresses.
            mac = buff.getUInt24()
            # SA.
            macSa = mac >> 12
            # DA.
            macDa = mac and 0xFFF
            # PAD length.
            padLen = buff.getUInt8()
            if buff.size < len_ + padLen + 2:
                data.complete = False
                buff.position = buff.position - (index + 6)
            else:
                # DL.Data.request
                ch = buff.getUInt8()
                if ch != PlcDataLinkData.REQUEST:
                    raise Exception(
                        "Parsing MAC LLC data failed. Invalid DataLink data request."
                    )
                # da =
                buff.getUInt8()
                # sa =
                buff.getUInt8()
                if settings.IsServer:
                    data.complete = data.xml or (
                        macDa
                        in (
                            PlcDestinationAddress.ALL_PHYSICAL,
                            settings.plc.macSourceAddress,
                        )
                        and macSa
                        in (
                            PlcSourceAddress.INITIATOR,
                            settings.plc.macDestinationAddress,
                        )
                    )
                    data.sourceAddress = macDa
                    data.targetAddress = macSa
                else:
                    data.complete = data.xml or (
                        macDa
                        in (
                            PlcDestinationAddress.ALL_PHYSICAL,
                            PlcSourceAddress.INITIATOR,
                            settings.plc.macDestinationAddress,
                        )
                    )
                    data.targetAddress = macDa
                    data.sourceAddress = macSa
                # Skip padding.
                if data.complete:
                    crcCount = _GXFCS16.countFCS16(buff.data, 0, len_ + padLen)
                    crc = buff.getUInt16(len_ + padLen)
                    # Check CRC.
                    if crc != crcCount:
                        if not data.xml:
                            raise Exception("Invalid data checksum.")
                        data.xml.appendComment("Invalid data checksum.")
                    data.packetLength = len_
                else:
                    buff.position = packetStartID

    # Get data from S-FSK PLC Hdlc frame.
    @classmethod
    def __getPlcHdlcData(cls, settings, buff, data):
        if buff.available() < 2:
            data.complete = False
            return 0
        frame = 0
        # SN field.
        frameLen = GXDLMS.getPlcSfskFrameSize(buff)
        if frameLen == 0:
            raise Exception("Invalid PLC frame size.")
        if buff.Available < frameLen:
            data.complete = False
        else:
            buff.position = buff.position + 2
            index = buff.position
            # Credit fields.  IC, CC, DC
            # credit =
            buff.getUInt8()
            # MAC Addresses.
            mac = buff.getUInt24()
            # SA.
            sa = mac >> 12
            # DA.
            da = mac & 0xFFF
            if settings.isServer:
                data.complete = data.xml or (
                    da
                    in (
                        PlcDestinationAddress.ALL_PHYSICAL,
                        settings.plc.macSourceAddress,
                    )
                    and sa
                    in (
                        PlcHdlcSourceAddress.INITIATOR,
                        settings.plc.macDestinationAddress,
                    )
                )
                data.sourceAddress = da
                data.targetAddress = sa
            else:
                data.complete = data.xml or da in (
                    PlcHdlcSourceAddress.INITIATOR,
                    settings.plc.macDestinationAddress,
                )
                data.targetAddress = sa
                data.sourceAddress = da
            if data.IsComplete:
                # PAD length.
                padLen = buff.getUInt8()
                frame = GXDLMS.getHdlcData(
                    settings.isServer, settings, buff, data, None
                )
                GXDLMS.getDataFromFrame(buff, data, True)
                buff.position = buff.position + padLen
                crcCount = _GXFCS16.countFCS24(buff.data, index, buff.position - index)
                crc = buff.getUInt24(buff.Position)
                # Check CRC.
                if crc != crcCount:
                    if not data.xml:
                        raise Exception("Invalid data checksum.")
                    data.xml.appendComment("Invalid data checksum.")
                data.packetLength = 2 + buff.position - index
            else:
                buff.position = buff.position + (frameLen - index - 4)
        return frame

    # Check is this wireless M-Bus message.
    @classmethod
    def isWirelessMBusData(cls, buff):
        if len(buff) - buff.position < 2:
            return False
        cmd = buff.getUInt8(buff.position + 1)
        return cmd in (MBusCommand.SND_NR, MBusCommand.SND_UD, MBusCommand.RSP_UD)

    # Check is this wired M-Bus message.
    @classmethod
    def isWiredMBusData(cls, buff):
        if len(buff) - buff.position < 1:
            return False
        return buff.getUInt8(buff.position) == 0x68

    # Check is this PLC S-FSK message.
    # buff: Received data.
    # Returns S-FSK frame size in bytes.
    @classmethod
    def getPlcSfskFrameSize(cls, buff):
        ret = 0
        if not buff.size - buff.position < 2:
            len_ = buff.getUInt16(buff.position)
            if len_ == int(PlcMacSubframes.ONE):
                ret = 36
            elif len_ == int(PlcMacSubframes.TWO):
                ret = 2 * 36
            elif len_ == int(PlcMacSubframes.THREE):
                ret = 3 * 36
            elif len_ == int(PlcMacSubframes.FOUR):
                ret = 4 * 36
            elif len_ == int(PlcMacSubframes.FIVE):
                ret = 5 * 36
            elif len_ == int(PlcMacSubframes.SIX):
                ret = 6 * 36
            elif len_ == int(PlcMacSubframes.SEVEN):
                ret = 7 * 36
        return ret

    @classmethod
    def checkWrapperAddress(cls, settings, buff, data, notify):
        ret = True
        value = 0
        if settings.isServer:
            value = buff.getUInt16()
            data.sourceAddress = value
            # Check that client addresses match.
            if (
                not data.xml
                and settings.clientAddress != 0
                and settings.clientAddress != value
            ):
                raise Exception(
                    "Source addresses do not match. It is "
                    + str(value)
                    + ". It should be "
                    + str(settings.clientAddress)
                    + "."
                )
            settings.clientAddress = value
            value = buff.getUInt16()
            data.targetAddress = value
            if (
                not data.xml
                and settings.serverAddress != 0
                and settings.serverAddress != value
            ):
                raise Exception(
                    "Destination addresses do not match. It is "
                    + str(value)
                    + ". It should be "
                    + str(settings.serverAddress)
                    + "."
                )
            settings.serverAddress = value
        else:
            value = buff.getUInt16()
            data.targetAddress = value
            if settings.clientAddress != 0 and settings.serverAddress != value:
                if notify is None:
                    raise Exception(
                        "Source addresses do not match. It is "
                        + str(value)
                        + ". It should be "
                        + str(settings.serverAddress)
                        + "."
                    )
                notify.sourceAddress = value
                ret = False
            else:
                settings.serverAddress = value
            value = buff.getUInt16()
            data.sourceAddress = value
            if (
                not data.xml
                and settings.clientAddress != 0
                and settings.clientAddress != value
            ):
                if notify is None:
                    raise Exception(
                        "Destination addresses do not match. It is "
                        + str(value)
                        + ". It should be "
                        + str(settings.clientAddress)
                        + "."
                    )
                ret = False
                notify.targetAddress = value
            else:
                settings.clientAddress = value
        return ret

    @classmethod
    def readResponseDataBlockResult(cls, settings, reply, index):
        reply.error = 0
        data = reply.data
        lastBlock = data.getUInt8()
        number = data.getUInt16()
        blockLength = _GXCommon.getObjectCount(data)
        if lastBlock == 0:
            reply.moreData = RequestTypes(reply.moreData | RequestTypes.DATABLOCK)
        else:
            reply.moreData = RequestTypes(reply.moreData & ~RequestTypes.DATABLOCK)
        if number != 1 and settings.blockIndex == 1:
            settings.setBlockIndex(number)
        expectedIndex = settings.blockIndex
        if number != expectedIndex:
            raise ValueError(
                "Invalid Block number. It is "
                + str(number)
                + " and it should be "
                + str(expectedIndex)
                + "."
            )
        if (reply.moreData & RequestTypes.FRAME) != 0:
            GXDLMS.getDataFromBlock(data, index)
            return False
        if blockLength != data.size - data.position:
            raise ValueError("Invalid block length.")
        reply.command = Command.NONE
        if reply.xml:
            data.strip()
            reply.xml.appendStartTag(
                Command.READ_RESPONSE, SingleReadResponse.DATA_BLOCK_RESULT
            )
            reply.xml.appendLine(
                TranslatorTags.LAST_BLOCK, None, reply.xml.integerToHex(lastBlock, 2)
            )
            reply.xml.appendLine(
                TranslatorTags.BLOCK_NUMBER, None, reply.xml.integerToHex(number, 4)
            )
            reply.xml.appendLine(
                TranslatorTags.RAW_DATA, None, data.toHex(False, 0, data.size)
            )
            reply.xml.appendEndTag(
                Command.READ_RESPONSE, SingleReadResponse.DATA_BLOCK_RESULT
            )
            return False
        GXDLMS.getDataFromBlock(reply.data, index)
        reply.setTotalCount(0)
        if reply.getMoreData() == RequestTypes.NONE:
            settings.resetBlockIndex()
        return True

    @classmethod
    def handleReadResponse(cls, settings, reply, index):
        data = reply.data
        pos = 0
        cnt = reply.getTotalCount()
        first = cnt == 0 or reply.commandType == SingleReadResponse.DATA_BLOCK_RESULT
        if first:
            cnt = _GXCommon.getObjectCount(reply.data)
            reply.totalCount = cnt
        type_ = 0
        values = None
        if cnt != 1:
            # Parse data after all data is received when readlist is used.
            if reply.isMoreData():
                GXDLMS.getDataFromBlock(reply.data, 0)
                return False
            if not first:
                reply.data.position = 0
                first = True
            values = []
            if isinstance(reply.value, list):
                values.append(reply.value)
            reply.value = None
        if reply.xml:
            reply.xml.appendStartTag(
                Command.READ_RESPONSE, "Qty", reply.xml.integerToHex(cnt, 2)
            )
        while pos != cnt:
            if first:
                type_ = data.getUInt8()
                reply.commandType = type_
            else:
                type_ = reply.commandType
            standardXml = (
                reply.xml and reply.xml.outputType == TranslatorOutputType.STANDARD_XML
            )
            if type_ == SingleReadResponse.DATA:
                reply.error = 0
                if reply.xml:
                    if standardXml:
                        reply.xml.appendStartTag(TranslatorTags.CHOICE)
                    reply.xml.appendStartTag(
                        Command.READ_RESPONSE, SingleReadResponse.DATA
                    )
                    di = _GXDataInfo()
                    di.xml = reply.xml
                    _GXCommon.getData(settings, reply.data, di)
                    reply.xml.appendEndTag(
                        Command.READ_RESPONSE, SingleReadResponse.DATA
                    )
                    if standardXml:
                        reply.xml.appendEndTag(TranslatorTags.CHOICE)
                elif cnt == 1:
                    GXDLMS.getDataFromBlock(reply.data, 0)
                else:
                    reply.readPosition = data.position
                    GXDLMS.getValueFromData(settings, reply)
                    data.position = reply.readPosition
                    values.append(reply.value)
                    reply.value = None
            elif type_ == SingleReadResponse.DATA_ACCESS_ERROR:
                reply.error = data.getUInt8()
                if reply.xml:
                    if standardXml:
                        reply.xml.appendStartTag(TranslatorTags.CHOICE)
                    reply.xml.appendLine(
                        Command.READ_RESPONSE << 8
                        | SingleReadResponse.DATA_ACCESS_ERROR,
                        None,
                        GXDLMS.errorCodeToString(reply.xml.outputType, reply.error),
                    )
                    if standardXml:
                        reply.xml.appendEndTag(TranslatorTags.CHOICE)
            elif type_ == SingleReadResponse.DATA_BLOCK_RESULT:
                if not GXDLMS.readResponseDataBlockResult(settings, reply, index):
                    if reply.xml:
                        reply.xml.appendEndTag(Command.READ_RESPONSE)
                    return False
            elif type_ == SingleReadResponse.BLOCK_NUMBER:
                number = data.getUInt16()
                if number != settings.blockIndex:
                    raise ValueError(
                        "Invalid Block number. It is "
                        + str(number)
                        + " and it should be "
                        + str(settings.blockIndex)
                        + "."
                    )
                settings.increaseBlockIndex()
                reply.moreData = RequestTypes(reply.moreData | RequestTypes.DATABLOCK)
            else:
                raise Exception("HandleReadResponse failed. Invalid tag.")
            pos += 1
        if reply.xml:
            reply.xml.appendEndTag(Command.READ_RESPONSE)
            return True
        if values:
            reply.value = values
        return cnt == 1

    @classmethod
    def errorCodeToString(cls, type_, value):
        if type_ == TranslatorOutputType.STANDARD_XML:
            return TranslatorStandardTags.errorCodeToString(value)
        return TranslatorSimpleTags.errorCodeToString(value)

    @classmethod
    def handleActionResponseNormal(cls, settings, data):
        ret = data.data.getUInt8()
        if ret != 0:
            data.error = ret
        if data.xml:
            if data.xml.outputType == TranslatorOutputType.STANDARD_XML:
                data.xml.appendStartTag(TranslatorTags.SINGLE_RESPONSE)
            data.xml.appendLine(
                TranslatorTags.RESULT,
                None,
                GXDLMS.errorCodeToString(data.xml.outputType, data.error),
            )
        settings.resetBlockIndex()
        if data.data.position < data.data.size:
            ret = data.data.getUInt8()
            if ret == 0:
                GXDLMS.getDataFromBlock(data.data, 0)
            elif ret == 1:
                ret = int(data.data.getUInt8())
                if ret != 0:
                    data.error = data.data.getUInt8()
                    if ret == 9 and data.getError() == 16:
                        data.data.position = data.data.position - 2
                        GXDLMS.getDataFromBlock(data.data, 0)
                        data.error = 0
                        ret = 0
                else:
                    GXDLMS.getDataFromBlock(data.data, 0)
            else:
                raise Exception("HandleActionResponseNormal failed. " + "Invalid tag.")
            if data.xml and (ret != 0 or data.data.position < data.data.size):
                data.xml.appendStartTag(TranslatorTags.RETURN_PARAMETERS)
                if ret != 0:
                    data.xml.appendLine(
                        TranslatorTags.DATA_ACCESS_ERROR,
                        None,
                        GXDLMS.errorCodeToString(data.xml.outputType, data.error),
                    )
                else:
                    data.xml.appendStartTag(
                        Command.READ_RESPONSE, SingleReadResponse.DATA
                    )
                    di = _GXDataInfo()
                    di.xml = data.xml
                    _GXCommon.getData(settings, data.data, di)
                    data.xml.appendEndTag(
                        Command.READ_RESPONSE, SingleReadResponse.DATA
                    )
                data.xml.appendEndTag(TranslatorTags.RETURN_PARAMETERS)
                if data.xml.outputType == TranslatorOutputType.STANDARD_XML:
                    data.xml.appendEndTag(TranslatorTags.SINGLE_RESPONSE)

    @classmethod
    def handleActionResponseWithBlock(cls, settings, reply, index):
        ret = True
        ch = reply.data.getUInt8()
        if reply.xml:
            # Result start tag.
            reply.xml.appendStartTag(TranslatorTags.P_BLOCK)
            # LastBlock
            reply.xml.appendLine(
                TranslatorTags.LAST_BLOCK, None, reply.xml.integerToHex(ch, 2)
            )
        if ch == 0:
            reply.moreData = reply.moreData | RequestTypes.DATABLOCK
        else:
            reply.moreData = reply.moreData & ~RequestTypes.DATABLOCK
        # Get Block number.
        number = reply.data.getUInt32()
        if reply.xml:
            # BlockNumber
            reply.xml.AppendLine(
                TranslatorTags.BLOCK_NUMBER, None, reply.xml.integerToHex(number, 8)
            )
        else:
            # Update initial block index.  This is critical if message is send
            # and received in multiple blocks.
            if number == 1:
                settings.resetBlockIndex()
            if number != settings.blockIndex:
                raise ValueError(
                    "Invalid Block number. It is "
                    + str(number)
                    + " and it should be "
                    + str(settings.BlockIndex)
                    + "."
                )
        # Note!  There is no status!!
        if reply.xml:
            if reply.data.available() != 0:
                # Get data size.
                blockLength = _GXCommon.getObjectCount(reply.data)
                # if whole block is read.
                if (reply.moreData & RequestTypes.FRAME) == 0:
                    # Check Block length.
                    if blockLength > reply.data.available():
                        reply.xml.appendComment(
                            "Block is not complete."
                            + str(reply.data.available())
                            + "/"
                            + str(blockLength)
                            + "."
                        )
                reply.xml.appendLine(
                    TranslatorTags.RAW_DATA,
                    None,
                    GXByteBuffer.toHex(
                        reply.data.data,
                        False,
                        reply.data.position,
                        reply.data.available(),
                    ),
                )
            reply.xml.AppendEndTag(TranslatorTags.P_BLOCK)
        elif reply.data.available() != 0:
            # Get data size.
            blockLength = _GXCommon.getObjectCount(reply.data)
            # if whole block is read.
            if (reply.moreData & RequestTypes.FRAME) == 0:
                # Check Block length.
                if blockLength > reply.data.available():
                    raise ValueError("Not enought data.")
                # Keep command if this is last block for XML Client.
                if (reply.moreData & RequestTypes.DATABLOCK) != 0:
                    reply.command = Command.NONE
            if blockLength == 0:
                # If meter sends empty data block.
                reply.data.size = index
            else:
                GXDLMS.getDataFromBlock(reply.data, index)
            # If last packet and data is not try to peek.
            if reply.moreData == RequestTypes.NONE:
                reply.data.position = 0
                settings.resetBlockIndex()
        elif reply.data.available() == 0:
            # Empty block.  Conformance tests uses this.
            reply.EmptyResponses |= RequestTypes.DATABLOCK
        if (
            reply.moreData == RequestTypes.NONE
            and settings
            and settings.command == Command.METHOD_REQUEST
            and settings.commandType == ActionResponseType.WITH_LIST
        ):
            raise ValueError("Action with list is not implemented.")
        return ret

    @classmethod
    def handleMethodResponse(cls, settings, data, index):
        type_ = int(data.data.getUInt8())
        data.invokeId = data.data.getUInt8()
        if data.xml:
            data.xml.appendStartTag(Command.METHOD_RESPONSE)
            data.xml.appendStartTag(Command.METHOD_RESPONSE, type_)
            data.xml.appendLine(
                TranslatorTags.INVOKE_ID, None, data.xml.integerToHex(data.invokeId, 2)
            )
        if type_ == ActionResponseType.NORMAL:
            GXDLMS.handleActionResponseNormal(settings, data)
        elif type_ == 2:
            GXDLMS.handleActionResponseWithBlock(settings, data, index)
        elif type_ == 3:
            raise ValueError("Invalid Command.")
        elif type_ == 4:
            number = data.data.getUInt32()
            if data.xml:
                data.xml.appendLine(
                    TranslatorTags.BLOCK_NUMBER, None, data.xml.integerToHex(number, 8)
                )
            elif number != settings.blockIndex:
                raise ValueError(
                    "Invalid Block number. It is "
                    + str(number)
                    + " and it should be "
                    + str(settings.BlockIndex)
                    + "."
                )
            settings.increaseBlockIndex()
        else:
            raise ValueError("Invalid Command.")
        if data.xml:
            data.xml.appendEndTag(Command.METHOD_RESPONSE, type_)
            data.xml.appendEndTag(Command.METHOD_RESPONSE)

    @classmethod
    def handlePush(cls, reply):
        data = reply.data
        index = data.position - 1
        last = data.getUInt8()
        if (last & 0x80) == 0:
            reply.moreData = RequestTypes(reply.moreData | RequestTypes.DATABLOCK)
        else:
            reply.moreData = RequestTypes(reply.moreData & ~RequestTypes.DATABLOCK)
        data.getUInt8()
        data.getUInt8()
        data.getUInt8()
        data.getUInt8()
        if (data.getUInt8() & 0x0F) == 0:
            raise ValueError("Invalid data.")
        reply.data.getUInt32()
        len_ = reply.data.getUInt8()
        if len_ != 0:
            reply.data.position = reply.data.position + len_
        GXDLMS.getDataFromBlock(reply.data, index)

    @classmethod
    def handleAccessResponse(cls, settings, reply):
        data = reply.data
        reply.invokeId = reply.data.getUInt32()
        len_ = reply.data.getUInt8()
        tmp = None
        if len_ != 0:
            tmp = bytearray(len_)
            data.get(tmp)
            reply.time = _GXCommon.changeType(settings, tmp, DataType.DATETIME)
        if reply.xml:
            reply.xml.appendStartTag(Command.ACCESS_RESPONSE)
            reply.xml.appendLine(
                TranslatorTags.LONG_INVOKE_ID,
                None,
                reply.xml.integerToHex(reply.invokeId, 8),
            )
            if reply.time:
                reply.xml.appendComment(str(reply.time))
            reply.xml.appendLine(
                TranslatorTags.DATE_TIME, None, GXByteBuffer.hex(tmp, False)
            )
            reply.data.getUInt8()
            len_ = _GXCommon.getObjectCount(reply.data)
            reply.xml.appendStartTag(TranslatorTags.ACCESS_RESPONSE_BODY)
            reply.xml.appendStartTag(
                TranslatorTags.ACCESS_RESPONSE_LIST_OF_DATA,
                "Qty",
                reply.xml.integerToHex(len_, 2),
            )
            pos = 0
            while pos != len_:
                if reply.xml.outputType == TranslatorOutputType.STANDARD_XML:
                    reply.xml.appendStartTag(
                        Command.WRITE_REQUEST, SingleReadResponse.DATA
                    )
                di = _GXDataInfo()
                di.xml = reply.xml
                _GXCommon.getData(settings, reply.data, di)
                if reply.xml.outputType == TranslatorOutputType.STANDARD_XML:
                    reply.xml.appendEndTag(
                        Command.WRITE_REQUEST, SingleReadResponse.DATA
                    )
                pos += 1
            reply.xml.appendEndTag(TranslatorTags.ACCESS_RESPONSE_LIST_OF_DATA)
            err = int()
            len_ = _GXCommon.getObjectCount(reply.data)
            reply.xml.appendStartTag(
                TranslatorTags.LIST_OF_ACCESS_RESPONSE_SPECIFICATION,
                "Qty",
                reply.xml.integerToHex(len_, 2),
            )
            pos = 0
            while pos != len_:
                type_ = int(data.getUInt8())
                err = data.getUInt8()
                if err != 0:
                    err = data.getUInt8()
                reply.xml.appendStartTag(TranslatorTags.ACCESS_RESPONSE_SPECIFICATION)
                reply.xml.appendStartTag(Command.ACCESS_RESPONSE, type_)
                reply.xml.appendLine(
                    TranslatorTags.RESULT,
                    None,
                    GXDLMS.errorCodeToString(reply.xml, err),
                )
                reply.xml.appendEndTag(Command.ACCESS_RESPONSE, type_)
                reply.xml.appendEndTag(TranslatorTags.ACCESS_RESPONSE_SPECIFICATION)
                pos += 1
            reply.xml.appendEndTag(TranslatorTags.LIST_OF_ACCESS_RESPONSE_SPECIFICATION)
            reply.xml.appendEndTag(TranslatorTags.ACCESS_RESPONSE_BODY)
            reply.xml.appendEndTag(Command.ACCESS_RESPONSE)
        else:
            data.getUInt8()

    @classmethod
    def handleDataNotification(cls, settings, reply):
        data = reply.data
        start = data.position - 1
        reply.invokeId = data.getUInt32()
        reply.time = None
        len_ = data.getUInt8()
        tmp = None
        if len_ != 0:
            tmp = bytearray(len_)
            data.get(tmp)
            dt = DataType.DATETIME
            if len_ == 4:
                dt = DataType.TIME
            elif len_ == 5:
                dt = DataType.DATE
            info = _GXDataInfo()
            info.type_ = dt
            reply.time = _GXCommon.getData(settings, GXByteBuffer(tmp), info)
        if reply.xml:
            reply.xml.appendStartTag(Command.DATA_NOTIFICATION)
            reply.xml.appendLine(
                TranslatorTags.LONG_INVOKE_ID,
                None,
                reply.xml.integerToHex(reply.invokeId, 8),
            )
            if reply.time:
                reply.xml.appendComment(str(reply.time))
            reply.xml.appendLine(
                TranslatorTags.DATE_TIME, None, GXByteBuffer.hex(tmp, False)
            )
            reply.xml.appendStartTag(TranslatorTags.NOTIFICATION_BODY)
            reply.xml.appendStartTag(TranslatorTags.DATA_VALUE)
            di = _GXDataInfo()
            di.xml = reply.xml
            _GXCommon.getData(settings, reply.data, di)
            reply.xml.appendEndTag(TranslatorTags.DATA_VALUE)
            reply.xml.appendEndTag(TranslatorTags.NOTIFICATION_BODY)
            reply.xml.appendEndTag(Command.DATA_NOTIFICATION)
        else:
            GXDLMS.getDataFromBlock(reply.data, start)
            GXDLMS.getValueFromData(settings, reply)

    @classmethod
    def handleSetResponse(cls, data):
        type_ = SetResponseType(data.data.getUInt8())
        data.invokeId = data.data.getUInt8()
        if data.xml:
            data.xml.appendStartTag(Command.SET_RESPONSE)
            data.xml.appendStartTag(Command.SET_RESPONSE, type_)
            data.xml.appendLine(
                TranslatorTags.INVOKE_ID, None, data.xml.integerToHex(data.invokeId, 2)
            )
        if type_ == SetResponseType.NORMAL:
            data.error = data.data.getUInt8()
            if data.xml:
                data.xml.appendLine(
                    TranslatorTags.RESULT,
                    None,
                    GXDLMS.errorCodeToString(data.xml.outputType, data.error),
                )
        elif type_ == SetResponseType.DATA_BLOCK:
            number = data.data.getUInt32()
            if data.xml:
                data.xml.appendLine(
                    TranslatorTags.BLOCK_NUMBER, None, data.xml.integerToHex(number, 8)
                )
        elif type_ == SetResponseType.LAST_DATA_BLOCK:
            data.error = data.data.getUInt8()
            number = data.data.getUInt32()
            if data.xml:
                data.xml.appendLine(
                    TranslatorTags.RESULT,
                    None,
                    GXDLMS.errorCodeToString(data.xml.outputType, data.error),
                )
                data.xml.appendLine(
                    TranslatorTags.BLOCK_NUMBER, None, data.xml.integerToHex(number, 8)
                )
        elif type_ == SetResponseType.WITH_LIST:
            cnt = _GXCommon.getObjectCount(data.data)
            if data.xml:
                data.xml.appendStartTag(TranslatorTags.RESULT, "Qty", str(cnt))
                pos = 0
                while pos != cnt:
                    err = data.data.getUInt8()
                    data.xml.appendLine(
                        TranslatorTags.DATA_ACCESS_RESULT,
                        None,
                        GXDLMS.errorCodeToString(data.xml.outputType, err),
                    )
                    pos += 1
                data.xml.appendEndTag(TranslatorTags.RESULT)
            else:
                pos = 0
                while pos != cnt:
                    err = data.data.getUInt8()
                    if data.getError() == 0 and err != 0:
                        data.error = err
                    pos += 1
        else:
            raise ValueError("Invalid data type.")
        if data.xml:
            data.xml.appendEndTag(Command.SET_RESPONSE, type_)
            data.xml.appendEndTag(Command.SET_RESPONSE)

    @classmethod
    def handleWriteResponse(cls, data):
        cnt = _GXCommon.getObjectCount(data.data)
        ret = int()
        if data.xml:
            data.xml.appendStartTag(
                Command.WRITE_RESPONSE, "Qty", data.xml.integerToHex(cnt, 2)
            )
        pos = 0
        while pos != cnt:
            ret = data.data.getUInt8()
            if ret != 0:
                data.error = data.data.getUInt8()
            if data.xml:
                if ret == 0:
                    data.xml.appendLine(
                        "<" + GXDLMS.errorCodeToString(data.xml.outputType, ret) + " />"
                    )
                else:
                    data.xml.appendLine(
                        TranslatorTags.DATA_ACCESS_ERROR,
                        None,
                        GXDLMS.errorCodeToString(data.xml.outputType, data.error),
                    )
            pos += 1
        if data.xml:
            data.xml.appendEndTag(Command.WRITE_RESPONSE)

    @classmethod
    def handleGetResponseWithList(cls, settings, reply):
        cnt = _GXCommon.getObjectCount(reply.data)
        values = list([None] * cnt)
        if reply.xml:
            reply.xml.appendStartTag(
                TranslatorTags.RESULT, "Qty", reply.xml.integerToHex(cnt, 2)
            )
        pos = 0
        while pos != cnt:
            ch = reply.data.getUInt8()
            if ch != 0:
                reply.error = reply.data.getUInt8()
            else:
                if reply.xml:
                    di = _GXDataInfo()
                    di.xml = reply.xml
                    reply.xml.appendStartTag(
                        Command.READ_RESPONSE, SingleReadResponse.DATA
                    )
                    _GXCommon.getData(settings, reply.data, di)
                    reply.xml.appendEndTag(
                        Command.READ_RESPONSE, SingleReadResponse.DATA
                    )
                else:
                    reply.readPosition = reply.data.position
                    GXDLMS.getValueFromData(settings, reply)
                    if reply.value is None:
                        # Increase read position if data is null. This is a special case.
                        reply.readPosition = 1 + reply.readPosition
                    reply.data.position = reply.readPosition
                    if values:
                        values[pos] = reply.value
                    reply.value = None
            pos += 1
        reply.value = values

    @classmethod
    def handleGetResponseNormal(cls, settings, reply):
        if reply.data.available() == 0:
            empty = True
            GXDLMS.getDataFromBlock(reply.data, 0)
        else:
            empty = False
            # Result
            ch = reply.data.getUInt8()
            if ch != 0:
                reply.error = reply.data.getUInt8()
            if reply.xml:
                # Result start tag.
                reply.xml.appendStartTag(TranslatorTags.RESULT)
                if reply.error:
                    reply.xml.appendLine(
                        TranslatorTags.DATA_ACCESS_ERROR,
                        None,
                        GXDLMS.errorCodeToString(reply.xml.outputType, reply.error),
                    )
                else:
                    reply.xml.appendStartTag(TranslatorTags.DATA)
                    di = _GXDataInfo()
                    di.xml = reply.xml
                    _GXCommon.getData(settings, reply.data, di)
                    reply.xml.appendEndTag(TranslatorTags.DATA)
            else:
                GXDLMS.getDataFromBlock(reply.data, 0)
        return empty

    @classmethod
    def handleGetResponseNextDataBlock(cls, settings, reply, index):
        ret = True
        ch = reply.data.getUInt8()
        if reply.xml:
            reply.xml.appendStartTag(TranslatorTags.RESULT)
            reply.xml.appendLine(
                TranslatorTags.LAST_BLOCK, None, reply.xml.integerToHex(ch, 2)
            )
        if ch == 0:
            reply.moreData = reply.moreData | RequestTypes.DATABLOCK
        else:
            reply.moreData = reply.moreData & ~RequestTypes.DATABLOCK
        number = reply.data.getUInt32()
        if reply.xml:
            reply.xml.appendLine(
                TranslatorTags.BLOCK_NUMBER, None, reply.xml.integerToHex(number, 8)
            )
        else:
            # If meter's block index is zero based.
            if number != 1 and settings.blockIndex == 1:
                settings.blockIndex = number
            if number != settings.blockIndex:
                raise ValueError(
                    "Invalid Block number. It is "
                    + str(number)
                    + " and it should be "
                    + str(settings.blockIndex)
                    + "."
                )
        # Get status.
        ch = reply.data.getUInt8()
        if ch != 0:
            reply.error = reply.data.getUInt8()
        if reply.xml:
            reply.xml.appendStartTag(TranslatorTags.RESULT)
            if reply.getError() != 0:
                reply.xml.appendLine(
                    TranslatorTags.DATA_ACCESS_RESULT,
                    None,
                    GXDLMS.errorCodeToString(reply.xml.outputType, reply.error),
                )
            elif reply.data.available() != 0:
                blockLength = _GXCommon.getObjectCount(reply.data)
                if (reply.moreData & RequestTypes.FRAME) == 0:
                    if blockLength > len(reply.data) - reply.data.position:
                        reply.xml.appendComment(
                            "Block is not complete."
                            + str(len(reply.data) - reply.data.position)
                            + "/"
                            + str(blockLength)
                            + "."
                        )
                reply.xml.appendLine(
                    TranslatorTags.RAW_DATA,
                    None,
                    reply.data.toHex(
                        False, reply.data.position, reply.data.available()
                    ),
                )
            reply.xml.appendEndTag(TranslatorTags.RESULT)
        elif reply.data.available() != 0:
            # Get data size.
            blockLength = _GXCommon.getObjectCount(reply.data)
            # if whole block is read.
            if (reply.moreData & RequestTypes.FRAME) == 0:
                # Check Block length.
                if blockLength > reply.data.available():
                    raise ValueError("Not enought data.")
                # Keep command if this is last block for XML Client.
                if (reply.moreData & RequestTypes.DATABLOCK) != 0:
                    reply.command = Command.NONE
            if blockLength == 0:
                # If meter sends empty data block.
                reply.data.Size = index
            else:
                GXDLMS.getDataFromBlock(reply.data, index)
            # If last packet and data is not try to peek.
            if reply.moreData == RequestTypes.NONE:
                reply.data.position = 0
                settings.resetBlockIndex()

            if (
                reply.moreData == RequestTypes.NONE
                and settings
                and settings.command == Command.GET_REQUEST
                and settings.commandType == GetCommandType.WITH_LIST
            ):
                GXDLMS.handleGetResponseWithList(settings, reply)
                ret = False
        return ret

    @classmethod
    def handleGetResponse(cls, settings, reply, index):
        # pylint: disable=too-many-locals
        ret = True
        type_ = reply.data.getUInt8()
        reply.invokeId = reply.data.getUInt8()
        if reply.xml:
            reply.xml.appendStartTag(Command.GET_RESPONSE)
            reply.xml.appendStartTag(Command.GET_RESPONSE, type_)
            reply.xml.appendLine(
                TranslatorTags.INVOKE_ID,
                None,
                reply.xml.integerToHex(reply.invokeId, 2),
            )
        empty = False
        if type_ == GetCommandType.NORMAL:
            empty = GXDLMS.handleGetResponseNormal(settings, reply)
        elif type_ == GetCommandType.NEXT_DATA_BLOCK:
            GXDLMS.handleGetResponseNextDataBlock(settings, reply, index)
        elif type_ == GetCommandType.WITH_LIST:
            GXDLMS.handleGetResponseWithList(settings, reply)
            ret = False
        else:
            raise ValueError("Invalid Get response.")
        if reply.xml:
            if not empty:
                reply.xml.appendEndTag(TranslatorTags.RESULT)
            reply.xml.appendEndTag(Command.GET_RESPONSE, type_)
            reply.xml.appendEndTag(Command.GET_RESPONSE)
        return ret

    @classmethod
    def handleGbt(cls, settings, data):
        # pylint: disable=broad-except
        index = data.data.position - 1
        data.gbtWindowSize = settings.gbtWindowSize
        bc = data.data.getUInt8()
        data.streaming = (bc & 0x40) != 0
        gbtWindowSize = int(bc & 0x3F)
        bn = data.data.getUInt16()
        bna = data.data.getUInt16()

        if not data.xml:
            # Remove existing data when first block is received.
            if bn == 1:
                index = 0
            elif bna != settings.blockIndex - 1:
                # If this block is already received.
                data.data.size = index
                data.command = Command.NONE
                return

        data.blockNumber = bn
        data.blockNumberAck = bna
        settings.blockNumberAck = data.blockNumber
        data.command = Command.NONE
        len_ = _GXCommon.getObjectCount(data.data)
        if len_ > data.data.size - data.data.position:
            data.complete = False
            return
        if data.xml:
            if (data.data.size - data.data.position) != len_:
                data.xml.appendComment(
                    "Data length is "
                    + str(len_)
                    + "and there are "
                    + str(data.data.size - data.data.position)
                    + " bytes."
                )
            data.xml.appendStartTag(Command.GENERAL_BLOCK_TRANSFER)
            if data.xml.comments:
                data.xml.appendComment("Last block: " + (bc & 0x80) != 0)
                data.xml.appendComment("Streaming: " + data.streaming)
                data.xml.appendComment("Window size: " + gbtWindowSize)
            data.xml.appendLine(
                TranslatorTags.BLOCK_CONTROL, None, data.xml.integerToHex(bc, 2)
            )
            data.xml.appendLine(
                TranslatorTags.BLOCK_NUMBER,
                None,
                data.xml.integerToHex(data.blockNumber, 4),
            )
            data.xml.appendLine(
                TranslatorTags.BLOCK_NUMBER_ACK,
                None,
                data.xml.integerToHex(data.blockNumberAck, 4),
            )
            if (bc & 0x80) != 0 and data.xml.comments:
                pos = data.data.position
                len2 = data.xml.getXmlLength()
                try:
                    reply = GXReplyData()
                    reply.data = data.data
                    reply.xml = data.xml
                    reply.xml.startComment("")
                    GXDLMS.getPdu(settings, reply)
                    reply.xml.endComment()
                except Exception:
                    data.xml.setXmlLength = len2
                data.data.position = pos
            data.xml.appendLine(
                TranslatorTags.BLOCK_DATA,
                None,
                data.data.toHex(False, data.data.position, len_),
            )
            data.xml.appendEndTag(Command.GENERAL_BLOCK_TRANSFER)
            return
        GXDLMS.getDataFromBlock(data.data, index)
        if (bc & 0x80) == 0:
            data.moreData = RequestTypes(data.moreData | RequestTypes.GBT)
        else:
            data.moreData = RequestTypes(data.moreData & ~RequestTypes.GBT)
            if data.data.size != 0:
                data.data.position = 0
                GXDLMS.getPdu(settings, data)
            if (
                data.data.position != data.data.size
                and (data.command in (Command.READ_RESPONSE, Command.GET_RESPONSE))
                and (data.moreData == RequestTypes.NONE or data.peek)
            ):
                data.data.position = 0
                GXDLMS.getValueFromData(settings, data)

    @classmethod
    def getPdu(cls, settings, data):
        cmd = data.command
        if data.command == Command.NONE:
            if data.data.size - data.data.position == 0:
                raise ValueError("Invalid PDU.")
            index = data.data.position
            cmd = data.data.getUInt8()
            data.command = cmd
            if cmd == Command.READ_RESPONSE:
                if not GXDLMS.handleReadResponse(settings, data, index):
                    return
            elif cmd == Command.GET_RESPONSE:
                if not GXDLMS.handleGetResponse(settings, data, index):
                    return
            elif cmd == Command.SET_RESPONSE:
                GXDLMS.handleSetResponse(data)
            elif cmd == Command.WRITE_RESPONSE:
                GXDLMS.handleWriteResponse(data)
            elif cmd == Command.METHOD_RESPONSE:
                GXDLMS.handleMethodResponse(settings, data, index)
            elif cmd == Command.ACCESS_RESPONSE:
                GXDLMS.handleAccessResponse(settings, data)
            elif cmd == Command.GENERAL_BLOCK_TRANSFER:
                if data.xml or (
                    not settings.isServer and (data.moreData & RequestTypes.FRAME) == 0
                ):
                    GXDLMS.handleGbt(settings, data)
            elif cmd in (Command.AARQ, Command.AARE):
                # This is parsed later.
                data.data.position = data.data.position - 1
            elif cmd == Command.RELEASE_RESPONSE:
                pass
            elif cmd == Command.CONFIRMED_SERVICE_ERROR:
                GXDLMS.handleConfirmedServiceError(data)
            elif cmd == Command.EXCEPTION_RESPONSE:
                GXDLMS.handleExceptionResponse(data)
            elif cmd in (
                Command.GET_REQUEST,
                Command.READ_REQUEST,
                Command.WRITE_REQUEST,
                Command.SET_REQUEST,
                Command.METHOD_REQUEST,
                Command.RELEASE_REQUEST,
            ):
                pass
            elif cmd in (
                Command.GLO_READ_REQUEST,
                Command.GLO_WRITE_REQUEST,
                Command.GLO_GET_REQUEST,
                Command.GLO_SET_REQUEST,
                Command.GLO_METHOD_REQUEST,
                Command.DED_GET_REQUEST,
                Command.DED_SET_REQUEST,
                Command.DED_METHOD_REQUEST,
            ):
                GXDLMS.handleGloDedRequest(settings, data)
            elif cmd in (
                Command.GLO_READ_RESPONSE,
                Command.GLO_WRITE_RESPONSE,
                Command.GLO_GET_RESPONSE,
                Command.GLO_SET_RESPONSE,
                Command.GLO_METHOD_RESPONSE,
                Command.GENERAL_GLO_CIPHERING,
                Command.GLO_EVENT_NOTIFICATION,
                Command.DED_GET_RESPONSE,
                Command.DED_SET_RESPONSE,
                Command.DED_METHOD_RESPONSE,
                Command.GENERAL_DED_CIPHERING,
                Command.DED_EVENT_NOTIFICATION,
                Command.GLO_CONFIRMED_SERVICE_ERROR,
                Command.DED_CONFIRMED_SERVICE_ERROR,
            ):
                GXDLMS.handleGloDedResponse(settings, data, index)
            elif cmd == Command.DATA_NOTIFICATION:
                GXDLMS.handleDataNotification(settings, data)
            elif cmd == Command.EVENT_NOTIFICATION:
                pass
            elif cmd == Command.INFORMATION_REPORT:
                pass
            elif cmd == Command.GENERAL_CIPHERING:
                GXDLMS.handleGeneralCiphering(settings, data)
            elif cmd == Command.GATEWAY_REQUEST:
                pass
            elif cmd == Command.GATEWAY_RESPONSE:
                data.data.getUInt8()
                pda = bytearray(_GXCommon.getObjectCount(data.data))
                data.data.get(pda)
                GXDLMS.getDataFromBlock(data.data, index)
                data.command = Command.NONE
                GXDLMS.getPdu(settings, data)
            else:
                raise ValueError("Invalid Command.")
        elif (data.moreData & RequestTypes.FRAME) == 0:
            if not data.peek and data.moreData == RequestTypes.NONE:
                if data.command in (Command.AARE, Command.AARQ):
                    data.data.position = 0
                else:
                    data.data.position = 1
            if cmd == Command.GENERAL_BLOCK_TRANSFER:
                data.data.position = data.cipherIndex + 1
                GXDLMS.handleGbt(settings, data)
                data.cipherIndex = data.data.size
                data.command = Command.NONE
            elif settings.isServer:
                if cmd in (
                    Command.GLO_READ_REQUEST,
                    Command.GLO_WRITE_REQUEST,
                    Command.GLO_GET_REQUEST,
                    Command.GLO_SET_REQUEST,
                    Command.GLO_METHOD_REQUEST,
                    Command.GLO_EVENT_NOTIFICATION,
                    Command.DED_GET_REQUEST,
                    Command.DED_SET_REQUEST,
                    Command.DED_METHOD_REQUEST,
                    Command.DED_EVENT_NOTIFICATION,
                ):
                    data.command = Command.NONE
                    data.data.position = data.getCipherIndex()
                    GXDLMS.getPdu(settings, data)
            else:
                # Client do not need a command any more.
                if data.isMoreData():
                    data.command = Command.NONE
                if cmd in (
                    Command.GLO_READ_RESPONSE,
                    Command.GLO_WRITE_RESPONSE,
                    Command.GLO_GET_RESPONSE,
                    Command.GLO_SET_RESPONSE,
                    Command.GLO_METHOD_RESPONSE,
                    Command.DED_GET_RESPONSE,
                    Command.DED_SET_RESPONSE,
                    Command.DED_METHOD_RESPONSE,
                    Command.GENERAL_GLO_CIPHERING,
                    Command.GENERAL_DED_CIPHERING,
                ):
                    data.command = Command.NONE
                    data.data.position = data.cipherIndex
                    GXDLMS.getPdu(settings, data)
                if cmd == Command.READ_RESPONSE and data.totalCount > 1:
                    if not GXDLMS.handleReadResponse(settings, data, 0):
                        return

        if (
            cmd == Command.READ_RESPONSE
            and data.commandType == SingleReadResponse.DATA_BLOCK_RESULT
            and (data.moreData & RequestTypes.FRAME) != 0
        ):
            return
        if (
            data.xml is None
            and data.data.position != data.data.size
            and cmd
            in (
                Command.READ_RESPONSE,
                Command.GET_RESPONSE,
                Command.METHOD_RESPONSE,
                Command.DATA_NOTIFICATION,
            )
            and (data.moreData == RequestTypes.NONE or data.peek)
        ):
            GXDLMS.getValueFromData(settings, data)

    @classmethod
    def handleConfirmedServiceError(cls, data):
        if data.xml:
            data.xml.appendStartTag(Command.CONFIRMED_SERVICE_ERROR)
            if data.xml.outputType == TranslatorOutputType.STANDARD_XML:
                data.data.getUInt8()
                data.xml.appendStartTag(TranslatorTags.INITIATE_ERROR)
                type_ = data.data.getUInt8()
                tag = TranslatorStandardTags.serviceErrorToString(type_)
                value = TranslatorStandardTags.getServiceErrorValue(
                    type_, data.data.getUInt8()
                )
                data.xml.appendLine("x:" + tag, None, value)
                data.xml.appendEndTag(TranslatorTags.INITIATE_ERROR)
            else:
                data.xml.appendLine(
                    TranslatorTags.SERVICE,
                    None,
                    data.xml.integerToHex(data.data.getUInt8(), 2),
                )
                type_ = data.data.getUInt8()
                data.xml.appendStartTag(TranslatorTags.SERVICE_ERROR)
                data.xml.appendLine(
                    TranslatorSimpleTags.serviceErrorToString(type_),
                    None,
                    TranslatorSimpleTags.getServiceErrorValue(
                        type_, data.data.getUInt8()
                    ),
                )
                data.xml.appendEndTag(TranslatorTags.SERVICE_ERROR)
            data.xml.appendEndTag(Command.CONFIRMED_SERVICE_ERROR)
        else:
            service = ConfirmedServiceError(data.data.getUInt8())
            type_ = data.data.getUInt8()
            raise GXDLMSConfirmedServiceError(service, type_, data.data.getUInt8())

    @classmethod
    def handleExceptionResponse(cls, data):
        state = data.data.getUInt8()
        error = ExceptionServiceError(data.data.getUInt8())
        value = None
        if (
            error == ExceptionServiceError.INVOCATION_COUNTER_ERROR
            and data.data.available() > 3
        ):
            value = data.data.getUInt32()
        if data.xml:
            data.xml.appendStartTag(Command.EXCEPTION_RESPONSE)
            if data.xml.outputType == TranslatorOutputType.STANDARD_XML:
                data.xml.appendLine(
                    TranslatorTags.STATE_ERROR,
                    None,
                    TranslatorStandardTags.stateErrorToString(state),
                )
                data.xml.appendLine(
                    TranslatorTags.SERVICE_ERROR,
                    None,
                    TranslatorStandardTags.exceptionServiceErrorToString(error),
                )
            else:
                data.xml.appendLine(
                    TranslatorTags.STATE_ERROR,
                    None,
                    TranslatorSimpleTags.stateErrorToString(state),
                )
                data.xml.appendLine(
                    TranslatorTags.SERVICE_ERROR,
                    None,
                    TranslatorSimpleTags.exceptionServiceErrorToString(error),
                )
            data.xml.appendEndTag(Command.EXCEPTION_RESPONSE)
        else:
            raise GXDLMSExceptionResponse(state, error, value)

    @classmethod
    def handleGloDedRequest(cls, settings, data):
        if settings.cipher is None:
            raise ValueError("Secure connection is not supported.")
        if (data.moreData & RequestTypes.FRAME) == 0:
            data.data.position = data.data.position - 1
            p = None
            if (
                settings.cipher.dedicatedKey
                and (settings.connected & ConnectionState.DLMS) != 0
            ):
                p = AesGcmParameter(
                    settings.sourceSystemTitle,
                    settings.cipher.dedicatedKey,
                    settings.cipher.authenticationKey,
                )
            else:
                p = AesGcmParameter(
                    settings.sourceSystemTitle,
                    settings.cipher.blockCipherKey,
                    settings.cipher.authenticationKey,
                )
            tmp = GXCiphering.decrypt(settings.cipher, p, data.data)
            if data.isComplete and (data.moreData & RequestTypes.FRAME) == 0:
                # pylint: disable=W0212
                settings._onPduEventHandler(data.moreData == 0, tmp)
            data.data.clear()
            data.data.set(tmp)
            data.command = Command(data.data.getUInt8())
            if data.command in (Command.DATA_NOTIFICATION, Command.INFORMATION_REPORT):
                data.command = Command.NONE
                data.data.position = data.data.position - 1
                GXDLMS.getPdu(cls, settings, data)
        else:
            data.data.position = data.data.position - 1

    @classmethod
    def handleGloDedResponse(cls, settings, data, index):
        if data.xml and not data.xml.comments:
            data.data.position = data.data.position - 1
        else:
            if settings.cipher is None:
                raise ValueError("Secure connection is not supported.")
            if (data.moreData & RequestTypes.FRAME) == 0:
                data.data.position = data.data.position - 1
                bb = GXByteBuffer(data.data)
                data.data.size = data.data.position = index
                p = None
                if (
                    settings.cipher.dedicatedKey
                    and (settings.connected & ConnectionState.DLMS) != 0
                ):
                    p = AesGcmParameter(
                        0,
                        settings.sourceSystemTitle,
                        settings.cipher.dedicatedKey,
                        settings.cipher.authenticationKey,
                    )
                else:
                    p = AesGcmParameter(
                        0,
                        settings.sourceSystemTitle,
                        settings.cipher.blockCipherKey,
                        settings.cipher.authenticationKey,
                    )
                data.data.set(GXCiphering.decrypt(settings.cipher, p, bb))
                # pylint: disable=W0212
                settings._onPduEventHandler(data.moreData == 0, data.data.array())
                data.cipheredCommand = data.command
                data.command = Command.NONE
                GXDLMS.getPdu(settings, data)
                data.cipherIndex = data.data.size

    @classmethod
    def handleGeneralCiphering(cls, settings, data):
        # pylint: disable=broad-except
        if settings.cipher is None:
            raise ValueError("Secure connection is not supported.")
        if (data.moreData & RequestTypes.FRAME) == 0:
            data.data.position = data.data.position - 1
            p = AesGcmParameter(
                0,
                settings.sourceSystemTitle,
                settings.cipher.blockCipherKey,
                settings.cipher.authenticationKey,
            )
            tmp = GXCiphering.decrypt(settings.cipher, p, data.data)
            # pylint: disable=W0212
            settings._onPduEventHandler(data.moreData == 0, tmp)
            data.data.clear()
            data.data.set(tmp)
            data.command = Command.NONE
            if p.security:
                try:
                    GXDLMS.getPdu(settings, data)
                except Exception as ex:
                    if data.xml is None:
                        raise ex
            if data.xml:
                data.xml.appendStartTag(Command.GENERAL_CIPHERING)
                data.xml.appendLine(
                    TranslatorTags.TRANSACTION_ID,
                    None,
                    data.xml.integerToHex(p.invocationCounter, 16, True),
                )
                data.xml.appendLine(
                    TranslatorTags.ORIGINATOR_SYSTEM_TITLE,
                    None,
                    GXByteBuffer.hex(p.systemTitle, False),
                )
                data.xml.appendLine(
                    TranslatorTags.RECIPIENT_SYSTEM_TITLE,
                    None,
                    GXByteBuffer.hex(p.recipientSystemTitle, False),
                )
                data.xml.appendLine(
                    TranslatorTags.DATE_TIME, None, GXByteBuffer.hex(p.dateTime, False)
                )
                data.xml.appendLine(
                    TranslatorTags.OTHER_INFORMATION,
                    None,
                    GXByteBuffer.hex(p.otherInformation, False),
                )
                data.xml.appendStartTag(TranslatorTags.KEY_INFO)
                data.xml.appendStartTag(TranslatorTags.AGREED_KEY)
                data.xml.appendLine(
                    TranslatorTags.KEY_PARAMETERS,
                    None,
                    data.xml.integerToHex(p.keyParameters, 2, True),
                )
                data.xml.appendLine(
                    TranslatorTags.KEY_CIPHERED_DATA,
                    None,
                    GXByteBuffer.hex(p.keyCipheredData, False),
                )
                data.xml.appendEndTag(TranslatorTags.AGREED_KEY)
                data.xml.appendEndTag(TranslatorTags.KEY_INFO)
                data.xml.appendLine(
                    TranslatorTags.CIPHERED_CONTENT,
                    None,
                    GXByteBuffer.hex(p.cipheredContent, False),
                )
                data.xml.appendEndTag(Command.GENERAL_CIPHERING)

    @classmethod
    def getValueFromData(cls, settings, reply):
        data = reply.data
        info = _GXDataInfo()
        if isinstance(reply.value, list):
            info.type_ = DataType.ARRAY
            info.count = reply.totalCount
            info.index = reply.getCount()
        index = data.position
        data.position = reply.readPosition
        try:
            value = _GXCommon.getData(settings, data, info)
            if value is not None:
                if not isinstance(value, list):
                    reply.valueType = info.type_
                    reply.value = value
                    reply.totalCount = 0
                    reply.readPosition = data.position
                else:
                    if value:
                        if reply.value is None:
                            reply.value = value
                        else:
                            list_ = []
                            list_ += reply.value
                            list_ += value
                            reply.value = list_
                    reply.readPosition = data.position
                    reply.totalCount = info.count
            elif info.complete and reply.command == Command.DATA_NOTIFICATION:
                reply.readPosition = data.position
        finally:
            data.position = index
        if (
            reply.command != Command.DATA_NOTIFICATION
            and info.complete
            and reply.moreData == RequestTypes.NONE
        ):
            if settings:
                settings.resetBlockIndex()
            data.position = 0

    @classmethod
    def getData(cls, settings, reply, data, notify):
        frame_ = 0
        isLast = True
        isNotify = False
        target = data
        index = reply.position
        if settings.interfaceType in (
            InterfaceType.HDLC,
            InterfaceType.HDLC_WITH_MODE_E,
        ):
            frame_ = GXDLMS.getHdlcData(
                settings.isServer, settings, reply, target, notify
            )
            isLast = (frame_ & 0x10) != 0
            if notify and frame_ in (0x13, 0x3):
                target = notify
                isNotify = True
            target.frameId = frame_
        elif settings.interfaceType == InterfaceType.WRAPPER:
            if not GXDLMS.__getTcpData(settings, reply, target, notify):
                target = notify
                isNotify = True
        elif settings.interfaceType == InterfaceType.WIRELESS_MBUS:
            GXDLMS.__getWirelessMBusData(settings, reply, target)
        elif settings.interfaceType == InterfaceType.PDU:
            target.packetLength = len(reply)
            target.complete = target.packetLength != 0
        elif settings.interfaceType == InterfaceType.PLC:
            GXDLMS.__getPlcData(settings, reply, data)
        elif settings.interfaceType == InterfaceType.PLC_HDLC:
            frame_ = GXDLMS.__getPlcHdlcData(settings, reply, data)
        elif settings.interfaceType == InterfaceType.WIRED_MBUS:
            GXDLMS.__getWiredMBusData(settings, reply, data)
        else:
            raise ValueError("Invalid Interface type.")
        if not target.complete:
            reply.position = index
            return False
        if settings.interfaceType != InterfaceType.PLC_HDLC:
            GXDLMS.getDataFromFrame(
                reply, target, GXDLMS.useHdlc(settings.interfaceType)
            )
        # If keepalive or get next frame request.
        if data.xml or (
            (frame_ not in (0x13, 0x3) or data.isMoreData()) and (frame_ & 0x1) != 0
        ):
            if frame_ == 0x3 and target.isMoreData():
                tmp = GXDLMS.getData(settings, reply, data, notify)
                target.data.position = 0
                return tmp
            return True

        if frame_ == 0x13 and not target.isMoreData():
            target.data.position = 0

        GXDLMS.getPdu(settings, target)
        if notify and not isNotify:
            # Check command to make sure it's not notify message.
            if data.command in (
                Command.DATA_NOTIFICATION,
                Command.GLO_EVENT_NOTIFICATION,
                Command.INFORMATION_REPORT,
                Command.EVENT_NOTIFICATION,
                Command.DED_INFORMATION_REPORT_REQUEST,
                Command.DED_EVENT_NOTIFICATION,
            ):
                isNotify = True
                notify.complete = data.complete
                notify.moreData = data.moreData
                notify.command = data.command
                data.command = Command.NONE
                notify.time = data.time
                data.time = None
                notify.data.set(data.data)
                data.data.trim()
                notify.value = data.value
                data.value = None
        if not isLast or (data.moreData == RequestTypes.GBT and reply.available() != 0):
            return GXDLMS.getData(settings, reply, data, notify)
        if isNotify:
            return False
        return True

    @classmethod
    def getDataFromFrame(cls, reply, info, hdlc):
        data = info.data
        offset = len(data)
        cnt = info.packetLength - reply.position
        if cnt != 0:
            data.capacity = offset + cnt
            data.set(reply, reply.position, cnt)
            if hdlc:
                reply.position = reply.position + 3
        data.position = offset

    @classmethod
    def getDataFromBlock(cls, data, index):
        # pylint: disable=protected-access
        if len(data) == data.position:
            data.clear()
            return 0
        len_ = data.position - index
        data._data[data.position - len_ : data.position] = data._data[
            data.position : len(data)
        ]
        data.position = data.position - len_
        data.size = len(data) - len_
        return len

    @classmethod
    def getActionInfo(cls, objectType, value, count):
        if objectType == ObjectType.IMAGE_TRANSFER:
            value[0] = 0x40
            count[0] = 4
        elif objectType == ObjectType.ACTIVITY_CALENDAR:
            value[0] = 0x50
            count[0] = 1
        elif objectType == ObjectType.ASSOCIATION_LOGICAL_NAME:
            value[0] = 0x60
            count[0] = 4
        elif objectType == ObjectType.ASSOCIATION_SHORT_NAME:
            value[0] = 0x20
            count[0] = 8
        elif objectType == ObjectType.CLOCK:
            value[0] = 0x60
            count[0] = 6
            value[0] = 0x48
            count[0] = 2
            value[0] = 0x38
            count[0] = 1
        elif objectType == ObjectType.IP4_SETUP:
            value[0] = 0x60
            count[0] = 3
        elif objectType == ObjectType.MBUS_SLAVE_PORT_SETUP:
            value[0] = 0x60
            count[0] = 8
        elif objectType == ObjectType.PROFILE_GENERIC:
            value[0] = 0x58
            count[0] = 4
            value[0] = 0x28
            count[0] = 1
            value[0] = 0x30
            count[0] = 3
            value[0] = 0x28
            count[0] = 2
        elif objectType == ObjectType.SAP_ASSIGNMENT:
            pass
        elif objectType == ObjectType.SCRIPT_TABLE:
            value[0] = 0x20
            count[0] = 1
        elif objectType == ObjectType.SPECIAL_DAYS_TABLE:
            value[0] = 0x10
            count[0] = 2
        elif objectType == ObjectType.SECURITY_SETUP:
            value[0] = 0x30
            count[0] = 8
        elif objectType == ObjectType.DISCONNECT_CONTROL:
            value[0] = 0x20
            count[0] = 2
        elif objectType == ObjectType.PUSH_SETUP:
            value[0] = 0x38
            count[0] = 1
        else:
            count[0] = 0
            value[0] = 0

    @classmethod
    def parseSnrmUaResponse(cls, data, settings):
        if data.available() != 0:
            data.getUInt8()
            data.getUInt8()
            data.getUInt8()
            while data.position < len(data):
                id_ = data.getUInt8()
                len2 = data.getUInt8()
                if len2 == 1:
                    val = data.getUInt8()
                elif len2 == 2:
                    val = data.getUInt16()
                elif len2 == 4:
                    val = data.getUInt32()
                else:
                    raise Exception("Invalid Exception.")
                if id_ == _HDLCInfo.MAX_INFO_RX:
                    settings.maxInfoTX = val
                elif id_ == _HDLCInfo.MAX_INFO_TX:
                    settings.maxInfoRX = val
                elif id_ == _HDLCInfo.WINDOW_SIZE_RX:
                    settings.windowSizeTX = val
                elif id_ == _HDLCInfo.WINDOW_SIZE_TX:
                    settings.windowSizeRX = val
                else:
                    raise Exception("Invalid UA response.")

    @classmethod
    def appendHdlcParameter(cls, data, value):
        if value < 0x100:
            data.setUInt8(1)
            data.setUInt8(value)
        else:
            data.setUInt8(2)
            data.setUInt16(value)

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
import xml.etree.cElementTree as ET
from .internal._GXCommon import _GXCommon
from .GXByteBuffer import GXByteBuffer
from .ActionRequestType import ActionRequestType
from .enums.TranslatorOutputType import TranslatorOutputType
from .TranslatorSimpleTags import TranslatorSimpleTags
from .TranslatorStandardTags import TranslatorStandardTags
from .GXDLMSTranslatorStructure import GXDLMSTranslatorStructure
from .GXDLMSSettings import GXDLMSSettings
from .enums import Command, Security
from .GXCiphering import GXCiphering
from .GXReplyData import GXReplyData
from .GXDLMSLNCommandHandler import GXDLMSLNCommandHandler
from .GXDLMSSNCommandHandler import GXDLMSSNCommandHandler
from ._GXAPDU import _GXAPDU
from .GXDLMS import GXDLMS
from .TranslatorTags import TranslatorTags
from .internal._GXDataInfo import _GXDataInfo
from .GXDLMSXmlSettings import GXDLMSXmlSettings
from .enums.InterfaceType import InterfaceType
from .enums.DataType import DataType
from .GXDLMSLNParameters import GXDLMSLNParameters
from .enums.HdlcFrameType import HdlcFrameType
from .GXDLMSSNParameters import GXDLMSSNParameters
from .enums.BerType import BerType
from .enums.RequestTypes import RequestTypes
from .GXDLMSConverter import GXDLMSConverter
from ._HDLCInfo import _HDLCInfo
from .TranslatorGeneralTags import TranslatorGeneralTags
from .SingleReadResponse import SingleReadResponse
from .VariableAccessSpecification import VariableAccessSpecification
from .enums.AccessServiceCommandType import AccessServiceCommandType
from .enums.Service import Service
from .ServiceError import ServiceError
from .enums.Priority import Priority
from .enums.ServiceClass import ServiceClass
from .GXDateTime import GXDateTime
from .SetResponseType import SetResponseType
from .GetCommandType import GetCommandType
from .SetRequestType import SetRequestType
from .enums.ErrorCode import ErrorCode
from .ActionResponseType import ActionResponseType
from .enums.Authentication import Authentication
from .enums.AssociationResult import AssociationResult
from .enums.SourceDiagnostic import SourceDiagnostic
from .AesGcmParameter import AesGcmParameter
from .GXDLMSException import GXDLMSException
from .enums.Standard import Standard
from .GXDLMSTranslatorMessage import GXDLMSTranslatorMessage
from .plc.enums import PlcSourceAddress, PlcDestinationAddress


# pylint:disable=bad-option-value,too-many-instance-attributes,too-many-function-args,too-many-public-methods,too-many-public-methods,too-many-function-args,too-many-instance-attributes,old-style-class,raise-missing-from
class GXDLMSTranslator:
    """
    This class is used to translate DLMS frame or PDU to xml.
    """

    def __init__(self, type_=TranslatorOutputType.SIMPLE_XML):
        """
        Constructor.
        type_: Translator output type.
        """
        self.tags = dict()
        self.tagsByName = dict()
        # Are numeric values shows as hex.
        self.hex = True
        # Is string serialized as hex.  {@link messageToXml} {@link PduOnly}
        self.showStringAsHex = False
        # Sending data in multiple frames.
        self.multipleFrames = False
        # If only PDUs are shown and PDU is received on parts.
        self.pduFrames = GXByteBuffer()
        # Is only PDU shown when data is parsed with messageToXml.
        # {@link messageToXml} {@link CompleatePdu}
        self.pduOnly = False
        self.outputType = None
        # Is XML declaration skipped.
        self.omitXmlDeclaration = False
        # Is XML name space skipped.
        self.omitXmlNameSpace = False
        # Add comments.
        self.comments = False
        # Used security.
        self.security = Security.NONE
        # System title.
        self.systemTitle = "ABCDEFGH".encode()
        # Block cipher key.
        self.blockCipherKey = bytearray(
            (
                0x00,
                0x01,
                0x02,
                0x03,
                0x04,
                0x05,
                0x06,
                0x07,
                0x08,
                0x09,
                0x0A,
                0x0B,
                0x0C,
                0x0D,
                0x0E,
                0x0F,
            )
        )
        # Authentication key.
        self.authenticationKey = bytearray(
            (
                0xD0,
                0xD1,
                0xD2,
                0xD3,
                0xD4,
                0xD5,
                0xD6,
                0xD7,
                0xD8,
                0xD9,
                0xDA,
                0xDB,
                0xDC,
                0xDD,
                0xDE,
                0xDF,
            )
        )
        # Invocation Counter.
        self.invocationCounter = 0
        # Dedicated key.
        self.dedicatedKey = None
        # Server system title.
        self.serverSystemTitle = None
        self.outputType = type_
        # Is only complete PDU parsed and shown.
        self.completePdu = False
        self.__getTags(self.outputType, self.tags, self.tagsByName)
        self.standard = Standard.DLMS

    #
    # Find next frame from the string.  Position of data is set to the begin of
    # new frame.  If PDU is None it is not updated.
    #
    # @param data
    #            Data where frame is search.
    # @param pdu
    #            PDU of received frame is set here.
    # Is new frame found.
    def findNextFrame(self, msg, pdu):
        if not isinstance(msg, (GXDLMSTranslatorMessage)):
            if not isinstance(msg, (GXByteBuffer)):
                data = GXByteBuffer(msg)
            else:
                data = msg
            msg = GXDLMSTranslatorMessage()
            msg.message = data
        msg.sourceAddress = msg.targetAddress = 0
        original = msg.message.position
        msg.exception = None
        data = msg.message
        settings = GXDLMSSettings(True, None)
        reply = GXReplyData()
        reply.moreData = msg.moreData
        reply.xml = GXDLMSTranslatorStructure(
            self.outputType,
            self.omitXmlNameSpace,
            self.hex,
            self.showStringAsHex,
            self.comments,
            self.tags,
        )
        pos = 0
        found = False
        while data.position < len(data):
            if (
                msg.interfaceType
                in (None, InterfaceType.HDLC, InterfaceType.HDLC_WITH_MODE_E)
                and data.getUInt8(data.position) == 0x7E
            ):
                pos = data.position
                settings.interfaceType = InterfaceType.HDLC
                found = GXDLMS.getData(settings, data, reply, None)
                data.position = pos
                if found:
                    break
            elif (
                msg.interfaceType in (None, InterfaceType.WRAPPER)
                and data.getUInt16(data.position) == 0x1
            ):
                pos = data.position
                settings.interfaceType = InterfaceType.WRAPPER
                found = GXDLMS.getData(settings, data, reply, None)
                data.position = pos
                if found:
                    break
            elif (
                msg.interfaceType in (None, InterfaceType.PLC)
                and msg.message.getUInt8(msg.message.position) == 2
            ):
                pos = data.position
                settings.interfaceType = InterfaceType.PLC
                found = GXDLMS.getData(settings, data, reply, None)
                data.position = pos
                if found:
                    break
            elif msg.interfaceType in (
                None,
                InterfaceType.WIRED_MBUS,
            ) and GXDLMS.isWiredMBusData(msg.message):
                pos = data.position
                settings.interfaceType = InterfaceType.WIRED_MBUS
                found = GXDLMS.getData(settings, data, reply, None)
                data.position = pos
                if found:
                    break
            elif msg.interfaceType in (
                None,
                InterfaceType.WIRELESS_MBUS,
            ) and GXDLMS.isWirelessMBusData(msg.message):
                pos = data.position
                settings.interfaceType = InterfaceType.WIRELESS_MBUS
                found = GXDLMS.getData(settings, data, reply, None)
                data.position = pos
                if found:
                    break
            data.position = data.position + 1
        msg.moreData = reply.moreData
        msg.sourceAddress = reply.sourceAddress
        msg.targetAddress = reply.targetAddress
        if pdu:
            pdu.clear()
            pdu.set(data.data, 0, len(data))
        r = data.position != len(data)
        if not found:
            data.position = original
        return r

    #
    # Find next frame from the string.  Position of data is set to the begin of
    # new frame.  If PDU is None it is not updated.
    #
    # @param data
    #            Data where frame is search.
    # @param pdu
    #            PDU of received frame is set here.
    # @param type
    #            Interface type.
    # Is new frame found.
    #
    def findNextFrame_0(self, data, pdu, type_):
        settings = GXDLMSSettings(True, None)
        settings.iInterfaceType = type_
        reply = GXReplyData()
        reply.xml = GXDLMSTranslatorStructure(
            self.outputType,
            self.omitXmlNameSpace,
            self.hex,
            self.showStringAsHex,
            self.comments,
            self.tags,
        )
        pos = int()
        found = bool()
        try:
            while data.position < len(data):
                if (
                    type_ in (InterfaceType.HDLC, InterfaceType.HDLC_WITH_MODE_E)
                    and data.getUInt8(data.position) == 0x7E
                ):
                    pos = data.position
                    found = GXDLMS.getData(settings, data, reply, None)
                    data.position = pos
                    if found:
                        break
                elif (
                    data.available() > 1
                    and type_ == InterfaceType.WRAPPER
                    and data.getUInt16(data.position) == 0x1
                ):
                    pos = data.position
                    found = GXDLMS.getData(settings, data, reply, None)
                    data.position = pos
                    if found:
                        break
                elif type_ == InterfaceType.WIRELESS_MBUS:
                    pos = data.position
                    settings.interfaceType = InterfaceType.WIRELESS_MBUS
                    found = GXDLMS.getData(settings, data, reply, None)
                    data.position = pos
                    if found:
                        break
                data.position = data.position + 1
        except Exception:
            raise ValueError("Invalid DLMS frame.")
        if pdu:
            pdu.clear()
            pdu.set(data, 0, data.size)
        return data.position != len(data)

    #
    # Get all tags.
    #
    # @param type
    #            Output type.
    # @param list
    #            List of tags by ID.
    # @param tagsByName
    #            List of tags by name.
    #
    @classmethod
    def __getTags(cls, type_, list_, tagsByName):
        if type_ == TranslatorOutputType.SIMPLE_XML:
            TranslatorSimpleTags.getGeneralTags(list_)
            TranslatorSimpleTags.getSnTags(list_)
            TranslatorSimpleTags.getLnTags(list_)
            TranslatorSimpleTags.getGloTags(list_)
            TranslatorSimpleTags.getDedTags(list_)
            TranslatorSimpleTags.getTranslatorTags(list_)
            TranslatorSimpleTags.getDataTypeTags(list_)
        else:
            TranslatorStandardTags.getGeneralTags(list_)
            TranslatorStandardTags.getSnTags(list_)
            TranslatorStandardTags.getLnTags(list_)
            TranslatorStandardTags.getGloTags(list_)
            TranslatorStandardTags.getDedTags(list_)
            TranslatorStandardTags.getTranslatorTags(list_)
            TranslatorStandardTags.getDataTypeTags(list_)
        #  Simple is not case sensitive.
        lowercase = type_ == TranslatorOutputType.SIMPLE_XML
        for it in list_:
            str_ = list_[it]
            if lowercase:
                str_ = str_.lower()
            if str_ not in tagsByName:
                tagsByName[str_] = it

    def getPdu(self, value):
        return self.getPdu(GXByteBuffer(value))

    #
    # Identify used DLMS framing type.
    #
    # @param value
    #            Input data.
    # Interface type.
    #
    @classmethod
    def getDlmsFraming(cls, value):
        pos = value.position
        while pos != len(value):
            if value.getUInt8(pos) == 0x7E:
                return InterfaceType.HDLC
            if value.available() > 1 and value.getUInt16(pos) == 1:
                return InterfaceType.WRAPPER
            if GXDLMS.isWirelessMBusData(value):
                return InterfaceType.WIRELESS_MBUS
            pos += 1
        raise ValueError("Invalid DLMS framing.")

    def getPdu_0(self, value):
        framing = self.getDlmsFraming(value)
        data = GXReplyData()
        data.xml = GXDLMSTranslatorStructure(
            self.outputType,
            self.omitXmlNameSpace,
            self.hex,
            self.showStringAsHex,
            self.comments,
            self.tags,
        )
        settings = GXDLMSSettings(True, None)
        settings.interfaceType = framing
        GXDLMS.getData(settings, value, data, None)
        return data.data

    def getCiphering(self, settings, force):
        if force or self.security != Security.NONE:
            c = GXCiphering(self.systemTitle)
            c.security = self.security
            c.systemTitle = self.systemTitle
            c.blockCipherKey = self.blockCipherKey
            c.authenticationKey = self.authenticationKey
            c.invocationCounter = self.invocationCounter
            c.dedicatedKey = self.dedicatedKey
            settings.sourceSystemTitle = self.serverSystemTitle
            settings.cipher = c
        else:
            settings.cipher = None

    #
    # Clear {@link messageToXml} internal settings.
    #
    def clear(self):
        self.multipleFrames = False
        self.pduFrames.clear()

    @classmethod
    def checkFrame(cls, frame_, xml):
        if frame_ == 0x93:
            xml.appendComment("SNRM frame.")
        elif frame_ == 0x73:
            xml.appendComment("UA frame.")
        elif (frame_ & HdlcFrameType.S_FRAME) == HdlcFrameType.S_FRAME:
            #  If S -frame.
            xml.appendComment("S frame.")
        elif (frame_ & 1) == HdlcFrameType.U_FRAME:
            #  Handle U-frame.
            xml.appendComment("U frame.")
        else:
            #  I-frame.
            if frame_ == 0x10:
                xml.appendComment("AARQ frame.")
            elif frame_ == 0x30:
                xml.appendComment("AARE frame.")
            else:
                xml.appendComment("I frame.")

    #
    # Get logical and physical address from the server address.
    #
    @classmethod
    def __getLogicalAndPhysicalAddress(cls, value):
        if value > 0x3FFF:
            logical = int(value >> 14)
            physical = int(value & 0x3FFF)
        else:
            logical = int(value >> 7)
            physical = int(value & 0x7F)
        return (logical, physical)

    @classmethod
    def __updateAddress(cls, settings, msg):
        reply = True
        if msg.command in (
            Command.READ_REQUEST,
            Command.WRITE_REQUEST,
            Command.GET_REQUEST,
            Command.SET_REQUEST,
            Command.METHOD_REQUEST,
            Command.SNRM,
            Command.AARQ,
            Command.DISCONNECT_REQUEST,
            Command.RELEASE_REQUEST,
            Command.ACCESS_REQUEST,
            Command.GLO_GET_REQUEST,
            Command.GLO_SET_REQUEST,
            Command.GLO_METHOD_REQUEST,
            Command.GLO_INITIATE_REQUEST,
            Command.GLO_READ_REQUEST,
            Command.GLO_WRITE_REQUEST,
            Command.DED_INITIATE_REQUEST,
            Command.DED_READ_REQUEST,
            Command.DED_WRITE_REQUEST,
            Command.DED_GET_REQUEST,
            Command.DED_SET_REQUEST,
            Command.DED_METHOD_REQUEST,
            Command.GATEWAY_REQUEST,
            Command.DISCOVER_REQUEST,
            Command.REGISTER_REQUEST,
            Command.PING_REQUEST,
        ):
            reply = False
        if reply:
            msg.targetAddress = settings.clientAddress
            msg.sourceAddress = settings.serverAddress
        else:
            msg.sourceAddress = settings.clientAddress
            msg.targetAddress = settings.serverAddress

    #
    #
    #
    # pylint:disable=broad-except
    def messageToXml(self, msg):
        """
        Convert message to XML.
        msg : Translator message data.
        Returns Converted xml.
        """
        # pylint: disable=too-many-nested-blocks
        if not isinstance(msg, (GXDLMSTranslatorMessage)):
            if not isinstance(msg, GXByteBuffer):
                data = GXByteBuffer(msg)
            else:
                data = msg
            msg = GXDLMSTranslatorMessage()
            msg.message = data
            if not msg:
                raise ValueError("msg")
        msg.exception = None
        xml = GXDLMSTranslatorStructure(
            self.outputType,
            self.omitXmlNameSpace,
            self.hex,
            self.showStringAsHex,
            self.comments,
            self.tags,
        )
        data = GXReplyData()
        settings = GXDLMSSettings(True, None)
        self.getCiphering(settings, True)
        data.xml = xml
        try:
            offset = msg.message.position
            #  If HDLC framing.
            if (
                msg.interfaceType
                in (None, InterfaceType.HDLC, InterfaceType.HDLC_WITH_MODE_E)
                and msg.message.getUInt8(msg.message.position) == 0x7E
            ):
                msg.interfaceType = settings.interfaceType = InterfaceType.HDLC
                if GXDLMS.getData(settings, msg.message, data, None):
                    msg.moreData = data.moreData
                    msg.sourceAddress = data.sourceAddress
                    msg.targetAddress = data.targetAddress
                    if not self.pduOnly:
                        xml.appendLine(
                            '<HDLC len="'
                            + xml.integerToHex(data.packetLength - offset, 0)
                            + '" >'
                        )
                        (
                            logical,
                            physical,
                        ) = GXDLMSTranslator.__getLogicalAndPhysicalAddress(
                            settings.serverAddress
                        )
                        if logical != 0:
                            xml.appendComment(
                                "Logical address:"
                                + str(logical)
                                + ", Physical address:"
                                + str(physical)
                            )
                        xml.appendLine(
                            '<TargetAddress Value="'
                            + xml.integerToHex(settings.serverAddress, 0)
                            + '" />'
                        )
                        xml.appendLine(
                            '<SourceAddress Value="'
                            + xml.integerToHex(settings.clientAddress, 0)
                            + '" />'
                        )
                        #  Check frame.
                        if self.comments:
                            self.checkFrame(data.frameId, xml)
                        xml.appendLine(
                            '<FrameType Value="'
                            + xml.integerToHex(data.frameId, 2, True)
                            + '" />'
                        )
                    if not data.data:
                        if (data.frameId & 1) != 0 and data.command == Command.NONE:
                            if not self.completePdu:
                                xml.appendLine('<Command Value="NextFrame" />')
                            self.multipleFrames = True
                        else:
                            xml.appendStartTag(data.command)
                            xml.appendEndTag(data.command)
                    else:
                        if self.multipleFrames or data.isMoreData():
                            if self.completePdu:
                                self.pduFrames.set(data.data)
                                if data.moreData == RequestTypes.NONE:
                                    xml.appendLine(
                                        self.__pduToXml(self.pduFrames, True, True)
                                    )
                                    self.pduFrames.clear()
                            else:
                                xml.appendLine(
                                    '<NextFrame Value="'
                                    + data.data.toHex(
                                        False,
                                        data.data.position,
                                        data.data.size - data.data.position,
                                    )
                                    + '" />'
                                )
                            if data.moreData != RequestTypes.DATABLOCK:
                                self.multipleFrames = False
                        else:
                            if not self.pduOnly:
                                xml.appendLine("<PDU>")
                            if self.pduFrames:
                                self.pduFrames.set(data.data.data)
                                xml.appendLine(
                                    self.__pduToXml(self.pduFrames, True, True)
                                )
                                self.pduFrames.clear()
                            else:
                                if data.command in (Command.SNRM, Command.UA):
                                    xml.appendStartTag(data.command)
                                    self._pduToXml2(xml, data.data, True, True, True)
                                    xml.appendEndTag(data.command)
                                    xml.setXmlLength(xml.getXmlLength() + 2)
                                else:
                                    xml.appendLine(self.__pduToXml(data.data, True, True))
                            #  Remove \r\n.
                            xml.trim()
                            if not self.pduOnly:
                                xml.appendLine("</PDU>")
                    if not self.pduOnly:
                        xml.appendLine("</HDLC>")
                self.__updateAddress(settings, msg)
                msg.xml = str(xml)
                return msg.xml
            #  If wrapper.
            if (
                msg.interfaceType in (None, InterfaceType.WRAPPER)
                and (msg.message.available() > 1)
                and msg.message.getUInt16(msg.message.position) == 1
            ):
                msg.interfaceType = settings.interfaceType = InterfaceType.WRAPPER
                GXDLMS.getData(settings, msg.message, data, None)
                msg.moreData = data.moreData
                msg.sourceAddress = data.sourceAddress
                msg.targetAddress = data.targetAddress
                pdu = self.__pduToXml(
                    data.data, self.omitXmlDeclaration, self.omitXmlNameSpace
                )
                if not self.pduOnly:
                    xml.appendLine(
                        '<WRAPPER len="'
                        + xml.integerToHex(data.packetLength - offset, 0)
                        + '" >'
                    )
                    xml.appendLine(
                        '<TargetAddress Value="'
                        + xml.integerToHex(settings.clientAddress, 0)
                        + '" />'
                    )
                    xml.appendLine(
                        '<SourceAddress Value="'
                        + xml.integerToHex(settings.serverAddress, 0)
                        + '" />'
                    )
                if not self.pduOnly:
                    xml.appendLine("<PDU>")
                xml.appendLine(pdu)
                #  Remove \r\n.
                xml.trim()
                if not self.pduOnly:
                    xml.appendLine("</PDU>")
                if not self.pduOnly:
                    xml.appendLine("</WRAPPER>")
                self.__updateAddress(settings, msg)
                msg.xml = str(xml)
                return msg.xml
            # If PLC.
            if (
                msg.interfaceType in (None, InterfaceType.PLC)
                and msg.message.getUInt8(msg.message.position) == 2
            ):
                msg.interfaceType = settings.interfaceType = InterfaceType.PLC
                GXDLMS.getData(settings, msg.message, data, None)
                msg.moreData = data.moreData
                msg.sourceAddress = data.sourceAddress
                msg.targetAddress = data.targetAddress
                if not self.pduOnly:
                    xml.appendLine(
                        '<Plc len="'
                        + xml.integerToHex(data.packetLength - offset, 0)
                        + '" >'
                    )
                    if self.comments:
                        if data.targetAddress == PlcSourceAddress.INITIATOR:
                            xml.appendComment("Initiator")
                        elif data.targetAddress == PlcSourceAddress.NEW:
                            xml.appendComment("New")
                    xml.appendLine(
                        '<SourceAddress Value="'
                        + xml.integerToHex(data.targetAddress, 0)
                        + '" />'
                    )
                    if (
                        self.comments
                        and data.sourceAddress == PlcDestinationAddress.ALL_PHYSICAL
                    ):
                        xml.appendComment("AllPhysical")
                    xml.appendLine(
                        '<DestinationAddress Value="'
                        + xml.integerToHex(data.sourceAddress, 0)
                        + '" />'
                    )
                if data.data.size == 0:
                    xml.appendLine(
                        '<Command Value="' + Command.toString(data.command) + '" />'
                    )
                else:
                    if not self.pduOnly:
                        xml.appendLine("<PDU>")
                    xml.appendLine(
                        self.__pduToXml(
                            data.data,
                            self.omitXmlDeclaration,
                            self.omitXmlNameSpace,
                            msg,
                        )
                    )
                    # Remove \r\n.
                    xml.trim()
                    if not self.pduOnly:
                        xml.appendLine("</PDU>")
                if not self.pduOnly:
                    xml.appendLine("</Plc>")
                self.__updateAddress(settings, msg)
                msg.xml = str(xml)
                return msg.xml
            # If Wired M-Bus.
            if msg.interfaceType in (
                None,
                InterfaceType.WIRED_MBUS,
            ) and GXDLMS.isWiredMBusData(msg.message):
                msg.interfaceType = settings.interfaceType = InterfaceType.WIRED_MBUS
                len_ = xml.getXmlLength()
                GXDLMS.getData(settings, msg.message, data, None)
                msg.moreData = data.moreData
                msg.sourceAddress = data.sourceAddress
                msg.targetAddress = data.targetAddress
                tmp = str(xml)[0:len_]
                xml.setXmlLength(len_)
                if not self.pduOnly:
                    xml.appendLine(
                        '<WiredMBus len="'
                        + xml.integerToHex(data.packetLength - offset, 0)
                        + '" >'
                    )
                    xml.appendLine(
                        '<TargetAddress Value="'
                        + xml.integerToHex(settings.serverAddress, 0)
                        + '" />'
                    )
                    xml.appendLine(
                        '<SourceAddress Value="'
                        + xml.integerToHex(settings.clientAddress, 0)
                        + '" />'
                    )
                    xml.append(tmp)
                if data.data.size == 0:
                    xml.appendLine(
                        '<Command Value="' + Command.toString(data.command) + '" />'
                    )
                else:
                    if self.multipleFrames or (data.moreData & RequestTypes.FRAME) != 0:
                        if self.completePdu:
                            self.pduFrames.set(data.data)
                            if data.moreData == RequestTypes.NONE:
                                xml.appendLine(
                                    self.__pduToXml(self.pduFrames, True, True)
                                )
                                self.pduFrames.clear()
                        else:
                            xml.appendLine(
                                '<NextFrame Value="'
                                + data.data.toHex(
                                    False, data.data.position, data.data.available()
                                )
                                + '" />'
                            )
                        if data.moreData & RequestTypes.FRAME != 0:
                            self.multipleFrames = True
                        if data.moreData == RequestTypes.DATABLOCK:
                            self.multipleFrames = False
                    else:
                        if not self.pduOnly:
                            xml.appendLine("<PDU>")
                        if self.pduFrames.size != 0:
                            self.pduFrames.set(data.data)
                            data.data.clear()
                            data.data.set(self.pduFrames)
                        xml.appendLine(
                            self.__pduToXml(
                                data.data,
                                self.omitXmlDeclaration,
                                self.omitXmlNameSpace,
                            )
                        )
                        # Remove \r\n.
                        xml.trim()
                        if not self.pduOnly:
                            xml.appendLine("</PDU>")
                if not self.pduOnly:
                    xml.appendLine("</WiredMBus>")
                self.__updateAddress(settings, msg)
                msg.xml = str(xml)
                return msg.xml
            # If Wireless M-Bus.
            if msg.interfaceType in (
                None,
                InterfaceType.WIRELESS_MBUS,
            ) and GXDLMS.isWirelessMBusData(msg.message):
                msg.interfaceType = settings.interfaceType = InterfaceType.WIRELESS_MBUS
                len_ = xml.getXmlLength()
                GXDLMS.getData(settings, msg.message, data, None)
                msg.moreData = data.moreData
                msg.sourceAddress = data.sourceAddress
                msg.targetAddress = data.targetAddress
                tmp = str(xml)[0:len_]
                xml.setXmlLength(len_)
                if not self.pduOnly:
                    xml.appendLine(
                        '<WirelessMBus len="'
                        + xml.integerToHex(data.packetLength - offset, 0)
                        + '" >'
                    )
                    xml.appendLine(
                        '<TargetAddress Value="'
                        + xml.integerToHex(settings.serverAddress, 0)
                        + '" />'
                    )
                    xml.appendLine(
                        '<SourceAddress Value="'
                        + xml.integerToHex(settings.clientAddress, 0)
                        + '" />'
                    )
                    xml.append(tmp)
                if data.data.size == 0:
                    xml.appendLine(
                        '<Command Value="' + Command.toString(data.command) + '" />'
                    )
                else:
                    if not self.pduOnly:
                        xml.appendLine("<PDU>")
                    xml.appendLine(
                        self.__pduToXml(
                            data.data,
                            self.omitXmlDeclaration,
                            self.omitXmlNameSpace,
                            msg,
                        )
                    )
                    # Remove \r\n.
                    xml.trim()
                    if not self.pduOnly:
                        xml.appendLine("</PDU>")
                if not self.pduOnly:
                    xml.appendLine("</WirelessMBus>")
                self.__updateAddress(settings, msg)
                msg.xml = str(xml)
                return msg.xml
        except Exception as ex:
            print(ex)
        raise ValueError("Invalid DLMS framing.")

    #
    # Convert PDU in hex string to XML.
    #
    # @param pdu
    #            Converted hex string or GXByteBuffer.
    # Converted XML.
    #
    def pduToXml(self, pdu):
        if not isinstance(pdu, GXByteBuffer):
            pdu = GXByteBuffer(pdu)
        return self.__pduToXml(pdu, self.omitXmlDeclaration, self.omitXmlNameSpace)

    @classmethod
    def getUa(cls, data, xml):
        data.getUInt8()
        #  Skip FromatID
        data.getUInt8()
        #  Skip Group ID.
        data.getUInt8()
        #  Skip Group length.
        val = None
        while data.position < len(data):
            id_ = data.getUInt8()
            len_ = data.getUInt8()
            if len_ == 1:
                val = data.getUInt8()
            elif len_ == 2:
                val = data.getUInt16()
            elif len_ == 4:
                val = data.getUInt32()
            else:
                raise GXDLMSException("Invalid Exception.")
            if id_ == _HDLCInfo.MAX_INFO_TX:
                xml.appendLine('<MaxInfoTX Value="' + str(val) + '" />')
            elif id_ == _HDLCInfo.MAX_INFO_RX:
                xml.appendLine('<MaxInfoRX Value="' + str(val) + '" />')
            elif id_ == _HDLCInfo.WINDOW_SIZE_TX:
                xml.appendLine('<WindowSizeTX Value="' + str(val) + '" />')
            elif id_ == _HDLCInfo.WINDOW_SIZE_RX:
                xml.appendLine('<WindowSizeRX Value="' + str(val) + '" />')
            else:
                raise GXDLMSException("Invalid UA response.")

    #
    # Convert bytes to XML.
    #
    # @param value
    #            Bytes to convert.
    # Converted XML.
    #
    def __pduToXml(self, value, omitDeclaration, omitNameSpace):
        xml = GXDLMSTranslatorStructure(
            self.outputType,
            self.omitXmlNameSpace,
            self.hex,
            self.showStringAsHex,
            self.comments,
            self.tags,
        )
        return self._pduToXml2(xml, value, omitDeclaration, omitNameSpace, True)

    @classmethod
    def isCiphered(cls, cmd):
        return cmd in (
            Command.GLO_READ_REQUEST,
            Command.GLO_WRITE_REQUEST,
            Command.GLO_GET_REQUEST,
            Command.GLO_SET_REQUEST,
            Command.GLO_READ_RESPONSE,
            Command.GLO_WRITE_RESPONSE,
            Command.GLO_GET_RESPONSE,
            Command.GLO_SET_RESPONSE,
            Command.GLO_METHOD_REQUEST,
            Command.GLO_METHOD_RESPONSE,
            Command.DED_GET_REQUEST,
            Command.DED_SET_REQUEST,
            Command.DED_READ_RESPONSE,
            Command.DED_GET_RESPONSE,
            Command.DED_SET_RESPONSE,
            Command.DED_METHOD_REQUEST,
            Command.DED_METHOD_RESPONSE,
            Command.GENERAL_GLO_CIPHERING,
            Command.GENERAL_DED_CIPHERING,
            Command.AARQ,
            Command.AARE,
            Command.GLO_CONFIRMED_SERVICE_ERROR,
            Command.DED_CONFIRMED_SERVICE_ERROR,
            Command.GENERAL_CIPHERING,
            Command.RELEASE_REQUEST,
        )

    #
    # Convert bytes to XML.
    #
    # @param value
    #            Bytes to convert.
    # Converted XML.
    #
    def _pduToXml2(
        self, xml, value, omitDeclaration, omitNameSpace, allowUnknownCommand=True
    ):
        # pylint: disable=bad-option-value,too-many-arguments,too-many-locals,
        # too-many-nested-blocks,redefined-variable-type
        if not value:
            raise ValueError("value")
        settings = GXDLMSSettings(True, None)
        settings.standard = self.standard
        cmd = value.getUInt8()
        self.getCiphering(settings, self.isCiphered(cmd))
        data = GXReplyData()
        str_ = None
        if cmd == Command.AARQ:
            value.position = 0
            _GXAPDU.parsePDU(settings, settings.cipher, value, xml)
        elif cmd == Command.INITIATE_REQUEST:
            value.position = 0
            settings = GXDLMSSettings(True, None)
            _GXAPDU.parseInitiate(True, settings, settings.cipher, value, xml)
        elif cmd == Command.INITIATE_RESPONSE:
            value.position = 0
            settings = GXDLMSSettings(False, None)
            self.getCiphering(settings, True)
            _GXAPDU.parseInitiate(True, settings, settings.cipher, value, xml)
        elif cmd == 0x81:
            #  Ua
            value.position = 0
            self.getUa(value, xml)
        elif cmd == Command.AARE:
            value.position = 0
            settings = GXDLMSSettings(False, None)
            self.getCiphering(settings, True)
            _GXAPDU.parsePDU(settings, settings.cipher, value, xml)
        elif cmd == Command.GET_REQUEST:
            GXDLMSLNCommandHandler.handleGetRequest(settings, None, value, None, xml)
        elif cmd == Command.SET_REQUEST:
            GXDLMSLNCommandHandler.handleSetRequest(settings, None, value, None, xml)
        elif cmd == Command.READ_REQUEST:
            GXDLMSSNCommandHandler.handleReadRequest(settings, None, value, None, xml)
        elif cmd == Command.METHOD_REQUEST:
            GXDLMSLNCommandHandler.handleMethodRequest(
                settings, None, value, None, None, xml
            )
        elif cmd == Command.WRITE_REQUEST:
            GXDLMSSNCommandHandler.handleWriteRequest(settings, None, value, None, xml)
        elif cmd == Command.ACCESS_REQUEST:
            GXDLMSLNCommandHandler.handleAccessRequest(settings, None, value, None, xml)
        elif cmd == Command.DATA_NOTIFICATION:
            data.xml = xml
            data.data = value
            value.position = 0
            GXDLMS.getPdu(settings, data)
        elif cmd == Command.INFORMATION_REPORT:
            data.xml = xml
            data.data = value
            GXDLMSSNCommandHandler.handleInformationReport(settings, data, None)
        elif cmd == Command.EVENT_NOTIFICATION:
            data.xml = xml
            data.data = value
            GXDLMSLNCommandHandler.handleEventNotification(settings, data, None)
        elif cmd in (
            Command.READ_RESPONSE,
            Command.WRITE_RESPONSE,
            Command.GET_RESPONSE,
            Command.SET_RESPONSE,
            Command.METHOD_RESPONSE,
            Command.ACCESS_RESPONSE,
            Command.GENERAL_BLOCK_TRANSFER,
        ):
            data.xml = xml
            data.data = value
            value.position = 0
            GXDLMS.getPdu(settings, data)
        elif cmd == Command.GENERAL_CIPHERING:
            settings.cipher = GXCiphering("ABCDEFGH".encode())
            data.xml = xml
            data.data = value
            value.position = 0
            GXDLMS.getPdu(settings, data)
        elif cmd == Command.RELEASE_REQUEST:
            xml.appendStartTag(cmd)
            value.getUInt8()
            #  Len.
            if value.available() != 0:
                #  BerType
                value.getUInt8()
                #  Len.
                value.getUInt8()
                if xml.outputType == TranslatorOutputType.SIMPLE_XML:
                    str_ = TranslatorSimpleTags.releaseRequestReasonToString(
                        value.getUInt8()
                    )
                else:
                    str_ = TranslatorStandardTags.releaseRequestReasonToString(
                        value.getUInt8()
                    )
                xml.appendLine(TranslatorTags.REASON, "Value", str_)
                if value.available() != 0:
                    _GXAPDU.parsePDU2(settings, settings.cipher, value, xml)
            xml.appendEndTag(cmd)
        elif cmd == Command.RELEASE_RESPONSE:
            xml.appendStartTag(cmd)
            value.getUInt8()
            #  Len.
            if value.available() != 0:
                #  BerType
                value.getUInt8()
                #  Len.
                value.getUInt8()
                if xml.outputType == TranslatorOutputType.SIMPLE_XML:
                    str_ = TranslatorSimpleTags.releaseResponseReasonToString(
                        value.getUInt8()
                    )
                else:
                    str_ = TranslatorStandardTags.releaseResponseReasonToString(
                        value.getUInt8()
                    )
                xml.appendLine(TranslatorTags.REASON, "Value", str_)
                if value.available() != 0:
                    _GXAPDU.parsePDU2(settings, settings.cipher, value, xml)
            xml.appendEndTag(cmd)
        elif cmd in (
            Command.GLO_READ_REQUEST,
            Command.GLO_WRITE_REQUEST,
            Command.GLO_GET_REQUEST,
            Command.GLO_SET_REQUEST,
            Command.GLO_READ_RESPONSE,
            Command.GLO_WRITE_RESPONSE,
            Command.GLO_GET_RESPONSE,
            Command.GLO_SET_RESPONSE,
            Command.GLO_METHOD_REQUEST,
            Command.GLO_METHOD_RESPONSE,
            Command.DED_GET_REQUEST,
            Command.DED_SET_REQUEST,
            Command.DED_READ_RESPONSE,
            Command.DED_GET_RESPONSE,
            Command.DED_SET_RESPONSE,
            Command.DED_METHOD_REQUEST,
            Command.DED_METHOD_RESPONSE,
            Command.GLO_CONFIRMED_SERVICE_ERROR,
            Command.DED_CONFIRMED_SERVICE_ERROR,
        ):
            if settings.cipher and self.comments:
                originalPosition = value.position
                len_ = xml.getXmlLength()
                try:
                    value.position = value.position - 1
                    if cmd in (
                        Command.GLO_READ_REQUEST,
                        Command.GLO_WRITE_REQUEST,
                        Command.GLO_GET_REQUEST,
                        Command.GLO_SET_REQUEST,
                        Command.GLO_METHOD_REQUEST,
                        Command.DED_GET_REQUEST,
                        Command.DED_SET_REQUEST,
                        Command.DED_METHOD_REQUEST,
                    ):
                        st = settings.cipher.getSystemTitle()
                    else:
                        st = settings.sourceSystemTitle
                    if st or cmd in (
                        Command.GENERAL_GLO_CIPHERING,
                        Command.GENERAL_DED_CIPHERING,
                    ):
                        p = None
                        if cmd in (
                            Command.DED_GET_REQUEST,
                            Command.DED_SET_REQUEST,
                            Command.DED_METHOD_REQUEST,
                        ):
                            p = AesGcmParameter(
                                0,
                                st,
                                settings.cipher.dedicatedKey,
                                settings.cipher.authenticationKey,
                            )
                        else:
                            p = AesGcmParameter(
                                0,
                                st,
                                settings.cipher.blockCipherKey,
                                settings.cipher.authenticationKey,
                            )
                        if p.blockCipherKey:
                            data2 = GXByteBuffer(
                                GXCiphering.decrypt(settings.cipher, p, value)
                            )
                            xml.startComment("Decrypt data: " + str(data2))
                            self._pduToXml2(
                                xml, data2, omitDeclaration, omitNameSpace, False
                            )
                            xml.endComment()
                except Exception:
                    #  It's OK if this fails.  Ciphering settings are not correct.
                    xml.xml.setXmlLength(len_)
                value.position = originalPosition
            cnt = _GXCommon.getObjectCount(value)
            if cnt != len(value) - value.position:
                xml.appendComment(
                    "Invalid length: "
                    + str(cnt)
                    + ". It should be: "
                    + str(len(value) - value.position)
                )
            xml.appendLine(
                cmd,
                "Value",
                value.toHex(False, value.position, len(value) - value.position),
            )
        elif cmd in (Command.GENERAL_GLO_CIPHERING, Command.GENERAL_DED_CIPHERING):
            if settings.cipher and self.comments:
                len_ = xml.getXmlLength()
                originalPosition = value.position
                try:
                    tmp = GXByteBuffer()
                    tmp.set(value, value.position - 1, len(value) - value.position + 1)
                    p = AesGcmParameter(
                        0,
                        settings.cipher.systemTitle,
                        settings.cipher.blockCipherKey,
                        settings.cipher.authenticationKey,
                    )
                    p.xml = xml
                    tmp = GXByteBuffer(GXCiphering.decrypt(settings.cipher, p, tmp))
                    len_ = xml.getXmlLength()
                    xml.startComment("Decrypt data: " + str(tmp))
                    self._pduToXml2(xml, tmp, omitDeclaration, omitNameSpace, False)
                    xml.endComment()
                except Exception:
                    #  It's OK if this fails.  Ciphering settings are not
                    #  correct.
                    xml.setXmlLength(len_)
                value.position = originalPosition
            len_ = _GXCommon.getObjectCount(value)
            tmp = bytearray(len_)
            value.get(tmp)
            xml.appendStartTag(Command.GENERAL_GLO_CIPHERING)
            xml.appendLine(
                TranslatorTags.SYSTEM_TITLE, None, GXByteBuffer.hex(tmp, False, 0, len_)
            )
            len_ = _GXCommon.getObjectCount(value)
            tmp = bytearray(len_)
            value.get(tmp)
            xml.appendLine(
                TranslatorTags.CIPHERED_SERVICE,
                None,
                GXByteBuffer.hex(tmp, False, 0, len_),
            )
            xml.appendEndTag(Command.GENERAL_GLO_CIPHERING)
        elif cmd == Command.CONFIRMED_SERVICE_ERROR:
            data.xml = xml
            data.data = value
            GXDLMS.handleConfirmedServiceError(data)
        elif cmd == Command.GATEWAY_REQUEST:
            pass
        elif cmd == Command.GATEWAY_RESPONSE:
            data.xml = xml
            data.data = value
            #  Get Network ID.
            id_ = value.getUInt8()
            #  Get Physical device address.
            len_ = _GXCommon.getObjectCount(value)
            tmp = bytearray(len_)
            value.get(tmp)
            xml.appendStartTag(cmd)
            xml.appendLine(TranslatorTags.NETWORK_ID, None, str(id_))
            xml.appendLine(
                TranslatorTags.PHYSICAL_DEVICE_ADDRESS,
                None,
                GXByteBuffer.hex(tmp, False, 0, len_),
            )
            self._pduToXml2(
                xml,
                GXByteBuffer(value.remaining()),
                omitDeclaration,
                omitNameSpace,
                allowUnknownCommand,
            )
            xml.appendEndTag(cmd)
        elif cmd == Command.EXCEPTION_RESPONSE:
            data.xml = xml
            data.data = value
            GXDLMS.handleExceptionResponse(data)
        else:
            if not allowUnknownCommand:
                raise Exception("Invalid command.")
            value.position -= 1
            xml.appendLine(
                '<Data="'
                + value.toHex(False, value.position, len(value) - value.position)
                + '" />'
            )
        if self.outputType == TranslatorOutputType.STANDARD_XML:
            sb = ""
            if not omitDeclaration:
                sb += '<?xml version="1.0" encoding="utf-8"?>\r\n'
            if not omitNameSpace:
                if not cmd in (
                    Command.AARE,
                    Command.AARQ,
                    Command.RELEASE_REQUEST,
                    Command.RELEASE_RESPONSE,
                ):
                    sb += '<x:xDLMS-APDU xmlns:x="http://www.dlms.com/COSEMpdu">\r\n'
                else:
                    sb += '<x:aCSE-APDU xmlns:x="http://www.dlms.com/COSEMpdu">\r\n'

            sb += str(xml)
            if not omitNameSpace:
                if not cmd in (
                    Command.AARE,
                    Command.AARQ,
                    Command.RELEASE_REQUEST,
                    Command.RELEASE_RESPONSE,
                ):
                    sb += "</x:xDLMS-APDU>\r\n"
                else:
                    sb += "</x:aCSE-APDU>\r\n"
            return sb
        return str(xml)

    #
    # Get command from XML.
    #
    # @param node
    #            XML node.
    # @param s
    #            XML settings.
    # @param tag
    #            Tag.
    #
    @classmethod
    def getCommand(cls, node, s, tag):
        s.command = tag
        if tag in (
            Command.SNRM,
            Command.AARQ,
            Command.READ_REQUEST,
            Command.WRITE_REQUEST,
            Command.GET_REQUEST,
            Command.SET_REQUEST,
            Command.RELEASE_REQUEST,
            Command.METHOD_REQUEST,
            Command.ACCESS_REQUEST,
            Command.INITIATE_REQUEST,
            Command.CONFIRMED_SERVICE_ERROR,
            Command.EXCEPTION_RESPONSE,
        ):
            s.settings.server = False
        elif tag in (
            Command.GLO_INITIATE_REQUEST,
            Command.GLO_GET_REQUEST,
            Command.GLO_SET_REQUEST,
            Command.GLO_METHOD_REQUEST,
            Command.GLO_READ_REQUEST,
            Command.GLO_WRITE_REQUEST,
            Command.DED_GET_REQUEST,
            Command.DED_SET_REQUEST,
            Command.DED_METHOD_REQUEST,
        ):
            s.settings.server = False
            tmp = GXByteBuffer.hexToBytes(cls.getValue(node, s))
            s.settings.getCipher().setSecurity(Security(tmp[0]))
            s.data.set(tmp)
        elif tag in (
            Command.UA,
            Command.AARE,
            Command.GET_RESPONSE,
            Command.SET_RESPONSE,
            Command.READ_RESPONSE,
            Command.WRITE_RESPONSE,
            Command.METHOD_RESPONSE,
            Command.RELEASE_RESPONSE,
            Command.DATA_NOTIFICATION,
            Command.ACCESS_RESPONSE,
            Command.INITIATE_RESPONSE,
            Command.INFORMATION_REPORT,
            Command.EVENT_NOTIFICATION,
            Command.DISCONNECT_REQUEST,
        ):
            pass
        elif tag in (
            Command.GLO_INITIATE_RESPONSE,
            Command.GLO_GET_RESPONSE,
            Command.GLO_SET_RESPONSE,
            Command.GLO_METHOD_RESPONSE,
            Command.GLO_READ_RESPONSE,
            Command.GLO_WRITE_RESPONSE,
            Command.GLO_EVENT_NOTIFICATION,
            Command.DED_GET_RESPONSE,
            Command.DED_SET_RESPONSE,
            Command.DED_METHOD_RESPONSE,
            Command.DED_EVENT_NOTIFICATION,
        ):
            tmp = GXByteBuffer.hexToBytes(cls.getValue(node, s))
            s.settings.getCipher().setSecurity(Security(tmp[0]))
            s.data.set(tmp)
        elif tag == Command.GENERAL_GLO_CIPHERING:
            pass
        elif tag == Command.GENERAL_CIPHERING:
            pass
        elif tag == TranslatorTags.FRAME_TYPE:
            s.command = 0
        elif tag == Command.GATEWAY_REQUEST:
            s.gwCommand = Command.GATEWAY_REQUEST
            s.settings.server = False
        elif tag == Command.GATEWAY_RESPONSE:
            s.gwCommand = Command.GATEWAY_RESPONSE
        else:
            raise ValueError("Invalid Command: " + node.tag)

    @classmethod
    def getFrame(cls, node, s, tag):
        found = True
        if tag == TranslatorTags.WRAPPER:
            s.settings.interfaceType = InterfaceType.WRAPPER
        elif tag == TranslatorTags.HDLC:
            s.settings.interfaceType = InterfaceType.HDLC
        elif tag == TranslatorTags.TARGET_ADDRESS:
            s.settings.serverAddress = s.parseInt(cls.getValue(node, s))
        elif tag == TranslatorTags.SOURCE_ADDRESS:
            s.settings.clientAddress = s.parseInt(cls.getValue(node, s))
        else:
            found = False
        return found

    @classmethod
    def getNodeCount(cls, node):
        cnt = 0
        for _ in node:
            cnt += 1
        return cnt

    @classmethod
    def handleAarqAare(cls, node, s, tag):
        # pylint: disable=bad-option-value,redefined-variable-type
        tmp = []
        list_ = None
        value = int()
        if tag == TranslatorGeneralTags.APPLICATION_CONTEXT_NAME:
            if s.outputType == TranslatorOutputType.STANDARD_XML:
                value = int(node.getFirstChild().getNodeValue())
                if value == 1:
                    s.settings.setUseLogicalNameReferencing(True)
                elif value == 2:
                    s.settings.setUseLogicalNameReferencing(False)
                elif value == 3:
                    s.settings.setUseLogicalNameReferencing(True)
                elif value == 4:
                    s.settings.setUseLogicalNameReferencing(False)
                else:
                    raise ValueError("Invalid application context name.")
            else:
                if (
                    node.attrib["Value"] == "SN"
                    or node.attrib["Value"] == "SN_WITH_CIPHERING"
                ):
                    s.settings.setUseLogicalNameReferencing(False)
                elif (
                    node.attrib["Value"] == "LN"
                    or node.attrib["Value"] == "LN_WITH_CIPHERING"
                ):
                    s.settings.setUseLogicalNameReferencing(True)
                else:
                    raise ValueError("Invalid Reference type name.")
        elif tag == Command.GLO_INITIATE_REQUEST:
            s.settings.setServer(False)
            s.command = tag
            tmp = GXByteBuffer.hexToBytes(cls.getValue(node, s))
            s.settings.getCipher().setSecurity(Security(tmp[0]))
            s.data.set(tmp)
        elif tag == Command.GLO_INITIATE_RESPONSE:
            s.command = tag
            tmp = GXByteBuffer.hexToBytes(cls.getValue(node, s))
            s.settings.getCipher().setSecurity(Security(tmp[0]))
            s.data.set(tmp)
        elif tag == Command.INITIATE_REQUEST:
            pass
        elif tag == Command.INITIATE_RESPONSE:
            pass
        elif tag == TranslatorGeneralTags.USER_INFORMATION:
            if s.outputType == TranslatorOutputType.STANDARD_XML:
                bb = GXByteBuffer()
                tmp = GXByteBuffer.hexToBytes(cls.getValue(node, s))
                bb.set(tmp)
                if s.settings.isServer:
                    s.settings.setProposedConformance(0xFFFFFF)
                _GXAPDU.parseInitiate(
                    False, s.settings, s.settings.getCipher(), bb, None
                )
                if not s.settings.isServer:
                    s.settings.proposedConformance = s.settings.negotiatedConformance
        elif tag == 0xBE00:
            pass
        elif tag == 0xBE06:
            pass
        elif tag == 0xBE01:
            pass
        elif tag == 0x8A:
            pass
        elif tag == 0xBE04:
            str_ = cls.getValue(node, s)
            if int(str_, 16) == 7:
                s.settings.setUseLogicalNameReferencing(True)
            else:
                s.settings.setUseLogicalNameReferencing(False)
        elif tag == 0x8B:
            pass
        elif tag == 0x89:
            if s.outputType == TranslatorOutputType.SIMPLE_XML:
                s.settings.authentication = Authentication.valueofString(
                    cls.getValue(node, s)
                )
            else:
                s.settings.authentication = Authentication(int(cls.getValue(node, s)))
        elif tag == 0xAC:
            if s.settings.authentication == Authentication.LOW:
                s.settings.password = GXByteBuffer.hexToBytes(cls.getValue(node, s))
            else:
                s.settings.setCtoSChallenge(
                    GXByteBuffer.hexToBytes(cls.getValue(node, s))
                )
        elif tag == TranslatorGeneralTags.DEDICATED_KEY:
            tmp = GXByteBuffer.hexToBytes(cls.getValue(node, s))
            s.settings.getCipher().setDedicatedKey(tmp)
        elif tag == TranslatorGeneralTags.CALLING_AP_TITLE:
            s.settings.setCtoSChallenge(GXByteBuffer.hexToBytes(cls.getValue(node, s)))
        elif tag == int(TranslatorGeneralTags.CALLING_AE_INVOCATION_ID):
            s.settings.setUserId(s.parseInt(cls.getValue(node, s)))
        elif tag == int(TranslatorGeneralTags.CALLED_AE_INVOCATION_ID):
            s.settings.setUserId(s.parseInt(cls.getValue(node, s)))
        elif tag == TranslatorGeneralTags.RESPONDING_AE_INVOCATION_ID:
            s.settings.setUserId(s.parseInt(cls.getValue(node, s)))
        elif tag == 0xA4:
            s.settings.setStoCChallenge(GXByteBuffer.hexToBytes(cls.getValue(node, s)))
        elif tag == 0xBE03:
            pass
        elif tag == 0xBE05:
            if s.settings.isServer:
                list_ = s.settings.negotiatedConformance
            else:
                list_ = s.settings.proposedConformance
            list_ = []
            if s.outputType == TranslatorOutputType.STANDARD_XML:
                nodes = node.getFirstChild().getNodeValue()
                for it in nodes.split(" "):
                    if it.strip():
                        list_.append(
                            TranslatorStandardTags.value_ofConformance(it.strip())
                        )
        elif tag == 0xBE08:
            if s.settings.isServer:
                list_ = s.settings.negotiatedConformance
            else:
                list_ = s.settings.proposedConformance
            list_ |= TranslatorSimpleTags.value_ofConformance(node.attrib["Name"])
        elif tag == 0xA2:
            s.result = AssociationResult(s.parseInt(cls.getValue(node, s)))
        elif tag == 0xBE02:
            pass
        elif tag == 0xBE07:
            s.settings.maxPduSize = s.parseInt(cls.getValue(node, s))
        elif tag == 0xA3:
            s.diagnostic = SourceDiagnostic.NONE
        elif tag == 0xA301:
            s.diagnostic = SourceDiagnostic(s.parseInt(cls.getValue(node, s)))
        elif tag == 0xBE09:
            pass
        elif tag == TranslatorGeneralTags.CHAR_STRING:
            if s.settings.authentication == Authentication.LOW:
                s.settings.password = GXByteBuffer.hexToBytes(cls.getValue(node, s))
            else:
                if s.command == Command.AARQ:
                    s.settings.setCtoSChallenge(
                        GXByteBuffer.hexToBytes(cls.getValue(node, s))
                    )
                else:
                    s.settings.setStoCChallenge(
                        GXByteBuffer.hexToBytes(cls.getValue(node, s))
                    )
        elif tag == TranslatorGeneralTags.RESPONDER_ACSE_REQUIREMENT:
            pass
        elif tag == TranslatorGeneralTags.RESPONDING_AUTHENTICATION:
            s.settings.setStoCChallenge(GXByteBuffer.hexToBytes(cls.getValue(node, s)))
        elif tag == TranslatorTags.RESULT:
            s.setResult(AssociationResult(int(cls.getValue(node, s))))
        elif tag == Command.CONFIRMED_SERVICE_ERROR:
            if s.command == Command.NONE:
                s.settings.setServer(False)
                s.command = tag
        elif tag == TranslatorTags.REASON:
            if s.command == Command.RELEASE_REQUEST:
                if s.OutputType == TranslatorOutputType.SIMPLE_XML:
                    s.reason = TranslatorSimpleTags.value_ofReleaseRequestReason(
                        cls.getValue(node, s)
                    )
                else:
                    s.reason = TranslatorStandardTags.value_ofReleaseRequestReason(
                        cls.getValue(node, s)
                    )
            else:
                if s.OutputType == TranslatorOutputType.SIMPLE_XML:
                    s.reason = TranslatorSimpleTags.value_ofReleaseResponseReason(
                        cls.getValue(node, s)
                    )
                else:
                    s.reason = TranslatorStandardTags.value_ofReleaseResponseReason(
                        cls.getValue(node, s)
                    )
        elif tag == TranslatorTags.SERVICE:
            s.attributeDescriptor.setUInt8(0xE)
            s.attributeDescriptor.setUInt8(s.parseInt(cls.getValue(node, s)))
        elif tag == TranslatorTags.SERVICE_ERROR:
            if s.command == Command.AARE:
                s.attributeDescriptor.setUInt8(6)
                for childNode in node:
                    s.attributeDescriptor.setUInt8(
                        TranslatorSimpleTags.getInitiateByValue(
                            cls.getValue(childNode, s)
                        )
                    )
                return False
        elif tag == TranslatorTags.PROTOCOL_VERSION:
            str_ = cls.getValue(node, s)
            pv = GXByteBuffer()
            pv.setUInt8(int((8 - len(str_))))
            _GXCommon.setBitString(pv, str_, False)
            s.settings.setProtocolVersion(str_)
        elif tag == TranslatorTags.CALLED_AP_TITLE:
            pass
        elif tag == TranslatorTags.CALLED_AE_QUALIFIER:
            tmp = GXByteBuffer.hexToBytes(cls.getValue(node, s))
            s.attributeDescriptor.setUInt8(
                int((0xA2 if tag == int(TranslatorTags.CALLED_AP_TITLE) else 0xA3))
            )
            s.attributeDescriptor.setUInt8(3)
            s.attributeDescriptor.setUInt8(BerType.OCTET_STRING)
            s.attributeDescriptor.setUInt8(len(tmp))
            s.attributeDescriptor.set(tmp)
        elif tag == int(TranslatorTags.CALLED_AP_INVOCATION_ID):
            s.attributeDescriptor.setUInt8(0xA6)
            s.attributeDescriptor.setUInt8(3)
            s.attributeDescriptor.setUInt8(BerType.INTEGER)
            s.attributeDescriptor.setUInt8(1)
            s.attributeDescriptor.setUInt8(int(s.parseInt(cls.getValue(node, s))))
        elif tag == int(TranslatorTags.CALLED_AE_INVOCATION_ID):
            s.attributeDescriptor.setUInt8(0xA5)
            s.attributeDescriptor.setUInt8(3)
            s.attributeDescriptor.setUInt8(BerType.INTEGER)
            s.attributeDescriptor.setUInt8(1)
            s.attributeDescriptor.setUInt8(int(s.parseInt(cls.getValue(node, s))))
        elif tag == int(TranslatorTags.CALLING_AP_INVOCATION_ID):
            s.attributeDescriptor.setUInt8(0xA4)
            s.attributeDescriptor.setUInt8(3)
            s.attributeDescriptor.setUInt8(BerType.INTEGER)
            s.attributeDescriptor.setUInt8(1)
            s.attributeDescriptor.setUInt8(int(s.parseInt(cls.getValue(node, s))))
        else:
            raise ValueError("Invalid AARQ node: " + node.tag)
        return True

    @classmethod
    def getValue(cls, node, s):
        str_ = ""
        if s.outputType == TranslatorOutputType.STANDARD_XML:
            if node.text:
                str_ = node.text.strip()
        else:
            # Get first element.
            for it in node.attrib:
                str_ = node.attrib[it]
                break
        return str_

    @classmethod
    def value_ofErrorCode(cls, type_, value):
        if type_ == TranslatorOutputType.STANDARD_XML:
            return TranslatorStandardTags.value_ofErrorCode(value)
        return TranslatorSimpleTags.value_ofErrorCode(value)

    @classmethod
    def errorCodeToString(cls, type_, value):
        if type_ == TranslatorOutputType.STANDARD_XML:
            return TranslatorStandardTags.errorCodeToString(value)
        return TranslatorSimpleTags.errorCodeToString(value)

    @classmethod
    def readNode(cls, node, s):
        # pylint: disable=bad-option-value,redefined-variable-type
        value = 0
        tmp = []
        preData = None
        str_ = None
        if s.outputType == TranslatorOutputType.SIMPLE_XML:
            str_ = node.tag.lower()
        else:
            pos = node.tag.find("}")
            if pos != -1:
                str_ = node.tag[1 + pos :]
            else:
                str_ = node.tag
        tag = 0
        if s.command != Command.CONFIRMED_SERVICE_ERROR or s.tags.containsKey(str_):
            tag = s.tags.get(str_)
        if s.command == Command.NONE:
            if not (
                (s.settings.clientAddress == 0 or s.settings.serverAddress == 0)
                and cls.getFrame(node, s, tag)
                or tag in (TranslatorTags.PDU_DLMS, TranslatorTags.PDU_CSE)
            ):
                cls.getCommand(node, s, tag)
        elif s.command in (
            Command.AARQ,
            Command.AARE,
            Command.INITIATE_REQUEST,
            Command.INITIATE_RESPONSE,
            Command.RELEASE_REQUEST,
            Command.RELEASE_RESPONSE,
        ):
            if not cls.handleAarqAare(node, s, tag):
                return
        elif tag >= _GXCommon.DATA_TYPE_OFFSET:
            if tag == DataType.DATETIME + _GXCommon.DATA_TYPE_OFFSET or (
                s.command == Command.EVENT_NOTIFICATION and not s.attributeDescriptor
            ):
                preData = cls.updateDateTime(node, s, preData)
                if preData is None and s.command == Command.GENERAL_CIPHERING:
                    s.data.setUInt8(0)
            else:
                preData = cls.updateDataType(node, s, tag)
        elif s.command == Command.CONFIRMED_SERVICE_ERROR:
            if s.outputType == TranslatorOutputType.STANDARD_XML:
                if tag == TranslatorTags.INITIATE_ERROR:
                    s.attributeDescriptor.setUInt8(1)
                else:
                    se = TranslatorStandardTags.getServiceError(str_[2:])
                    s.attributeDescriptor.setUInt8(se)
                    s.attributeDescriptor.setUInt8(
                        TranslatorStandardTags.getError(se, cls.getValue(node, s))
                    )
            else:
                if tag != TranslatorTags.SERVICE_ERROR:
                    if s.attributeDescriptor.size == 0:
                        s.attributeDescriptor.setUInt8(
                            s.parseShort(cls.getValue(node, s))
                        )
                    else:
                        se = TranslatorSimpleTags.getServiceError(str_)
                        s.attributeDescriptor.setUInt8(se)
                        s.attributeDescriptor.setUInt8(
                            TranslatorSimpleTags.getError(se, cls.getValue(node, s))
                        )
        else:
            if tag in (
                Command.GET_REQUEST << 8 | GetCommandType.NORMAL,
                Command.GET_REQUEST << 8 | GetCommandType.NEXT_DATA_BLOCK,
                Command.GET_REQUEST << 8 | GetCommandType.WITH_LIST,
                Command.SET_REQUEST << 8 | SetRequestType.NORMAL,
                Command.SET_REQUEST << 8 | SetRequestType.FIRST_DATA_BLOCK,
                Command.SET_REQUEST << 8 | SetRequestType.WITH_DATA_BLOCK,
                Command.SET_REQUEST << 8 | SetRequestType.WITH_LIST,
            ):
                s.requestType = tag & 0xF
            elif tag in (
                Command.GET_RESPONSE << 8 | GetCommandType.NORMAL,
                Command.GET_RESPONSE << 8 | GetCommandType.NEXT_DATA_BLOCK,
                Command.GET_RESPONSE << 8 | GetCommandType.WITH_LIST,
                Command.SET_RESPONSE << 8 | SetResponseType.NORMAL,
                Command.SET_RESPONSE << 8 | SetResponseType.DATA_BLOCK,
                Command.SET_RESPONSE << 8 | SetResponseType.LAST_DATA_BLOCK,
                Command.SET_RESPONSE << 8 | SetResponseType.WITH_LIST,
                Command.SET_RESPONSE << 8 | SetResponseType.LAST_DATA_BLOCK_WITH_LIST,
            ):
                s.requestType = tag & 0xF
            elif (
                tag == Command.READ_RESPONSE << 8 | SingleReadResponse.DATA_BLOCK_RESULT
            ):
                s.count = s.count + 1
                s.requestType = tag & 0xF
            elif (
                tag
                == Command.READ_REQUEST << 8
                | VariableAccessSpecification.PARAMETERISED_ACCESS
            ):
                s.requestType = VariableAccessSpecification.PARAMETERISED_ACCESS
            elif (
                tag
                == Command.READ_REQUEST << 8
                | VariableAccessSpecification.BLOCK_NUMBER_ACCESS
            ):
                s.requestType = VariableAccessSpecification.BLOCK_NUMBER_ACCESS
                s.count = s.count + 1
            elif tag == Command.METHOD_REQUEST << 8 | ActionRequestType.NORMAL:
                s.requestType = tag & 0xF
            elif tag == Command.METHOD_REQUEST << 8 | ActionRequestType.NEXT_BLOCK:
                s.requestType = tag & 0xF
            elif tag == Command.METHOD_REQUEST << 8 | ActionRequestType.WITH_LIST:
                s.requestType = tag & 0xF
            elif tag == Command.METHOD_RESPONSE << 8 | ActionResponseType.NORMAL:
                s.requestType = tag & 0xF
            elif tag in (
                Command.READ_RESPONSE << 8 | SingleReadResponse.DATA,
                TranslatorTags.DATA,
            ):
                if s.command in (Command.READ_REQUEST, Command.READ_RESPONSE, Command.GET_REQUEST):
                    s.count = s.count + 1
                    s.requestType = 0
                elif s.command in (Command.GET_RESPONSE, Command.METHOD_RESPONSE):
                    s.data.setUInt8(0)
            elif tag == TranslatorTags.SUCCESS:
                s.count = s.count + 1
                s.attributeDescriptor.setUInt8(ErrorCode.OK)
            elif tag == TranslatorTags.DATA_ACCESS_ERROR:
                s.count = s.count + 1
                s.attributeDescriptor.setUInt8(1)
                s.attributeDescriptor.setUInt8(
                    cls.value_ofErrorCode(s.outputType, cls.getValue(node, s))
                )
            elif tag == TranslatorTags.LIST_OF_VARIABLE_ACCESS_SPECIFICATION:
                if s.command == Command.WRITE_REQUEST:
                    _GXCommon.setObjectCount(cls.getNodeCount(node), s.data)
            elif tag == TranslatorTags.VARIABLE_ACCESS_SPECIFICATION:
                pass
            elif tag == TranslatorTags.LIST_OF_DATA:
                if s.command == Command.ACCESS_RESPONSE and not s.data:
                    s.data.setUInt8(0)
                if (
                    s.outputType == TranslatorOutputType.SIMPLE_XML
                    or s.command != Command.WRITE_REQUEST
                ):
                    _GXCommon.setObjectCount(cls.getNodeCount(node), s.data)
            elif tag in (
                Command.ACCESS_RESPONSE << 8 | AccessServiceCommandType.GET,
                Command.ACCESS_RESPONSE << 8 | AccessServiceCommandType.SET,
                Command.ACCESS_RESPONSE << 8 | AccessServiceCommandType.ACTION,
            ):
                s.requestType = tag & 0xF
            elif tag == TranslatorTags.DATE_TIME:
                preData = cls.updateDateTime(node, s, preData)
                if preData is None and s.command == Command.GENERAL_CIPHERING:
                    s.data.setUInt8(0)
            elif tag == TranslatorTags.CURRENT_TIME:
                if s.outputType == TranslatorOutputType.SIMPLE_XML:
                    cls.updateDateTime(node, s, preData)
                else:
                    str_ = cls.getValue(node, s)
                    s.setTime(GXDateTime(_GXCommon.getGeneralizedTime(str_)))
            elif tag == TranslatorTags.TIME:
                preData = cls.updateDateTime(node, s, preData)
            elif tag == TranslatorTags.INVOKE_ID:
                value = s.parseShort(cls.getValue(node, s))
                s.settings.updateInvokeId(value)
            elif tag == TranslatorTags.LONG_INVOKE_ID:
                value = s.parseLong(cls.getValue(node, s))
                if (value & 0x80000000) != 0:
                    s.settings.priority = Priority.HIGH
                else:
                    s.settings.priority = Priority.NORMAL
                if (value & 0x40000000) != 0:
                    s.settings.serviceClass = ServiceClass.CONFIRMED
                else:
                    s.settings.serviceClass = ServiceClass.UN_CONFIRMED
                s.settings.longInvokeID = value & 0xFFFFFFF
            elif tag == 0x88:
                # ResponderACSERequirement
                pass
            elif tag == 0x80:
                s.settings.stoCChallenge = GXByteBuffer.hexToBytes(
                    cls.getValue(node, s)
                )
            elif tag == TranslatorTags.ATTRIBUTE_DESCRIPTOR:
                pass
            elif tag == TranslatorTags.CLASS_ID:
                s.attributeDescriptor.setUInt16(s.parseInt(cls.getValue(node, s)))
            elif tag == TranslatorTags.INSTANCE_ID:
                s.attributeDescriptor.set(
                    GXByteBuffer.hexToBytes(cls.getValue(node, s))
                )
            elif tag == TranslatorTags.ATTRIBUTE_ID:
                s.attributeDescriptor.setUInt8(s.parseShort(cls.getValue(node, s)))
                if s.command not in (
                    Command.ACCESS_REQUEST,
                    Command.EVENT_NOTIFICATION,
                ):
                    s.attributeDescriptor.setUInt8(0)
            elif tag == TranslatorTags.METHOD_INVOCATION_PARAMETERS:
                s.attributeDescriptor.setUInt8(1, len(s.attributeDescriptor) - 1)
            elif tag == TranslatorTags.SELECTOR:
                s.attributeDescriptor.set(
                    GXByteBuffer.hexToBytes(cls.getValue(node, s))
                )
            elif tag == TranslatorTags.PARAMETER:
                pass
            elif tag == TranslatorTags.LAST_BLOCK:
                s.data.setUInt8(s.parseShort(cls.getValue(node, s)))
            elif tag == TranslatorTags.BLOCK_NUMBER:
                if s.command in (
                    Command.GET_REQUEST,
                    Command.GET_RESPONSE,
                    Command.SET_REQUEST,
                    Command.SET_RESPONSE,
                    Command.METHOD_REQUEST,
                    Command.METHOD_RESPONSE,
                ):
                    s.data.setUInt32(s.parseLong(cls.getValue(node, s)))
                else:
                    s.data.setUInt16(s.parseInt(cls.getValue(node, s)))
            elif tag == TranslatorTags.RAW_DATA:
                if s.command == Command.GET_RESPONSE:
                    s.data.setUInt8(0)
                tmp = GXByteBuffer.hexToBytes(cls.getValue(node, s))
                _GXCommon.setObjectCount(len(tmp), s.data)
                s.data.set(tmp)
            elif tag == TranslatorTags.METHOD_DESCRIPTOR:
                pass
            elif tag == TranslatorTags.METHOD_ID:
                s.attributeDescriptor.setUInt8(s.parseShort(cls.getValue(node, s)))
                s.attributeDescriptor.setUInt8(0)
            elif tag in (
                TranslatorTags.RESULT,
                TranslatorGeneralTags.ASSOCIATION_RESULT,
            ):
                if s.command == Command.GET_REQUEST or s.requestType == 3:
                    _GXCommon.setObjectCount(
                        node.getChildNodes().getLength(), s.attributeDescriptor
                    )
                elif s.command in (Command.METHOD_RESPONSE, Command.SET_RESPONSE):
                    str_ = cls.getValue(node, s)
                    if str_:
                        s.attributeDescriptor.setUInt8(
                            cls.value_ofErrorCode(s.outputType, str_)
                        )
                elif s.command == Command.ACCESS_RESPONSE:
                    str_ = cls.getValue(node, s)
                    if str_:
                        s.data.setUInt8(cls.value_ofErrorCode(s.outputType, str_))
            elif tag == TranslatorTags.REASON:
                if s.command == Command.RELEASE_REQUEST:
                    if s.outputType == TranslatorOutputType.SIMPLE_XML:
                        s.reason = int(
                            TranslatorSimpleTags.value_ofReleaseRequestReason(
                                cls.getValue(node, s)
                            )
                        )
                    else:
                        s.reason = int(
                            TranslatorStandardTags.value_ofReleaseRequestReason(
                                cls.getValue(node, s)
                            )
                        )
                else:
                    if s.outputType == TranslatorOutputType.SIMPLE_XML:
                        s.reason = int(
                            TranslatorSimpleTags.value_ofReleaseResponseReason(
                                cls.getValue(node, s)
                            )
                        )
                    else:
                        s.reason = int(
                            TranslatorStandardTags.value_ofReleaseResponseReason(
                                cls.getValue(node, s)
                            )
                        )
            elif tag == TranslatorTags.RETURN_PARAMETERS:
                s.attributeDescriptor.setUInt8(1)
            elif tag == TranslatorTags.ACCESS_SELECTION:
                s.attributeDescriptor.setUInt8(1, s.attributeDescriptor.size - 1)
            elif tag == TranslatorTags.VALUE:
                pass
            elif tag == TranslatorTags.SERVICE:
                if s.attributeDescriptor.size == 0:
                    s.attributeDescriptor.setUInt8(s.parseShort(cls.getValue(node, s)))
                else:
                    s.attributeDescriptor.setUInt8(ServiceError.SERVICE)
                    s.attributeDescriptor.setUInt8(
                        Service.valueofString(cls.getValue(node, s)).value
                    )
            elif tag == TranslatorTags.ACCESS_SELECTOR:
                s.data.setUInt8(s.parseShort(cls.getValue(node, s)))
            elif tag == TranslatorTags.ACCESS_PARAMETERS:
                pass
            elif tag == TranslatorTags.ATTRIBUTE_DESCRIPTOR_LIST:
                _GXCommon.setObjectCount(cls.getNodeCount(node), s.attributeDescriptor)
            elif tag in (
                TranslatorTags.ATTRIBUTE_DESCRIPTOR_WITH_SELECTION,
                Command.ACCESS_REQUEST << 8 | AccessServiceCommandType.GET,
                Command.ACCESS_REQUEST << 8 | AccessServiceCommandType.SET,
                Command.ACCESS_REQUEST << 8 | AccessServiceCommandType.ACTION,
            ):
                if s.command != Command.SET_REQUEST:
                    s.attributeDescriptor.setUInt8(tag & 0xFF)
            elif tag in (
                Command.READ_REQUEST << 8 | VariableAccessSpecification.VARIABLE_NAME,
                Command.WRITE_REQUEST << 8 | VariableAccessSpecification.VARIABLE_NAME,
                Command.WRITE_REQUEST << 8 | SingleReadResponse.DATA,
            ):
                if s.command not in (Command.ACCESS_REQUEST, Command.ACCESS_RESPONSE):
                    if not (
                        s.outputType == TranslatorOutputType.STANDARD_XML
                        and tag
                        == (Command.WRITE_REQUEST << 8 | SingleReadResponse.DATA)
                    ):
                        if s.requestType == 0xFF:
                            s.attributeDescriptor.setUInt8(
                                VariableAccessSpecification.VARIABLE_NAME
                            )
                        else:
                            s.attributeDescriptor.setUInt8(s.requestType)
                            s.requestType = 0xFF
                        s.count = s.count + 1
                    elif s.command != Command.INFORMATION_REPORT:
                        s.attributeDescriptor.setUInt8(s.count)
                    if s.outputType == TranslatorOutputType.SIMPLE_XML:
                        s.attributeDescriptor.setUInt16(int(cls.getValue(node, s), 16))
                    else:
                        str_ = cls.getValue(node, s)
                        if str_:
                            s.attributeDescriptor.setUInt16(int(str_))
            elif tag == TranslatorTags.CHOICE:
                pass
            elif (
                tag == Command.READ_RESPONSE << 8 | SingleReadResponse.DATA_ACCESS_ERROR
            ):
                err = cls.value_ofErrorCode(s.outputType, cls.getValue(node, s))
                s.count = s.count + 1
                s.data.setUInt8(1)
                s.data.setUInt8(err)
            elif tag == TranslatorTags.NOTIFICATION_BODY:
                pass
            elif tag == TranslatorTags.DATA_VALUE:
                pass
            elif tag == TranslatorTags.ACCESS_REQUEST_BODY:
                pass
            elif tag == TranslatorTags.LIST_OF_ACCESS_REQUEST_SPECIFICATION:
                s.attributeDescriptor.setUInt8(cls.getNodeCount(node))
            elif tag == TranslatorTags.ACCESS_REQUEST_SPECIFICATION:
                pass
            elif tag == TranslatorTags.ACCESS_REQUEST_LIST_OF_DATA:
                s.attributeDescriptor.setUInt8(cls.getNodeCount(node))
            elif tag == TranslatorTags.ACCESS_RESPONSE_BODY:
                pass
            elif tag == TranslatorTags.LIST_OF_ACCESS_RESPONSE_SPECIFICATION:
                s.data.setUInt8(cls.getNodeCount(node))
            elif tag == TranslatorTags.ACCESS_RESPONSE_SPECIFICATION:
                pass
            elif tag == TranslatorTags.ACCESS_RESPONSE_LIST_OF_DATA:
                s.data.setUInt8(0)
                s.data.setUInt8(cls.getNodeCount(node))
            elif tag == TranslatorTags.SINGLE_RESPONSE:
                pass
            elif tag == TranslatorTags.SYSTEM_TITLE:
                tmp = GXByteBuffer.hexToBytes(cls.getValue(node, s))
                s.settings.sourceSystemTitle = tmp
            elif tag == TranslatorTags.CIPHERED_SERVICE:
                pass
            elif tag == Command.GLO_INITIATE_REQUEST:
                tmp = GXByteBuffer.hexToBytes(cls.getValue(node, s))
                if s.command == Command.GENERAL_CIPHERING:
                    _GXCommon.setObjectCount(len(tmp), s.data)
                elif s.command == Command.RELEASE_REQUEST:
                    s.data.setUInt8(0xBE)
                    _GXCommon.setObjectCount(4 + len(tmp), s.data)
                    s.data.setUInt8(4)
                    _GXCommon.setObjectCount(2 + len(tmp), s.data)
                    s.data.setUInt8(0x21)
                    _GXCommon.setObjectCount(len(tmp), s.data)
                s.data.set(tmp)
            elif tag == TranslatorTags.DATA_BLOCK:
                pass
            elif tag == TranslatorGeneralTags.USER_INFORMATION:
                tmp = GXByteBuffer.hexToBytes(cls.getValue(node, s))
                s.data.setUInt8(0xBE)
                s.data.setUInt8(len(tmp))
                s.data.setUInt8(0x4)
                s.data.setUInt8()
                s.data.set(tmp)
            elif tag == TranslatorTags.TRANSACTION_ID:
                tmp = GXByteBuffer.hexToBytes(cls.getValue(node, s))
                _GXCommon.setObjectCount(len(tmp), s.data)
                s.data.set(tmp)
            elif tag == TranslatorTags.ORIGINATOR_SYSTEM_TITLE:
                pass
            elif tag == TranslatorTags.RECIPIENT_SYSTEM_TITLE:
                pass
            elif tag == TranslatorTags.OTHER_INFORMATION:
                pass
            elif tag == TranslatorTags.KEY_CIPHERED_DATA:
                tmp = GXByteBuffer.hexToBytes(cls.getValue(node, s))
                _GXCommon.setObjectCount(len(tmp), s.data)
                s.data.set(tmp)
            elif tag == TranslatorTags.CIPHERED_CONTENT:
                tmp = GXByteBuffer.hexToBytes(cls.getValue(node, s))
                _GXCommon.setObjectCount(len(tmp), s.data)
                s.data.set(tmp)
            elif tag == TranslatorTags.KEY_INFO:
                s.data.setUInt8(1)
            elif tag == TranslatorTags.AGREED_KEY:
                s.data.setUInt8(2)
            elif tag == TranslatorTags.KEY_PARAMETERS:
                s.data.setUInt8(1)
                s.data.setUInt8(int(cls.getValue(node, s)))
            elif tag == TranslatorTags.ATTRIBUTE_VALUE:
                pass
            elif tag == TranslatorTags.MAX_INFO_TX:
                value = int(cls.getValue(node, s))
                if (s.command == Command.SNRM and not s.settings.isServer) or (
                    s.command == Command.UA and s.settings.isServer
                ):
                    s.settings.hdlc.setMaxInfoRX(int(value))
                s.data.setUInt8(_HDLCInfo.MAX_INFO_RX)
                s.data.setUInt8(1)
                s.data.setUInt8(int(value))
            elif tag == TranslatorTags.MAX_INFO_RX:
                value = int(cls.getValue(node, s))
                if (s.command == Command.SNRM and not s.settings.isServer) or (
                    s.command == Command.UA and s.settings.isServer
                ):
                    s.settings.hdlc.setMaxInfoTX(int(value))
                s.data.setUInt8(_HDLCInfo.MAX_INFO_TX)
                s.data.setUInt8(1)
                s.data.setUInt8(int(value))
            elif tag == TranslatorTags.WINDOW_SIZE_TX:
                value = int(cls.getValue(node, s))
                if (s.command == Command.SNRM and not s.settings.isServer) or (
                    s.command == Command.UA and s.settings.isServer
                ):
                    s.settings.hdlc.setWindowSizeRX(int(value))
                s.data.setUInt8(int(_HDLCInfo.WINDOW_SIZE_RX))
                s.data.setUInt8(4)
                s.data.setUInt32(value)
            elif tag == TranslatorTags.WINDOW_SIZE_RX:
                value = int(cls.getValue(node, s))
                if (s.command == Command.SNRM and not s.settings.isServer) or (
                    s.command == Command.UA and s.settings.isServer
                ):
                    s.settings.hdlc.setWindowSizeTX(int(value))
                s.data.setUInt8(_HDLCInfo.WINDOW_SIZE_TX)
                s.data.setUInt8(4)
                s.data.setUInt32(value)
            elif tag == Command.INITIATE_REQUEST:
                pass
            elif tag == TranslatorTags.VALUE_LIST:
                _GXCommon.setObjectCount(cls.getNodeCount(node), s.data)
            elif tag == TranslatorTags.DATA_ACCESS_RESULT:
                s.data.setUInt8(
                    cls.value_ofErrorCode(s.outputType, cls.getValue(node, s))
                )
            elif tag == TranslatorTags.WRITE_DATA_BLOCK_ACCESS:
                pass
            elif tag == TranslatorTags.FRAME_TYPE:
                pass
            elif tag == TranslatorTags.BLOCK_CONTROL:
                s.attributeDescriptor.setUInt8(s.parseShort(cls.getValue(node, s)))
            elif tag == TranslatorTags.BLOCK_NUMBER_ACK:
                s.attributeDescriptor.setUInt16(s.parseShort(cls.getValue(node, s)))
            elif tag == TranslatorTags.BLOCK_DATA:
                s.data.set(GXByteBuffer.hexToBytes(cls.getValue(node, s)))
            elif tag == TranslatorTags.CONTENTS_DESCRIPTION:
                cls.getNodeTypes(s, node)
                return
            elif tag == TranslatorTags.ARRAY_CONTENTS:
                if s.outputType == TranslatorOutputType.SIMPLE_XML:
                    cls.getNodeValues(s, node)
                else:
                    tmp = GXByteBuffer.hexToBytes(cls.getValue(node, s))
                    _GXCommon.setObjectCount(len(tmp), s.data)
                    s.data.set(tmp)
            elif tag == TranslatorTags.NETWORK_ID:
                s.setNetworkId(s.parseShort(cls.getValue(node, s)))
            elif tag == TranslatorTags.PHYSICAL_DEVICE_ADDRESS:
                s.setPhysicalDeviceAddress(
                    GXByteBuffer.hexToBytes(cls.getValue(node, s))
                )
                s.command = Command.NONE
            elif tag == TranslatorTags.STATE_ERROR:
                if s.outputType == TranslatorOutputType.SIMPLE_XML:
                    s.attributeDescriptor.setUInt8(
                        TranslatorSimpleTags.valueofStateError(cls.getValue(node, s))
                    )
                else:
                    s.attributeDescriptor.setUInt8(
                        TranslatorStandardTags.valueofStateError(cls.getValue(node, s))
                    )
            elif tag == TranslatorTags.SERVICE_ERROR:
                if s.outputType == TranslatorOutputType.SIMPLE_XML:
                    s.attributeDescriptor.setUInt8(
                        TranslatorSimpleTags.valueOfExceptionServiceError(
                            cls.getValue(node, s)
                        )
                    )
                else:
                    s.attributeDescriptor.setUInt8(
                        TranslatorStandardTags.valueOfExceptionServiceError(
                            cls.getValue(node, s)
                        )
                    )
            else:
                raise ValueError("Invalid node: " + node.tag)
        cnt = 0
        for node2 in node:
            cls.readNode(node2, s)
            cnt += 1
        if preData:
            _GXCommon.setObjectCount(cnt, preData)
            preData.set(s.data)
            s.data.size = 0
            s.data.set(preData)

    @classmethod
    def getNodeValues(cls, s, node):
        cnt = 1
        offset = 2
        if DataType(s.data.getUInt8(2)) == DataType.STRUCTURE:
            cnt = s.data.getUInt8(3)
            offset = 4
        types = bytearray(cnt)
        pos = 0
        while pos != cnt:
            types[pos] = DataType(s.data.getUInt8(offset + pos))
            pos += 1
        tmp = GXByteBuffer()
        tmp2 = GXByteBuffer()
        row = 0
        while row != node.getChildNodes().getLength():
            str_ = node.getChildNodes().item(row).getNodeValue()
            for r in str_.split("\n"):
                if r.strip() and not r == "\r":
                    col = 0
                    for it in r.strip().split(";"):
                        tmp.clear()
                        _GXCommon.setData(
                            None,
                            tmp,
                            types[len(types)],
                            GXDLMSConverter.changeType(it, types[len(types)]),
                        )
                        if len(tmp) == 1:
                            s.data.setUInt8(0)
                        else:
                            tmp2.set(tmp.subArray(1, len(tmp) - 1))
                        col += 1
            row += 1
        _GXCommon.setObjectCount(len(tmp2), s.data)
        s.data.set(tmp2)

    @classmethod
    def getNodeTypes(cls, s, node):
        len1 = cls.getNodeCount(node)
        if len1 > 1:
            s.data.setUInt8(DataType.STRUCTURE)
            _GXCommon.setObjectCount(len, s.data)
        for node2 in node:
            if s.outputType == TranslatorOutputType.SIMPLE_XML:
                str_ = node2.tag.lower()
            else:
                str_ = node2.tag
            tag = s.tags.get(str_)
            s.data.setUInt8(tag - _GXCommon.DATA_TYPE_OFFSET)

    @classmethod
    def updateDateTime(cls, node, s, preData):
        bb = preData
        if s.requestType != 0xFF:
            bb = cls.updateDataType(
                node, s, DataType.DATETIME + _GXCommon.DATA_TYPE_OFFSET
            )
        else:
            dt = DataType.DATETIME
            tmp = GXByteBuffer.hexToBytes(cls.getValue(node, s))
            if tmp:
                if len(tmp) == 5:
                    dt = DataType.DATE
                elif len(tmp) == 4:
                    dt = DataType.TIME
                s.setTime(_GXCommon.changeType(None, tmp, dt))
        return bb

    @classmethod
    def updateDataType(cls, node, s, tag):
        # pylint: disable=bad-option-value,redefined-variable-type
        preData = None
        v = cls.getValue(node, s)
        if s.template or v == "*":
            s.template = True
            return preData
        dt = DataType(tag - _GXCommon.DATA_TYPE_OFFSET)
        if dt == DataType.ARRAY:
            s.data.setUInt8(DataType.ARRAY)
            preData = GXByteBuffer(s.data)
            s.data.size = 0
        elif dt == DataType.BCD:
            _GXCommon.setData(
                None, s.data, DataType.BCD, s.parseShort(cls.getValue(node, s))
            )
        elif dt == DataType.BITSTRING:
            _GXCommon.setData(None, s.data, DataType.BITSTRING, cls.getValue(node, s))
        elif dt == DataType.BOOLEAN:
            _GXCommon.setData(
                None, s.data, DataType.BOOLEAN, s.parseShort(cls.getValue(node, s))
            )
        elif dt == DataType.DATE:
            _GXCommon.setData(
                None,
                s.data,
                DataType.DATE,
                _GXCommon.changeType(
                    None, GXByteBuffer.hexToBytes(cls.getValue(node, s)), DataType.DATE
                ),
            )
        elif dt == DataType.DATETIME:
            tmp = GXByteBuffer.hexToBytes(cls.getValue(node, s))
            if len(tmp) == 5:
                dt = DataType.DATE
            elif len(tmp) == 4:
                dt = DataType.TIME
            _GXCommon.setData(None, s.data, dt, _GXCommon.changeType(None, tmp, dt))
        elif dt == DataType.ENUM:
            _GXCommon.setData(
                None, s.data, DataType.ENUM, s.parseShort(cls.getValue(node, s))
            )
        elif dt == DataType.FLOAT32:
            cls.getFloat32(node, s)
        elif dt == DataType.FLOAT64:
            cls.getFloat64(node, s)
        elif dt == DataType.INT16:
            _GXCommon.setData(
                None, s.data, DataType.INT16, s.parseShort(cls.getValue(node, s))
            )
        elif dt == DataType.INT32:
            _GXCommon.setData(
                None, s.data, DataType.INT32, s.parseInt(cls.getValue(node, s))
            )
        elif dt == DataType.INT64:
            _GXCommon.setData(
                None, s.data, DataType.INT64, s.parseLong(cls.getValue(node, s))
            )
        elif dt == DataType.INT8:
            _GXCommon.setData(
                None, s.data, DataType.INT8, s.parseShort(cls.getValue(node, s))
            )
        elif dt == DataType.NONE:
            _GXCommon.setData(None, s.data, DataType.NONE, None)
        elif dt == DataType.OCTET_STRING:
            cls.getOctetString(node, s)
        elif dt == DataType.STRING:
            if s.showStringAsHex:
                _GXCommon.setData(
                    None,
                    s.data,
                    DataType.STRING,
                    GXByteBuffer.hexToBytes(cls.getValue(node, s)),
                )
            else:
                _GXCommon.setData(None, s.data, DataType.STRING, cls.getValue(node, s))
        elif dt == DataType.STRING_UTF8:
            if s.showStringAsHex:
                _GXCommon.setData(
                    None,
                    s.data,
                    DataType.STRING_UTF8,
                    GXByteBuffer.hexToBytes(cls.getValue(node, s)),
                )
            else:
                _GXCommon.setData(
                    None, s.data, DataType.STRING_UTF8, cls.getValue(node, s)
                )
        elif dt == DataType.STRUCTURE:
            s.data.setUInt8(DataType.STRUCTURE)
            preData = GXByteBuffer(s.data)
            s.data.size = 0
        elif dt == DataType.TIME:
            _GXCommon.setData(
                None,
                s.data,
                DataType.TIME,
                _GXCommon.changeType(
                    None, GXByteBuffer.hexToBytes(cls.getValue(node, s)), DataType.TIME
                ),
            )
        elif dt == DataType.UINT16:
            _GXCommon.setData(
                None, s.data, DataType.UINT16, s.parseShort(cls.getValue(node, s))
            )
        elif dt == DataType.UINT32:
            _GXCommon.setData(
                None, s.data, DataType.UINT32, s.parseLong(cls.getValue(node, s))
            )
        elif dt == DataType.UINT64:
            _GXCommon.setData(
                None, s.data, DataType.UINT64, s.parseLong(cls.getValue(node, s))
            )
        elif dt == DataType.UINT8:
            _GXCommon.setData(
                None, s.data, DataType.UINT8, s.parseShort(cls.getValue(node, s))
            )
        elif dt == DataType.COMPACT_ARRAY:
            s.data.setUInt8(dt.value)
        else:
            raise ValueError("Invalid node: " + node.tag)
        return preData

    @classmethod
    def getOctetString(cls, node, s):
        bb = GXByteBuffer()
        bb.setHexString(cls.getValue(node, s))
        _GXCommon.setData(None, s.data, DataType.OCTET_STRING, bb.array())

    @classmethod
    def getFloat32(cls, node, s):
        bb = GXByteBuffer()
        bb.setHexString(cls.getValue(node, s))
        _GXCommon.setData(None, s.data, DataType.FLOAT32, bb.getFloat())

    @classmethod
    def getFloat64(cls, node, s):
        bb = GXByteBuffer()
        bb.setHexString(cls.getValue(node, s))
        _GXCommon.setData(None, s.data, DataType.FLOAT64, bb.getDouble())

    def xmlToHexPdu(self, xml, addSpace=False):
        return GXByteBuffer.hex(self.xmlToPdu(xml, None), addSpace)

    def xmlToPdu(self, xml, settings=None):
        s = settings
        if s is None:
            s = GXDLMSXmlSettings(
                self.outputType, self.hex, self.showStringAsHex, self.tagsByName
            )

        tmp = ET.fromstring(xml)
        if tmp.tag == "{http://www.dlms.com/COSEMpdu}xDLMS-APDU":
            for it in tmp:
                tmp = it
                break
        self.readNode(tmp, s)
        bb = GXByteBuffer()
        ln = None
        sn = None
        if s.command == Command.INITIATE_REQUEST:
            _GXAPDU.getInitiateRequest(s.settings, bb)
        elif s.command == Command.INITIATE_RESPONSE:
            bb.set(_GXAPDU.getUserInformation(s.settings, s.settings.cipher))
        elif s.command in (
            Command.READ_REQUEST,
            Command.WRITE_REQUEST,
            Command.READ_RESPONSE,
            Command.WRITE_RESPONSE,
        ):
            sn = GXDLMSSNParameters(
                s.settings,
                s.command,
                s.count,
                s.requestType,
                s.attributeDescriptor,
                s.data,
            )
            GXDLMS.getSNPdu(sn, bb)
        elif s.command in (
            Command.GET_REQUEST,
            Command.GET_RESPONSE,
            Command.SET_REQUEST,
            Command.SET_RESPONSE,
            Command.METHOD_REQUEST,
            Command.METHOD_RESPONSE,
        ):
            ln = GXDLMSLNParameters(
                s.settings,
                0,
                s.command,
                s.requestType,
                s.attributeDescriptor,
                s.data,
                0xFF,
            )
            GXDLMS.getLNPdu(ln, bb)
        elif s.command in (
            Command.GLO_GET_REQUEST,
            Command.GLO_GET_RESPONSE,
            Command.GLO_SET_REQUEST,
            Command.GLO_SET_RESPONSE,
            Command.GLO_METHOD_REQUEST,
            Command.GLO_METHOD_RESPONSE,
            Command.GLO_READ_REQUEST,
            Command.GLO_WRITE_REQUEST,
            Command.GLO_READ_RESPONSE,
            Command.GLO_WRITE_RESPONSE,
            Command.DED_GET_REQUEST,
            Command.DED_GET_RESPONSE,
            Command.DED_SET_REQUEST,
            Command.DED_SET_RESPONSE,
            Command.DED_METHOD_REQUEST,
            Command.DED_METHOD_RESPONSE,
        ):
            bb.setUInt8(s.command)
            _GXCommon.setObjectCount(len(s.data), bb)
            bb.set(s.data)
        elif s.command == Command.UNACCEPTABLE_FRAME:
            pass
        elif s.command == Command.SNRM:
            s.settings.server = False
            if s.data:
                bb.setUInt8(0x81)
                bb.setUInt8(0x80)
                bb.setUInt8(len(s.data))
                bb.set(s.data)
                s.data.clear()
                s.data.set(bb)
                bb.clear()
            bb.set(GXDLMS.getHdlcFrame(s.settings, int(Command.SNRM), s.data))
        elif s.command == Command.UA:
            if s.data:
                bb.setUInt8(0x81)
                bb.setUInt8(0x80)
                bb.setUInt8(len(s.data))
                bb.set(s.data)
                s.data.clear()
                s.data.set(bb)
                bb.clear()
            bb.set(GXDLMS.getHdlcFrame(s.settings, s.command, s.data))
        elif s.command in (Command.AARQ, Command.GLO_INITIATE_REQUEST):
            _GXAPDU.generateAarq(s.settings, s.settings.cipher, s.data, bb)
        elif s.command in (Command.AARE, Command.GLO_INITIATE_RESPONSE):
            _GXAPDU.generateAARE(
                s.settings,
                bb,
                s.result,
                s.diagnostic,
                s.settings.cipher,
                s.attributeDescriptor,
                s.data,
            )
        elif s.command == Command.DISCONNECT_REQUEST:
            pass
        elif s.command == Command.RELEASE_REQUEST:
            bb.setUInt8(s.command)
            bb.setUInt8(3 + len(s.data))
            bb.setUInt8(BerType.CONTEXT)
            bb.setUInt8(1)
            bb.setUInt8(s.reason)
            if s.data.size == 0:
                bb.setUInt8(0)
            else:
                bb.set(s.data)
        elif s.command == Command.RELEASE_RESPONSE:
            bb.setUInt8(s.command)
            bb.setUInt8(3)
            bb.setUInt8(BerType.CONTEXT)
            bb.setUInt8(1)
            bb.setUInt8(s.reason)
        elif s.command in (Command.CONFIRMED_SERVICE_ERROR, Command.EXCEPTION_RESPONSE):
            bb.setUInt8(s.command)
            bb.set(s.attributeDescriptor)
        elif s.command == Command.EXCEPTION_RESPONSE:
            pass
        elif s.command == Command.GENERAL_BLOCK_TRANSFER:
            ln = GXDLMSLNParameters(
                s.settings,
                0,
                s.command,
                s.requestType,
                s.attributeDescriptor,
                s.data,
                0xFF,
                Command.NONE,
            )
            GXDLMS.getLNPdu(ln, bb)
        elif s.command == Command.ACCESS_REQUEST:
            ln = GXDLMSLNParameters(
                s.settings,
                0,
                s.command,
                s.requestType,
                s.attributeDescriptor,
                s.data,
                0xFF,
            )
            GXDLMS.getLNPdu(ln, bb)
        elif s.command == Command.ACCESS_RESPONSE:
            ln = GXDLMSLNParameters(
                s.settings,
                0,
                s.command,
                s.requestType,
                s.attributeDescriptor,
                s.data,
                0xFF,
            )
            GXDLMS.getLNPdu(ln, bb)
        elif s.command == Command.DATA_NOTIFICATION:
            ln = GXDLMSLNParameters(
                s.settings,
                0,
                s.command,
                s.requestType,
                s.attributeDescriptor,
                s.data,
                0xFF,
            )
            ln.time = s.time
            GXDLMS.getLNPdu(ln, bb)
        elif s.command == Command.INFORMATION_REPORT:
            sn = GXDLMSSNParameters(
                s.settings,
                s.command,
                s.count,
                s.requestType,
                s.attributeDescriptor,
                s.data,
            )
            sn.time = s.time
            GXDLMS.getSNPdu(sn, bb)
        elif s.command == Command.EVENT_NOTIFICATION:
            ln = GXDLMSLNParameters(
                s.settings,
                0,
                s.command,
                s.requestType,
                s.attributeDescriptor,
                s.data,
                0xFF,
            )
            ln.time = s.time
            GXDLMS.getLNPdu(ln, bb)
        elif s.command == Command.GENERAL_GLO_CIPHERING:
            bb.setUInt8(s.command)
            _GXCommon.setObjectCount(len(s.settings.sourceSystemTitle), bb)
            bb.set(s.settings.sourceSystemTitle)
            _GXCommon.setObjectCount(len(s.data), bb)
            bb.set(s.data)
        elif s.command == Command.GENERAL_CIPHERING:
            bb.setUInt8(s.command)
            bb.set(s.data)
        elif s.command == Command.GLO_EVENT_NOTIFICATION:
            pass
        else:
            raise ValueError("Invalid command.")
        if s.physicalDeviceAddress:
            bb2 = GXByteBuffer()
            bb2.setUInt8(s.gwCommand)
            bb2.setUInt8(s.networkId)
            _GXCommon.setObjectCount(len(s.physicalDeviceAddress), bb2)
            bb2.set(s.physicalDeviceAddress)
            bb2.set(bb)
            return bb2
        return bb

    def dataToXml(self, data):
        di = _GXDataInfo()
        xml = GXDLMSTranslatorStructure(
            self.outputType,
            self.omitXmlNameSpace,
            self.hex,
            self.showStringAsHex,
            self.comments,
            self.tags,
        )
        di.xml = xml
        _GXCommon.getData(None, data, di)
        return str(di.xml)

    def __getAllDataNodes(self, nodes, s):
        preData = None
        tag = int()
        for it in nodes:
            if s.outputType == TranslatorOutputType.SIMPLE_XML:
                tag = s.tags.get(it.tag.tolower())
            else:
                tag = s.tags.get(it.tag)
            if tag == TranslatorTags.RAW_DATA:
                s.data.setHexString(it.value)
            else:
                preData = self.updateDataType(it, s, tag)
                if preData:
                    _GXCommon.setObjectCount(it.getChildNodes().getLength(), preData)
                    preData.set(s.data)
                    s.data.size(0)
                    s.data.set(preData)
                    self.__getAllDataNodes(it.getChildNodes(), s)

    def XmlToData(self, xml):
        s = GXDLMSXmlSettings(
            self.outputType, self.hex, self.showStringAsHex, self.tagsByName
        )
        self.__getAllDataNodes(ET.fromstring(xml).iter(), s)
        return s.data

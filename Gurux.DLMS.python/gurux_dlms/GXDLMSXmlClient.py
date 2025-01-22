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
import xml.etree.cElementTree as ET
from .secure.GXDLMSSecureClient import GXDLMSSecureClient
from .enums import InterfaceType, Command, DataType
from .GXDLMS import GXDLMS
from .internal._GXCommon import _GXCommon
from .GXByteBuffer import GXByteBuffer
from .GXDLMSLNParameters import GXDLMSLNParameters
from .GXDLMSXmlSettings import GXDLMSXmlSettings
from .GXDLMSTranslator import GXDLMSTranslator
from .enums.Security import Security
from .GXDLMSXmlPdu import GXDLMSXmlPdu
from .enums.TranslatorOutputType import TranslatorOutputType

class GXDLMSXmlClient(GXDLMSSecureClient):
    """
    GXDLMS Xml client implements methods to communicate with DLMS/COSEM metering
    devices using XML.
    """

    #
    # Constructor
    #
    # @param type
    #            XML type.
    #
    def __init__(self, type_ = TranslatorOutputType.SIMPLE_XML):
        GXDLMSSecureClient.__init__(self)
        # XML client don't throw exceptions. It serializes them as a default. Set
        # value to true, if exceptions are thrown.
        #
        self.throwExceptions = False
        self.translator = GXDLMSTranslator(type_)
        self.translator.hex = False
        self.useLogicalNameReferencing = True


    @classmethod
    def removeRecursively(cls, node, nodeType, name):
        if node.getNodeType() == nodeType and (name is None or node.tag == name):
            node.getParentNode().removeChild(node)
        else:
            #  check the children recursively
            list_ = node.getChildNodes()
            i = 0
            while i < list_.getLength():
                cls.removeRecursively(list_.item(i), nodeType, name)
                i += 1

    #
    # Load XML commands from the string or file.
    #
    # @param filename
    #            XML file name.
    # @param settings
    #            Load settings.
    # Loaded XML objects.
    # pylint: disable=too-many-locals,too-many-nested-blocks
    def load(self, filename, loadSettings = None):
        tree = ET.parse(filename)
        root = tree.getroot()
        actions = []
        description = None
        error = None
        errorUrl = None
        sleep = None
        for node in root:
            if node.tag == "Description":
                description = node.text
                continue
            if node.tag == "Error":
                error = node.text
                continue
            if node.tag == "ErrorUrl":
                errorUrl = node.text
                continue
            if node.tag == "Sleep":
                sleep = node.text
                continue
            if loadSettings and node.tag == "GetRequest":
                structure = node.find("./GetRequestNormal/AccessSelection/AccessSelector/AccessParameters/Structure")
                if structure:
                    start = False
                    for node2 in structure:
                        if start:
                            bb = GXByteBuffer()
                            if start:
                                _GXCommon.setData(self.settings, bb, DataType.OCTET_STRING, loadSettings.start)
                                node2.attrib["Value"] = bb.toHex(False, 2)
                                start = False
                            else:
                                _GXCommon.setData(self.settings, bb, DataType.OCTET_STRING, loadSettings.end)
                                node2.attrib["Value"] = bb.toHex(False, 2)

            s = GXDLMSXmlSettings(self.translator.outputType, self.translator.hex, self.translator.showStringAsHex, self.translator.tagsByName)
            s.settings.clientAddress = self.settings.clientAddress
            s.settings.serverAddress = self.settings.serverAddress
            reply = []
            reply = self.translator.xmlToPdu(GXDLMSXmlPdu.getOuterXml(node), s)
            if s.command == Command.SNRM and not s.settings.isServer:
                self.settings.hdlc.maxInfoTX = s.settings.hdlc.maxInfoTX
                self.settings.hdlc.maxInfoRX = s.settings.hdlc.maxInfoRX
                self.settings.hdlc.windowSizeRX = s.settings.hdlc.windowSizeRX
                self.settings.hdlc.windowSizeTX = s.settings.hdlc.windowSizeTX
            elif s.command == Command.UA and s.settings.isServer:
                self.settings.hdlc.maxInfoTX = s.settings.hdlc.maxInfoTX
                self.settings.hdlc.maxInfoRX = s.settings.hdlc.maxInfoRX
                self.settings.hdlc.windowSizeRX = s.settings.hdlc.windowSizeRX
                self.settings.hdlc.windowSizeTX = s.settings.hdlc.windowSizeTX
            if s.template:
                reply = None
            p = GXDLMSXmlPdu(s.command, node, reply)
            if description:
                p.description = description
            if error:
                p.error = error
            if errorUrl:
                p.errorUrl = errorUrl
            if sleep:
                p.sleep = int(sleep)
            actions.append(p)
        return actions

    def pduToMessages(self, pdu):
        self.settings.command = pdu.command
        messages = []
        if pdu.command == Command.SNRM:
            messages.append(pdu.data)
        elif pdu.command == Command.UA:
            messages.append(pdu.data)
        elif pdu.command == Command.DISCONNECT_REQUEST:
            messages.append(GXDLMS.getHdlcFrame(self.settings, int(Command.DISCONNECT_REQUEST), GXByteBuffer(pdu.data)))
        else:
            reply = None
            if self.settings.interfaceType == InterfaceType.WRAPPER:
                if self.ciphering.security != Security.NONE:
                    p = GXDLMSLNParameters(self.settings, 0, pdu.command, 0x0, None, None, 0xff)
                    reply = GXByteBuffer(GXDLMS.cipher0(p, pdu.data))
                else:
                    reply = GXByteBuffer(pdu.data)
            else:
                if self.ciphering.security != Security.NONE:
                    p = GXDLMSLNParameters(self.settings, 0, pdu.command, 0x0, None, None, 0xff)
                    tmp = GXDLMS.cipher0(p, pdu.data)
                    reply = GXByteBuffer(len(tmp))
                    reply.set(_GXCommon.LLC_SEND_BYTES)
                    reply.set(tmp)
                else:
                    reply = GXByteBuffer(len(pdu.data))
                    reply.set(_GXCommon.LLC_SEND_BYTES)
                    reply.set(pdu.data)
            frame_ = 0
            while reply.position != len(reply):
                if self.settings.interfaceType == InterfaceType.WRAPPER:
                    messages.append(GXDLMS.getWrapperFrame(self.settings, pdu.command, reply))
                elif self.settings.interfaceType == InterfaceType.HDLC or self.settings.interfaceType == InterfaceType.HDLC_WITH_MODE_E:
                    if pdu.command == Command.AARQ:
                        frame_ = 0x10
                    elif pdu.command == Command.AARE:
                        frame_ = 0x30
                    elif pdu.command == Command.EVENT_NOTIFICATION:
                        frame_ = 0x13
                    messages.append(GXDLMS.getHdlcFrame(self.settings, frame_, reply))
                    if reply.position != len(reply):
                        frame_ = self.settings.getNextSend(False)
                elif self.settings.interfaceType == InterfaceType.PDU:
                    messages.append(reply.array())
                    break
                else:
                    raise ValueError("InterfaceType")
        return messages

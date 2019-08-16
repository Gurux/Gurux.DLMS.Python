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
from .enums.Command import Command
# pylint: disable=bad-option-value,old-style-class
class GXDLMSXmlPdu:
    #pylint: disable=too-many-instance-attributes
    def __init__(self, command=0, xml=None, pdu=None):
        # XML Node.
        self.xmlNode = xml
        # Command.
        self.command = command
        # Description of the test.
        self.description = None
        # Shown error if this test fails.
        self.error = None
        # Error url if test fails.
        self.errorUrl = None
        # Generated Pdu.
        self.data = pdu
        # Sleep time in milliseconds.
        self.privateSleep = 0

    @classmethod
    def getOuterXml(cls, node):
        return ""

    #
    # Return PDU as XML string.
    #
    def getPduAsXml(self):
        if self.xmlNode is None:
            return ""
        return self.getOuterXml(self.xmlNode)

    @classmethod
    def compare(cls, expectedNode, actualNode, list_):
        cnt = expectedNode.getChildNodes().getLength()
        if expectedNode.getNodeName().compareTo(actualNode.getNodeName()) != 0:
            a = expectedNode.getAttributes().getNamedItem("Value")
            if expectedNode.getNodeName().compareTo("None") == 0 and a and a.getNodeValue().compareTo("*") == 0:
                return
            list_.append(expectedNode.getNodeName() + "-" + actualNode.getNodeName())
            return
        if cnt != actualNode.getChildNodes().getLength():
            #  If we are reading array items count might vary.
            if expectedNode.getNodeName() == "Array" or expectedNode.getNodeName() == "Structure":
                #  Check only first If meter is returning more nodes what
                #  wehave in template.
                if not cnt < actualNode.getChildNodes().getLength():
                    cnt = actualNode.getChildNodes().getLength()
            else:
                list_.append("Different amount: " + expectedNode.getNodeName() + "-" + actualNode.getNodeName())
                return
        pos = 0
        while pos != cnt:
            if actualNode.getChildNodes().item(pos) is None:
                list_.append("Different values. Expected: '" + expectedNode.getChildNodes().item(pos).getNodeValue() + "'. Actual: 'null'.")
            elif actualNode.getChildNodes().item(pos).getChildNodes().getLength() != 0:
                cls.compare(expectedNode.getChildNodes().item(pos), actualNode.getChildNodes().item(pos), list_)
            elif expectedNode.getChildNodes().item(pos).getNodeValue().compareTo(actualNode.getChildNodes().item(pos).getNodeValue()) != 0:
                a = expectedNode.getChildNodes().item(pos).getAttributes().getNamedItem("Value")
                if a is None or (expectedNode.getChildNodes().item(pos).getNodeName().compareTo("None") != 0 and expectedNode.getChildNodes().item(pos).getNodeName().compareTo(actualNode.getChildNodes().item(pos).getNodeName()) != 0) or a.getNodeValue().compareTo("*") != 0:
                    if not expectedNode.getFirstChild().getNodeName() == "Structure" and not expectedNode.getFirstChild().getNodeName() == "Array" and not expectedNode.getParentNode().getNodeName() == "Array":
                        list_.append("Different values. Expected: '" + expectedNode.getChildNodes().item(pos).getNodeValue() + "'. Actual: '" + actualNode.getChildNodes().item(pos).getNodeValue() + "'.")
            pos += 1

    def isRequest(self):
        return self.command in (Command.SNRM, Command.AARQ, Command.READ_REQUEST, Command.GLO_READ_REQUEST,\
            Command.WRITE_REQUEST, Command.GLO_WRITE_REQUEST, Command.GET_REQUEST, Command.GLO_GET_REQUEST,\
            Command.SET_REQUEST, Command.GLO_SET_REQUEST, Command.METHOD_REQUEST, Command.GLO_METHOD_REQUEST,\
            Command.DISCONNECT_REQUEST, Command.RELEASE_REQUEST)

    def __str__(self):
        return self.getPduAsXml()

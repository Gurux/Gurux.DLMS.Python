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
#
from .enums.TranslatorOutputType import TranslatorOutputType
from .internal._GXCommon import _GXCommon
# pylint: disable=too-many-arguments, too-many-instance-attributes
class GXDLMSTranslatorStructure:
    """
    This class is used internally in GXDLMSTranslator to save generated XML.
    """

    def setOffset(self, value):
        """
        Amount of spaces.
        """
        if value < 0:
            raise ValueError("offset")
        self.offset = value

    #
    # Constructor.
    #
    # @param list
    #            List of tags.
    #
    def __init__(self, type_, numericsAshex, numericshex, isHex, addComments, list_):
        self.sb = ""
        self.tags = None
        self.outputType = None
        # Are numeric values shows as hex.
        self.showNumericsAsHex = False
        # Amount of spaces.
        self.offset = 0
        self.outputType = type_
        numericsAshex = numericshex
        self.showNumericsAsHex = numericsAshex
        self.showStringAsHex = isHex
        self.tags = list_
        # Are comments added.
        self.comments = addComments
        self.omitNameSpace = False

    def __str__(self):
        return str(self.sb)

    def getDataType(self, type_):
        return self.__getTag(_GXCommon.DATA_TYPE_OFFSET + type_)

    def __getTag(self, tag):
        if self.outputType == TranslatorOutputType.SIMPLE_XML or self.omitNameSpace:
            return self.tags.get(tag)
        return "x:" + self.tags.get(tag)

    #
    # Append spaces to the buffer.
    #
    # @param count
    #            Amount of spaces.
    #
    def appendSpaces(self, count):
        pos = 0
        while pos != count:
            self.sb += ' '
            pos += 1

    def appendLine(self, tag, name=None, value=None):
        self.appendSpaces(2 * self.offset)
        if name is None and value is None:
            self.sb += tag
        else:
            self.sb += '<'
            if isinstance(tag, int):
                tag = self.__getTag(tag)
            self.sb += tag
            if self.outputType == TranslatorOutputType.SIMPLE_XML:
                self.sb += ' '
                if name is None:
                    self.sb += "Value"
                else:
                    self.sb += name
                self.sb += "=\""
            else:
                self.sb += '>'
            self.sb += value
            if self.outputType == TranslatorOutputType.SIMPLE_XML:
                self.sb += "\" />"
            else:
                self.sb += "</"
                self.sb += tag
                self.sb += '>'
        self.sb += '\r'
        self.sb += '\n'

    #
    # Append comment.
    #
    # @param comment
    #            Comment to add.
    #
    def appendComment(self, comment):
        if self.comments:
            self.appendSpaces(2 * self.offset)
            self.sb += "<!--"
            self.sb += comment
            self.sb += "-->"
            self.sb += '\r'
            self.sb += '\n'

    #
    # Start comment section.
    #
    # @param comment
    #            Comment to add.
    #
    def startComment(self, comment):
        if self.comments:
            self.appendSpaces(2 * self.offset)
            self.sb += "<!--"
            self.sb += comment
            self.sb += '\r'
            self.sb += '\n'
            self.offset += 1

    #
    # End comment section.
    #
    def endComment(self):
        if self.comments:
            self.offset -= 1
            self.appendSpaces(2 * self.offset)
            self.sb += "-->"
            self.sb += '\r'
            self.sb += '\n'

    def append(self, tag, start=None):
        if isinstance(tag, str):
            self.sb += tag
            return
        if start:
            self.appendSpaces(2 * self.offset)
            self.sb += '<'
        else:
            self.sb += "</"
        self.sb += self.__getTag(tag)
        self.sb += '>'

    def appendStartTag(self, tag, name=None, value=None, plain=False):
        if isinstance(name, int):
            tag = self.__getTag(tag << 8 | name)
            name = None
        elif isinstance(tag, int):
            tag = self.__getTag(tag)
        self.appendSpaces(2 * self.offset)
        self.sb += '<'
        self.sb += tag
        if self.outputType == TranslatorOutputType.SIMPLE_XML and name:
            self.sb += ' '
            self.sb += name
            self.sb += "=\""
            self.sb += value
            self.sb += "\" >"
        else:
            self.sb += '>'
        if not plain:
            self.sb += '\r'
            self.sb += '\n'
        self.offset += 1

    def appendEndTag(self, tag, plain=False):
        if isinstance(tag, int):
            if not isinstance(plain, bool) and (isinstance(plain, int)):
                tag = self.__getTag(tag << 8 | plain)
            else:
                tag = self.__getTag(tag)
        self.setOffset(self.offset - 1)
        if not isinstance(plain, bool) or not plain:
            self.appendSpaces(2 * self.offset)
        self.sb += "</"
        self.sb += tag
        self.sb += '>'
        self.sb += '\r'
        self.sb += '\n'

    def appendEmptyTag(self, tag):
        if isinstance(tag, int):
            tag = self.__getTag(tag)
        self.appendSpaces(2 * self.offset)
        self.sb += "<"
        self.sb += tag
        self.sb += '/'
        self.sb += '>'
        self.sb += '\r'
        self.sb += '\n'

    def trim(self):
        """
        Remove \r\n.
        """
        self.sb = self.sb[:-2]

    def getXmlLength(self):
        """
        XML Length.
        """
        return len(self.sb)

    def setXmlLength(self, value):
        """
        Set XML Length.
        """
        self.sb = self.sb[0:value]

    #
    # Convert integer to string.
    #
    # @param value
    #            Converted value.
    # @param desimals
    #            Amount of decimals.
    # @param forceHex
    #            Force value as hex.
    # Integer as string.
    #
    def integerToHex(self, value, desimals, forceHex=False):
        if forceHex or (self.showNumericsAsHex and self.outputType == TranslatorOutputType.SIMPLE_XML):
            return _GXCommon.integerToHex(value, desimals)
        return str(value)

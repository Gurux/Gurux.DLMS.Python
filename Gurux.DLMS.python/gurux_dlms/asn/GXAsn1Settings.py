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
#  Gurux Device Framework is Open Source software you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http:#www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http:#www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------

from gurux_dlms.enums.BerType import BerType


class GXAsn1Settings:
    __count = 0

    __comments = None
    """
    Are comments used.
    """

    __sb = ""

    __tags = {}

    __tagbyName = {}

    @property
    def comments(self):
        """
        Are comments used.
        """
        return self.__comments

    @comments.setter
    def comments(self, value):
        self.__comments = value

    @property
    def xmlLength(self):
        return len(self.__sb)

    def __init__(self):
        """
        Constructor.
        """

        self.__addTag(BerType.APPLICATION, "Application")
        self.__addTag((BerType.CONSTRUCTED | BerType.CONTEXT), "Context")
        self.__addTag(
            ((BerType.CONSTRUCTED | BerType.CONTEXT | 1)),
            "Constructed-Context-Specific-1",
        )
        self.__addTag(
            ((BerType.CONSTRUCTED | BerType.CONTEXT | 2)),
            "Constructed-Context-Specific-2",
        )
        self.__addTag(
            ((BerType.CONSTRUCTED | BerType.CONTEXT | 3)),
            "Constructed-Context-Specific-3",
        )
        self.__addTag((BerType.CONSTRUCTED | BerType.SEQUENCE), "Sequence")
        self.__addTag((BerType.CONSTRUCTED | BerType.SET), "Set")
        self.__addTag(BerType.OBJECT_IDENTIFIER, "ObjectIdentifier")
        self.__addTag(BerType.PRINTABLE_STRING, "String")
        self.__addTag(BerType.UTF8STRING, "UTF8")
        self.__addTag(BerType.IA5_STRING, "IA5")
        self.__addTag(BerType.INTEGER, "Integer")
        self.__addTag(BerType.NULL, "Null")
        self.__addTag(BerType.BIT_STRING, "BitString")
        self.__addTag(BerType.UTC_TIME, "UtcTime")
        self.__addTag(BerType.GENERALIZED_TIME, "GeneralizedTime")
        self.__addTag(BerType.OCTET_STRING, "OctetString")
        self.__addTag(BerType.BOOLEAN, "Bool")
        self.__addTag(-1, "Byte")
        self.__addTag(-2, "Short")
        self.__addTag(-4, "Int")
        self.__addTag(-8, "Long")

    def __addTag(self, key, value):
        self.__tags[key] = value
        self.__tagbyName[value.lower()] = key

    def getTag(self, value):
        if isinstance(value, str):
            return self.__tagbyName[value]
        return self.__tags[value]

    # pylint: disable=unused-variable
    def appendComment(self, offset, value):
        """
        Add comment.

            Parameters:
                offset: Offset.
                value: Comment value.
        """
        if self.comments:
            empty_ = len(self.__sb) == 0
            if empty_:
                tmp = self.__sb
            else:
                tmp = ""

            for pos in range(0, self.__count - 1):
                tmp += " "
            tmp += "<!--"
            tmp += value
            tmp += "-->\r\n"
            if not empty_:
                self.__sb = self.__sb[:offset] + tmp + self.__sb[offset:]

    # pylint: disable=unused-variable
    def appendSpaces(self):
        """
        Append spaces to the buffer.
        """
        for pos in range(0, self.__count - 1):
            __sb += " "

    def append(self, value):
        self.__sb += value

    def increase(self):
        self.__count += 1
        self.append("\r\n")

    def decrease(self):
        self.__count -= 1
        self.appendSpaces()

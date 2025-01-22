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
#  More information of Gurux products: http:#www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http:#www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
from .enums.ProtectionType import ProtectionType
from .GXDLMSDataProtectionKey import GXDLMSDataProtectionKey

class GXPushProtectionParameters:
    """
    Push protection parameters.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.__keyInfo = GXDLMSDataProtectionKey()
        self.__protectionType = ProtectionType.AUTHENTICATION
        self.__transactionId = bytearray()
        self.__originatorSystemTitle = bytearray()
        self.__recipientSystemTitle = bytearray()
        self.__otherInformation = bytearray()

    @property
    def protectionType(self):
        """
        Protection type.
        """
        return self.__protectionType

    @protectionType.setter
    def protectionType(self, value):
        self.__protectionType = value

    @property
    def transactionId(self):
        """
        Transaction Id.
        """
        return self.__transactionId

    @transactionId.setter
    def transactionId(self, value):
        self.__transactionId = value

    @property
    def originatorSystemTitle(self):
        """
        Originator system title.
        """
        return self.__originatorSystemTitle

    @originatorSystemTitle.setter
    def originatorSystemTitle(self, value):
        self.__originatorSystemTitle = value

    @property
    def recipientSystemTitle(self):
        """
        Recipient system title.
        """
        return self.__recipientSystemTitle

    @recipientSystemTitle.setter
    def recipientSystemTitle(self, value):
        self.__recipientSystemTitle = value

    @property
    def otherInformation(self):
        """
        Other information.
        """
        return self.__otherInformation

    @otherInformation.setter
    def otherInformation(self, value):
        self.__otherInformation = value

    @property
    def keyInfo(self):
        """
        Key info.
        """
        return self.__keyInfo

    @keyInfo.setter
    def keyInfo(self, value):
        self.__keyInfo = value

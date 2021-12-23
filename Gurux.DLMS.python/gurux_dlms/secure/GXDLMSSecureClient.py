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
from ..enums import InterfaceType, Authentication
from ..GXDLMSClient import GXDLMSClient
from ..GXCiphering import GXCiphering
from ..GXDLMSChipperingStream import GXDLMSChipperingStream

#pylint: disable=too-many-arguments
class GXDLMSSecureClient(GXDLMSClient):
    """
    GXDLMSSecureClient implements secure client where all messages are secured
    using transport security.
    """

    #
    # Constructor.
    #      *
    # @param useLogicalNameReferencing
    #            Is Logical Name referencing used.
    # @param clientAddress
    #            Server address.
    # @param serverAddress
    #            Client address.
    # @param forAuthentication
    #            Authentication type.
    # @param password
    #            Password if authentication is used.
    # @param interfaceType
    #            Object type.
    #
    def __init__(self, useLogicalNameReferencing=False, clientAddress=16, serverAddress=1, forAuthentication=Authentication.NONE, password=None, interfaceType=InterfaceType.HDLC):
        GXDLMSClient.__init__(self, useLogicalNameReferencing, clientAddress, serverAddress, forAuthentication, password, interfaceType)
        # Ciphering settings.
        self.settings.cipher = GXCiphering("ABCDEFGH".encode())

    #
    # Encrypt data using Key Encrypting Key.
    #      *
    # @param kek
    #            Key Encrypting Key, also known as Master key.
    # @param data
    #            Data to encrypt.
    # @return Encrypt data.
    #
    @classmethod
    def encrypt(cls, kek, data):
        if len(kek) != 16:
            raise ValueError("Key Encrypting Key")
        if not data:
            raise ValueError("data")
        gcm = GXDLMSChipperingStream(None, True, kek, None, None, 0)
        return gcm.encryptAes(data)

    #
    # Decrypt data using Key Encrypting Key.
    #      *
    # @param kek
    #            Key Encrypting Key, also known as Master key.
    # @param data
    #            Data to decrypt.
    # @return Decrypted data.
    #
    @classmethod
    def decrypt(cls, kek, data):
        if len(kek) != 16:
            raise ValueError("Key Encrypting Key")
        if not data:
            raise ValueError("data")
        gcm = GXDLMSChipperingStream(None, False, kek, None, None, 0)
        return gcm.decryptAes(data)

    def getSecuritySuite(self):
        return self.ciphering.securitySuite

    def setSecuritySuite(self, value):
        self.ciphering.securitySuite = value

    # Used security suite.
    securitySuite = property(getSecuritySuite, setSecuritySuite)

    def getServerSystemTitle(self):
        return self.settings.preEstablishedSystemTitle

    def setServerSystemTitle(self, value):
        self.settings.preEstablishedSystemTitle = value

    # Server system title.
    serverSystemTitle = property(getServerSystemTitle, setServerSystemTitle)

    def getCiphering(self):
        return self.settings.cipher

    # Ciphering.
    ciphering = property(getCiphering)

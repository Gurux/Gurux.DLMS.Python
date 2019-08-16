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
from abc import ABCMeta, abstractmethod

ABC = ABCMeta('ABC', (object,), {'__slots__': ()})

# pylint: disable=too-many-public-methods
class GXICipher(ABC):
    #
    # Reset encrypt settings.
    #
    @abstractmethod
    def reset(self):
        raise ValueError("abstract method is called.")

    # Is ciphering used.
    @abstractmethod
    def isCiphered(self):
        raise ValueError("abstract method is called.")

    #
    # Used security.
    #
    @abstractmethod
    def getSecurity(self):
        raise ValueError("abstract method is called.")

    #
    # @param value
    #            Used security.
    #
    @abstractmethod
    def setSecurity(self, value):
        raise ValueError("abstract method is called.")

    #
    # System title.
    #
    @abstractmethod
    def getSystemTitle(self):
        raise ValueError("abstract method is called.")

    #
    # Recipient system Title.
    #
    @abstractmethod
    def getRecipientSystemTitle(self):
        raise ValueError("abstract method is called.")

    #
    # Block cipher key.
    #
    @abstractmethod
    def getBlockCipherKey(self):
        raise ValueError("abstract method is called.")

    #
    # Authentication key.
    #
    @abstractmethod
    def getAuthenticationKey(self):
        raise ValueError("abstract method is called.")

    #
    # @param value
    #            Authentication key.
    #
    @abstractmethod
    def setAuthenticationKey(self, value):
        raise ValueError("abstract method is called.")

    #
    # Invocation counter.
    #
    @abstractmethod
    def getInvocationCounter(self):
        raise ValueError("abstract method is called.")

    #
    # Used security suite.
    #
    @abstractmethod
    def getSecuritySuite(self):
        raise ValueError("abstract method is called.")

    #
    # Ephemeral key pair.
    #
    @abstractmethod
    def getEphemeralKeyPair(self):
        raise ValueError("abstract method is called.")

    #
    # @param value
    #            Ephemeral key pair.
    #
    @abstractmethod
    def setEphemeralKeyPair(self, value):
        raise ValueError("abstract method is called.")

    #
    # Client's key agreement key pair.
    #
    @abstractmethod
    def getKeyAgreementKeyPair(self):
        raise ValueError("abstract method is called.")

    #
    # @param value
    #            Client's key agreement key pair.
    #
    @abstractmethod
    def setKeyAgreementKeyPair(self, value):
        raise ValueError("abstract method is called.")

    #
    # Target (Server or client) Public key.
    #
    @abstractmethod
    def getPublicKeys(self):
        raise ValueError("abstract method is called.")

    #
    # Available certificates.
    #
    @abstractmethod
    def getCertificates(self):
        raise ValueError("abstract method is called.")

    #
    # Signing key pair.
    #
    @abstractmethod
    def getSigningKeyPair(self):
        raise ValueError("abstract method is called.")

    #
    # @param value
    #            Signing key pair.
    #
    @abstractmethod
    def setSigningKeyPair(self, value):
        raise ValueError("abstract method is called.")

    #
    # Shared secret is generated when connection is made.
    #
    @abstractmethod
    def getSharedSecret(self):
        raise ValueError("abstract method is called.")

    #
    # @param value
    #            Shared secret is generated when connection is made.
    #
    @abstractmethod
    def setSharedSecret(self, value):
        raise ValueError("abstract method is called.")

    #
    # Dedicated key.
    #
    @abstractmethod
    def getDedicatedKey(self):
        raise ValueError("abstract method is called.")

    #
    # @param value
    #            Dedicated key.
    #
    @abstractmethod
    def setDedicatedKey(self, value):
        raise ValueError("abstract method is called.")

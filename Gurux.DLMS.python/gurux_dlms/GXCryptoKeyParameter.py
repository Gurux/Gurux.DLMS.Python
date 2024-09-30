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
from .enums.CryptoKeyType import CryptoKeyType
from .enums.Security import Security
from .objects.enums.SecuritySuite import SecuritySuite
from .objects.enums.SecurityPolicy import SecurityPolicy
from .objects.enums.CertificateType import CertificateType


# pylint: disable=too-many-instance-attributes,too-few-public-methods
class GXCryptoKeyParameter:
    def __init__(self):
        self.command = 0
        # Crypto key type.
        self.keyType = CryptoKeyType.BLOCK_CIPHER
        # Is data encrypted or decrypted.
        self.encrypt = False
        # Encrypted data.
        self.encrypted = None
        # Decrypted data.
        self.plainText = None
        # Used security.
        self.security = Security.NONE
        # Used security suite.
        self.securitySuite = SecuritySuite.SUITE_0
        # Used security policy.
        self.securityPolicy = SecurityPolicy.NOTHING
        # Used certificate type.
        self.certificateType = CertificateType.DIGITAL_SIGNATURE
        # System title
        self.systemTitle = None
        # Recipient system title.
        self.recipientSystemTitle = None
        # Block cipher key.
        self.blockCipherKey = None
        # Authentication key.
        self.authenticationKey = None
        # Frame counter. Invocation counter.
        self.invocationCounter = 0
        # Transaction Id.
        self.transactionId = None
        # key to used to encrypt the data.
        self.privateKey = None
        # Public key to used to decrypt the data.
        self.publicKey = None

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
from .enums.Security import Security
from .objects.enums.SecuritySuite import SecuritySuite
from .CountType import CountType

 # pylint: disable=too-many-instance-attributes
class AesGcmParameter:
    def __init__(self, tag=0, systemTitle=None, blockCipherKey=None, authenticationKey=None):
        """
        Constructor.

        tag : Tag.
        systemTitle : System title.
        blockCipherKey : Block cipher key.
        authenticationKey : Authentication key.
        """
        self.tag = tag
        self.security = Security.NONE
        # Invocation counter.
        self.invocationCounter = 0
        # Used security suite.
        self.securitySuite = SecuritySuite.AES_GCM_128
        # Block cipher key.
        self.blockCipherKey = blockCipherKey
        # Authentication key.
        self.authenticationKey = authenticationKey
        # System title.
        self.systemTitle = systemTitle
        # Recipient system title.
        self.recipientSystemTitle = None
        # Count type.
        self.type_ = CountType.PACKET
        # Date time.
        self.dateTime = None
        # Other information.
        self.otherInformation = None
        # Counted tag.
        self.countTag = None
        # Key parameters.
        self.keyParameters = None
        # Key ciphered data.
        self.keyCipheredData = None
        # Ciphered content.
        self.cipheredContent = None
        # Shared secret is generated when connection is made.
        self.sharedSecret = None
        # xml settings. This is used only on xml parser.
        self.xml = None
        # System title is not send on pre-established connecions.
        self.ignoreSystemTitle = False

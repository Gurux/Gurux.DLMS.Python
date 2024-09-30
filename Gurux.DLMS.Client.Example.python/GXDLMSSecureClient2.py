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
from gurux_dlms.GXDLMSClient import GXDLMSTranslatorStructure
from gurux_dlms.enums.Authentication import Authentication
from gurux_dlms.enums.InterfaceType import InterfaceType
from gurux_dlms.secure.GXDLMSSecureClient import GXDLMSSecureClient
from gurux_dlms.IGXCryptoNotifier import IGXCryptoNotifier
from gurux_common.GXCommon import GXCommon
from gurux_dlms.GXDLMSTranslator import GXDLMSTranslator

class GXDLMSSecureClient2(GXDLMSSecureClient, IGXCryptoNotifier):
    #
    # Constructor.
    #
    def __init__(self, useLogicalNameReferencing=False, clientAddress=16, serverAddress=1, forAuthentication=Authentication.NONE, password=None, interfaceType=InterfaceType.HDLC):
        GXDLMSSecureClient.__init__(self, useLogicalNameReferencing, clientAddress, serverAddress, forAuthentication, password, interfaceType)
        self.__translator = GXDLMSTranslator()

    def onPduEventHandler(self, sender, complete, data):
        print("Decrypted PDU: " + GXCommon.toHex(data))   
        if complete:
            try:
                print(self.__translator.pduToXml(data))
            except Exception as ex:
                print(str(ex));
    def onKey(self, sender, args):
        """Called when the public or private key is needed 
        and it's unknown.

        sender : The source of the event.
        args : Event arguments.
        """

    def onCrypto(self, sender, args):
        """Called to encrypt or decrypt the data using 
        external Hardware Security Module.

        sender : The source of the event.
        args : Event arguments.
        """

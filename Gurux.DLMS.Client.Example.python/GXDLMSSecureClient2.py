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
import os
from gurux_dlms.GXDLMSClient import GXDLMSTranslatorStructure
from gurux_dlms.enums.Authentication import Authentication
from gurux_dlms.enums.InterfaceType import InterfaceType
from gurux_dlms.secure.GXDLMSSecureClient import GXDLMSSecureClient
from gurux_dlms.IGXCryptoNotifier import IGXCryptoNotifier
from gurux_common.GXCommon import GXCommon
from gurux_dlms.GXDLMSTranslator import GXDLMSTranslator
from gurux_dlms.asn.GXPkcs8 import GXPkcs8
from gurux_dlms.asn.GXx509Certificate import GXx509Certificate
from gurux_dlms.objects.enums.SecuritySuite import SecuritySuite
from gurux_dlms.objects.enums.CertificateType import CertificateType
from gurux_dlms.GXByteBuffer import GXByteBuffer


class GXDLMSSecureClient2(GXDLMSSecureClient, IGXCryptoNotifier):
    #
    # Constructor.
    #
    def __init__(
        self,
        useLogicalNameReferencing=False,
        clientAddress=16,
        serverAddress=1,
        forAuthentication=Authentication.NONE,
        password=None,
        interfaceType=InterfaceType.HDLC,
    ):
        GXDLMSSecureClient.__init__(
            self,
            useLogicalNameReferencing,
            clientAddress,
            serverAddress,
            forAuthentication,
            password,
            interfaceType,
        )
        self.__translator = GXDLMSTranslator()

    def onPduEventHandler(self, sender, complete, data):
        print("Decrypted PDU: " + GXCommon.toHex(data))
        if complete:
            try:
                print(self.__translator.pduToXml(data))
            except Exception as ex:
                print(str(ex))

    def getPath(self, securitySuite, certType, path, systemTitle):
        """
        Return correct path.

        :param securitySuite: SecuritySuite enum.
        :param certType: CertificateType enum.
        :param path: Folder path as string.
        :param systemTitle: System title as bytes.
        :return: Full file path or folder path.
        """
        if securitySuite == SecuritySuite.SUITE_2:
            path = os.path.join(path, "384")

        if systemTitle is None:
            return path

        if certType == CertificateType.DIGITAL_SIGNATURE:
            prefix = "D"
        elif certType == CertificateType.KEY_AGREEMENT:
            prefix = "A"
        else:
            raise Exception("Invalid type.")
        filename = prefix + GXByteBuffer.hex(systemTitle, False) + ".pem"
        return os.path.join(path, filename)

    def onKey(self, sender, args):
        """Called when the public or private key is needed
        and it's unknown.

        sender : The source of the event.
        args : Event arguments.
        """
        try:
            if args.encrypt:
                # Find private key.
                path = self.getPath(
                    args.securitySuite, args.certificateType, "Keys", args.systemTitle
                )
                args.privateKey = GXPkcs8.load(path).privateKey
                print("Client private key:" + path + " " + args.privateKey.toHex())
                print(
                    "Client public key:"
                    + path
                    + " "
                    + args.privateKey.getPublicKey().toHex()
                )
            else:
                # Find public key.
                if not args.systemTitle:
                    path = self.getPath(
                        args.securitySuite,
                        args.certificateType,
                        "Certificates",
                        args.systemTitle,
                    )
                    pk = GXx509Certificate.search(path, args.systemTitle)
                    args.publicKey = pk.publicKey
                    print("Server public key:" + str(pk.serialNumber))
                else:
                    path = self.getPath(
                        args.securitySuite,
                        args.certificateType,
                        "Certificates",
                        args.systemTitle,
                    )
                    pk = GXx509Certificate.load(path)
                    args.publicKey = pk.publicKey
                    print("Server public key:" + str(pk.serialNumber))
        except Exception as ex:
            print(ex.message)

    def onCrypto(self, sender, args):
        """Called to encrypt or decrypt the data using
        external Hardware Security Module.

        sender : The source of the event.
        args : Event arguments.
        """

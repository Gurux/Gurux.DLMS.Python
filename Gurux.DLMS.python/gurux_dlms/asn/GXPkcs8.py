#
# --------------------------------------------------------------------------
#  Gurux Ltd
#
#
#
# Filename:        $HeadURL$
#
# Version:         $Revision$,
#                  $Date$
#                  $Author$
#
# Copyright (c) Gurux Ltd
#
# ---------------------------------------------------------------------------
#
#  DESCRIPTION
#
# This file is a part of Gurux Device Framework.
#
# Gurux Device Framework is Open Source software you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation version 2 of the License.
# Gurux Device Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# More information of Gurux products: https:#www.gurux.org
#
# This code is licensed under the GNU General Public License v2.
# Full text may be retrieved at http:#www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
import os
from ..asn.enums.CertificateVersion import CertificateVersion
from ..asn.enums.X9ObjectIdentifier import X9ObjectIdentifier
from ..ecdsa.enums.Ecc import Ecc
from ..objects.enums.CertificateType import CertificateType
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from .GXAsn1Sequence import GXAsn1Sequence
from .GXAsn1ObjectIdentifier import GXAsn1ObjectIdentifier
from .X9ObjectIdentifierConverter import X9ObjectIdentifierConverter
from .GXAsn1Context import GXAsn1Context
from ..GXBitString import GXBitString
from .GXAsn1Converter import GXAsn1Converter
from ..GXInt8 import GXInt8
from ..ecdsa.GXDLMSCertificateException import GXDLMSCertificateException
from ..ecdsa.GXEcdsa import GXEcdsa
from .enums.PkcsType import PkcsType


class GXPkcs8:
    """
    Pkcs8 certification request. Private key is saved using this format.
    """

    __rawData = bytearray()
    """
    Loaded PKCS #8 certificate as a raw data.
    """

    __description = ""
    """
    Description is extra metadata that is saved to PEM file.
    """

    __version = CertificateVersion.VERSION1
    """
    Private key version.
    """

    __algorithm = X9ObjectIdentifier.ID_EC_PUBLIC_KEY
    """
    Algorithm.
    """

    __privateKey = None
    """
    Private key.
    """

    __publicKey = None
    """
    Public key.
    """

    @property
    def algorithm(self):
        """
        Algorithm.
        """
        return self.__algorithm

    @property
    def description(self):
        """
        Description is extra metadata that is saved to PEM file.
        """
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    @property
    def version(self):
        """
        Private key version.
        """
        return self.__version

    @version.setter
    def version(self, value):
        self.__version = value

    @property
    def privateKey(self):
        """
        Private key.
        """
        return self.__privateKey

    @property
    def publicKey(self):
        """
        Public key.
        """
        return self.__publicKey

    @property
    def encoded(self):
        if self.__rawData:
            return self.__rawData
        d = GXAsn1Sequence()
        d.append(GXInt8(self.version))
        d1 = GXAsn1Sequence()
        d1.append(
            GXAsn1ObjectIdentifier(
                X9ObjectIdentifierConverter.getString(self.__algorithm)
            )
        )
        if self.publicKey.scheme == Ecc.P256:
            alg = GXAsn1ObjectIdentifier("1.2.840.10045.3.1.7")
        else:
            alg = GXAsn1ObjectIdentifier("1.3.132.0.34")
        d1.append(alg)
        d.append(d1)
        d2 = GXAsn1Sequence()
        d2.append(GXInt8(1))
        d2.append(self.privateKey.rawValue)
        d3 = GXAsn1Context()
        d3.index = 1
        d3.append(GXBitString(self.publicKey.rawValue, 0))
        d2.append(d3)
        d.append(GXAsn1Converter.toByteArray(d2))
        self.__rawData = GXAsn1Converter.toByteArray(d)
        return self.__rawData

    def __init__(self, pair=None):
        """
        Constructor.

            Parameters:
                pair: Private key or private/public key pair.
        """
        if pair:
            self.__privateKey = pair[1]
            self.__publicKey = pair[0]

    @classmethod
    def getFilePath(cls, scheme, certificateType, systemTitle):
        """
        Returns default file path.

            Parameters:
                scheme: Used scheme.
                certificateType: Certificate type.
                systemTitle: System title.

            Returns:
                File path.
        """
        if certificateType == CertificateType.DIGITAL_SIGNATURE:
            path = "D"
        elif certificateType == CertificateType.KEY_AGREEMENT:
            path = "A"
        elif certificateType == CertificateType.TLS:
            path = "T"
        else:
            raise ValueError("Unknown certificate type.")

        path += GXByteBuffer.hex(systemTitle, False) + ".pem"
        if scheme == Ecc.P256:
            path = os.path.join("Keys", path)
        else:
            path = os.path.join("Keys384", path)
        return path

    # pylint: disable=unused-private-member
    @classmethod
    def fromPem(cls, data):
        """
        Create PKCS #8 from PEM string.

            Parameters:
                data: PEM string.
        """
        START = "PRIVATE KEY-----\n"
        END = "-----END"
        data = data.replace("\r\n", "\n")
        start = data.find(START)
        if start == -1:
            raise ValueError("Invalid PEM file.")
        desc = None
        if start != len(START):
            desc = data[:start]
            DESCRIPTION = "#Description"
            # Check if there is a description metadata.
            descStart = desc.rfind(DESCRIPTION)
            if descStart != -1:
                descEnd = desc.find("\n", descStart, start)
                desc = desc[descStart + len(DESCRIPTION) : descEnd - len(DESCRIPTION)]
                desc = desc.strip()
            else:
                desc = None
        data = data[start + len(START) :]
        end = data.find(END)
        if end == -1:
            raise ValueError("Invalid PEM file.")

        cert = cls.fromDer(data[0:end])
        cert.__description = desc
        return cert

    @classmethod
    def fromHexString(cls, data):
        """
        Create PKCS 8 from hex string.

            Parameters:
                data: Hex string.

        Returns:
            PKCS 8
        """
        cert = GXPkcs8()
        cert.__init(GXByteBuffer.hexToBytes(data))
        return cert

    @classmethod
    def fromDer(cls, der):
        """
           Create PKCS #8 from DER Base64 encoded string.

               Parameters:
                   der: Base64 DER string.

        *
        * @return
        """
        der = der.replace("\r\n", "")
        der = der.replace("\n", "")
        cert = GXPkcs8()
        cert.__init(_GXCommon.fromBase64(der))
        return cert

    # pylint: disable=import-outside-toplevel, unused-private-member, protected-access
    def __init(self, data):
        """
        Initialize the private key from ASN.1 encoded data.
        :param data: Byte array containing ASN.1 encoded PKCS#8 data.
        """
        from gurux_dlms.ecdsa.GXPrivateKey import GXPrivateKey
        from gurux_dlms.ecdsa.GXPublicKey import GXPublicKey

        self.__rawData = data
        seq = GXAsn1Converter.fromByteArray(data)
        if len(seq) < 3:
            raise ValueError("Wrong number of elements in sequence.")

        if not isinstance(seq[0], int):
            cert_type = GXAsn1Converter.__getCertificateType(data, seq)
            if cert_type == PkcsType.PKCS10:
                raise GXDLMSCertificateException(
                    "Invalid Certificate. This is PKCS 10 certification request, not PKCS 8."
                )
            if cert_type == PkcsType.X509CERTIFICATE:
                raise GXDLMSCertificateException(
                    "Invalid Certificate. This is a PKCS x509 certificate, not PKCS 8."
                )
            raise GXDLMSCertificateException("Invalid Certificate Version.")

        self.version = CertificateVersion(seq[0])

        if isinstance(seq[1], (bytes, bytearray)):
            raise GXDLMSCertificateException(
                "Invalid Certificate. This looks more like a private key, not PKCS 8."
            )

        tmp = seq[1]
        self.__algorithm = X9ObjectIdentifierConverter.fromString(str(tmp[0]))
        self.__privateKey = GXPrivateKey.fromRawBytes(seq[2][1])
        if self.__privateKey is None:
            raise Exception("Invalid private key.")

        # Public key optional
        tmp2 = seq[2]
        if len(tmp2) > 2:
            self.__publicKey = GXPublicKey.fromRawBytes(tmp2[2][0].value)
            GXEcdsa.validate(self.__publicKey)
        else:
            self.__publicKey = self.__privateKey.getPublicKey()

    def __str__(self):
        bb = "PKCS #8:"
        bb += "Version: " + str(self.version) + "\n"
        bb += "Algorithm: " + str(self.algorithm) + "\n"
        bb += "PrivateKey: " + self.privateKey.toHex() + "\n"
        bb += "PublicKey: " + str(self.publicKey)
        return bb

    @classmethod
    def load(cls, path):
        """
        Load private key from the PEM file.

            Parameters:
                path: File path.

            Returns:
                Created GXPkcs8 object.
        """

        with open(path, "r", encoding="utf-8") as file:
            return cls.fromPem(file.read())

    def save(self, path):
        """
        Save private key to PEM file.

            Parameters:
                path: File path.
        """

        with open(path, "w", encoding="utf-8") as file:
            file.write(self.toPem())

    def toPem(self):
        """
           Private key in PEM format.
        *
        * @return Private key as in PEM string.
        """
        sb = ""
        if not self.privateKey:
            raise ValueError("Public or private key is not set.")
        if self.description:
            sb = "#Description"
            sb += self.description + "\r"
        sb += "-----BEGIN PRIVATE KEY-----\r"
        sb += self.toDer()
        sb += "\r-----END PRIVATE KEY-----"
        return sb

    def toDer(self):
        """
        Private key in DER format.

            Returns:
                Private key as in DER string.
        """
        return _GXCommon.toBase64(self.encoded)

    def __eq__(self, other):
        return isinstance(other, GXPkcs8) and self.privateKey == other.privateKey

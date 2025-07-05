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
from ..ecdsa.enums.Ecc import Ecc
from ..asn.enums.X9ObjectIdentifier import X9ObjectIdentifier
from ..asn.enums.CertificateVersion import CertificateVersion
from ..internal._GXCommon import _GXCommon
from ..asn.GXAsn1Converter import GXAsn1Converter
from ..asn.X9ObjectIdentifierConverter import X9ObjectIdentifierConverter
from .GXPublicKey import GXPublicKey
from ..GXBitString import GXBitString
from ..asn.GXAsn1Sequence import GXAsn1Sequence
from ..asn.GXAsn1ObjectIdentifier import GXAsn1ObjectIdentifier
from ..asn.GXAsn1Context import GXAsn1Context
from .GXCurve import GXCurve
from .GXEccPoint import GXEccPoint
from ._GXShamirs import _GXShamirs
from ..GXByteBuffer import GXByteBuffer
from ..GXInt8 import GXInt8

# from gurux_dlms.GXDLMSTranslator import GXDLMSTranslator


class GXPrivateKey:
    """
    Private key.
    """

    __scheme = Ecc.P256
    """
    Used scheme.
    """

    __rawValue = bytearray()
    """
    Private key raw value.
    """

    __systemTitle = bytearray()
    """
    SystemTitle is an extra information that can be used in debugging.
    """

    __publicKey = None

    @property
    def scheme(self):
        """
        Used scheme.
        """
        return self.__scheme

    @property
    def rawValue(self):
        """
        Private key raw value.
        """
        return self.__rawValue

    @property
    def systemTitle(self):
        """
        SystemTitle is an extra information that can be used in debugging.
        """
        return self.__systemTitle

    @systemTitle.setter
    def systemTitle(self, value):
        self.__systemTitle = value

    # pylint: disable=unused-private-member
    @classmethod
    def fromRawBytes(cls, key):
        """
        Create the private key from raw bytes.

            Parameters:
                key: Raw data

            Returns:
                Private key.
        """
        value = GXPrivateKey()
        # If private key is given
        if len(key) == 32:
            value.__scheme = Ecc.P256
            value.__rawValue = key
        elif len(key) == 48:
            value.__scheme = Ecc.P384
            value.__rawValue = key
        else:
            raise ValueError("Invalid private key.")
        return value

    # pylint: disable=unused-private-member
    @classmethod
    def fromDer(cls, der):
        """
        Create the private key from DER.

            Parameters:
                key: DER Base64 coded string.

            Returns:
                Private key.
        """
        der = der.replace("\r\n", "")
        der = der.replace("\n", "")
        key = _GXCommon.fromBase64(der)
        seq = GXAsn1Converter.fromByteArray(key)
        if seq[0] > 3:
            raise ValueError("Invalid private key version.")
        tmp = seq[2]
        value = GXPrivateKey()
        id_ = X9ObjectIdentifierConverter.fromString(str(tmp[0]))
        if id_ == X9ObjectIdentifier.PRIME256V1:
            value.__scheme = Ecc.P256
        elif id_ == X9ObjectIdentifier.SECP384R1:
            value.__scheme = Ecc.P384
        else:
            if id_ == X9ObjectIdentifier.NONE:
                raise ValueError("Invalid private key " + str(tmp[0]) + ".")
            raise ValueError("Invalid private key " + str(id_) + " " + str(tmp[0]) + ".")

        value.__rawValue = seq[1]
        if isinstance(seq[3], bytes):
            value.__publicKey = GXPublicKey.fromRawBytes(seq[3])
        elif isinstance(seq[3], GXBitString):
            value.__publicKey = GXPublicKey.fromRawBytes((seq[3]).value)
        else:
            # Open SSL PEM.
            value.__publicKey = GXPublicKey.fromRawBytes(seq[3][0].value)
        return value

    @classmethod
    def fromPem(cls, pem):
        """
        Create the private key from PEM.

            Parameters:
                pem: PEM in Base64 coded string.

        Returns
            Private key.
        """
        pem = pem.replace("\r\n", "\n")
        START = "PRIVATE KEY-----\n"
        END = "-----END"
        index = pem.find(START)
        if index == -1:
            raise ValueError("Invalid PEM file.")
        pem = pem[index + len(START) :]
        index = pem.find(END)
        if index == -1:
            raise ValueError("Invalid PEM file.")
        return cls.fromDer(pem[0:index])

    @classmethod
    def load(cls, path):
        """
        Create the private key from PEM file.

            Parameters:
                path: Path to the PEM file.

            Returns
                Private key.
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

    def toDer(self):
        d = GXAsn1Sequence()
        d.append(GXInt8(CertificateVersion.VERSION2))
        d.append(self.__rawValue)
        d1 = GXAsn1Sequence()
        if self.scheme == Ecc.P256:
            d1.append(GXAsn1ObjectIdentifier("1.2.840.10045.3.1.7"))
        elif self.scheme == Ecc.P384:
            d1.append(GXAsn1ObjectIdentifier("1.3.132.0.34"))
        else:
            raise ValueError("Invalid ECC scheme.")
        d.append(d1)
        d2 = GXAsn1Context()
        d2.index = 1
        d2.append(GXBitString(self.getPublicKey().rawValue, 0))
        d.append(d2)
        return _GXCommon.toBase64(GXAsn1Converter.toByteArray(d))

    def toPem(self):
        """
        Get private key as PEM format.
        """
        return (
            "-----BEGIN EC PRIVATE KEY-----\n"
            + self.toDer()
            + "\n-----END EC PRIVATE KEY-----"
        )

    def getPublicKey(self):
        """
        Get public key from private key.

            @returns:
                Public key.
        """
        if not self.__publicKey:
            pk = int.from_bytes(self.__rawValue, byteorder="big")
            curve = GXCurve(self.scheme)
            ret = GXEccPoint()
            _GXShamirs.pointMulti(curve, ret, curve.g, pk)
            if self.scheme == Ecc.P256:
                size = 32
            else:
                size = 48
            # Public key is un-compressed format.
            key = bytearray(int(4).to_bytes(1))
            key.extend(ret.x.to_bytes(size, byteorder="big"))
            key.extend(ret.y.to_bytes(size, byteorder="big"))
            self.__publicKey = GXPublicKey.fromRawBytes(key)
        return self.__publicKey

    def toHex(self, addSpace=True):
        """
           Returns the private key as a hex string.

               Parameters:
                   addSpace: Is space added between the bytes.

        *
        * @return Private key as hex string.
        """
        return GXByteBuffer.hex(self.__rawValue, addSpace)

    def __eq__(self, other):
        return isinstance(other, GXPrivateKey) and self.__rawValue == other.rawValue

    def __str__(self):
        return self.toHex(True)

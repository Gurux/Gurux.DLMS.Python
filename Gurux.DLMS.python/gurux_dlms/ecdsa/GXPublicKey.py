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
from gurux_dlms.ecdsa.enums.Ecc import Ecc
from gurux_dlms.GXByteBuffer import GXByteBuffer
from gurux_dlms.internal._GXCommon import _GXCommon

from gurux_dlms.asn.GXAsn1Converter import GXAsn1Converter
from gurux_dlms.asn.X9ObjectIdentifierConverter import X9ObjectIdentifierConverter
from gurux_dlms.asn.enums.X9ObjectIdentifier import X9ObjectIdentifier
from gurux_dlms.asn.GXAsn1Sequence import GXAsn1Sequence
from gurux_dlms.asn.GXAsn1ObjectIdentifier import GXAsn1ObjectIdentifier

# from gurux_dlms.GXDLMSTranslator import GXDLMSTranslator
from gurux_dlms.GXBitString import GXBitString


class GXPublicKey:
    """
    Public key.
    """

    _scheme = Ecc.P256
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

    @property
    def scheme(self):
        """
        Used scheme.
        """
        return self._scheme

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

    @property
    def x(self):
        """
        X Coordinate.
        """
        pk = GXByteBuffer(self.__rawValue)
        size = int(pk.size / 2)
        return pk.subArray(1, size)

    @property
    def y(self):
        """
        Y Coordinate.
        """
        pk = GXByteBuffer(self.__rawValue)
        size = int(pk.size / 2)
        return pk.subArray(1 + size, size)

    # pylint: disable=unused-private-member
    @classmethod
    def fromRawBytes(cls, key):
        """
        Create the public key from raw bytes.

            Parameters:
                key: Raw data

            Returns:
                Public key.
        """
        value = GXPublicKey()
        if len(key) == 65:
            value._scheme = Ecc.P256
            value.__rawValue = key
        elif len(key) == 97:
            value._scheme = Ecc.P384
            value.__rawValue = key
        elif len(key) == 64:
            # Compression tag is not send in DLMS messages.
            value._scheme = Ecc.P256
            value.__rawValue = [65]
            value.__rawValue[0] = 4
            value.__rawValue[1:64] = key[0:64]
        elif len(key) == 96:
            # Compression tag is not send in DLMS messages.
            value._scheme = Ecc.P384
            value.__rawValue = [96]
            value.__rawValue[0] = 4
            value.__rawValue[1:95] = key[0:95]
        else:
            raise ValueError("Invalid public key.")
        return value

    @classmethod
    def fromDer(cls, der):
        """
        Create the public key from DER.

            Parameters:
                der: DER Base64 coded string.

            Returns:
                Public key.
        """
        der = der.replace("\r\n", "")
        der = der.replace("\n", "")
        value = GXPublicKey()
        key = _GXCommon.fromBase64(der)
        seq = GXAsn1Converter.fromByteArray(key)
        id_ = X9ObjectIdentifierConverter.fromString(str(seq[0][1]))
        if id_ == X9ObjectIdentifier.PRIME256V1:
            value._scheme = Ecc.P256
        elif id_ == X9ObjectIdentifier.SECP384R1:
            value._scheme = Ecc.P384
        else:
            if id_ == X9ObjectIdentifier.NONE:
                raise ValueError("Invalid public key " + str(seq[0]) + ".")
            raise ValueError("Invalid public key " + id_ + " " + str(seq[0]) + ".")
        if isinstance(seq[1], bytes):
            value.__rawValue = seq[1]
        else:
            # Open SSL PEM.
            value.__rawValue = seq[1].value
        return value

    @classmethod
    def fromPem(cls, pem):
        """
        Create the public key from PEM.

            Parameters:
                pem: PEM Base64 coded string.

            Returns:
                Public key.
        """
        pem = pem.replace("\r\n", "\n")
        START = "-----BEGIN PUBLIC KEY-----\n"
        END = "\n-----END PUBLIC KEY-----"
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
        Create the public key from PEM file.

            Parameters:
                path: Path to the PEM file.

            Returns
            Public key.
        """
        with open(path, "r", encoding="utf-8") as file:
            return cls.fromPem(file.read())

    def save(self, path):
        """
        Save public key to PEM file.

            Parameters:
                path: File path.
        """
        with open(path, "w", encoding="utf-8") as file:
            file.write(self.toPem())

    def toHex(self):
        """
        Returns the public key as a hex string.
        """
        return GXByteBuffer.hex(self.__rawValue)

    def toDer(self):
        """
        Get public key as DER format.
        """
        return _GXCommon.toBase64(self.toEncoded())

    def toEncoded(self):
        """
        Get public key as encoded format.
        """
        # Subject Public Key Info.
        d = GXAsn1Sequence()
        d1 = GXAsn1Sequence()
        d1.append(GXAsn1ObjectIdentifier("1.2.840.10045.2.1"))
        if self.scheme == Ecc.P256:
            d1.append(GXAsn1ObjectIdentifier("1.2.840.10045.3.1.7"))
        elif self.scheme == Ecc.P384:
            d1.append(GXAsn1ObjectIdentifier("1.3.132.0.34"))
        else:
            raise ValueError("Invalid ECC scheme.")
        d.append(d1)
        d.append(GXBitString(self.__rawValue, 0))
        return GXAsn1Converter.toByteArray(d)

    def toPem(self):
        """
        Get public key as PEM format.
        """
        return (
            "-----BEGIN PUBLIC KEY-----\n"
            + self.toDer()
            + "\n-----END PUBLIC KEY-----\n"
        )

    def __str__(self):
        if self.scheme == Ecc.P256:
            sb = "NIST P-256"
            size = 32
        elif self.scheme == Ecc.P384:
            sb = "NIST P-384"
            size = 48
        else:
            raise ValueError("Invalid scheme.")
        sb += " public x coord: 0x"
        sb += format(
            int.from_bytes(self.__rawValue[1 : 1 + size], byteorder="big"), "X"
        )
        sb += "\r public y coord: 0x"
        sb += (
            format(int.from_bytes(self.__rawValue[1 + size :], byteorder="big"), "X")
            + "\r"
        )
        return sb

    def __eq__(self, other):
        return isinstance(other, GXPublicKey) and self.__rawValue == other.rawValue

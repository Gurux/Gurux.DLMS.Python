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
#  Gurux Device Framework is Open Source software you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http:#www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http:#www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
import random
import hashlib
from ..GXByteBuffer import GXByteBuffer
from .enums.Ecc import Ecc
from ._GXShamirs import _GXShamirs
from .GXEccPoint import GXEccPoint
from .GXCurve import GXCurve


class GXEcdsa:
    """
    ECDSA asynchronous ciphering.
    """

    __publicKey = None
    """
    Public key.
    """

    __privateKey = None
    """
    Private key.
    """

    __curve = None

    @classmethod
    def __schemeSize(cls, scheme):
        """
        Get scheme size in bytes.

            Parameters:
                scheme:

            Returns:
        """
        if scheme == Ecc.P256:
            return 32
        return 48

    @classmethod
    def __getRandomNumber(cls, scheme):
        """
        Generate random number.

            Parameters:
                scheme: Scheme

            Returns:
                Random number as byte array.
        """
        return random.randbytes(cls.__schemeSize(scheme))

    def sign(self, data):
        """
        Sign given data using public and private key.

            Parameters:
                data: Data to sign.

            Returns:
                Signature
        """
        if self.__privateKey is None:
            raise ValueError("Invalid private key.")
        if self.__privateKey.scheme == Ecc.P256:
            h = hashlib.sha256()
        elif self.__privateKey.scheme == Ecc.P256:
            h = hashlib.sha384()
        else:
            raise ValueError("Invalid private key scheme.")
        h.update(data)
        msg = int.from_bytes(h.digest(), byteorder="big")
        k = int.from_bytes(
            self.__getRandomNumber(self.__privateKey.scheme), byteorder="big"
        )
        pk = int.from_bytes(self.__privateKey.rawValue, byteorder="big")
        R = GXEccPoint(0, 0)
        _GXShamirs.pointMulti(self.__curve, R, self.__curve.g, k)
        r = int(R.x)
        r %= self.__curve.n
        # s = (k ^ -1 * (e + d * r)) mod n
        s = pk
        s *= r
        s += msg
        kinv = pow(k, -1, self.__curve.n)
        s *= kinv
        s %= self.__curve.n
        size = self.__schemeSize(self.__privateKey.scheme)
        signature = bytearray(r.to_bytes(size, byteorder="big"))
        signature.extend(bytearray(s.to_bytes(size, byteorder="big")))
        return bytes(signature)

    def generateSecret(self, publicKey):
        """
        Generate shared secret from public and private key.

        Parameters:
            publicKey: Public key.

        Returns:
            Generated secret.
        """
        if self.__privateKey is None:
            raise ValueError("Invalid private key.")
        if self.__privateKey.scheme != publicKey.scheme:
            raise ValueError("Private key scheme is different than public key.")
        pk = int(self.__privateKey.rawValue)
        bb = GXByteBuffer()
        bb.set(publicKey.rawValue)
        size = self.__schemeSize(self.__privateKey.scheme)
        x = int(bb.subArray(1, size))
        y = int(bb.subArray(1 + size, size))
        p = GXEccPoint(x, y)
        curve = GXCurve(self.__privateKey.scheme)
        ret = GXEccPoint()
        _GXShamirs.pointMulti(curve, ret, p, pk)
        return ret.x.toArray

    # pylint: disable=import-outside-toplevel
    @classmethod
    def generateKeyPair(cls, scheme):
        """
        Generate public and private key pair.

        Returns:
            Generated public and private keys.
        """
        from .GXPrivateKey import GXPrivateKey

        raw = cls.__getRandomNumber(scheme)
        pk = GXPrivateKey.fromRawBytes(raw)
        pub = pk.getPublicKey()
        return (pub, pk)

    def verify(self, signature, data):
        """
        Verify that signature matches the data.

            Parameters:
                signature: Generated signature.
                data: Data to valuate.

            Returns:
                True if the signature is valid; otherwise, false.
        """
        if self.__publicKey is None:
            if self.__privateKey is None:
                raise ValueError("Invalid private key.")
            self.__publicKey = self.__privateKey.getPublicKey()

        if self.__publicKey.scheme == Ecc.P256:
            h = hashlib.sha256()
        elif self.__publicKey.scheme == Ecc.P256:
            h = hashlib.sha384()
        else:
            raise ValueError("Invalid private key scheme.")
        h.update(data)
        msg = int.from_bytes(h.digest(), byteorder="big")
        size = self.__schemeSize(self.__publicKey.scheme)
        sigR = int.from_bytes(signature[0:size], byteorder="big")
        sigS = int.from_bytes(signature[size:], byteorder="big")
        w = pow(sigS, -1, self.__curve.n)
        u1 = msg
        u1 *= w
        u1 %= self.__curve.n
        u2 = sigR
        u2 *= w
        u2 %= self.__curve.n
        tmp = GXEccPoint()
        _GXShamirs.trick(self.__curve, self.__publicKey, tmp, u1, u2)
        tmp.x %= self.__curve.n
        return tmp.x == sigR

    @classmethod
    def validate(cls, publicKey):
        """
        Check that this is correct public key.
        """
        if publicKey is None:
            raise ValueError("Invalid public key.")
        size = cls.__schemeSize(publicKey.scheme)
        x = int.from_bytes(publicKey.rawValue[1 : 1 + size], byteorder="big")
        y = int.from_bytes(publicKey.rawValue[1 + size :], byteorder="big")
        curve = GXCurve(publicKey.scheme)
        y *= y
        y %= curve.p
        tmpX = x
        tmpX *= x
        tmpX %= curve.p
        tmpX += curve.a
        tmpX *= x
        tmpX += curve.b
        tmpX %= curve.p
        if y != tmpX:
            raise ValueError(
                "Public key validate failed. Public key is not valid ECDSA public key."
            )

    # pylint: disable=import-outside-toplevel
    def __init__(self, value):
        """
        Constructor.

            Parameters:
                value: Private key, public key or scheme.
        """
        from .GXPrivateKey import GXPrivateKey
        from .GXPublicKey import GXPublicKey

        if isinstance(value, GXPrivateKey):
            self.__privateKey = value
            self.__curve = GXCurve(value.scheme)
        elif isinstance(value, GXPublicKey):
            self.__publicKey = value
            self.__curve = GXCurve(value.scheme)
        elif isinstance(value, Ecc):
            self.__curve = GXCurve(value)
        else:
            raise ValueError("argument.")

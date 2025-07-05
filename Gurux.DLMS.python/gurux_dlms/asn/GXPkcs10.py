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
import sys
import re
from .enums.CertificateVersion import CertificateVersion
from .enums.HashAlgorithm import HashAlgorithm
from .enums.PkcsObjectIdentifier import PkcsObjectIdentifier
from .enums.X9ObjectIdentifier import X9ObjectIdentifier
from ..ecdsa.GXPublicKey import GXPublicKey
from ..GXInt8 import GXInt8
from ..GXByteBuffer import GXByteBuffer
from ..GXBitString import GXBitString
from ..ecdsa.GXDLMSCertificateException import GXDLMSCertificateException
from .GXAsn1Sequence import GXAsn1Sequence
from .GXAsn1Converter import GXAsn1Converter
from .PkcsObjectIdentifierConverter import PkcsObjectIdentifierConverter
from .GXAsn1ObjectIdentifier import GXAsn1ObjectIdentifier
from .enums.PkcsType import PkcsType
from ..ecdsa.enums.Ecc import Ecc
from .GXAsn1Context import GXAsn1Context
from .GXAsn1Integer import GXAsn1Integer
from ..internal._GXCommon import _GXCommon
from .HashAlgorithmConverter import HashAlgorithmConverter
from .X9ObjectIdentifierConverter import X9ObjectIdentifierConverter
from ..ecdsa.GXEcdsa import GXEcdsa
from ..objects.enums.CertificateType import CertificateType
from ..asn.enums.KeyUsage import KeyUsage
from .enums.ExtendedKeyUsage import ExtendedKeyUsage
from .GXx509Certificate import GXx509Certificate
from ..GXArray import GXArray

if sys.version_info >= (3, 0):
    import urllib.request


# pylint: disable=too-many-instance-attributes
class GXPkcs10:
    """
    Pkcs10 Certificate Signing Request.
    """

    __rawData = bytearray()
    """
    Loaded PKCS #10 certificate as a raw data.
    """

    __version = CertificateVersion.VERSION1
    """
    Certificate version.
    """

    __subject = ""
    """
    Subject.
    """

    __attributes = []
    """
    Collection of attributes providing additional information about the subject of the certificate.
    """

    __algorithm = X9ObjectIdentifier.ID_EC_PUBLIC_KEY
    """
    Algorithm.
    """

    __publicKey = None
    """
    Subject public key.
    """

    __signatureAlgorithm = HashAlgorithm.NONE
    """
    Signature algorithm.
    """

    __signatureParameters = None
    """
    Signature parameters.
    """

    __signature = bytearray()
    """
    Signature.
    """

    @property
    def version(self):
        """
        Certificate version.
        """
        return self.__version

    @property
    def subject(self):
        """
        Subject.
        """
        return self.__subject

    @property
    def attributes(self):
        """
        Collection of attributes providing additional information about the subject of the certificate.
        """
        return self.__attributes

    @property
    def algorithm(self):
        """
        Algorithm.
        """
        return self.__algorithm

    @property
    def publicKey(self):
        """
        Subject public key.
        """
        return self.__publicKey

    @property
    def signatureAlgorithm(self):
        """
        Signature algorithm.
        """
        return self.__signatureAlgorithm

    @property
    def signatureParameters(self):
        """
        Signature parameters.
        """
        return self.__signatureParameters

    @property
    def signature(self):
        """
        Signature.
        """
        return self.__signature

    @property
    def encoded(self):
        if self.__rawData:
            return self.__rawData
        if not self.signature:
            raise ValueError("Sign first.")

        # Certification request info.
        # subject Public key info.
        sa = GXAsn1ObjectIdentifier(
            HashAlgorithmConverter.getString(self.__signatureAlgorithm)
        )
        value = GXArray(
            (self.__getData(), GXArray((sa,)), GXBitString(self.signature, 0))
        )
        return GXAsn1Converter.toByteArray(value)

    def __init__(self, value=None):
        """
        Constructor.
        """
        if value:
            self.__init(value)

    # pylint: disable=too-many-locals, protected-access
    def __init(self, data):
        self.__rawData = data
        seq = GXAsn1Converter.fromByteArray(data)
        if len(seq) < 3:
            raise ValueError("Wrong number of elements in sequence.")
        if not isinstance(seq[0], GXAsn1Sequence):
            type_ = GXAsn1Converter.__getCertificateType(data, seq)
            if type_ == PkcsType.PKCS8:
                raise GXDLMSCertificateException(
                    "Invalid Certificate. This is PKCS 8, not PKCS 10."
                )
            if type_ == PkcsType.X509CERTIFICATE:
                raise GXDLMSCertificateException(
                    "Invalid Certificate. This is PKCS x509 certificate, not PKCS 10."
                )
            raise GXDLMSCertificateException("Invalid Certificate Version.")

        reqInfo = seq[0]
        self.__version = CertificateVersion(reqInfo[0])
        self.__subject = GXAsn1Converter.getSubject(reqInfo[1])
        # subject Public key info.
        subjectPKInfo = reqInfo[2]
        if len(reqInfo) > 3:
            # PkcsObjectIdentifier
            for it in reqInfo[3]:
                values = []
                for _, v in it[1]:
                    values.append(v)
                self.attributes.append(
                    (PkcsObjectIdentifierConverter.fromString(str(it[0])), values)
                )

        tmp = GXAsn1Sequence(subjectPKInfo[0])
        self.__algorithm = X9ObjectIdentifierConverter.fromString(str(tmp[0]))
        if self.__algorithm != X9ObjectIdentifier.ID_EC_PUBLIC_KEY:
            algorithm = self.algorithm
            if self.algorithm == X9ObjectIdentifier.NONE:
                algorithm = PkcsObjectIdentifierConverter.fromString(str(tmp[0]))
                if algorithm == PkcsObjectIdentifier.NONE:
                    algorithm = str(tmp[0])
            raise ValueError("Invalid PKCS #10 certificate algorithm. " + algorithm)

        self.__publicKey = GXPublicKey.fromRawBytes(subjectPKInfo[1].value)
        GXEcdsa.validate(self.publicKey)
        # signatureAlgorithm
        sign = seq[1]
        self.__signatureAlgorithm = HashAlgorithmConverter.fromString(str(sign[0]))
        if not self.__signatureAlgorithm in (
            HashAlgorithm.SHA256WITH_ECDSA,
            HashAlgorithm.SHA384WITH_ECDSA,
        ):
            raise GXDLMSCertificateException(
                "Invalid signature algorithm. " + str(sign[0])
            )
        if len(sign) != 1:
            self.signatureParameters = sign[1]
        # signature
        # Get raw data
        tmp2 = GXByteBuffer()
        tmp2.set(data)
        GXAsn1Converter._getNext(tmp2)
        tmp2.size = tmp2.position
        tmp2.position = 1
        _GXCommon.getObjectCount(tmp2)
        # Get signature.
        self.__signature = seq[2].value
        e = GXEcdsa(self.publicKey)
        tmp3 = GXAsn1Converter.fromByteArray(self.signature)
        bb = GXByteBuffer()
        if self.__signatureAlgorithm == HashAlgorithm.SHA256WITH_ECDSA:
            size = 32
        else:
            size = 48
        # Some implementations might add extra byte. It must removed.
        if tmp3[0].length == size:
            start = 0
        else:
            start = 1

        bb.set(tmp3[0].toArray(), start, size)
        if tmp3[1].length == size:
            start = 0
        else:
            start = 1
        bb.set(tmp3[1].toArray(), start, size)
        if not e.verify(bb.array(), tmp2.subArray(tmp2.position, tmp2.available())):
            raise ValueError("Invalid Signature.")

    def __getData(self):
        if self.publicKey.scheme == Ecc.P256:
            alg = GXAsn1ObjectIdentifier("1.2.840.10045.3.1.7")
        else:
            alg = GXAsn1ObjectIdentifier("1.3.132.0.34")

        subjectPKInfo = GXBitString(self.publicKey.rawValue, 0)
        tmp = GXArray([GXAsn1ObjectIdentifier("1.2.840.10045.2.1"), alg])
        attributes = GXAsn1Context()
        for k, v in self.attributes:
            s = GXAsn1Sequence()
            s.append(GXAsn1ObjectIdentifier(PkcsObjectIdentifierConverter.getString(k)))
            # Convert object array to list.
            values = v
            s.append((values, None))
            attributes.append(s)
        return GXArray(
            [
                GXInt8(self.version),
                GXAsn1Converter.encodeSubject(self.subject),
                GXArray([tmp, subjectPKInfo]),
                attributes,
            ]
        )

    def sign(self, key, hashAlgorithm):
        """
        Sign

            Parameters:
                key: Private key.
                hashAlgorithm: Used algorithm for signing.
        """
        data = GXAsn1Converter.toByteArray(self.__getData())
        e = GXEcdsa(key)
        self.__signatureAlgorithm = hashAlgorithm
        bb = e.sign(data)
        if self.__signatureAlgorithm == HashAlgorithm.SHA256WITH_ECDSA:
            size = 32
        else:
            size = 48
        tmp = GXArray((GXAsn1Integer(bb[0:size]), GXAsn1Integer(bb[size:])))
        self.__signature = GXAsn1Converter.toByteArray(tmp)

    @classmethod
    def fromHexString(cls, data):
        """
        Create PKCS 10 from hex string.

            Parameters:
                data: Hex string.

            Returns:
                PKCS 10
        """
        cert = GXPkcs10()
        cert.__init(GXByteBuffer.hexToBytes(data))
        return cert

    @classmethod
    def fromPem(cls, data):
        """
        Create x509Certificate from PEM string.

            Parameters:
                data: PEM string.
        """
        data.replace("\r\n", "\n")
        START = "CERTIFICATE REQUEST-----\n"
        END = "-----END"
        data = data.replace("\r\n", "\n")
        start = data.find(START)
        if start == -1:
            raise ValueError("Invalid PEM file.")
        data = data[start + len(START) :]
        end = data.find(END)
        if end == -1:
            raise ValueError("Invalid PEM file.")
        return cls.fromDer(data[0:end].strip())

    @classmethod
    def fromDer(cls, der):
        """
        Create x509Certificate from DER Base64 encoded string.

            Parameters:
                der: Base64 DER string.

            Returns:
        """
        der = der.replace("\r\n", "")
        der = der.replace("\n", "")
        cert = GXPkcs10()
        cert.__init(_GXCommon.fromBase64(der))
        return cert

    def toString(self):
        bb = "PKCS #10 certificate request:"
        bb += "\r\n"
        bb += "Version: " + str(self.version)
        bb += "\r\n"
        bb += "Subject: " + self.subject
        bb += "\r\n"
        bb += "Algorithm: " + str(self.algorithm)
        bb += "\r\n"
        bb += "Public Key: "
        if self.publicKey:
            bb += str(self.publicKey)
        bb += "\r\n"
        bb += "Signature algorithm: " + str(self.__signatureAlgorithm)
        bb += "\r\n"
        if self.signatureParameters:
            bb += "Signature parameters: "
            bb += str(self.signatureParameters)
            bb += "\r\n"

        bb += "Signature: " + GXByteBuffer.toHex(self.signature, False)
        bb += "\r\n"
        return bb

    # pylint: disable=unused-private-member
    @classmethod
    def createCertificateSigningRequest(cls, kp, subject):
        """
        Create Certificate Signing Request.

            Parameters:
                kp: KeyPair
                subject: Subject.

            Returns:
                Created GXPkcs10.
        """
        if not subject or subject.find("CN=") == -1:
            raise ValueError("subject")

        pkc10 = GXPkcs10()
        pkc10.__algorithm = X9ObjectIdentifier.ID_EC_PUBLIC_KEY
        pkc10.__publicKey = kp[0]
        pkc10.__subject = subject
        if pkc10.__publicKey.scheme == Ecc.P256:
            ha = HashAlgorithm.SHA256WITH_ECDSA
        else:
            ha = HashAlgorithm.SHA384WITH_ECDSA
        pkc10.sign(kp[1], ha)
        return pkc10

    @classmethod
    def getCertificate(cls, address, certifications):
        """
        Ask Gurux certificate server to generate the new certificate.

            Parameters:
                address: Certificate server address.
                certifications: List of certification requests.

            Returns:
                Generated certificate(s).
        """
        usage = ""
        for it in certifications:
            if usage:
                usage += ", "
            usage += '{"KeyUsage":'
            if it.certificateType == CertificateType.DIGITAL_SIGNATURE:
                usage += str(int(KeyUsage.DIGITAL_SIGNATURE))
            elif it.certificateType == CertificateType.KEY_AGREEMENT:
                usage += str(int(KeyUsage.KEY_AGREEMENT))
            elif it.certificateType == CertificateType.TLS:
                usage += str(int(KeyUsage.DIGITAL_SIGNATURE | KeyUsage.KEY_AGREEMENT))
            else:
                raise ValueError("Invalid type.")

            if it.extendedKeyUsage != ExtendedKeyUsage.NONE:
                usage += ', "ExtendedKeyUsage":'
                usage += str(int(it.extendedKeyUsage))
            usage += ', "CSR":"'
            usage += it.certificate.toDer()
            usage += '"}'

        der = '{"Certificates":[' + usage + "]}"
        req = urllib.request.Request(address, der.encode("utf-8"), method="POST")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req) as response:
            result = response.read().decode("utf-8")
            pos = result.find("[")
            if pos == -1:
                raise ValueError("Certificates are missing.")
            result = result[pos + 2 :]
            pos = result.find("]")
            if pos == -1:
                raise ValueError("Certificates are missing.")

            result = result[0 : pos - 1]
            certs = []
            tmp = re.split(r'[";,]', result)
            tmp = [p for p in tmp if p.strip()]
            pos = 0
            for it in tmp:
                # Ignore empty.
                if it:
                    x509 = GXx509Certificate.fromDer(it)
                    if (
                        certifications[pos].certificate.publicKey.rawValue
                        != x509.publicKey.rawValue
                    ):
                        raise ValueError(
                            "Create certificate signingRequest generated wrong public key."
                        )
                    pos += 1
                    certs.append(x509)
        return certs

    @classmethod
    def load(cls, path):
        """
        Load Pkcs10 Certificate Signing Request from the PEM (.csr) file.

            Parameters:
                path: File path.

            Returns:
                Created GXPkcs10 object.
        """

        with open(path, "r", encoding="utf-8") as file:
            return cls.fromPem(file.read())

    def save(self, path):
        """
        Save Pkcs #10 Certificate Signing Request to PEM file.

            Parameters:
                path: File path.
        """

        with open(path, "w", encoding="utf-8") as file:
            file.write(self.toPem())

    def toPem(self):
        """
        Pkcs #10 Certificate Signing Request in DER format.
            Returns:
                Public key as in PEM string.
        """
        sb = "-----BEGIN CERTIFICATE REQUEST-----\r"
        sb += self.toDer()
        sb += "-----END CERTIFICATE REQUEST-----\r"
        return sb

    def toDer(self):
        """
        Pkcs #10 Certificate Signing Request in DER format.
            Returns:
                Public key as in PEM string.
        """
        return _GXCommon.toBase64(self.encoded)

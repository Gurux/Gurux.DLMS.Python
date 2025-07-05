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

from .enums.CertificateVersion import CertificateVersion
from .enums.ExtendedKeyUsage import ExtendedKeyUsage
from .enums.HashAlgorithm import HashAlgorithm
from .enums.KeyUsage import KeyUsage
from ..enums.BerType import BerType

from ..objects.enums.CertificateType import CertificateType
from ..internal._GXCommon import _GXCommon
from ..ecdsa.enums.Ecc import Ecc
from ..GXByteBuffer import GXByteBuffer
from .HashAlgorithmConverter import HashAlgorithmConverter
from .GXAsn1ObjectIdentifier import GXAsn1ObjectIdentifier
from ..GXBitString import GXBitString
from ..ecdsa.GXEcdsa import GXEcdsa
from ..ecdsa.GXDLMSCertificateException import GXDLMSCertificateException
from .GXAsn1Sequence import GXAsn1Sequence
from .GXAsn1Integer import GXAsn1Integer
from .X509CertificateTypeConverter import X509CertificateTypeConverter
from .enums.X509CertificateType import X509CertificateType
from .X509NameConverter import X509NameConverter
from .enums.X509Name import X509Name
from ..GXArray import GXArray
from .GXAsn1Context import GXAsn1Context
from ..GXInt8 import GXInt8
from .enums.PkcsType import PkcsType


# pylint: disable=too-many-public-methods, too-many-instance-attributes
class GXx509Certificate:
    """
    x509 Certificate.
    """

    __description = ""
    """
    Description is extra metadata that is saved to PEM file.
    """

    __rawData = bytearray()
    """
    Loaded x509Certificate as raw data.
    """

    __subjectKeyIdentifier = bytearray()
    """
    This extension identifies the public key being certified.
    """

    __authorityKeyIdentifier = bytearray()
    """
    May be used either as a certificate or CRL extension. It identifies the
        
 public key to be used to verify the signature on this certificate or CRL.
        
 It enables distinct keys used by the same CA to be distinguished.
    """

    __authorityCertificationSerialNumber = None
    """
    Authority certification serial number.
    """

    __basicConstraints = None
    """
    Indicates if the Subject may act as a CA.
    """

    __extendedKeyUsage = ExtendedKeyUsage.NONE
    """
    Indicates that a certificate can be used as an TLS server or client certificate.
    """

    __signatureAlgorithm = HashAlgorithm.SHA256WITH_ECDSA
    """
    Signature algorithm.
    """

    __signatureParameters = None
    """
    Signature Parameters.
    """

    __publicKey = None
    """
    Public key.
    """

    __publicKeyAlgorithm = HashAlgorithm.NONE
    """
    Public Key algorithm.
    """

    __publicKeyParameters = None
    """
    Parameters.
    """

    __signature = bytearray()
    """
    Signature.
    """

    __subject = ""
    """
    Subject. Example: "CN=Test, O=Gurux, L=Tampere, C=FI".
    """

    __subjectAlternativeName = ""
    """
    Subject Alternative Name.
    """

    __issuer = ""
    """
    Issuer. Example: "CN=Test O=Gurux, L=Tampere, C=FI".
    """

    __issuerRaw = bytearray()
    """
    Raw Issuer in ASN1 format.
    """

    __authorityCertIssuer = ""
    """
    Authority Cert Issuer. Example: "CN=Test O=Gurux, L=Tampere, C=FI".
    """

    __serialNumber = None
    """
    Serial number.
    """

    __version = CertificateVersion.VERSION3
    """
    Version.
    """

    __validFrom = None
    """
    Validity from.
    """

    __validTo = None
    """
    Validity to.
    """

    __keyUsage = KeyUsage.NONE
    """
    Indicates the purpose for which the certified public key is used.
    """

    # pylint: disable=import-outside-toplevel
    @classmethod
    def getFilePath(cls, cert):
        """Returns the default file path."""
        from .GXAsn1Converter import GXAsn1Converter

        if cert.keyUsage == KeyUsage.DIGITAL_SIGNATURE:
            path = "D"
        elif cert.keyUsage == KeyUsage.KEY_AGREEMENT:
            path = "A"
        elif cert.keyUsage == (KeyUsage.DIGITAL_SIGNATURE | KeyUsage.KEY_AGREEMENT):
            path = "T"
        else:
            raise ValueError("Unknown certificate type.")

        st = GXAsn1Converter.hexSystemTitleFromSubject(cert.subject).strip()
        path += st + ".pem"
        if cert.publicKey.scheme == Ecc.P256:
            path = os.path.join("Certificates", path)
        else:
            path = os.path.join("Certificates384", path)
        return path

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
    def rawData(self):
        """
        Loaded x509Certificate as raw data.
        """
        return self.__rawData

    @property
    def subjectKeyIdentifier(self):
        """
        This extension identifies the public key being certified.
        """
        return self.__subjectKeyIdentifier

    @subjectKeyIdentifier.setter
    def subjectKeyIdentifier(self, value):
        self.__subjectKeyIdentifier = value

    @property
    def authorityKeyIdentifier(self):
        """
        May be used either as a certificate or CRL extension. It identifies the
        public key to be used to verify the signature on this certificate or CRL.
        It enables distinct keys used by the same CA to be distinguished.
        """
        return self.__authorityKeyIdentifier

    @authorityKeyIdentifier.setter
    def authorityKeyIdentifier(self, value):
        self.__authorityKeyIdentifier = value

    @property
    def authorityCertificationSerialNumber(self):
        """
        Authority certification serial number.
        """
        return self.__authorityCertificationSerialNumber

    @authorityCertificationSerialNumber.setter
    def authorityCertificationSerialNumber(self, value):
        self.__authorityCertificationSerialNumber = value

    @property
    def basicConstraints(self):
        """
        Indicates if the Subject may act as a CA.
        """
        return self.__basicConstraints

    @basicConstraints.setter
    def basicConstraints(self, value):
        self.__basicConstraints = value

    @property
    def extendedKeyUsage(self):
        """
        Indicates that a certificate can be used as an TLS server or client certificate.
        """
        return self.__extendedKeyUsage

    @extendedKeyUsage.setter
    def extendedKeyUsage(self, value):
        self.__extendedKeyUsage = value

    @property
    def signatureAlgorithm(self):
        """
        Signature algorithm.
        """
        return self.__signatureAlgorithm

    @signatureAlgorithm.setter
    def signatureAlgorithm(self, value):
        self.__signatureAlgorithm = value

    @property
    def signatureParameters(self):
        """
        Signature Parameters.
        """
        return self.__signatureParameters

    @signatureParameters.setter
    def signatureParameters(self, value):
        self.__signatureParameters = value

    @property
    def publicKey(self):
        """
        Public key.
        """
        return self.__publicKey

    @publicKey.setter
    def publicKey(self, value):
        self.__publicKey = value

    @property
    def publicKeyAlgorithm(self):
        """
        Public Key algorithm.
        """
        return self.__publicKeyAlgorithm

    @publicKeyAlgorithm.setter
    def publicKeyAlgorithm(self, value):
        self.__publicKeyAlgorithm = value

    @property
    def publicKeyParameters(self):
        """
        Parameters.
        """
        return self.__publicKeyParameters

    @publicKeyParameters.setter
    def publicKeyParameters(self, value):
        self.__publicKeyParameters = value

    @property
    def signature(self):
        """
        Signature.
        """
        return self.__signature

    @signature.setter
    def signature(self, value):
        self.__signature = value

    @property
    def subject(self):
        """
        Subject. Example: "CN=Test, O=Gurux, L=Tampere, C=FI".
        """
        return self.__subject

    @subject.setter
    def subject(self, value):
        self.__subject = value

    @property
    def subjectAlternativeName(self):
        """
        Subject Alternative Name.
        """
        return self.__subjectAlternativeName

    @subjectAlternativeName.setter
    def subjectAlternativeName(self, value):
        self.__subjectAlternativeName = value

    @property
    def issuer(self):
        """
        Issuer. Example: "CN=Test O=Gurux, L=Tampere, C=FI".
        """
        return self.__issuer

    @issuer.setter
    def issuer(self, value):
        self.__issuer = value

    @property
    def issuerRaw(self):
        """
        Raw Issuer in ASN1 format.
        """
        return self.__issuerRaw

    @property
    def authorityCertIssuer(self):
        """
        Authority Cert Issuer. Example: "CN=Test O=Gurux, L=Tampere, C=FI".
        """
        return self.__authorityCertIssuer

    @authorityCertIssuer.setter
    def authorityCertIssuer(self, value):
        self.__authorityCertIssuer = value

    @property
    def serialNumber(self):
        """
        Serial number.
        """
        return self.__serialNumber

    @serialNumber.setter
    def serialNumber(self, value):
        self.__serialNumber = value

    @property
    def version(self):
        """
        Version.
        """
        return self.__version

    @property
    def validFrom(self):
        """
        Validity from.
        """
        return self.__validFrom

    @validFrom.setter
    def validFrom(self, value):
        self.__validFrom = value

    @property
    def validTo(self):
        """
        Validity to.
        """
        return self.__validTo

    @validTo.setter
    def validTo(self, value):
        self.__validTo = value

    @property
    def keyUsage(self):
        """
        Indicates the purpose for which the certified public key is used.
        """
        return self.__keyUsage

    @keyUsage.setter
    def keyUsage(self, value):
        self.__keyUsage = value

    def __init__(self, data=None):
        """
        Constructor.
        """
        if data:
            self.__init(data)

    @classmethod
    def fromHexString(cls, data):
        """
        Create x509Certificate from hex string.

            Parameters:
                data: Hex string.
            Returns:
                x509 certificate
        """
        cert = GXx509Certificate()
        cert.__init(GXByteBuffer.hexToBytes(data))
        return cert

    @classmethod
    def fromPem(cls, data):
        """
        Create x509Certificate from PEM string.

            Parameters:
                data: PEM string.

            Returns:
                x509 certificate
        """
        data = data.replace("\r\n", "\n")
        START = "CERTIFICATE-----\n"
        END = "-----END"
        data = data.replace("\r\n", "\n")
        start = data.find(START)
        if start == -1:
            raise ValueError("Invalid PEM file.")
        desc = None
        if start != 11:
            desc = data[:start]
            DESCRIPTION = "#Description"
            # Check if there is a description metadata.
            descStart = desc.rfind(DESCRIPTION)
            if descStart != -1:
                descEnd = desc.find("\n", descStart, start)
                desc = desc[descStart + len(DESCRIPTION), descEnd - len(DESCRIPTION)]
                desc = desc.strip()
            else:
                desc = None

        data = data[start + len(START) :]
        end = data.find(END)
        if end == -1:
            raise ValueError("Invalid PEM file.")
        cert = cls.fromDer(data[0:end])
        cert.description = desc
        return cert

    @classmethod
    def fromDer(cls, der):
        """
        Create x509Certificate from DER Base64 encoded string.

            Parameters:
                der: Base64 DER string.

            Returns:
                x509 certificate
        """
        der = der.replace("\r\n", "")
        der = der.replace("\n", "")
        cert = GXx509Certificate()
        cert.__init(_GXCommon.fromBase64(der))
        return cert

    # pylint: disable=import-outside-toplevel, too-many-locals, protected-access
    def __init(self, data):
        from .GXAsn1Converter import GXAsn1Converter
        from ..ecdsa.GXPublicKey import GXPublicKey

        self.__rawData = data
        seq = GXAsn1Converter.fromByteArray(data)
        if len(seq) != 3:
            raise GXDLMSCertificateException(
                "Invalid Certificate Version. Wrong number of elements in sequence."
            )

        if not isinstance(seq[0], GXAsn1Sequence):
            certType = GXAsn1Converter.__getCertificateType(data, seq)
            if certType == PkcsType.PKCS8:
                raise GXDLMSCertificateException(
                    "Invalid Certificate. This is PKCS 8 private key, not x509 certificate."
                )
            if certType == PkcsType.PKCS10:
                raise GXDLMSCertificateException(
                    "Invalid Certificate. This is PKCS 10 certification requests, not x509 certificate."
                )
            raise GXDLMSCertificateException("Invalid Certificate Version.")

        req_info = seq[0]

        if isinstance(req_info[0], GXAsn1Integer):
            raise GXDLMSCertificateException(
                "Invalid Certificate. DLMS certificate version number must be integer."
            )

        self.__version = CertificateVersion(req_info[0][0])
        self.__serialNumber = req_info[1]
        self.__signatureAlgorithm = HashAlgorithmConverter.fromString(
            str(req_info[2][0])
        )
        if self.__signatureAlgorithm not in [
            HashAlgorithm.SHA256WITH_ECDSA,
            HashAlgorithm.SHA384WITH_ECDSA,
        ]:
            raise Exception(
                "DLMS certificate must be signed with ECDSA with SHA256 or SHA384."
            )

        if len(req_info[2]) > 1:
            self.__signatureParameters = req_info[2][1]

        self.__issuerRaw = GXAsn1Converter.toByteArray(req_info[3])
        self.__issuer = GXAsn1Converter.getSubject(req_info[3])

        validity = req_info[4]

        self.__validFrom = validity[0]
        self.__validTo = validity[1]
        self.__subject = GXAsn1Converter.getSubject(req_info[5])

        subject_pk_info = req_info[6]
        self.__publicKey = GXPublicKey.fromRawBytes(subject_pk_info[1].value)
        GXEcdsa.validate(self.__publicKey)
        basicConstraintsExists = False
        if len(req_info) > 7:
            for s in req_info[7][0]:
                oid = s[0]
                value = s[1]
                cert_type = X509CertificateTypeConverter.fromString(str(oid))

                if cert_type == X509CertificateType.SUBJECT_KEY_IDENTIFIER:
                    self.subject_key_identifier = value

                elif cert_type == X509CertificateType.SUBJECT_ALTERNATIVE_NAME:
                    alt_names = []
                    for it in value:
                        alt_names.append("DNS:" + it[0].decode("ascii"))
                    self.subject_alternative_name = ", ".join(alt_names)

                elif cert_type == X509CertificateType.AUTHORITY_KEY_IDENTIFIER:
                    for it in value:
                        if it.index == 0:
                            self.authority_key_identifier = it[0]
                        elif it.index == 1:
                            pairs = [
                                f"{X509NameConverter.fromString(str(k))}={v}"
                                for k, v in it[0][0]
                            ]
                            self.authority_cert_issuer = ", ".join(pairs)
                        elif it.index == 2:
                            self.__authorityCertificationSerialNumber = int.from_bytes(
                                it[0], "big"
                            )
                        else:
                            raise Exception(f"Invalid context. {it.index}")

                elif cert_type == X509CertificateType.KEY_USAGE:
                    if isinstance(value, GXBitString):
                        self.__keyUsage = KeyUsage(value.toInteger())
                    else:
                        self.__keyUsage = KeyUsage(value[2].toInteger())

                elif cert_type == X509CertificateType.EXTENDED_KEY_USAGE:
                    self.__extendedKeyUsage = ExtendedKeyUsage.NONE
                    for it in value:
                        if it.object_identifier == "1.3.6.1.5.5.7.3.1":
                            self.__extendedKeyUsage |= ExtendedKeyUsage.SERVER_AUTH
                        elif it.object_identifier == "1.3.6.1.5.5.7.3.2":
                            self.__extendedKeyUsage |= ExtendedKeyUsage.CLIENT_AUTH
                        else:
                            raise Exception("Invalid extended key usage.")

                elif cert_type == X509CertificateType.BASIC_CONSTRAINTS:
                    basicConstraintsExists = True
                    if isinstance(value, GXAsn1Sequence) and len(value) > 0:
                        self.basic_constraints = bool(value[0])
                    else:
                        self.basic_constraints = bool(value)

        if not basicConstraintsExists:
            cnFound = False
            for k, v in req_info[5]:
                if (
                    X509NameConverter.getString(X509Name.CN) == str(k)
                    and len(str(v)) == 16
                ):
                    cnFound = True
                    break
            if not cnFound:
                raise GXDLMSCertificateException(
                    "Common name doesn't exist or system title is invalid."
                )

        if self.__keyUsage == KeyUsage.NONE:
            raise Exception("Key usage not present. It's mandatory.")

        if (
            self.__keyUsage & (KeyUsage.KEY_CERT_SIGN | KeyUsage.CRL_SIGN)
        ) and not basicConstraintsExists:
            raise Exception("Basic Constraints value not present. It's mandatory.")

        if (
            self.__keyUsage == (KeyUsage.DIGITAL_SIGNATURE | KeyUsage.KEY_AGREEMENT)
            and self.__extendedKeyUsage == ExtendedKeyUsage.NONE
        ):
            raise Exception("Extended key usage not present. It's mandatory for TLS.")

        if self.__extendedKeyUsage != ExtendedKeyUsage.NONE and self.__keyUsage != (
            KeyUsage.DIGITAL_SIGNATURE | KeyUsage.KEY_AGREEMENT
        ):
            raise Exception("Extended key usage present. It's used only for TLS.")

        self.__publicKeyAlgorithm = HashAlgorithmConverter.fromString(str(seq[1][0]))

        if self.__publicKeyAlgorithm not in [
            HashAlgorithm.SHA256WITH_ECDSA,
            HashAlgorithm.SHA384WITH_ECDSA,
        ]:
            raise Exception(
                "DLMS certificate must be signed with ECDSA with SHA256 or SHA384."
            )

        if len(seq[1]) > 1:
            self.__publicKeyParameters = seq[1][1]
        self.__signature = seq[2].value

    # pylint: disable=import-outside-toplevel,too-many-locals
    def getDataList(self):
        from .GXAsn1Converter import GXAsn1Converter

        if not self.issuer:
            raise ValueError("Issuer is empty.")
        if not self.subject:
            raise ValueError("Subject is empty.")

        a = GXAsn1ObjectIdentifier(
            HashAlgorithmConverter.getString(self.__signatureAlgorithm)
        )

        p = GXAsn1Context()
        p.append(GXInt8(self.version))

        s = GXAsn1Sequence()

        if self.__subjectKeyIdentifier:
            s1 = GXAsn1Sequence()
            s1.append(
                GXAsn1ObjectIdentifier(
                    X509CertificateTypeConverter.getString(
                        X509CertificateType.SUBJECT_KEY_IDENTIFIER
                    )
                )
            )
            bb = GXByteBuffer()
            bb.setUInt8(BerType.OCTET_STRING)
            _GXCommon.setObjectCount(len(self.__subjectKeyIdentifier), bb)
            bb.set(self.__subjectKeyIdentifier)
            s1.append(bb.array())
            s.append(s1)

            if (
                self.authorityKeyIdentifier
                or self.authorityCertIssuer
                or self.authorityCertificationSerialNumber
            ):
                s1 = GXAsn1Sequence()
                s1.append(
                    GXAsn1ObjectIdentifier(
                        X509CertificateTypeConverter.getString(
                            X509CertificateType.AUTHORITY_KEY_IDENTIFIER
                        )
                    )
                )
                s.append(s1)
                s2 = GXAsn1Context()
                s2.index = 3
                c1 = GXAsn1Sequence()
                if self.authorityKeyIdentifier:
                    c4 = GXAsn1Context()
                    c4.constructed = False
                    c4.index = 0
                    c4.append(self.authorityKeyIdentifier)
                    c1.append(c4)
                    s1.append(GXAsn1Converter.toByteArray(c1))

                if self.authorityCertIssuer:
                    c2 = GXAsn1Context()
                    c2.index = 1
                    c1.append(c2)
                    c3 = GXAsn1Context()
                    c3.index = 4
                    c2.append(c3)
                    c3.append(GXAsn1Converter.encodeSubject(self.authorityCertIssuer))
                    s2.append(c1)
                if self.authorityCertificationSerialNumber:
                    c4 = GXAsn1Context()
                    c4.constructed = False
                    c4.index = 2
                    tmp5 = self.authorityCertificationSerialNumber.toByteArray()
                    tmp5.reverse()
                    c4.append(tmp5)
                    c1.append(c4)
                    s1.append(GXAsn1Converter.toByteArray(c1))
        # BasicConstraints
        s1 = GXAsn1Sequence()
        s1.append(
            GXAsn1ObjectIdentifier(
                X509CertificateTypeConverter.getString(
                    X509CertificateType.BASIC_CONSTRAINTS
                )
            )
        )
        seq = GXAsn1Sequence()

        if self.__basicConstraints:
            s1.append(self.__basicConstraints)
        elif self.__keyUsage == KeyUsage.NONE:
            raise Exception("Key usage not present.")

        s1.append(GXAsn1Converter.toByteArray(seq))
        s.append(s1)

        # KeyUsage
        s1 = GXAsn1Sequence()
        s1.append(
            GXAsn1ObjectIdentifier(
                X509CertificateTypeConverter.getString(X509CertificateType.KEY_USAGE)
            )
        )

        keyUsage = _GXCommon.swapBits(self.__keyUsage)
        min_bit = min([bit for bit in KeyUsage if (bit & keyUsage)])
        ignore = min_bit.bit_length() - 1 if min_bit else 0

        bs = GXBitString([ignore % 8, keyUsage])
        s1.append(GXAsn1Converter.toByteArray(bs))
        s.append(s1)

        # ExtendedKeyUsage
        if self.__extendedKeyUsage != ExtendedKeyUsage.NONE:
            s1 = GXAsn1Sequence()
            s1.append(
                GXAsn1ObjectIdentifier(
                    X509CertificateTypeConverter.getString(
                        X509CertificateType.EXTENDED_KEY_USAGE
                    )
                )
            )
            s2 = GXAsn1Sequence()
            if self.__extendedKeyUsage & ExtendedKeyUsage.SERVER_AUTH:
                s2.append(GXAsn1ObjectIdentifier("1.3.6.1.5.5.7.3.1"))
            if self.__extendedKeyUsage & ExtendedKeyUsage.CLIENT_AUTH:
                s2.append(GXAsn1ObjectIdentifier("1.3.6.1.5.5.7.3.2"))

            s1.append(GXAsn1Converter.toByteArray(s2))
            s.append(s1)

        valid = GXAsn1Sequence()
        valid.append(self.__validFrom)
        valid.append(self.__validTo)
        if self.__publicKey.scheme == Ecc.P256:
            alg = GXAsn1ObjectIdentifier("1.2.840.10045.3.1.7")
        else:
            alg = GXAsn1ObjectIdentifier("1.3.132.0.34")
        tmp3 = GXArray((GXAsn1ObjectIdentifier("1.2.840.10045.2.1"), alg))
        tmp4 = GXAsn1Context()
        tmp4.index = 3
        tmp4.append(s)

        tmp2 = GXArray((tmp3, GXBitString(self.__publicKey.rawValue, 0)))
        if self.signatureParameters:
            p2 = GXArray((a, self.signatureParameters))
        else:
            p2 = GXArray((a,))

        return GXArray(
            (
                p,
                GXAsn1Integer(self.__serialNumber),
                p2,
                GXAsn1Converter.encodeSubject(self.__issuer),
                valid,
                GXAsn1Converter.encodeSubject(self.__subject),
                tmp2,
                tmp4,
            )
        )

    # pylint: disable=import-outside-toplevel
    @property
    def encoded(self):
        from .GXAsn1Converter import GXAsn1Converter

        if self.__rawData:
            return self.__rawData
        tmp = GXArray(
            (
                GXAsn1ObjectIdentifier(
                    HashAlgorithmConverter.getString(self.signatureAlgorithm)
                ),  # Don't remove the comma.
            )
        )
        list_ = GXArray((self.getDataList(), tmp, GXBitString(self.signature, 0)))
        self.__rawData = GXAsn1Converter.toByteArray(list_)
        return self.__rawData

    # pylint: disable=import-outside-toplevel
    def getData(self):
        """
        Get data as byte array.
        """
        from .GXAsn1Converter import GXAsn1Converter

        return GXAsn1Converter.toByteArray(self.getDataList())

    def __str__(self):
        if self.extendedKeyUsage == ExtendedKeyUsage.SERVER_AUTH:
            bb = "Server certificate" + os.linesep
        elif ExtendedKeyUsage == ExtendedKeyUsage.CLIENT_AUTH:
            bb = "Client certificate" + os.linesep
        elif ExtendedKeyUsage == (
            ExtendedKeyUsage.SERVER_AUTH | ExtendedKeyUsage.CLIENT_AUTH
        ):
            bb = "TLS certificate" + os.linesep
        bb += os.linesep
        bb += "Version: " + str(self.version)
        bb += os.linesep + "SerialNumber: " + str(self.serialNumber)
        bb += os.linesep + "Signature: " + str(self.signatureAlgorithm)
        bb += ", OID = "
        bb += HashAlgorithmConverter.getString(self.signatureAlgorithm)
        bb += os.linesep
        bb += "Issuer: " + self.issuer
        bb += os.linesep
        bb += "Validity: [From: " + str(self.validFrom)
        bb += " GMT To: " + str(self.validTo) + " GMT]" + os.linesep
        bb += "Subject: "
        bb += self.subject
        bb += os.linesep
        bb += "Public Key Algorithm: "
        bb += str(self.publicKeyAlgorithm)
        bb += os.linesep
        bb += "Key: "
        bb += self.publicKey.toHex()
        bb += os.linesep
        if self.publicKey.scheme == Ecc.P256:
            bb += "ASN1 OID: prime256v1" + os.linesep
            bb += "NIST CURVE: P-256"
        elif self.publicKey.scheme == Ecc.P384:
            bb += "ASN1 OID: prime384v1" + os.linesep
            bb += os.linesep
            bb += "NIST CURVE: P-384"
        bb += os.linesep
        bb += "Basic constraints: "
        bb += self.basicConstraints
        bb += os.linesep
        bb += "SubjectKeyIdentifier: "
        bb += GXByteBuffer.hex(self.subjectKeyIdentifier, True)
        bb += os.linesep
        bb += "KeyUsage: "
        bb += str(self.keyUsage)
        bb += os.linesep
        bb += "Signature Algorithm: "
        bb += str(self.signatureAlgorithm)
        bb += os.linesep
        bb += "Signature: "
        bb += GXByteBuffer.hex(self.signature, False)
        bb += os.linesep
        return bb

    @classmethod
    def load(cls, path):
        """
        Load x509 certificate from the PEM file.

            Parameters:
                path: File path.

            Returns:
                Created GXx509Certificate object.
        """
        with open(path, "r", encoding="utf-8") as file:
            return cls.fromPem(file.read())

    def save(self, path):
        """
        x509 certificate to PEM file.

            Parameters:
                path: File path.
        """
        with open(path, "w", encoding="utf-8") as file:
            file.write(self.toPem())

    def toPem(self):
        """
           x509 certificate in PEM format.
        *
        * @return Public key as in PEM string.
        """
        if not self.publicKey:
            raise ValueError("Public or private key is not set.")
        sb = ""
        if self.description:
            sb = "#Description"
            sb += self.description + "\r"
        sb += "-----BEGIN CERTIFICATE-----\r"
        sb += self.toDer()
        sb += "\r-----END CERTIFICATE-----\r"
        return sb

    def toDer(self):
        """
           x509 certificate in DER format.
        *
        * @return Public key as in PEM string.
        """
        return _GXCommon.toBase64(self.encoded)

    def __eq__(self, other):
        return (
            isinstance(other, GXx509Certificate)
            and self.serialNumber == other.serialNumber
        )

    # pylint: disable=import-outside-toplevel,protected-access
    def isCertified(self, certifier):
        """
        Test is x509 file certified by the certifier.

            Parameters:
                certifier: Public key of the certifier.

            Returns:
                True, if certifier has certified the certificate.
        """
        from .GXAsn1Converter import GXAsn1Converter

        if not certifier:
            raise ValueError("certifier")
        # Get raw data
        tmp2 = GXByteBuffer()
        tmp2.set(self.encoded)
        GXAsn1Converter._getNext(tmp2)
        tmp2.size = tmp2.position
        tmp2.position = 1
        _GXCommon.getObjectCount(tmp2)
        e = GXEcdsa(certifier)
        tmp3 = GXAsn1Converter.fromByteArray(self.signature)
        bb = GXByteBuffer()
        if self.signatureAlgorithm == HashAlgorithm.SHA256WITH_ECDSA:
            size = 32
        else:
            size = 48
        # Some implementations might add extra byte. It must removed.
        if len(tmp3[0]).value == size:
            start = 0
        else:
            start = 1
        bb.set(tmp3[0].value, start, size)
        if len(tmp3[1]).value == size:
            start = 0
        else:
            start = 1
        bb.set(tmp3[1].value, start, size)
        return e.verify(bb.array(), tmp2.subArray(tmp2.position, tmp2.available))

    # pylint: disable=import-outside-toplevel, bare-except
    @classmethod
    def search(cls, folder, type_, systemtitle):
        """
        Search x509 Certificate from the PEM file in given folder.

            Parameters:
                folder: Folder to search.
                type: Certificate type.

            Returns:
                Created GXPkcs8 object.
        """
        from .GXAsn1Converter import GXAsn1Converter

        if type_ == CertificateType.DIGITAL_SIGNATURE:
            usage = KeyUsage.DIGITAL_SIGNATURE
        elif type_ == CertificateType.KEY_AGREEMENT:
            usage = KeyUsage.KEY_AGREEMENT
        elif type_ == CertificateType.TLS:
            usage = KeyUsage.DIGITAL_SIGNATURE | KeyUsage.KEY_AGREEMENT
        else:
            usage = KeyUsage.NONE
        subject = GXAsn1Converter.systemTitleToSubject(systemtitle)
        certificates = []
        files = [
            f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))
        ]
        for it in files:
            if it.endswith(".pem") or it.endswith(".cer"):
                try:
                    cert = cls.load(it)
                    if (
                        usage in (KeyUsage.NONE, cert.keyUsage)
                    ) and cert.subject.contains(subject):
                        certificates.append(cert)
                except:
                    pass
        return certificates

    # pylint: disable=import-outside-toplevel
    def getSystemTitle(self):
        """
        Returns system title from the certificate.
        """
        from .GXAsn1Converter import GXAsn1Converter

        if not self.subject:
            return None
        return GXByteBuffer.hexToBytes(
            GXAsn1Converter.hexSystemTitleFromSubject(self.subject)
        )

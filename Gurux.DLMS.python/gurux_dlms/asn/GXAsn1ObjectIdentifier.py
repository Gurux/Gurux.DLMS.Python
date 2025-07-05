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
from gurux_dlms.GXByteBuffer import GXByteBuffer
from gurux_dlms.asn.enums.HashAlgorithm import HashAlgorithm
from gurux_dlms.asn.enums.PkcsObjectIdentifier import PkcsObjectIdentifier
from gurux_dlms.asn.enums.X509CertificateType import X509CertificateType
from gurux_dlms.asn.enums.X509Name import X509Name
from gurux_dlms.asn.enums.X9ObjectIdentifier import X9ObjectIdentifier
from .X509NameConverter import X509NameConverter
from .HashAlgorithmConverter import HashAlgorithmConverter
from .PkcsObjectIdentifierConverter import PkcsObjectIdentifierConverter
from .X9ObjectIdentifierConverter import X9ObjectIdentifierConverter
from .X509CertificateTypeConverter import X509CertificateTypeConverter


class GXAsn1ObjectIdentifier:
    __objectIdentifier = ""

    @property
    def objectIdentifier(self):
        return self.__objectIdentifier

    @property
    def encoded(self):
        return self.oidStringtoBytes(self.__objectIdentifier)

    @property
    def description(self):
        tmp = X509NameConverter.fromString(self.__objectIdentifier)
        if tmp != X509Name.NONE:
            return X509NameConverter.getString(tmp)
        tmp = HashAlgorithmConverter.fromString(self.objectIdentifier)
        if tmp != HashAlgorithm.NONE:
            return HashAlgorithmConverter.getString(tmp)
        tmp = X9ObjectIdentifierConverter.fromString(self.objectIdentifier)
        if tmp != X9ObjectIdentifier.NONE:
            return X9ObjectIdentifierConverter.getString(tmp)
        tmp = PkcsObjectIdentifierConverter.fromString(self.__objectIdentifier)
        if tmp != PkcsObjectIdentifier.NONE:
            return PkcsObjectIdentifierConverter.getString(tmp)
        tmp = X509CertificateTypeConverter.fromString(self.__objectIdentifier)
        if tmp != X509CertificateType.NONE:
            return X509CertificateTypeConverter.getString(tmp)
        return None

    @classmethod
    def __oidStringFromBytes(cls, bb, len_):
        """
        Get OID string from bytes.

            Parameters:
                bb: converted bytes.
                len: byte count.

            Returns:
                OID string.
        """
        sb = ""
        value = 0
        if len_ != 0:
            # pylint: disable=unused-variable
            # Get first byte.
            tmp = bb.getUInt8()
            sb += str(int(tmp / 40))
            sb += "."
            sb += str(tmp % 40)
            for pos in range(1, len_):
                tmp = bb.getUInt8()
                if (tmp & 0x80) != 0:
                    value += tmp & 0x7F
                    value <<= 7
                else:
                    value += tmp
                    sb += "."
                    sb += str(value)
                    value = 0
        return sb

    @classmethod
    def oidStringtoBytes(cls, oid):
        """
        Convert OID string to bytes.
        """
        arr = oid.strip().split(".")
        # Make first byte.
        tmp = GXByteBuffer()
        value = int(arr[0]) * 40
        value += int(arr[1])
        tmp.setUInt8(value)
        for pos in range(2, len(arr)):
            value = int(arr[pos])
            if value < 0x80:
                tmp.setUInt8(value)
            elif value < 0x4000:
                tmp.setUInt8((0x80 | (value >> 7)))
                tmp.setUInt8((value & 0x7F))
            elif value < 0x200000:
                tmp.setUInt8((0x80 | (value >> 14)))
                tmp.setUInt8((0x80 | (value >> 7)))
                tmp.setUInt8((value & 0x7F))
            elif value < 0x10000000:
                tmp.setUInt8((0x80 | (value >> 21)))
                tmp.setUInt8((0x80 | (value >> 14)))
                tmp.setUInt8((0x80 | (value >> 7)))
                tmp.setUInt8((value & 0x7F))
            elif value < 0x800000000:
                tmp.setUInt8((0x80 | (value >> 49)))
                tmp.setUInt8((0x80 | (value >> 42)))
                tmp.setUInt8((0x80 | (value >> 35)))
                tmp.setUInt8((0x80 | (value >> 28)))
                tmp.setUInt8((0x80 | (value >> 21)))
                tmp.setUInt8((0x80 | (value >> 14)))
                tmp.setUInt8((0x80 | (value >> 7)))
                tmp.setUInt8((value & 0x7F))
            else:
                raise ValueError("Invalid OID.")
        return tmp.array()

    def __str__(self):
        return self.__objectIdentifier

    def __init__(self, oid, count=None):
        """
        Constructor.

            Parameters:
                oid: Object identifier in dotted format.
        """
        if isinstance(oid, GXByteBuffer):
            self.__objectIdentifier = self.__oidStringFromBytes(oid, count)
        elif isinstance(oid, str):
            self.__objectIdentifier = oid
        else:
            raise ValueError("Invalid Object identifier.")

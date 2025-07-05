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
import datetime
from gurux_dlms.GXByteBuffer import GXByteBuffer
from gurux_dlms.objects.enums.CertificateType import CertificateType
from gurux_dlms.internal._GXCommon import _GXCommon
from gurux_dlms.enums.BerType import BerType
from .GXAsn1Context import GXAsn1Context
from .enums.X509Name import X509Name
from .GXAsn1Ia5String import GXAsn1Ia5String
from .GXAsn1Utf8String import GXAsn1Utf8String
from .GXAsn1ObjectIdentifier import GXAsn1ObjectIdentifier
from .X509NameConverter import X509NameConverter
from .GXAsn1Sequence import GXAsn1Sequence
from .GXAsn1Integer import GXAsn1Integer
from ..GXBitString import GXBitString
from .enums.KeyUsage import KeyUsage
from .GXx509Certificate import GXx509Certificate
from .enums.PkcsType import PkcsType
from ..GXInt8 import GXInt8
from ..GXInt16 import GXInt16
from ..GXInt32 import GXInt32
from ..GXInt64 import GXInt64
from ..GXArray import GXArray
from ..asn.GXAsn1PublicKey import GXAsn1PublicKey


class GXAsn1Converter:
    """
    ASN1 converter. This class is used to convert public and private keys to byte array and vice verse.
    """

    @classmethod
    def encodeSubject(cls, value):
        list_ = []
        for tmp in value.split(","):
            it = tmp.split("=")
            if len(it) != 2:
                raise ValueError("Invalid subject.")
            name = X509Name.valueofString(it[0].strip())
            if name == X509Name.C:
                # Country code is printable string
                val = it[1]
            elif name == X509Name.E:
                # email address in Verisign certificates
                val = GXAsn1Ia5String(it[1].strip())
            else:
                val = GXAsn1Utf8String(it[1].strip())
            oid = X509NameConverter.getString(name)
            list_.append((GXAsn1ObjectIdentifier(oid), val))
        return list_

    @classmethod
    def getSubject(cls, values):
        sb = ""
        first = True
        for k, v in values:
            if first:
                first = False
            else:
                sb += ", "
            sb += str(X509NameConverter.fromString(str(k)))
            sb += "="
            sb += str(v)
        return sb

    # pylint: disable=too-many-locals
    @classmethod
    def __getValue(cls, bb, objects, s, getNext):
        type_ = bb.getUInt8()
        len_ = _GXCommon.getObjectCount(bb)
        if len_ > bb.available():
            raise ValueError("GXAsn1Converter.GetValue")
        connectPos = 0
        if s:
            connectPos = s.xmlLength
        start = bb.position
        tagString = ""
        if s:
            s.appendSpaces()
            if type == BerType.INTEGER:
                if len_ in (1, 2, 4, 8):
                    tagString = s.getTag(-len_)
                else:
                    tagString = s.getTag(BerType.INTEGER)
            else:
                tagString = s.GetTag(type_)
            s.append("<" + tagString + ">")

        if type_ in (
            (BerType.CONSTRUCTED | BerType.CONTEXT),
            (BerType.CONSTRUCTED | BerType.CONTEXT | 1),
            (BerType.CONSTRUCTED | BerType.CONTEXT | 2),
            (BerType.CONSTRUCTED | BerType.CONTEXT | 3),
            (BerType.CONSTRUCTED | BerType.CONTEXT | 4),
            (BerType.CONSTRUCTED | BerType.CONTEXT | 5),
        ):
            if s:
                s.increase()
            tmp = GXAsn1Context()
            tmp.index = type_ & 0xF
            objects.append(tmp)
            while bb.position < start + len_:
                cls.__getValue(bb, tmp, s, False)
            if s:
                s.decrease()
        elif type_ == (BerType.CONSTRUCTED | BerType.SEQUENCE):
            if s:
                s.increase()
            tmp = GXAsn1Sequence()
            objects.append(tmp)
            cnt = 0
            while bb.position < start + len_:
                cnt += 1
                cls.__getValue(bb, tmp, s, False)
                if getNext:
                    break
            if s:
                # Append comment.
                s.appendComment(connectPos, str(cnt) + " elements.")
                s.decrease()
        elif type_ == (BerType.CONSTRUCTED | BerType.SET):
            if s:
                s.increase()
            tmp = []
            cls.__getValue(bb, tmp, s, False)
            if isinstance(tmp[0], GXAsn1Sequence):
                tmp = tmp[0]
                v = None
                if len(tmp) != 1:
                    v = tmp[1]
                objects.append((tmp[0], v))
            else:
                e = (tmp, None)
                objects.append(e)
            if s:
                s.decrease()
        elif type_ == BerType.OBJECT_IDENTIFIER:
            oi = GXAsn1ObjectIdentifier(bb, len_)
            objects.append(oi)
            if s:
                if oi.description:
                    s.appendComment(connectPos, oi.description)
                s.append(str(oi))
        elif type_ == BerType.PRINTABLE_STRING:
            str_ = bb.getString(bb.position, len_)
            bb.position += len_
            objects.append(str_)
            if s:
                s.Append(str_)
        elif type_ == BerType.BMP_STRING:
            str_ = bb.GetStringUnicode(len_)
            objects.append(str_)
            if s:
                s.Append(str_)
        elif type_ == BerType.UTF8STRING:
            objects.append(GXAsn1Utf8String(bb.getString(bb.position, len_)))
            bb.position += len_
            if s:
                s.append(str(objects[len(objects) - 1]))
        elif type_ == BerType.IA5_STRING:
            objects.append(GXAsn1Ia5String(bb.getString(len_)))
            if s:
                s.Append(str(objects[len(objects) - 1]))
        elif type_ == BerType.INTEGER:
            if len_ == 1:
                objects.append(bb.getInt8())
            elif len_ == 2:
                objects.append(bb.getInt16())
            elif len_ == 4:
                objects.append(bb.getInt32())
            else:
                tmp2 = bytearray(len_)
                bb.get(tmp2)
                objects.append(GXAsn1Integer(tmp2))
            if s:
                s.Append(str(objects[len(objects) - 1]))
        elif type_ == BerType.NULL:
            objects.append(None)
        elif type_ == BerType.BIT_STRING:
            tmp3 = GXBitString(bb.subArray(bb.position, len_))
            objects.append(tmp3)
            bb.position += len_
            if s:
                # Append comment.
                s.appendComment(connectPos, str(len(tmp3)) + " bit.")
                s.append(str(tmp3))
        elif type_ == BerType.UTC_TIME:
            tmp2 = bytearray(len_)
            bb.get(tmp2)
            objects.append(cls.__getUtcTime(tmp2.decode("utf-8")))
            if s:
                s.append(str(objects[objects.Count - 1]))
        elif type_ == BerType.GENERALIZED_TIME:
            tmp2 = bytes(len_)
            bb.get(tmp2)
            objects.append(_GXCommon.getGeneralizedTime(str(tmp2)))
            if s:
                s.append(str(objects[objects.Count - 1]))
        elif type_ in (
            BerType.CONTEXT,
            (BerType.CONTEXT | 1),
            (BerType.CONTEXT | 2),
            (BerType.CONTEXT | 3),
            (BerType.CONTEXT | 4),
            (BerType.CONTEXT | 5),
            (BerType.CONTEXT | 6),
        ):
            tmp = GXAsn1Context()
            tmp.constructed = False
            tmp.index = type_ & 0xF
            tmp2 = bytearray(len_)
            bb.get(tmp2)
            tmp.append(tmp2)
            objects.append(tmp)
            if s:
                s.append(GXByteBuffer.toHex(tmp2, False))
        elif type_ == BerType.OCTET_STRING:
            t = bb.getUInt8(bb.position)
            if t in ((BerType.CONSTRUCTED | BerType.SEQUENCE), BerType.BIT_STRING):
                if s:
                    s.increase()
                cls.__getValue(bb, objects, s, False)
                if s:
                    s.decrease()
            else:
                tmp2 = bytearray(len_)
                bb.get(tmp2)
                objects.append(tmp2)
                if s:
                    s.append(GXByteBuffer.toHex(tmp2, False))
        elif type_ == BerType.BOOLEAN:
            b = bb.getUInt8() != 0
            objects.append(b)
            if s:
                s.append(str(b))
        else:
            raise ValueError("Invalid type: " + str(type_))
        if s:
            s.append("</" + tagString + ">\r\n")

    @classmethod
    def __getUtcTime(cls, dateString):
        year = 2000 + int(dateString[0:2])
        month = int(dateString[2:4])
        day = int(dateString[4:6])
        hour = int(dateString[6:8])
        minute = int(dateString[8:10])
        # If UTC time.
        if dateString.find("Z") != -1:
            second = 0
            if len(dateString) > 11:
                second = int(dateString[10:12])
            return datetime.datetime(year, month, day, hour, minute, second, 0)
        if len(dateString) > 15:
            second = int(dateString[10:12])
        return datetime.datetime(year, month, day, hour, minute, second, 0)

    @classmethod
    def __dateToString(cls, date):
        sb = f"{date.year - 2000:02d}"
        sb += f"{date.month:02d}"
        sb += f"{date.day:02d}"
        sb += f"{date.hour:02d}"
        sb += f"{date.minute:02d}"
        sb += f"{date.second:02d}"
        sb += "Z"
        return sb

    @classmethod
    def fromByteArray(cls, data):
        """
        Convert byte array to ASN1 objects.

        Parameters:
            data: ASN-1 bytes.

        Returns:
            Parsed objects.
        """
        bb = GXByteBuffer(data)
        objects = []
        while bb.position != bb.size:
            cls.__getValue(bb, objects, None, False)

        if not objects:
            return None
        return objects[0]

    # Get next ASN1 value from the byte buffer.
    @classmethod
    def _getNext(cls, data):
        objects = []
        cls.__getValue(data, objects, None, True)
        return objects[0]

    # add ASN1 object to byte buffer.
    @classmethod
    def __getBytes(cls, bb, target):
        start = bb.size
        cnt = 0
        if isinstance(target, GXAsn1Context):
            tmp = GXByteBuffer()
            for it in target:
                cnt += cls.__getBytes(tmp, it)
            start = bb.size
            if target.constructed:
                bb.setUInt8(BerType.CONSTRUCTED | BerType.CONTEXT | target.index)
                _GXCommon.setObjectCount(cnt, bb)
            else:
                tmp.setUInt8(0, BerType.CONTEXT | target.index)
            cnt += bb.size - start
            bb.set(tmp)
            return cnt
        if isinstance(target, GXArray):
            tmp = GXByteBuffer()
            for it in target:
                cnt += cls.__getBytes(tmp, it)
            start = bb.size
            bb.setUInt8(BerType.CONSTRUCTED | BerType.SEQUENCE)
            _GXCommon.setObjectCount(cnt, bb)
            cnt += bb.size - start
            bb.set(tmp)
            return cnt
        if isinstance(target, str):
            bb.setUInt8(BerType.PRINTABLE_STRING)
            _GXCommon.setObjectCount(len(target), bb)
            bb.set(target)
        elif isinstance(target, GXInt8):
            bb.setUInt8(BerType.INTEGER)
            _GXCommon.setObjectCount(1, bb)
            bb.setInt8(target)
        elif isinstance(target, GXInt16):
            bb.setUInt8(BerType.INTEGER)
            _GXCommon.setObjectCount(2, bb)
            bb.setInt16(target)
        elif isinstance(target, GXInt32):
            bb.setUInt8(BerType.INTEGER)
            _GXCommon.setObjectCount(4, bb)
            bb.setInt32(target)
        elif isinstance(target, GXAsn1Integer):
            bb.setUInt8(BerType.INTEGER)
            b = target.toArray()
            _GXCommon.setObjectCount(len(b), bb)
            bb.set(b)
        elif isinstance(target, GXInt64):
            bb.setUInt8(BerType.INTEGER)
            _GXCommon.setObjectCount(8, bb)
            bb.setInt64(target)
        elif isinstance(target, (bytes, bytearray)):
            bb.setUInt8(BerType.OCTET_STRING)
            _GXCommon.setObjectCount(len(target), bb)
            bb.set(target)
        elif target is None:
            bb.setUInt8(BerType.NULL)
            _GXCommon.setObjectCount(0, bb)
        elif isinstance(target, bool):
            bb.setUInt8(BerType.BOOLEAN)
            bb.setUInt8(1)
            if target:
                bb.setUInt8(255)
            else:
                bb.setUInt8(0)
        elif isinstance(target, GXAsn1ObjectIdentifier):
            bb.setUInt8(BerType.OBJECT_IDENTIFIER)
            t = target.encoded
            _GXCommon.setObjectCount(len(t), bb)
            bb.set(t)
        elif isinstance(target, tuple):
            tmp2 = GXByteBuffer()
            if target[1]:
                tmp = GXByteBuffer()
                cnt += cls.__getBytes(tmp2, target[0])
                cnt += cls.__getBytes(tmp2, target[1])
                tmp.setUInt8(BerType.CONSTRUCTED | BerType.SEQUENCE)
                _GXCommon.setObjectCount(cnt, tmp)
                tmp.set(tmp2)
            else:
                cls.__getBytes(tmp2, target[0])
                tmp = tmp2
            # Update len.
            cnt = bb.size
            bb.setUInt8(BerType.CONSTRUCTED | BerType.SET)
            _GXCommon.setObjectCount(tmp.size, bb)
            bb.set(tmp)
            return bb.size - cnt
        elif isinstance(target, GXAsn1Utf8String):
            bb.setUInt8(BerType.UTF8STRING)
            str_ = str(target)
            _GXCommon.setObjectCount(len(str_), bb)
            bb.set(str_)
        elif isinstance(target, GXAsn1Ia5String):
            bb.setUInt8(BerType.IA5_STRING)
            _GXCommon.setObjectCount(len(target), bb)
            bb.set(target)
        elif isinstance(target, GXBitString):
            bb.setUInt8(BerType.BIT_STRING)
            _GXCommon.setObjectCount(1 + len(target.value), bb)
            bb.setUInt8(target.padBits)
            bb.set(target.value)
        elif isinstance(target, GXAsn1PublicKey):
            bb.setUInt8(BerType.BIT_STRING)
            # size is 64 bytes + padding and uncompressed point indicator.
            _GXCommon.setObjectCount(66, bb)
            # add padding.
            bb.setUInt8(0)
            # prefixed with the uncompressed point indicator 04
            bb.setUInt8(4)
            bb.add(target.value)
            # Count is type + size + 64 bytes + padding + uncompressed point
            # indicator.
            return 68
        elif isinstance(target, datetime.datetime):
            # Save date time in UTC.
            bb.setUInt8(BerType.UTC_TIME)
            str_ = cls.__dateToString(target)
            bb.setUInt8(len(str_))
            bb.add(str_)
        elif isinstance(target, (GXAsn1Sequence, list)):
            tmp = GXByteBuffer()
            for it in target:
                cnt += cls.__getBytes(tmp, it)
            start = bb.size
            if isinstance(target, GXAsn1Context):
                if target.constructed:
                    bb.setUInt8((BerType.CONSTRUCTED | BerType.SEQUENCE | target.Index))
                else:
                    bb.setUInt8(BerType.SEQUENCE | target.index)
            else:
                bb.setUInt8(BerType.CONSTRUCTED | BerType.SEQUENCE)
            _GXCommon.setObjectCount(cnt, bb)
            cnt += bb.size - start
            bb.set(tmp)
            return cnt
        else:
            raise ValueError("Invalid type: " + str(target))
        return bb.size - start

    # Convert ASN1 objects to byte array.
    @classmethod
    def toByteArray(cls, objects):
        bb = GXByteBuffer()
        cls.__getBytes(bb, objects)
        return bb.array()

    @classmethod
    def systemTitleToSubject(cls, systemTitle):
        """
        Convert system title to subject.

            Parameters:
                systemTitle: System title.

            Returns:
                Subject.
        """
        bb = GXByteBuffer(systemTitle)
        return "CN=" + bb.toHex(False, 0)

    @classmethod
    def systemTitleFromSubject(cls, subject):
        """
        Get system title from the subject.

            Parameters:
                subject: Subject.

            Returns:
                System title.
        """
        return GXByteBuffer.hexToBytes(cls.hexSystemTitleFromSubject(subject))

    @classmethod
    def hexSystemTitleFromSubject(cls, subject):
        """
        Get system title in hex string from the subject.

            Parameters:
                subject: Subject.

            Returns:
                System title.
        """
        index = subject.find("CN=")
        if index == -1:
            raise ValueError("System title not found from the subject.")
        return subject[index + 3 : index + 3 + 16]

    @classmethod
    def certificateTypeToKeyUsage(cls, value):
        """
        Convert ASN1 certificate type to DLMS key usage.

            Parameters:
                type: Certificate type.

            Returns:
                Key usage.
        """
        if value == CertificateType.DIGITAL_SIGNATURE:
            k = KeyUsage.DIGITAL_SIGNATURE
        elif value == CertificateType.KEY_AGREEMENT:
            k = KeyUsage.KEY_AGREEMENT
        elif value == CertificateType.TLS:
            k = KeyUsage.KEY_CERT_SIGN
        elif value == CertificateType.OTHER:
            k = KeyUsage.CRL_SIGN
        else:
            # At least one bit must be used.
            k = KeyUsage.NONE
        return k

    @classmethod
    def getCertificateType(cls, value):
        """
        Get certificate type from byte array or DER string.

        Parameters:
            value: Byte array or DER string.

        Returns:
            Certificate type.
        """
        if isinstance(value, str):
            return cls.__getCertificateType(_GXCommon.fromBase64(value), None)
        return cls.__getCertificateType(value, None)

    # pylint: disable=bare-except, import-outside-toplevel
    @classmethod
    def __getCertificateType(cls, data, seq):
        if not seq:
            seq = GXAsn1Converter.fromByteArray(data)
        if isinstance(seq[0], GXAsn1Sequence):
            try:
                GXx509Certificate(data)
                return PkcsType.X509CERTIFICATE
            except:
                # It's ok if this fails.
                pass
        if isinstance(seq[0], GXAsn1Sequence):
            try:
                from .GXPkcs10 import GXPkcs10

                GXPkcs10(data)
                return PkcsType.PKCS10
            except:
                # It's ok if this fails.
                pass
        if isinstance(seq[0], int):
            try:
                from .GXPkcs8 import GXPkcs8

                GXPkcs8(data)
                return PkcsType.PKCS8
            except:
                # It's ok if this fails.
                pass
        return PkcsType.NONE

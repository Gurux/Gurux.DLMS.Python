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
#  More information of Gurux products: http:#www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http:#www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
from gurux_dlms.asn.enums.HashAlgorithm import HashAlgorithm


class HashAlgorithmConverter:
    @classmethod
    def getString(cls, value):
        if value == HashAlgorithm.SHA1RSA:
            return "1.2.840.113549.1.1.5"
        elif value == HashAlgorithm.MD5RSA:
            return "1.2.840.113549.1.1.4"
        elif value == HashAlgorithm.SHA1DSA:
            return "1.2.840.10040.4.3"
        elif value == HashAlgorithm.SHA1RSA1:
            return "1.3.14.3.2.29"
        elif value == HashAlgorithm.SHA_RSA:
            return "1.3.14.3.2.15"
        elif value == HashAlgorithm.MD5RSA1:
            return "1.3.14.3.2.3"
        elif value == HashAlgorithm.MD2RSA1:
            return "1.2.840.113549.1.1.2"
        elif value == HashAlgorithm.MD4RSA:
            return "1.2.840.113549.1.1.3"
        elif value == HashAlgorithm.MD4RSA1:
            return "1.3.14.3.2.2"
        elif value == HashAlgorithm.MD4RSA2:
            return "1.3.14.3.2.4"
        elif value == HashAlgorithm.MD2RSA:
            return "1.3.14.7.2.3.1"
        elif value == HashAlgorithm.SHA1DSA1:
            return "1.3.14.3.2.13"
        elif value == HashAlgorithm.DSA_SHA1:
            return "1.3.14.3.2.27"
        elif value == HashAlgorithm.MOSAIC_UPDATED_SIG:
            return "2.16.840.1.101.2.1.1.19"
        elif value == HashAlgorithm.SHA1NO_SIGN:
            return "1.3.14.3.2.26"
        elif value == HashAlgorithm.MD5NO_SIGN:
            return "1.2.840.113549.2.5"
        elif value == HashAlgorithm.SHA256NO_SIGN:
            return "2.16.840.1.101.3.4.2.1"
        elif value == HashAlgorithm.SHA384NO_SIGN:
            return "2.16.840.1.101.3.4.2.2"
        elif value == HashAlgorithm.SHA512NO_SIGN:
            return "2.16.840.1.101.3.4.2.3"
        elif value == HashAlgorithm.SHA256RSA:
            return "1.2.840.113549.1.1.11"
        elif value == HashAlgorithm.SHA384RSA:
            return "1.2.840.113549.1.1.12"
        elif value == HashAlgorithm.SHA512RSA:
            return "1.2.840.113549.1.1.13"
        elif value == HashAlgorithm.RSA_SSA_PSS:
            return "1.2.840.113549.1.1.10"
        elif value == HashAlgorithm.SHA1WITHECDSA:
            return "1.2.840.10045.4.1"
        elif value == HashAlgorithm.SHA256WITH_ECDSA:
            return "1.2.840.10045.4.3.2"
        elif value == HashAlgorithm.SHA384WITH_ECDSA:
            return "1.2.840.10045.4.3.3"
        elif value == HashAlgorithm.SHA512WITH_ECDSA:
            return "1.2.840.10045.4.3.4"
        elif value == HashAlgorithm.SPECIFIED_ECDSA:
            return "1.2.840.10045.4.3"
        else:
            raise ValueError("Invalid HashAlgorithm. " + value)

    @classmethod
    def fromString(cls, value):
        if value == "1.2.840.113549.1.1.5":
            return HashAlgorithm.SHA1RSA
        elif value == "1.2.840.113549.1.1.4":
            return HashAlgorithm.MD5RSA
        elif value == "1.2.840.10040.4.3":
            return HashAlgorithm.SHA1DSA
        elif value == "1.3.14.3.2.29":
            return HashAlgorithm.SHA1RSA1
        elif value == "1.3.14.3.2.15":
            return HashAlgorithm.SHA_RSA
        elif value == "1.3.14.3.2.3":
            return HashAlgorithm.MD5RSA1
        elif value == "1.2.840.113549.1.1.2":
            return HashAlgorithm.MD2RSA1
        elif value == "1.2.840.113549.1.1.3":
            return HashAlgorithm.MD4RSA
        elif value == "1.3.14.3.2.2":
            return HashAlgorithm.MD4RSA1
        elif value == "1.3.14.3.2.4":
            return HashAlgorithm.MD4RSA2
        elif value == "1.3.14.7.2.3.1":
            return HashAlgorithm.MD2RSA
        elif value == "1.3.14.3.2.13":
            return HashAlgorithm.SHA1DSA1
        elif value == "1.3.14.3.2.27":
            return HashAlgorithm.DSA_SHA1
        elif value == "2.16.840.1.101.2.1.1.19":
            return HashAlgorithm.MOSAIC_UPDATED_SIG
        elif value == "1.3.14.3.2.26":
            return HashAlgorithm.SHA1NO_SIGN
        elif value == "1.2.840.113549.2.5":
            return HashAlgorithm.MD5NO_SIGN
        elif value == "2.16.840.1.101.3.4.2.1":
            return HashAlgorithm.SHA256NO_SIGN
        elif value == "2.16.840.1.101.3.4.2.2":
            return HashAlgorithm.SHA384NO_SIGN
        elif value == "2.16.840.1.101.3.4.2.3":
            return HashAlgorithm.SHA512NO_SIGN
        elif value == "1.2.840.113549.1.1.11":
            return HashAlgorithm.SHA256RSA
        elif value == "1.2.840.113549.1.1.12":
            return HashAlgorithm.SHA384RSA
        elif value == "1.2.840.113549.1.1.13":
            return HashAlgorithm.SHA512RSA
        elif value == "1.2.840.113549.1.1.10":
            return HashAlgorithm.RSA_SSA_PSS
        elif value == "1.2.840.10045.4.1":
            return HashAlgorithm.SHA1WITHECDSA
        elif value == "1.2.840.10045.4.3.2":
            return HashAlgorithm.SHA256WITH_ECDSA
        elif value == "1.2.840.10045.4.3.3":
            return HashAlgorithm.SHA384WITH_ECDSA
        elif value == "1.2.840.10045.4.3.4":
            return HashAlgorithm.SHA512WITH_ECDSA
        elif value == "1.2.840.10045.4.3":
            return HashAlgorithm.SPECIFIED_ECDSA
        else:
            return HashAlgorithm.NONE

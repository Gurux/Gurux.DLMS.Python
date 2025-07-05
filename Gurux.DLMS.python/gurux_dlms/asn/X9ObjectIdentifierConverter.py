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
from gurux_dlms.asn.enums.X9ObjectIdentifier import X9ObjectIdentifier


class X9ObjectIdentifierConverter:
    __OID_STRING_MAP = {
        X9ObjectIdentifier.ID_FIELD_TYPE: "1.2.840.10045.1",
        X9ObjectIdentifier.PRIME_FIELD: "1.2.840.10045.1",
        X9ObjectIdentifier.CHARACTERISTIC_TWO_FIELD: "1.2.840.10045.1.2",
        X9ObjectIdentifier.GN_BASIS: "1.2.840.10045.1.2.3.1",
        X9ObjectIdentifier.TP_BASIS: "1.2.840.10045.1.2.3.2",
        X9ObjectIdentifier.PP_BASIS: "1.2.840.10045.1.2.3.3",
        X9ObjectIdentifier.EC_DSA_WITH_SHA1: "1.2.840.10045.4.1",
        X9ObjectIdentifier.ID_EC_PUBLIC_KEY: "1.2.840.10045.2.1",
        X9ObjectIdentifier.EC_DSA_WITH_SHA2: "1.2.840.10045.4.3",
        X9ObjectIdentifier.EC_DSA_WITH_SHA224: "1.2.840.10045.4.31",
        X9ObjectIdentifier.EC_DSA_WITH_SHA256: "1.2.840.10045.4.32",
        X9ObjectIdentifier.EC_DSA_WITH_SHA384: "1.2.840.10045.4.33",
        X9ObjectIdentifier.EC_DSA_WITH_SHA512: "1.2.840.10045.4.34",
        X9ObjectIdentifier.ELLIPTIC_CURVE: "1.2.840.10045.3",
        X9ObjectIdentifier.C_TWO_CURVE: "1.2.840.10045.3.0",
        X9ObjectIdentifier.C2PNB163V1: "1.2.840.10045.3.0.1",
        X9ObjectIdentifier.C2PNB163V2: "1.2.840.10045.3.0.2",
        X9ObjectIdentifier.C2PNB163V3: "1.2.840.10045.3.0.3",
        X9ObjectIdentifier.C2PNB176W1: "1.2.840.10045.3.0.4",
        X9ObjectIdentifier.C2TNB191V1: "1.2.840.10045.3.0.5",
        X9ObjectIdentifier.C2TNB191V2: "1.2.840.10045.3.0.6",
        X9ObjectIdentifier.C2TNB191V3: "1.2.840.10045.3.0.7",
        X9ObjectIdentifier.C2ONB191V4: "1.2.840.10045.3.0.8",
        X9ObjectIdentifier.C2ONB191V5: "1.2.840.10045.3.0.9",
        X9ObjectIdentifier.C2PNB208W1: "1.2.840.10045.3.0.10",
        X9ObjectIdentifier.C2TNB239V1: "1.2.840.10045.3.0.11",
        X9ObjectIdentifier.C2TNB239V2: "1.2.840.10045.3.0.12",
        X9ObjectIdentifier.C2TNB239V3: "1.2.840.10045.3.0.13",
        X9ObjectIdentifier.C2ONB239V4: "1.2.840.10045.3.0.14",
        X9ObjectIdentifier.C2ONB239V5: "1.2.840.10045.3.0.15",
        X9ObjectIdentifier.C2PNB272W1: "1.2.840.10045.3.0.16",
        X9ObjectIdentifier.C2PNB304W1: "1.2.840.10045.3.0.17",
        X9ObjectIdentifier.C2TNB359V1: "1.2.840.10045.3.0.18",
        X9ObjectIdentifier.C2PNB368W1: "1.2.840.10045.3.0.19",
        X9ObjectIdentifier.C2TNB431R1: "1.2.840.10045.3.0.20",
        X9ObjectIdentifier.PRIME_CURVE: "1.2.840.10045.3.1",
        X9ObjectIdentifier.PRIME192V1: "1.2.840.10045.3.1.1",
        X9ObjectIdentifier.PRIME192V2: "1.2.840.10045.3.1.2",
        X9ObjectIdentifier.PRIME192V3: "1.2.840.10045.3.1.3",
        X9ObjectIdentifier.PRIME239V1: "1.2.840.10045.3.1.4",
        X9ObjectIdentifier.PRIME239V2: "1.2.840.10045.3.1.5",
        X9ObjectIdentifier.PRIME239V3: "1.2.840.10045.3.1.6",
        X9ObjectIdentifier.PRIME256V1: "1.2.840.10045.3.1.7",
        X9ObjectIdentifier.ID_DSA: "1.2.840.10040.4.1",
        X9ObjectIdentifier.ID_DSA_WITH_SHA1: "1.2.840.10040.4.3",
        X9ObjectIdentifier.X9X63SCHEME: "1.3.133.16.840.63.0",
        X9ObjectIdentifier.DH_SINGLE_PASS_STD_DH_SHA1KDF_SCHEME: "1.3.133.16.840.63.0.2",
        X9ObjectIdentifier.DH_SINGLE_PASS_COFACTOR_DH_SHA1KDF_SCHEME: "1.3.133.16.840.63.0.3",
        X9ObjectIdentifier.MQV_SINGLE_PASS_SHA1KDF_SCHEME: "1.3.133.16.840.63.0.16",
        X9ObjectIdentifier.ANSI_X9_42: "1.2.840.10046",
        X9ObjectIdentifier.DH_PUBLIC_NUMBER: "1.2.840.10046.2.1",
        X9ObjectIdentifier.X9X42SCHEMES: "1.2.840.10046.2.3",
        X9ObjectIdentifier.DH_STATIC: "1.2.840.10046.2.3.1",
        X9ObjectIdentifier.DH_EPHEM: "1.2.840.10046.2.3.2",
        X9ObjectIdentifier.DH_ONE_FLOW: "1.2.840.10046.2.3.3",
        X9ObjectIdentifier.DH_HYBRID1: "1.2.840.10046.2.3.4",
        X9ObjectIdentifier.DH_HYBRID2: "1.2.840.10046.2.3.5",
        X9ObjectIdentifier.DH_HYBRID_ONE_FLOW: "1.2.840.10046.2.3.6",
        X9ObjectIdentifier.MQV2: "1.2.840.10046.2.3.7",
        X9ObjectIdentifier.MQV1: "1.2.840.10046.2.3.8",
        X9ObjectIdentifier.SECP384R1: "1.3.132.0.34",
    }

    @classmethod
    def getString(cls, value):
        try:
            return cls.__OID_STRING_MAP[value]
        except KeyError:
            raise KeyError(f"Invalid X509Name. {value}")

    @classmethod
    def fromString(cls, value):
        for enum_value, oid in cls.__OID_STRING_MAP.items():
            if oid == value:
                return enum_value
        raise KeyError(f"Unknown OID string: {value}")

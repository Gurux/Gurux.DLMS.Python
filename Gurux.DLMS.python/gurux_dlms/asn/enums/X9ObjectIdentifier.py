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
from gurux_dlms.GXIntEnum import GXIntEnum


class X9ObjectIdentifier(GXIntEnum):
    NONE = 0
    ID_FIELD_TYPE = 1
    PRIME_FIELD = 2
    CHARACTERISTIC_TWO_FIELD = 3
    GN_BASIS = 4
    TP_BASIS = 5
    PP_BASIS = 6
    EC_DSA_WITH_SHA1 = 7
    ID_EC_PUBLIC_KEY = 8
    EC_DSA_WITH_SHA2 = 9
    EC_DSA_WITH_SHA224 = 10
    EC_DSA_WITH_SHA256 = 11
    EC_DSA_WITH_SHA384 = 12
    EC_DSA_WITH_SHA512 = 13
    ELLIPTIC_CURVE = 14
    C_TWO_CURVE = 15
    C2PNB163V1 = 16
    C2PNB163V2 = 17
    C2PNB163V3 = 18
    C2PNB176W1 = 19
    C2TNB191V1 = 20
    C2TNB191V2 = 21
    C2TNB191V3 = 22
    C2ONB191V4 = 23
    C2ONB191V5 = 24
    C2PNB208W1 = 25
    C2TNB239V1 = 26
    C2TNB239V2 = 27
    C2TNB239V3 = 28
    C2ONB239V4 = 29
    C2ONB239V5 = 30
    C2PNB272W1 = 31
    C2PNB304W1 = 32
    C2TNB359V1 = 33
    C2PNB368W1 = 34
    C2TNB431R1 = 35
    PRIME_CURVE = 36
    PRIME192V1 = 37
    PRIME192V2 = 38
    PRIME192V3 = 39
    PRIME239V1 = 40
    PRIME239V2 = 41
    PRIME239V3 = 42
    PRIME256V1 = 43
    ID_DSA = 44
    ID_DSA_WITH_SHA1 = 45
    X9X63SCHEME = 46
    DH_SINGLE_PASS_STD_DH_SHA1KDF_SCHEME = 47
    DH_SINGLE_PASS_COFACTOR_DH_SHA1KDF_SCHEME = 48
    MQV_SINGLE_PASS_SHA1KDF_SCHEME = 49
    ANSI_X9_42 = 50
    DH_PUBLIC_NUMBER = 51
    X9X42SCHEMES = 52
    DH_STATIC = 53
    DH_EPHEM = 54
    DH_ONE_FLOW = 55
    DH_HYBRID1 = 56
    DH_HYBRID2 = 57
    DH_HYBRID_ONE_FLOW = 58
    MQV2 = 59
    MQV1 = 60
    SECP384R1 = 61

    @classmethod
    def valueofString(cls, value):
        return X9ObjectIdentifier[value.upper()]

    def __str__(self):
        if self.value == X9ObjectIdentifier.NONE:
            ret = "None"
        elif self.value == X9ObjectIdentifier.ID_FIELD_TYPE:
            ret = "Id field type"
        elif self.value == X9ObjectIdentifier.PRIME_FIELD:
            ret = "Prime field"
        elif self.value == X9ObjectIdentifier.CHARACTERISTIC_TWO_FIELD:
            ret = "Characteristic two field"
        elif self.value == X9ObjectIdentifier.GN_BASIS:
            ret = "Gn basis"
        elif self.value == X9ObjectIdentifier.TP_BASIS:
            ret = "Tp basis"
        elif self.value == X9ObjectIdentifier.PP_BASIS:
            ret = "Pp basis"
        elif self.value == X9ObjectIdentifier.EC_DSA_WITH_SHA1:
            ret = "Ec dsa with sha1"
        elif self.value == X9ObjectIdentifier.ID_EC_PUBLIC_KEY:
            ret = "Id ec public key"
        elif self.value == X9ObjectIdentifier.EC_DSA_WITH_SHA2:
            ret = "Ec dsa with sha2"
        elif self.value == X9ObjectIdentifier.EC_DSA_WITH_SHA224:
            ret = "Ec dsa with sha224"
        elif self.value == X9ObjectIdentifier.EC_DSA_WITH_SHA256:
            ret = "Ec dsa with sha256"
        elif self.value == X9ObjectIdentifier.EC_DSA_WITH_SHA384:
            ret = "Ec dsa with sha384"
        elif self.value == X9ObjectIdentifier.EC_DSA_WITH_SHA512:
            ret = "Ec dsa with sha512"
        elif self.value == X9ObjectIdentifier.ELLIPTIC_CURVE:
            ret = "Elliptic curve"
        elif self.value == X9ObjectIdentifier.C_TWO_CURVE:
            ret = "C two curve"
        elif self.value == X9ObjectIdentifier.C2PNB163V1:
            ret = "C2pnb163v1"
        elif self.value == X9ObjectIdentifier.C2PNB163V2:
            ret = "C2pnb163v2"
        elif self.value == X9ObjectIdentifier.C2PNB163V3:
            ret = "C2pnb163v3"
        elif self.value == X9ObjectIdentifier.C2PNB176W1:
            ret = "C2pnb176w1"
        elif self.value == X9ObjectIdentifier.C2TNB191V1:
            ret = "C2tnb191v1"
        elif self.value == X9ObjectIdentifier.C2TNB191V2:
            ret = "C2tnb191v2"
        elif self.value == X9ObjectIdentifier.C2TNB191V3:
            ret = "C2tnb191v3"
        elif self.value == X9ObjectIdentifier.C2ONB191V4:
            ret = "C2onb191v4"
        elif self.value == X9ObjectIdentifier.C2ONB191V5:
            ret = "C2onb191v5"
        elif self.value == X9ObjectIdentifier.C2PNB208W1:
            ret = "C2pnb208w1"
        elif self.value == X9ObjectIdentifier.C2TNB239V1:
            ret = "C2tnb239v1"
        elif self.value == X9ObjectIdentifier.C2TNB239V2:
            ret = "C2tnb239v2"
        elif self.value == X9ObjectIdentifier.C2TNB239V3:
            ret = "C2tnb239v3"
        elif self.value == X9ObjectIdentifier.C2ONB239V4:
            ret = "C2onb239v4"
        elif self.value == X9ObjectIdentifier.C2ONB239V5:
            ret = "C2onb239v5"
        elif self.value == X9ObjectIdentifier.C2PNB272W1:
            ret = "C2pnb272w1"
        elif self.value == X9ObjectIdentifier.C2PNB304W1:
            ret = "C2pnb304w1"
        elif self.value == X9ObjectIdentifier.C2TNB359V1:
            ret = "C2tnb359v1"
        elif self.value == X9ObjectIdentifier.C2PNB368W1:
            ret = "C2pnb368w1"
        elif self.value == X9ObjectIdentifier.C2TNB431R1:
            ret = "C2tnb431r1"
        elif self.value == X9ObjectIdentifier.PRIME_CURVE:
            ret = "Prime curve"
        elif self.value == X9ObjectIdentifier.PRIME192V1:
            ret = "Prime192v1"
        elif self.value == X9ObjectIdentifier.PRIME192V2:
            ret = "Prime192v2"
        elif self.value == X9ObjectIdentifier.PRIME192V3:
            ret = "Prime192v3"
        elif self.value == X9ObjectIdentifier.PRIME239V1:
            ret = "Prime239v1"
        elif self.value == X9ObjectIdentifier.PRIME239V2:
            ret = "Prime239v2"
        elif self.value == X9ObjectIdentifier.PRIME239V3:
            ret = "Prime239v3"
        elif self.value == X9ObjectIdentifier.PRIME256V1:
            ret = "Prime256v1"
        elif self.value == X9ObjectIdentifier.ID_DSA:
            ret = "Id dsa"
        elif self.value == X9ObjectIdentifier.ID_DSA_WITH_SHA1:
            ret = "Id dsa with sha1"
        elif self.value == X9ObjectIdentifier.X9X63SCHEME:
            ret = "X9x63scheme"
        elif self.value == X9ObjectIdentifier.DH_SINGLE_PASS_STD_DH_SHA1KDF_SCHEME:
            ret = "Dh single pass std dh sha1kdf scheme"
        elif self.value == X9ObjectIdentifier.DH_SINGLE_PASS_COFACTOR_DH_SHA1KDF_SCHEME:
            ret = "Dh single pass cofactor dh sha1kdf scheme"
        elif self.value == X9ObjectIdentifier.MQV_SINGLE_PASS_SHA1KDF_SCHEME:
            ret = "Mqv single pass sha1kdf scheme"
        elif self.value == X9ObjectIdentifier.ANSI_X9_42:
            ret = "ansi_x9_42"
        elif self.value == X9ObjectIdentifier.DH_PUBLIC_NUMBER:
            ret = "Dh public number"
        elif self.value == X9ObjectIdentifier.X9X42SCHEMES:
            ret = "X9x42schemes"
        elif self.value == X9ObjectIdentifier.DH_STATIC:
            ret = "Dh static"
        elif self.value == X9ObjectIdentifier.DH_EPHEM:
            ret = "Dh ephem"
        elif self.value == X9ObjectIdentifier.DH_ONE_FLOW:
            ret = "Dh one flow"
        elif self.value == X9ObjectIdentifier.DH_HYBRID1:
            ret = "Dh hybrid1"
        elif self.value == X9ObjectIdentifier.DH_HYBRID2:
            ret = "Dh hybrid2"
        elif self.value == X9ObjectIdentifier.DH_HYBRID_ONE_FLOW:
            ret = "Dh hybrid one flow"
        elif self.value == X9ObjectIdentifier.MQV2:
            ret = "Mqv2"
        elif self.value == X9ObjectIdentifier.MQV1:
            ret = "Mqv1"
        elif self.value == X9ObjectIdentifier.SECP384R1:
            ret = "Secp384r1"
        else:
            ret = "Unknown enum value:" + str(self.value)
        return ret

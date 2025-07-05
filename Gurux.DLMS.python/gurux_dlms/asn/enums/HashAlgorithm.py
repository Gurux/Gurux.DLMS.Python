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


class HashAlgorithm(GXIntEnum):
    """
    Hash algorithms.
    """

    NONE = 0
    SHA1RSA = 1
    MD5RSA = 2
    SHA1DSA = 3
    SHA1RSA1 = 4
    SHA_RSA = 5
    MD5RSA1 = 6
    MD2RSA1 = 7
    MD4RSA = 8
    MD4RSA1 = 9
    MD4RSA2 = 10
    MD2RSA = 11
    SHA1DSA1 = 12
    DSA_SHA1 = 13
    MOSAIC_UPDATED_SIG = 14
    SHA1NO_SIGN = 15
    MD5NO_SIGN = 16
    SHA256NO_SIGN = 17
    SHA384NO_SIGN = 18
    SHA512NO_SIGN = 19
    SHA256RSA = 20
    SHA384RSA = 21
    SHA512RSA = 22
    RSA_SSA_PSS = 23
    SHA1WITHECDSA = 24
    SHA256WITH_ECDSA = 25
    SHA384WITH_ECDSA = 26
    SHA512WITH_ECDSA = 27
    SPECIFIED_ECDSA = 28

    @classmethod
    def valueofString(cls, value):
        return HashAlgorithm[value.upper()]

    def __str__(self):
        if self.value == HashAlgorithm.NONE:
            ret = "None"
        elif self.value == HashAlgorithm.SHA1RSA:
            ret = "Sha1rsa"
        elif self.value == HashAlgorithm.MD5RSA:
            ret = "Md5rsa"
        elif self.value == HashAlgorithm.SHA1DSA:
            ret = "Sha1dsa"
        elif self.value == HashAlgorithm.SHA1RSA1:
            ret = "Sha1rsa1"
        elif self.value == HashAlgorithm.SHA_RSA:
            ret = "Sha rsa"
        elif self.value == HashAlgorithm.MD5RSA1:
            ret = "Md5rsa1"
        elif self.value == HashAlgorithm.MD2RSA1:
            ret = "Md2rsa1"
        elif self.value == HashAlgorithm.MD4RSA:
            ret = "Md4rsa"
        elif self.value == HashAlgorithm.MD4RSA1:
            ret = "Md4rsa1"
        elif self.value == HashAlgorithm.MD4RSA2:
            ret = "Md4rsa2"
        elif self.value == HashAlgorithm.MD2RSA:
            ret = "Md2rsa"
        elif self.value == HashAlgorithm.SHA1DSA1:
            ret = "Sha1dsa1"
        elif self.value == HashAlgorithm.DSA_SHA1:
            ret = "Dsa sha1"
        elif self.value == HashAlgorithm.MOSAIC_UPDATED_SIG:
            ret = "Mosaic updated sig"
        elif self.value == HashAlgorithm.SHA1NO_SIGN:
            ret = "Sha1no sign"
        elif self.value == HashAlgorithm.MD5NO_SIGN:
            ret = "Md5no sign"
        elif self.value == HashAlgorithm.SHA256NO_SIGN:
            ret = "Sha256no sign"
        elif self.value == HashAlgorithm.SHA384NO_SIGN:
            ret = "Sha384no sign"
        elif self.value == HashAlgorithm.SHA512NO_SIGN:
            ret = "Sha512no sign"
        elif self.value == HashAlgorithm.SHA256RSA:
            ret = "Sha256rsa"
        elif self.value == HashAlgorithm.SHA384RSA:
            ret = "Sha384rsa"
        elif self.value == HashAlgorithm.SHA512RSA:
            ret = "Sha512rsa"
        elif self.value == HashAlgorithm.RSA_SSA_PSS:
            ret = "Rsa ssa pss"
        elif self.value == HashAlgorithm.SHA1WITHECDSA:
            ret = "Sha1withecdsa"
        elif self.value == HashAlgorithm.SHA256WITH_ECDSA:
            ret = "Sha256with ecdsa"
        elif self.value == HashAlgorithm.SHA384WITH_ECDSA:
            ret = "Sha384with ecdsa"
        elif self.value == HashAlgorithm.SHA512WITH_ECDSA:
            ret = "Sha512with ecdsa"
        elif self.value == HashAlgorithm.SPECIFIED_ECDSA:
            ret = "Specified ecdsa"
        else:
            ret = "Unknown enum value:" + str(self.value)
        return ret

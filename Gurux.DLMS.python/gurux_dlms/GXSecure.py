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
#  More information of Gurux products: http://www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http://www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
import random
import hashlib
from .enums import Authentication, Security
from .GXDLMSChipperingStream import GXDLMSChipperingStream
from .GXByteBuffer import GXByteBuffer
from .CountType import CountType
from .GXDLMSChippering import GXDLMSChippering
#
class GXSecure:
    #
    #      * Chipher text.
    #      *
    #      * @param settings
    #      * DLMS settings.
    #      * @param cipher
    #      * Chipher settings.
    #      * @param ic
    #      * IC
    #      * @param data
    #      * Text to chipher.
    #      * @param secret
    #      * Secret.
    #      * @return Chiphered text.
    #pylint: disable=too-many-arguments
    @classmethod
    def secure(cls, settings, cipher, ic, data, secret):
        #pylint: disable=import-outside-toplevel
        from .AesGcmParameter import AesGcmParameter
        if isinstance(secret, str):
            secret = secret.encode()
        d = []
        s = []
        if settings.authentication == Authentication.HIGH:
            len_ = len(data)
            if (len_ % 16) != 0:
                len_ += (16 - (len(data) % 16))

            if len(secret) > len(data):
                len_ = len(secret)
            if len_ % 16 != 0:
                len_ += 16 - (len(secret) % 16)
            s = bytearray(len_)
            d = bytearray(len_)
            s[0:len(secret)] = secret[0:]
            d[0:len(data)] = data[0:]
            pos = 0
            while pos < len(d) / 16:
                GXDLMSChipperingStream.aes1Encrypt(d, pos * 16, s)
                pos += 1
            return d
        #  Get server Challenge.
        challenge = GXByteBuffer()
        #  Get shared secret
        if settings.authentication == Authentication.HIGH_GMAC:
            challenge.set(data)
        elif settings.authentication == Authentication.HIGH_SHA256:
            challenge.set(secret)
        else:
            challenge.set(data)
            challenge.set(secret)
        d = challenge.array()
        if settings.authentication == Authentication.HIGH_MD5:
            md = hashlib.md5()
            md.update(d)
            d = md.digest()
        elif settings.authentication == Authentication.HIGH_SHA1:
            md = hashlib.sha1()
            md.update(d)
            d = md.digest()
        elif settings.authentication == Authentication.HIGH_SHA256:
            md = hashlib.sha256()
            md.update(d)
            d = md.digest()
        elif settings.authentication == Authentication.HIGH_GMAC:
            #  SC is always Security.Authentication.
            p = AesGcmParameter(0, secret, cipher.blockCipherKey, cipher.authenticationKey)
            p.security = Security.AUTHENTICATION
            p.invocationCounter = ic
            p.type_ = CountType.TAG
            challenge.clear()
            challenge.setUInt8(Security.AUTHENTICATION)
            challenge.setUInt32(p.invocationCounter)
            challenge.set(GXDLMSChippering.encryptAesGcm(p, d))
            d = challenge.array()
        elif settings.authentication == Authentication.HIGH_ECDSA:
            raise Exception("ECDSA is not supported.")
        return d

    #
    #      * Generates challenge.
    #      *
    #      * @param authentication
    #      * Used authentication.
    #      * @return Generated challenge.
    #
    @classmethod
    def generateChallenge(cls):
        #  Random challenge is 8 to 64 bytes.
        #  Texas Instruments accepts only 16 byte long challenge.
        #  For this reason challenge size is 16 bytes at the moment.
        len_ = 16
        result = [None] * len_
        pos = 0
        while pos != len_:
            result[pos] = random.randint(0, 255)
            pos += 1
        return result

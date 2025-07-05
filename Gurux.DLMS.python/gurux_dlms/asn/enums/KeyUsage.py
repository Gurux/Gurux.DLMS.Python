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
# Gurux Device Framework is Open Source software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2 of the License.
# Gurux Device Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# More information of Gurux products: https:#www.gurux.org
#
# This code is licensed under the GNU General Public License v2.
# Full text may be retrieved at http:#www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------

from gurux_dlms.GXIntFlag import GXIntFlag


class KeyUsage(GXIntFlag):
    """
    Key Usage.
    """

    NONE = 0
    """
    Key is not used.
    """
    DIGITAL_SIGNATURE = 0x1
    """
    Digital signature.
    """
    NON_REPUDIATION = 0x2
    """
    Non Repudiation.
    """
    KEY_ENCIPHERMENT = 0x4
    """
    Key encipherment.
    """
    DATA_ENCIPHERMENT = 0x8
    """
    Data encipherment.
    """
    KEY_AGREEMENT = 0x10
    """
    Key agreement.
    """
    KEY_CERT_SIGN = 0x20
    """
    Used with CA certificates when the subject public key is used to verify a signature on certificates.
    """
    CRL_SIGN = 0x40
    """
    Used when the subject public key is to verify a signature.
    """
    ENCIPHER_ONLY = 0x80
    """
    Encipher only.
    """
    DECIPHER_ONLY = 0x100
    """
    Decipher only.
    """

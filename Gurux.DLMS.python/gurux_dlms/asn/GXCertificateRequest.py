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
from gurux_dlms.asn.enums.ExtendedKeyUsage import ExtendedKeyUsage
from gurux_dlms.objects.enums.CertificateType import CertificateType


class GXCertificateRequest:
    """
    Certificate request
    """

    __certificateType = CertificateType.DIGITAL_SIGNATURE
    """
    Certificate type.
    """

    __extendedKeyUsage = ExtendedKeyUsage.NONE
    """
    Indicates the purpose for which the certified public key is used.
    """

    __certificate = None
    """
    Certificate Signing Request.
    """

    @property
    def certificateType(self):
        """
        Certificate type.
        """
        return self.__certificateType

    @certificateType.setter
    def certificateType(self, value):
        self.__certificateType = value

    @property
    def extendedKeyUsage(self):
        """
        Indicates the purpose for which the certified public key is used.
        """
        return self.__extendedKeyUsage

    @extendedKeyUsage.setter
    def extendedKeyUsage(self, value):
        self.__extendedKeyUsage = value

    @property
    def certificate(self):
        """
        Certificate Signing Request.
        """
        return self.__certificate

    @certificate.setter
    def certificate(self, value):
        self.__certificate = value

    def __init__(
        self, certificateType=CertificateType.DIGITAL_SIGNATURE, certificate=None
    ):
        """
        Constructor.
        """
        self.__certificate = certificate
        self.__certificateType = certificateType

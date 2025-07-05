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
from os import listdir
from os.path import isfile, join
from .enums.KeyUsage import KeyUsage
from .GXAsn1Converter import GXAsn1Converter
from .GXx509Certificate import GXx509Certificate


class GXx509CertificateCollection(list):
    """
    List of x509 certificates.
    """

    def find(self, key):
        """
        Find public key certificate by public key.

            Parameters:
                key: X509 certificate to search for.

            Returns:
                Certificate found or null, if the certificate is not found.
        """
        for it in self:
            if it.publicKey == key:
                return it
        return None

    def findBySerial(self, serialNumber, issuer):
        """
        Find public key certificate by serial number.

            Parameters:
                serialNumber: X509 certificate serial number to search for.
                issuer: X509 certificate issuer.

            Returns:
                Certificate found or null, if the certificate is not found.
        """
        for it in self:
            if it.serialNumber == serialNumber and it.issuer == issuer:
                return it
        return None

    def findBySystemTitle(self, systemTitle, usage):
        """
        Find public key certificate by system title.

            Parameters:
                systemTitle: System title.
                usage: Key usage.

            Returns:
                Certificate found or null, if the certificate is not found.
        """
        if not systemTitle:
            commonName = None
        else:
            commonName = GXAsn1Converter.systemTitleToSubject(systemTitle)
        return self.findByCommonName(commonName, usage)

    def getCertificates(self, usage):
        """
        Find certificates by key usage.

            Parameters:
                usage: Key usage.

            Returns:
                Found certificates.
        """
        certificates = []
        for it in self:
            if it.keyUsage == usage:
                certificates.append(it)
        return certificates

    def findByCommonName(self, commonName, usage):
        """
        Find public key certificate by common name (CN).

            Parameters:
                commonName: Common name.
                usage: Key usage.

            Returns:
                Certificate found or null, if the certificate is not found.
        """
        for it in self:
            if (
                usage == KeyUsage.NONE
                or (it.keyUsage and usage) != 0
                and it.subject.contains(commonName)
            ):
                return it
        return None

    def import_(self, folder):
        """
        Import certificates from the given folder.

            Parameters:
                path: The folder from which the certificates are imported.
        """

        files = [f for f in listdir(folder) if isfile(join(folder, f))]
        for it in files:
            if it.endswith(".pem") or it.endswith(".cer"):
                cert = GXx509Certificate.load(it)
                self.append(cert)

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


class X509CertificateType(GXIntEnum):
    """
    x509 Certificate.
    """

    NONE = 0
    OLD_AUTHORITY_KEY_IDENTIFIER = 1
    OLD_PRIMARY_KEY_ATTRIBUTES = 2
    CERTIFICATE_POLICIES = 3
    ORIMARY_KEY_USAGE_RESTRICTION = 4
    SUBJECT_DIRECTORY_ATTRIBUTES = 5
    SUBJECT_KEY_IDENTIFIER = 6
    KEY_USAGE = 7
    PRIVATE_KEY_USAGE_PERIOD = 8
    SUBJECT_ALTERNATIVE_NAME = 9
    ISSUER_ALTERNATIVE_NAME = 10
    BASIC_CONSTRAINTS = 11
    CRL_NUMBER = 12
    REASON_CODE = 13
    HOLD_INSTRUCTION_CODE = 14
    INVALIDITY_DATE = 15
    DELTA_CRL_INDICATOR = 16
    ISSUING_DISTRIBUTION_POINT = 17
    CERTIFICATE_ISSUER = 18
    NAME_CONSTRAINTS = 19
    CRL_DISTRIBUTION_POINTS = 20
    CERTIFICATE_POLICIES2 = 21
    POLICY_MAPPINGS = 22
    AUTHORITY_KEY_IDENTIFIER = 23
    POLICY_CONSTRAINTS = 24
    EXTENDED_KEY_USAGE = 25
    FRESHEST_CRL = 26

    @classmethod
    def valueofString(cls, value):
        return X509CertificateType[value.upper()]

    def __str__(self):
        if self.value == X509CertificateType.NONE:
            ret = "None"
        elif self.value == X509CertificateType.OLD_AUTHORITY_KEY_IDENTIFIER:
            ret = "Old authority key identifier"
        elif self.value == X509CertificateType.OLD_PRIMARY_KEY_ATTRIBUTES:
            ret = "Old primary key attributes"
        elif self.value == X509CertificateType.CERTIFICATE_POLICIES:
            ret = "Certificate policies"
        elif self.value == X509CertificateType.ORIMARY_KEY_USAGE_RESTRICTION:
            ret = "Orimary key usage restriction"
        elif self.value == X509CertificateType.SUBJECT_DIRECTORY_ATTRIBUTES:
            ret = "Subject directory attributes"
        elif self.value == X509CertificateType.SUBJECT_KEY_IDENTIFIER:
            ret = "Subject key identifier"
        elif self.value == X509CertificateType.KEY_USAGE:
            ret = "Key usage"
        elif self.value == X509CertificateType.PRIVATE_KEY_USAGE_PERIOD:
            ret = "Private key usage period"
        elif self.value == X509CertificateType.SUBJECT_ALTERNATIVE_NAME:
            ret = "Subject alternative name"
        elif self.value == X509CertificateType.ISSUER_ALTERNATIVE_NAME:
            ret = "Issuer alternative name"
        elif self.value == X509CertificateType.BASIC_CONSTRAINTS:
            ret = "Basic constraints"
        elif self.value == X509CertificateType.CRL_NUMBER:
            ret = "Crl number"
        elif self.value == X509CertificateType.REASON_CODE:
            ret = "Reason code"
        elif self.value == X509CertificateType.HOLD_INSTRUCTION_CODE:
            ret = "Hold instruction code"
        elif self.value == X509CertificateType.INVALIDITY_DATE:
            ret = "Invalidity date"
        elif self.value == X509CertificateType.DELTA_CRL_INDICATOR:
            ret = "Delta crl indicator"
        elif self.value == X509CertificateType.ISSUING_DISTRIBUTION_POINT:
            ret = "Issuing distribution point"
        elif self.value == X509CertificateType.CERTIFICATE_ISSUER:
            ret = "Certificate issuer"
        elif self.value == X509CertificateType.NAME_CONSTRAINTS:
            ret = "Name constraints"
        elif self.value == X509CertificateType.CRL_DISTRIBUTION_POINTS:
            ret = "Crl distribution points"
        elif self.value == X509CertificateType.CERTIFICATE_POLICIES2:
            ret = "Certificate policies2"
        elif self.value == X509CertificateType.POLICY_MAPPINGS:
            ret = "Policy mappings"
        elif self.value == X509CertificateType.AUTHORITY_KEY_IDENTIFIER:
            ret = "Authority key identifier"
        elif self.value == X509CertificateType.POLICY_CONSTRAINTS:
            ret = "Policy constraints"
        elif self.value == X509CertificateType.EXTENDED_KEY_USAGE:
            ret = "Extended key usage"
        elif self.value == X509CertificateType.FRESHEST_CRL:
            ret = "Freshest crl"
        else:
            ret = "Unknown enum value:" + str(self.value)
        return ret

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
from gurux_dlms.asn.enums.X509CertificateType import X509CertificateType


class X509CertificateTypeConverter:
    @classmethod
    def getString(cls, value):
        if value == X509CertificateType.OLD_AUTHORITY_KEY_IDENTIFIER:
            ret = "2.5.29.1"
        elif value == X509CertificateType.OLD_PRIMARY_KEY_ATTRIBUTES:
            ret = "2.5.29.2"
        elif value == X509CertificateType.CERTIFICATE_POLICIES:
            ret = "2.5.29.3"
        elif value == X509CertificateType.ORIMARY_KEY_USAGE_RESTRICTION:
            ret = "2.5.29.4"
        elif value == X509CertificateType.SUBJECT_DIRECTORY_ATTRIBUTES:
            ret = "2.5.29.9"
        elif value == X509CertificateType.SUBJECT_KEY_IDENTIFIER:
            ret = "2.5.29.14"
        elif value == X509CertificateType.KEY_USAGE:
            ret = "2.5.29.15"
        elif value == X509CertificateType.PRIVATE_KEY_USAGE_PERIOD:
            ret = "2.5.29.16"
        elif value == X509CertificateType.SUBJECT_ALTERNATIVE_NAME:
            ret = "2.5.29.17"
        elif value == X509CertificateType.ISSUER_ALTERNATIVE_NAME:
            ret = "2.5.29.18"
        elif value == X509CertificateType.BASIC_CONSTRAINTS:
            ret = "2.5.29.19"
        elif value == X509CertificateType.CRL_NUMBER:
            ret = "2.5.29.20"
        elif value == X509CertificateType.REASON_CODE:
            ret = "2.5.29.21"
        elif value == X509CertificateType.HOLD_INSTRUCTION_CODE:
            ret = "2.5.29.23"
        elif value == X509CertificateType.INVALIDITY_DATE:
            ret = "2.5.29.24"
        elif value == X509CertificateType.DELTA_CRL_INDICATOR:
            ret = "2.5.29.27"
        elif value == X509CertificateType.ISSUING_DISTRIBUTION_POINT:
            ret = "2.5.29.28"
        elif value == X509CertificateType.CERTIFICATE_ISSUER:
            ret = "2.5.29.29"
        elif value == X509CertificateType.NAME_CONSTRAINTS:
            ret = "2.5.29.30"
        elif value == X509CertificateType.CRL_DISTRIBUTION_POINTS:
            ret = "2.5.29.31"
        elif value == X509CertificateType.CERTIFICATE_POLICIES2:
            ret = "2.5.29.32"
        elif value == X509CertificateType.POLICY_MAPPINGS:
            ret = "2.5.29.33"
        elif value == X509CertificateType.AUTHORITY_KEY_IDENTIFIER:
            ret = "2.5.29.35"
        elif value == X509CertificateType.POLICY_CONSTRAINTS:
            ret = "2.5.29.36"
        elif value == X509CertificateType.EXTENDED_KEY_USAGE:
            ret = "2.5.29.37"
        elif value == X509CertificateType.FRESHEST_CRL:
            ret = "2.5.29.46"
        else:
            raise ValueError("Invalid X509Certificate. " + str(value))
        return ret

    @classmethod
    def fromString(cls, value):
        if value == "2.5.29.1":
            ret = X509CertificateType.OLD_AUTHORITY_KEY_IDENTIFIER
        elif value == "2.5.29.2":
            ret = X509CertificateType.OLD_PRIMARY_KEY_ATTRIBUTES
        elif value == "2.5.29.3":
            ret = X509CertificateType.CERTIFICATE_POLICIES
        elif value == "2.5.29.4":
            ret = X509CertificateType.ORIMARY_KEY_USAGE_RESTRICTION
        elif value == "2.5.29.9":
            ret = X509CertificateType.SUBJECT_DIRECTORY_ATTRIBUTES
        elif value == "2.5.29.14":
            ret = X509CertificateType.SUBJECT_KEY_IDENTIFIER
        elif value == "2.5.29.15":
            ret = X509CertificateType.KEY_USAGE
        elif value == "2.5.29.16":
            ret = X509CertificateType.PRIVATE_KEY_USAGE_PERIOD
        elif value == "2.5.29.17":
            ret = X509CertificateType.SUBJECT_ALTERNATIVE_NAME
        elif value == "2.5.29.18":
            ret = X509CertificateType.ISSUER_ALTERNATIVE_NAME
        elif value == "2.5.29.19":
            ret = X509CertificateType.BASIC_CONSTRAINTS
        elif value == "2.5.29.20":
            ret = X509CertificateType.CRL_NUMBER
        elif value == "2.5.29.21":
            ret = X509CertificateType.REASON_CODE
        elif value == "2.5.29.23":
            ret = X509CertificateType.HOLD_INSTRUCTION_CODE
        elif value == "2.5.29.24":
            ret = X509CertificateType.INVALIDITY_DATE
        elif value == "2.5.29.27":
            ret = X509CertificateType.DELTA_CRL_INDICATOR
        elif value == "2.5.29.28":
            ret = X509CertificateType.ISSUING_DISTRIBUTION_POINT
        elif value == "2.5.29.29":
            ret = X509CertificateType.CERTIFICATE_ISSUER
        elif value == "2.5.29.30":
            ret = X509CertificateType.NAME_CONSTRAINTS
        elif value == "2.5.29.31":
            ret = X509CertificateType.CRL_DISTRIBUTION_POINTS
        elif value == "2.5.29.32":
            ret = X509CertificateType.CERTIFICATE_POLICIES2
        elif value == "2.5.29.33":
            ret = X509CertificateType.POLICY_MAPPINGS
        elif value == "2.5.29.35":
            ret = X509CertificateType.AUTHORITY_KEY_IDENTIFIER
        elif value == "2.5.29.36":
            ret = X509CertificateType.POLICY_CONSTRAINTS
        elif value == "2.5.29.37":
            ret = X509CertificateType.EXTENDED_KEY_USAGE
        elif value == "2.5.29.46":
            ret = X509CertificateType.FRESHEST_CRL
        else:
            ret = X509CertificateType.NONE
        return ret

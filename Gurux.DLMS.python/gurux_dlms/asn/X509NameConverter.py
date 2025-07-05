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
from gurux_dlms.asn.enums.X509Name import X509Name


class X509NameConverter:
    @classmethod
    def getString(cls, value):
        if value == X509Name.C:
            ret = "2.5.4.6"
        elif value == X509Name.O:
            ret = "2.5.4.10"
        elif value == X509Name.OU:
            ret = "2.5.4.11"
        elif value == X509Name.T:
            ret = "2.5.4.12"
        elif value == X509Name.CN:
            ret = "2.5.4.3"
        elif value == X509Name.STREET:
            ret = "2.5.4.9"
        elif value == X509Name.SERIAL_NUMBER:
            ret = "2.5.4.5"
        elif value == X509Name.L:
            ret = "2.5.4.7"
        elif value == X509Name.ST:
            ret = "2.5.4.8"
        elif value == X509Name.SUR_NAME:
            ret = "2.5.4.4"
        elif value == X509Name.GIVEN_NAME:
            ret = "2.5.4.42"
        elif value == X509Name.INITIALS:
            ret = "2.5.4.43"
        elif value == X509Name.GENERATION:
            ret = "2.5.4.44"
        elif value == X509Name.UNIQUE_IDENTIFIER:
            ret = "2.5.4.45"
        elif value == X509Name.BUSINESS_CATEGORY:
            ret = "2.5.4.15"
        elif value == X509Name.POSTAL_CODE:
            ret = "2.5.4.17"
        elif value == X509Name.DN_QUALIFIER:
            ret = "2.5.4.46"
        elif value == X509Name.PSEUDONYM:
            ret = "2.5.4.65"
        elif value == X509Name.DATE_OF_BIRTH:
            ret = "1.3.6.1.5.5.7.9.1"
        elif value == X509Name.PLACE_OF_BIRTH:
            ret = "1.3.6.1.5.5.7.9.2"
        elif value == X509Name.GENDER:
            ret = "1.3.6.1.5.5.7.9.3"
        elif value == X509Name.COUNTRY_OF_CITIZENSHIP:
            ret = "1.3.6.1.5.5.7.9.4"
        elif value == X509Name.COUNTRY_OF_RESIDENCE:
            ret = "1.3.6.1.5.5.7.9.5"
        elif value == X509Name.NAME_AT_BIRTH:
            ret = "1.3.36.8.3.14"
        elif value == X509Name.POSTAL_ADDRESS:
            ret = "2.5.4.16"
        elif value == X509Name.DMD_NAME:
            ret = "2.5.4.54"
        elif value == X509Name.TELEPHONE_NUMBER:
            ret = "2.5.4.20"
        elif value == X509Name.NAME:
            ret = "2.5.4.41"
        elif value == X509Name.E:
            ret = "1.2.840.113549.1.9.1"
        elif value == X509Name.DC:
            ret = "0.9.2342.19200300.100.1.25"
        elif value == X509Name.UID:
            ret = "0.9.2342.19200300.100.1.1"
        else:
            raise ValueError("Invalid X509Name. " + value)
        return ret

    @classmethod
    def fromString(cls, value):
        if value == "2.5.4.6":
            ret = X509Name.C
        elif value == "2.5.4.10":
            ret = X509Name.O
        elif value == "2.5.4.11":
            ret = X509Name.OU
        elif value == "2.5.4.12":
            ret = X509Name.T
        elif value == "2.5.4.3":
            ret = X509Name.CN
        elif value == "2.5.4.9":
            ret = X509Name.STREET
        elif value == "2.5.4.5":
            ret = X509Name.SERIAL_NUMBER
        elif value == "2.5.4.7":
            ret = X509Name.L
        elif value == "2.5.4.8":
            ret = X509Name.ST
        elif value == "2.5.4.4":
            ret = X509Name.SUR_NAME
        elif value == "2.5.4.42":
            ret = X509Name.GIVEN_NAME
        elif value == "2.5.4.43":
            ret = X509Name.INITIALS
        elif value == "2.5.4.44":
            ret = X509Name.GENERATION
        elif value == "2.5.4.45":
            ret = X509Name.UNIQUE_IDENTIFIER
        elif value == "2.5.4.15":
            ret = X509Name.BUSINESS_CATEGORY
        elif value == "2.5.4.17":
            ret = X509Name.POSTAL_CODE
        elif value == "2.5.4.46":
            ret = X509Name.DN_QUALIFIER
        elif value == "2.5.4.65":
            ret = X509Name.PSEUDONYM
        elif value == "1.3.6.1.5.5.7.9.1":
            ret = X509Name.DATE_OF_BIRTH
        elif value == "1.3.6.1.5.5.7.9.2":
            ret = X509Name.PLACE_OF_BIRTH
        elif value == "1.3.6.1.5.5.7.9.3":
            ret = X509Name.GENDER
        elif value == "1.3.6.1.5.5.7.9.4":
            ret = X509Name.COUNTRY_OF_CITIZENSHIP
        elif value == "1.3.6.1.5.5.7.9.5":
            ret = X509Name.COUNTRY_OF_RESIDENCE
        elif value == "1.3.36.8.3.14":
            ret = X509Name.NAME_AT_BIRTH
        elif value == "2.5.4.16":
            ret = X509Name.POSTAL_ADDRESS
        elif value == "2.5.4.54":
            ret = X509Name.DMD_NAME
        elif value == "2.5.4.20":
            ret = X509Name.TELEPHONE_NUMBER
        elif value == "2.5.4.41":
            ret = X509Name.NAME
        elif value == "1.2.840.113549.1.9.1":
            ret = X509Name.E
        elif value == "0.9.2342.19200300.100.1.25":
            ret = X509Name.DC
        elif value == "0.9.2342.19200300.100.1.1":
            ret = X509Name.UID
        else:
            ret = X509Name.NONE
        return ret

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


class X509Name(GXIntEnum):
    """
    X509 names.
    """

    NONE = 0
    C = 1
    """
    country code - StringType(SIZE(2))
    """
    O = 2
    """
    organization - StringType(SIZE(1..64))
    """
    OU = 3
    """
    organizational unit name - StringType(SIZE(1..64))
    """
    T = 4
    """
    Title
    """
    CN = 5
    """
    common name - StringType(SIZE(1..64))
    """
    STREET = 6
    """
    street - StringType(SIZE(1..64))
    """
    SERIAL_NUMBER = 7
    """
    device serial number name - StringType(SIZE(1..64))
    """
    L = 8
    """
    locality name - StringType(SIZE(1..64))
    """
    ST = 9
    """
    state, or province name - StringType(SIZE(1..64))
    """
    SUR_NAME = 10
    """
    Naming attributes of type X520name
    """
    GIVEN_NAME = 11
    """
    Given name.
    """
    INITIALS = 12
    """
    Initials.
    """
    GENERATION = 13
    """
    Generation.
    """
    UNIQUE_IDENTIFIER = 14
    """
    Unique identifier.
    """
    BUSINESS_CATEGORY = 15
    """
    businessCategory - DirectoryString(SIZE(1..128))
    """
    POSTAL_CODE = 16
    """
    postalCode - DirectoryString(SIZE(1..40))
    """
    DN_QUALIFIER = 17
    """
    dnQualifier - DirectoryString(SIZE(1..64))
    """
    PSEUDONYM = 18
    """
    RFC 3039 Pseudonym - DirectoryString(SIZE(1..64))
    """
    DATE_OF_BIRTH = 19
    """
    RFC 3039 DateOfBirth - GeneralizedTime - YYYYMMDD000000Z
    """
    PLACE_OF_BIRTH = 20
    """
    RFC 3039 PlaceOfBirth - DirectoryString(SIZE(1..128))
    """
    GENDER = 21
    """
    RFC 3039 DateOfBirth - PrintableString (SIZE(1 -- "M", "F", "m" or "f")
    """
    COUNTRY_OF_CITIZENSHIP = 22
    """
    RFC 3039 CountryOfCitizenship - PrintableString (SIZE (2 -- ISO 3166)) codes only
    """
    COUNTRY_OF_RESIDENCE = 23
    """
    RFC 3039 CountryOfCitizenship - PrintableString (SIZE (2 -- ISO 3166)) codes only
    """
    NAME_AT_BIRTH = 24
    """
    ISIS-MTT NameAtBirth - DirectoryString(SIZE(1..64))
    """
    POSTAL_ADDRESS = 25
    """
    RFC 3039 PostalAddress - SEQUENCE SIZE (1..6 OF DirectoryString(SIZE(1..30)))
    """
    DMD_NAME = 26
    """
    RFC 2256 dmdName
    """
    TELEPHONE_NUMBER = 27
    """
    id-at-telephoneNumber
    """
    NAME = 28
    """
    id-at-name
    """
    E = 29
    """
    email address in Verisign certificates
    """
    DC = 30
    """
    Domain component
    """
    UID = 31
    """
    LDAP User id.
    """

    @classmethod
    def valueofString(cls, value):
        return X509Name[value.upper()]

    def __str__(self):
        if self.value == X509Name.NONE:
            ret = "None"
        elif self.value == X509Name.C:
            ret = "C"
        elif self.value == X509Name.O:
            ret = "O"
        elif self.value == X509Name.OU:
            ret = "OU"
        elif self.value == X509Name.T:
            ret = "T"
        elif self.value == X509Name.CN:
            ret = "CN"
        elif self.value == X509Name.STREET:
            ret = "Street"
        elif self.value == X509Name.SERIAL_NUMBER:
            ret = "Serial number"
        elif self.value == X509Name.L:
            ret = "L"
        elif self.value == X509Name.ST:
            ret = "ST"
        elif self.value == X509Name.SUR_NAME:
            ret = "Sur name"
        elif self.value == X509Name.GIVEN_NAME:
            ret = "Given name"
        elif self.value == X509Name.INITIALS:
            ret = "Initials"
        elif self.value == X509Name.GENERATION:
            ret = "Generation"
        elif self.value == X509Name.UNIQUE_IDENTIFIER:
            ret = "Unique identifier"
        elif self.value == X509Name.BUSINESS_CATEGORY:
            ret = "Business category"
        elif self.value == X509Name.POSTAL_CODE:
            ret = "Postal code"
        elif self.value == X509Name.DN_QUALIFIER:
            ret = "Dn qualifier"
        elif self.value == X509Name.PSEUDONYM:
            ret = "Pseudonym"
        elif self.value == X509Name.DATE_OF_BIRTH:
            ret = "Date of birth"
        elif self.value == X509Name.PLACE_OF_BIRTH:
            ret = "Place of birth"
        elif self.value == X509Name.GENDER:
            ret = "Gender"
        elif self.value == X509Name.COUNTRY_OF_CITIZENSHIP:
            ret = "Country of citizenship"
        elif self.value == X509Name.COUNTRY_OF_RESIDENCE:
            ret = "Country of residence"
        elif self.value == X509Name.NAME_AT_BIRTH:
            ret = "Name at birth"
        elif self.value == X509Name.POSTAL_ADDRESS:
            ret = "Postal address"
        elif self.value == X509Name.DMD_NAME:
            ret = "Dmd name"
        elif self.value == X509Name.TELEPHONE_NUMBER:
            ret = "Telephone number"
        elif self.value == X509Name.NAME:
            ret = "Name"
        elif self.value == X509Name.E:
            ret = "E"
        elif self.value == X509Name.DC:
            ret = "DC"
        elif self.value == X509Name.UID:
            ret = "Uid"
        else:
            ret = "Unknown enum value:" + str(self.value)
        return ret

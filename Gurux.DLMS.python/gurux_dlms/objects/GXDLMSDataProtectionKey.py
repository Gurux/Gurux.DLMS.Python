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
from .enums.DataProtectionKeyType import DataProtectionKeyType
from .GXDLMSDataProtectionIdentifiedKey import GXDLMSDataProtectionIdentifiedKey
from .GXDLMSDataProtectionWrappeddKey import GXDLMSDataProtectionWrappeddKey
from .GXDLMSDataProtectionAgreedKey import GXDLMSDataProtectionAgreedKey


class GXDLMSDataProtectionKey:
    """
    Data protection Key.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.__identifiedKey = GXDLMSDataProtectionIdentifiedKey()
        self.__wrappedKey = GXDLMSDataProtectionWrappeddKey()
        self.__agreedKey = GXDLMSDataProtectionAgreedKey()
        self.__dataProtectionKeyType = DataProtectionKeyType.IDENTIFIED

    @property
    def dataProtectionKeyType(self):
        """
        Data protection key type.
        """
        return self.__dataProtectionKeyType

    @dataProtectionKeyType.setter
    def dataProtectionKeyType(self, value):
        self.__dataProtectionKeyType = value

    @property
    def identifiedKey(self):
        """
        Identified key parameters.
        """
        return self.__identifiedKey

    @identifiedKey.setter
    def identifiedKey(self, value):
        self.__identifiedKey = value

    @property
    def wrappedKey(self):
        """
        Wrapped key parameters.
        """
        return self.__wrappedKey

    @wrappedKey.setter
    def wrappedKey(self, value):
        self.__wrappedKey = value

    @property
    def agreedKey(self):
        """
        Agreed key parameters.
        """
        return self.__agreedKey

    @agreedKey.setter
    def agreedKey(self, value):
        self.__agreedKey = value

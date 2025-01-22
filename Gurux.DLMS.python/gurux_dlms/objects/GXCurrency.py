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

from .enums import Currency


###Python 2 requires this
# pylint: disable=bad-option-value,old-style-class, too-few-public-methods
class GXCurrency:
    """
    Used currency.
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSAccount
    """

    def __init__(self):
        """
        Constructor.
        """

        # Currency unit.
        self.unit = Currency.TIME
        # Currency name.
        self.name = None
        # Currency scale.
        self.scale = 0

    def __str__(self):
        return str(self.unit) + " " + str(self.name) + " " + str(self.scale)

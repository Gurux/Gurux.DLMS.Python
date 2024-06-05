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
from ..enums import DataType


###Python 2 requires this
# pylint: disable=bad-option-value,old-style-class,too-few-public-methods
class _GXDataInfo:
    """This class is used in DLMS data parsing."""

    def __init__(self):
        """Constructor."""
        # Last array index.
        self.index = 0
        # Items count in array.
        self.count = 0
        # Object data type.
        self.type_ = DataType.NONE
        # Is data parsed to the end.
        self.complete = True
        self.xml = None

    def clear(self):
        self.index = 0
        self.count = 0
        self.type_ = DataType.NONE
        self.complete = True

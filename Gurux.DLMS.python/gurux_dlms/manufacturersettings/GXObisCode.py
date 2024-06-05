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
from ..enums import ObjectType
from .GXAttributeCollection import GXAttributeCollection


class GXObisCode:
    # pylint: disable=too-few-public-methods

    #
    # Constructor.
    #
    # ln: Logical name.
    # ot: Object type.
    # index: Attribute index.
    #
    def __init__(self, ln=None, ot=ObjectType.NONE, index=0, desc=None):
        self.version = 0
        self.attributeIndex = index
        self.logicalName = ln
        self.description = desc
        self.objectType = ot
        self.attributes = GXAttributeCollection(self)
        self.attributes.parent = self
        # UI data types.
        self.uiDataType = None

    def __str__(self):
        return str(self.objectType)

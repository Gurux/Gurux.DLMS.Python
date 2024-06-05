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
from ..enums import AccessMode
from ..enums import MethodAccessMode
from ..enums import AccessMode3
from ..enums import MethodAccessMode3


###Python 2 requires this
# pylint: disable=bad-option-value,old-style-class,too-few-public-methods, too-many-instance-attributes
class GXDLMSAttributeSettings:
    def __init__(self, index=0):
        #
        # Constructor.
        # index: Attribute index.
        #
        self.name = ""
        self.index = index
        self.type_ = DataType.NONE
        self.uiType = DataType.NONE
        self.access = AccessMode.READ_WRITE
        self.access3 = AccessMode3.READ_WRITE
        self.methodAccess = MethodAccessMode.ACCESS
        self.methodAccess3 = MethodAccessMode3.ACCESS
        self.static = False
        self.values = None
        self.order = 0
        self.minimumVersion = 0
        self.xml = ""

    def copyTo(self, target):
        target.name = self.name
        target.index = self.index
        target.type_ = self.type_
        target.uiType = self.uiType
        target.access = self.access
        target.access3 = self.access3
        target.methodAccess = self.methodAccess
        target.methodAccess3 = self.methodAccess3
        target.static = self.static
        target.values = self.values
        target.order = self.order
        target.minimumVersion = self.minimumVersion
        target.xml = self.xml

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
from .GXDLMSAttributeSettings import GXDLMSAttributeSettings
from ..enums import DataType

class GXDLMSAttribute(GXDLMSAttributeSettings):
    #pylint: disable=too-few-public-methods
    def __init__(self, index=0, type_=DataType.NONE, uiType=DataType.NONE, order=0):
        """
        Constructor.

        index : Attribute index.
        type : Data type.
        uiType : UI data type.
        order : Order.
        """
        GXDLMSAttributeSettings.__init__(self)
        self.index = index
        self.type_ = type_
        self.UIType = uiType
        self.order = order

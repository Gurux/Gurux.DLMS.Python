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
from abc import abstractmethod
from ..internal._GXCommon import _GXCommon
from ..manufacturersettings import GXAttributeCollection, GXDLMSAttributeSettings
from ..enums.DataType import DataType
from ..enums.AccessMode import AccessMode
from ..enums.MethodAccessMode import MethodAccessMode
#
# pylint: disable=too-many-public-methods,too-many-instance-attributes,useless-object-inheritance
class GXDLMSObject(object):
    #
    # Constructor,
    #
    def __init__(self, ot, ln=None, sn=0):
        # DLMS version number.
        self.version = 0
        self.objectType = ot
        self.shortName = sn
        # Description of COSEM object.
        self.description = ""
        self.attributes = GXAttributeCollection()
        self.methodAttributes = GXAttributeCollection()
        if ln:
            items = ln.split('.')
            if len(items) != 6:
                raise Exception("Invalid Logical Name.")
        # Logical Name of COSEM object.
        self.logicalName = ln
        self.readTimes = dict()

    #
    # Validate logical name.
    # value: Logical Name.
    #
    @classmethod
    def validateLogicalName(cls, value):
        _GXCommon.logicalNameToBytes(value)

    #
    # Is attribute read.  This can be used with static attributes to
    #      make meter
    # reading faster.
    #
    def isRead(self, index):
        if not self.canRead(index):
            return True
        return not self.getLastReadTime(index)

    def canRead(self, index):
        return self.getAccess(index) and AccessMode.READ != 0

    #
    # Returns time when attribute was last time read.  -
    #
    # @param attributeIndex
    # Attribute index.
    # Is attribute read only.
    #
    def getLastReadTime(self, attributeIndex):
        for k, v in self.readTimes:
            if k == attributeIndex:
                return v
        return None

    #
    # Set time when attribute was last time read.
    # @param attributeIndex Attribute index.
    # @param tm Read time.
    #
    def setLastReadTime(self, attributeIndex, tm):
        self.readTimes[attributeIndex] = tm

    #
    # Logical or Short Name of DLMS object.
    #
    def __str__(self):
        str_ = None
        if self.shortName != 0:
            str_ = str(self.shortName)
        else:
            str_ = self.logicalName
        if self.description:
            str_ += " " + self.description
        return str_

    #
    # Interface type of the COSEM object.
    #
    def getObjectType(self):
        return self.objectType

    #
    # The base name of the object, if using SN.  When using SN
    #      referencing,
    # retrieves the base name of the DLMS object.  When using LN
    #      referencing,
    # the value is 0.
    #
    # The base name of the object.
    #
    def getShortName(self):
        return self.shortName

    def getName(self):
        if self.shortName != 0:
            return self.shortName
        return self.logicalName

    #
    # Logical or Short Name of DLMS object.
    #
    # Logical or Short Name of DLMS object
    #
    name = property(getName)

    #
    # Object attribute collection.
    #
    def getAttributes(self):
        return self.attributes

    #
    # Object method attribute collection.
    #
    def getMethodAttributes(self):
        return self.methodAttributes

    #
    # Returns is attribute read only.  -
    #
    # @param index
    # Attribute index.
    # Is attribute read only.
    #
    def getAccess(self, index):
        if index == 1:
            return AccessMode.READ
        att = self.attributes.find(index)
        if att is None:
            return AccessMode.READ_WRITE
        return att.access

    #
    # Set attribute access.
    #
    # @param index
    # Attribute index.
    # @param access
    # Attribute access.
    #
    def setAccess(self, index, access):
        att = self.attributes.find(index)
        if att is None:
            att = GXDLMSAttributeSettings(index)
            self.attributes.append(att)
        att.access = access

    #
    # Returns amount of methods.
    #
    @abstractmethod
    def getMethodCount(self):
        raise ValueError("getMethodCount")

    #
    # Returns is Method attribute read only.  -
    #
    # @param index
    # Method Attribute index.
    # Is attribute read only.
    #
    def getMethodAccess(self, index):
        att = self.getMethodAttributes().find(index)
        if att:
            return att.methodAccess
        return MethodAccessMode.ACCESS

    #
    # Set Method attribute access.
    #
    # @param index
    # Method index.
    # @param access
    # Method access mode.
    #
    def setMethodAccess(self, index, access):
        att = self.getMethodAttributes().find(index)
        if att is None:
            att = GXDLMSAttributeSettings(index)
            self.methodAttributes.append(att)
        att.methodAccess = access


    def getDataType(self, index):
        att = self.attributes.find(index)
        if not att:
            return DataType.NONE
        return att.type_



    def getUIDataType(self, index):
        att = self.attributes.find(index)
        if not att:
            return DataType.NONE
        return att.uiType


    #
    # Amount of attributes.
    #
    @abstractmethod
    def getAttributeCount(self):
        raise ValueError("getAttributeCount")

    #
    # Object values as an array.
    #
    @abstractmethod
    def getValues(self):
        raise ValueError("getValues")

    @abstractmethod
    def getValue(self, settings, e):
        #
        # Get value.
        # settings: DLMS settings.
        # e: Value event parameters.
        #
        raise ValueError("getValue")

    @abstractmethod
    def setValue(self, settings, e):
        #
        # Set value of given attribute.
        #
        # settings: DLMS settings.
        # e: event parameters.
        raise ValueError("setValue")

    #
    # Server calls this invokes method.
    # @param settings DLMS settings.
    # @param e Value event parameters.
    # pylint: disable=no-self-use
    def invoke(self, settings, e):
        #pylint: disable=unused-argument
        raise ValueError("invoke")

    def setDataType(self, index, type_):
        att = self.attributes.find(index)
        if att is None:
            att = GXDLMSAttributeSettings(index)
            self.attributes.append(att)
        att.type_ = type_

    def setUIDataType(self, index, type_):
        att = self.attributes.find(index)
        if att is None:
            att = GXDLMSAttributeSettings(index)
            self.attributes.append(att)
        att.uiType = type_

    def setStatic(self, index, isStatic):
        att = self.attributes.find(index)
        if att is None:
            att = GXDLMSAttributeSettings(index)
            self.attributes.append(att)
        att.static = isStatic

    def getStatic(self, index):
        att = self.attributes.find(index)
        if att is None:
            att = GXDLMSAttributeSettings(index)
            self.attributes.append(att)
        return att.static

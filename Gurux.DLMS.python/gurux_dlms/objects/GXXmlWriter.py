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

import xml.etree.cElementTree as ET
from ..GXByteBuffer import GXByteBuffer
from ..GXDateTime import GXDateTime
from ..GXDLMSConverter import GXDLMSConverter
from ..internal._GXCommon import _GXCommon
from ..enums import DataType

###Python 2 requires this
#pylint: disable=bad-option-value,old-style-class
class GXXmlWriter:
    """
    Save COSEM object to the file.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.objects = list()
        self.skipDefaults = False

    def getTarget(self):
        return self.objects[len(self.objects) - 1]

    # pylint: disable=unused-argument
    def writeStartElement(self, elementName, attributeName=None, value=None, newLine=True):
        target = None
        if value:
            target = ET.SubElement(self.getTarget(), elementName)
        else:
            target = ET.SubElement(self.getTarget(), elementName)

        if attributeName:
            target.set(attributeName, value)
        self.objects.append(target)
        return target

    def writeEndElement(self):
        self.objects.pop()


    def writeElementString(self, name, value, defaultValue=None):
        if not(value and self.skipDefaults) or value != defaultValue:
            if value is None:
                ET.SubElement(self.getTarget(), name)
            elif isinstance(value, str):
                ET.SubElement(self.getTarget(), name).text = value
            elif isinstance(value, GXDateTime):
                ET.SubElement(self.getTarget(), name).text = value.toFormatString()
            elif isinstance(value, bool):
                if value:
                    ET.SubElement(self.getTarget(), name).text = "1"
                else:
                    ET.SubElement(self.getTarget(), name).text = "0"
            elif isinstance(value, int):
                ET.SubElement(self.getTarget(), name).text = str(value)
            elif isinstance(value, (bytearray, bytes)):
                ET.SubElement(self.getTarget(), name).text = GXByteBuffer.hex(value)

    def writeArray(self, data):
        if isinstance(data, []):
            arr = data
            for tmp in arr:
                if isinstance(tmp, bytearray):
                    self.writeElementObject("Item", tmp, False)
                elif isinstance(tmp, (object,)):
                    self.writeStartElement("Item", "Type", str(DataType.ARRAY), True)
                    self.writeArray(tmp)
                    self.writeEndElement()
                else:
                    self.writeElementObject("Item", tmp)

    def __writeElementObject(self, name, value, type_, uiType):
        if type_ != DataType.NONE and isinstance(value, str):
            if type_ == DataType.OCTET_STRING:
                if uiType == DataType.STRING:
                    self.writeElementObject(name, (str(value)).encode(), True)
                elif uiType == DataType.OCTET_STRING:
                    self.writeElementObject(name, GXByteBuffer.hexToBytes(str(value)), True)
                return
            if not isinstance(value, (GXDateTime)):
                self.writeElementObject(name, GXDLMSConverter.changeType(value, type_), True)
                return
        self.writeElementObject(name, value, True)

    #
    # Write object value to file.
    #
    # @param name
    # Object name.
    # @param value
    # Object value.
    # @param skipDefaultValue
    # Is default value serialized.
    #
    # pylint: disable=too-many-arguments
    def writeElementObject(self, name, value, skipDefaultValue=True, type_=DataType.NONE, uiType=DataType.NONE):
        if value or not skipDefaultValue:
            if type_ == DataType.OCTET_STRING:
                if uiType == DataType.STRING:
                    value = str(value)
                elif uiType == DataType.OCTET_STRING:
                    value = GXByteBuffer.hexToBytes(value)
            elif not isinstance(value, GXDateTime):
                value = GXDLMSConverter.changeType(value, type_)

            dt = _GXCommon.getDLMSDataType(value)
            target = self.writeStartElement(name, "Type", str(dt), False)
            if dt == DataType.ARRAY:
                self.writeArray(value)
            else:
                if isinstance(value, GXDateTime):
                    target.text = value.toFormatString()
                elif isinstance(value, (bytearray, bytes)):
                    target.text = GXByteBuffer.hex(value)
                else:
                    target.text = str(value)
            self.writeEndElement()

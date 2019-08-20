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
from __future__ import print_function
import pkg_resources
from .enums import Standard, ObjectType, DataType
from .GXStandardObisCodeCollection import GXStandardObisCodeCollection
from .GXStandardObisCode import GXStandardObisCode
from .internal._GXCommon import _GXCommon
from .GXDate import GXDate
from .GXDateTime import GXDateTime
from .GXTime import GXTime
from .GXByteBuffer import GXByteBuffer
from .manufacturersettings.GXObisCode import GXObisCode

###Python 2 requires this
#pylint: disable=bad-option-value,old-style-class
class GXDLMSConverter:
    #
    # Constructor.
    #
    # value: Used standard.
    #
    def __init__(self, value=Standard.DLMS):
        self.standard = value
        # Collection of standard OBIS codes.
        self.codes = GXStandardObisCodeCollection()

    #
    # Get OBIS code description.
    #
    # @param logicalName
    # Logical name (OBIS code).
    # @param type
    # Object type.
    # @param description
    # Description filter.
    # Array of descriptions that match given OBIS code.
    #
    def getDescription(self, logicalName, type_=ObjectType.NONE, description=None):
        if not self.codes:
            self.__readStandardObisInfo(self.standard, self.codes)
        list_ = list()
        all_ = not logicalName
        for it in self.codes.find(logicalName, type_):
            if description and not it.description.lower().contains(description.lower()):
                continue
            if all_:
                list_.append("A=" + it.getOBIS()[0] + ", B=" + it.getOBIS()[1] + ", C=" + it.getOBIS()[2] + ", D=" + it.getOBIS()[3] + ", E=" + it.getOBIS()[4] + ", F=" + it.getOBIS()[5] + "\r\n" + it.description)
            else:
                list_.append(it.description)
        return list_

    #pylint: disable=too-many-boolean-expressions
    @classmethod
    def __updateOBISCodeInfo(cls, codes, it):
        if it.description:
            return
        ln = it.logicalName
        code_ = codes.find(ln, it.objectType)[0]
        if code_:
            it.description = code_.description
            if "10" in code_.dataType:
                code_.dataType = "10"
            elif "25" in code_.dataType or "26" in code_.dataType:
                code_.dataType = "25"
            elif "9" in code_.dataType:
                if (GXStandardObisCodeCollection.equalsMask2("0.0-64.96.7.10-14.255", ln) or GXStandardObisCodeCollection.equalsMask2("0.0-64.0.1.5.0-99,255", ln) or GXStandardObisCodeCollection.equalsMask2("0.0-64.0.1.2.0-99,255", ln) or GXStandardObisCodeCollection.equalsMask2("1.0-64.0.1.2.0-99,255", ln) or GXStandardObisCodeCollection.equalsMask2("1.0-64.0.1.5.0-99,255", ln) or GXStandardObisCodeCollection.equalsMask2("1.0-64.0.9.0.255", ln) or GXStandardObisCodeCollection.equalsMask2("1.0-64.0.9.6.255", ln) or GXStandardObisCodeCollection.equalsMask2("1.0-64.0.9.7.255", ln) or GXStandardObisCodeCollection.equalsMask2("1.0-64.0.9.13.255", ln) or GXStandardObisCodeCollection.equalsMask2("1.0-64.0.9.14.255", ln) or GXStandardObisCodeCollection.equalsMask2("1.0-64.0.9.15.255", ln)):
                    code_.dataType = "25"
                elif GXStandardObisCodeCollection.equalsMask2("1.0-64.0.9.1.255", ln):
                    code_.dataType = "27"
                elif GXStandardObisCodeCollection.equalsMask2("1.0-64.0.9.2.255", ln):
                    code_.dataType = "26"
            if not code_.dataType == "*" and not code_.dataType == "" and "," not in code_.dataType:
                type_ = code_.dataType
                it.uiDataType = 2, type_
        else:
            print("Unknown OBIS Code: " + it.logicalName + " Type: " + it.objectType)

    def updateOBISCodeInformation(self, objects):
        if not self.codes:
            self.__readStandardObisInfo(self.standard, self.codes)
        if isinstance(objects, list):
            for it in objects:
                self.__updateOBISCodeInfo(self.codes, it)
        else:
            self.__updateOBISCodeInfo(self.codes, objects)

    @classmethod
    def __getObjects(cls, standard):
        codes = list()
        if standard == Standard.ITALY:
            str_ = pkg_resources.resource_string(__name__, "Italy.txt").decode("utf-8")
        elif standard == Standard.INDIA:
            str_ = pkg_resources.resource_string(__name__, "India.txt").decode("utf-8")
        elif standard == Standard.SAUDI_ARABIA:
            str_ = pkg_resources.resource_string(__name__, "SaudiArabia.txt").decode("utf-8")
        if not str_:
            return None
        str_ = str_.replace("\r", " ")
        rows = str_.split('\n')
        for it in rows:
            items = it.split(';')
            if len(items) > 1:
                ot = ObjectType(int(items.get(0)))
                ln = _GXCommon.toLogicalName(_GXCommon.logicalNameToBytes(items.get(1)))
                version = int(items.get(2))
                desc = items.get(3)
                code_ = GXObisCode(ln, ot, desc)
                code_.version = version
                codes.append(code_)
        return codes

    @classmethod
    def __readStandardObisInfo(cls, standard, codes):
        if standard != Standard.DLMS:
            for it in cls.__getObjects(standard):
                tmp = GXStandardObisCode(None)
                tmp.interfaces = str(it.objectType)
                tmp.OBIS = it.logicalName.split('.')
                tmp.description = it.description
                codes.append(tmp)

        str_ = pkg_resources.resource_string(__name__, "OBISCodes.txt").decode("utf-8")
        str_ = str_.replace("\r", "")
        rows = str_.split('\n')
        for it in rows:
            if it != "":
                items = it.split(';')
                obis = items[0].split('.')
                try:
                    code_ = GXStandardObisCode(obis, str(items[3]) + "; " + str(items[4]) + "; " + str(items[5]) + "; " + str(items[6]) + "; " + str(items[7]), str(items[1]), str(items[2]))
                    codes.append(code_)
                except UnicodeEncodeError:
                    pass

    @classmethod
    def changeType(cls, value, type_):
        if _GXCommon.getDLMSDataType(value) == type_:
            return value
        if type_ == DataType.ARRAY:
            raise ValueError("Can't change array types.")
        if type_ == DataType.BCD:
            ret = int(value)
        elif type_ == DataType.BOOLEAN:
            ret = bool(value)
        elif type_ == DataType.COMPACT_ARRAY:
            raise ValueError("Can't change compact array types.")
        elif type_ == DataType.DATE:
            ret = GXDate(value)
        elif type_ == DataType.DATETIME:
            ret = GXDateTime(value)
        elif type_ == DataType.ENUM:
            raise ValueError("Can't change enumeration types.")
        elif type_ == DataType.FLOAT32:
            ret = float(value)
        elif type_ == DataType.FLOAT64:
            ret = float(value)
        elif type_ == DataType.INT16:
            ret = int(value)
        elif type_ == DataType.INT32:
            ret = int(value)
        elif type_ == DataType.INT64:
            ret = int(value)
        elif type_ == DataType.INT8:
            ret = int(value)
        elif type_ == DataType.NONE:
            ret = None
        elif type_ == DataType.OCTET_STRING:
            if isinstance(value, str):
                ret = GXByteBuffer.hexToBytes(str(value))
            else:
                raise ValueError("Can't change octect string type.")
        elif type_ == DataType.STRING:
            ret = str(value)
        elif type_ == DataType.BITSTRING:
            ret = str(value)
        elif type_ == DataType.STRING_UTF8:
            ret = str(value)
        elif type_ == DataType.STRUCTURE:
            raise ValueError("Can't change structure types.")
        elif type_ == DataType.TIME:
            ret = GXTime(value)
        elif type_ == DataType.UINT16:
            ret = int(value)
        elif type_ == DataType.UINT32:
            ret = int(value)
        elif type_ == DataType.UINT64:
            ret = int(value)
        elif type_ == DataType.UINT8:
            ret = int(value)
        else:
            raise ValueError('Invalid data type.')
        return ret

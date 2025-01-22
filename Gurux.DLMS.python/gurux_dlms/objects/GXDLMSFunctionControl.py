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
#  self file is a part of Gurux Device Framework.
#
#  Gurux Device Framework is Open Source software you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http:#www.gurux.org
#
#  self code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http:#www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from ..enums import ObjectType, DataType, ErrorCode


class GXDLMSFunctionControl(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
        https://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSFunctionControl
    """

    def __init__(self, ln="0.0.1.0.0.255", sn=0):
        """
        Constructor.

            Parameters:
                ln: Logical Name of the object.
                sn: Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.FUNCTION_CONTROL, ln, sn)
        self.__activationStatus = []
        self.__functionList = []

    @property
    def activationStatus(self):
        """
        The current status of each functional block defined in the functions property.
        """
        return self.__activationStatus

    @activationStatus.setter
    def activationStatus(self, value):
        self.__activationStatus = value

    @property
    def functionList(self):
        """
        List of modified functions.
        """
        return self.__functionList

    @functionList.setter
    def functionList(self, value):
        self.__functionList = value

    @classmethod
    def __functionStatusToByteArray(cls, functions):
        """
        Convert function states to byte array.

            Parameters:
                functions: Functions.

            Returns:
        """
        bb = GXByteBuffer()
        bb.setUInt8(DataType.ARRAY)
        _GXCommon.setObjectCount(len(functions), bb)
        for k, v in functions:
            bb.setUInt8(DataType.STRUCTURE)
            bb.setUInt8(2)
            bb.setUInt8(DataType.OCTET_STRING)
            _GXCommon.setObjectCount(len(k), bb)
            bb.set(k.encode())
            bb.setUInt8(DataType.BOOLEAN)
            bb.setUInt8((1 if v else 0))
        return bb.array()

    @classmethod
    def __functionStatusFromByteArray(cls, values):
        """
        Get function states from byte array.

            Parameters:
                values: Byte buffer.

            Returns:
                Function statuses.
        """
        functions = []
        for it in values:
            functions.append((it[0].decode(), it[1]))
        return functions

    @classmethod
    def __functionListToByteArray(cls, functions):
        """
        Convert function list to byte array.

            Parameters:
                functions: Functions.

            Returns:
                Action bytes.
        """
        bb = GXByteBuffer()
        bb.setUInt8(DataType.ARRAY)
        _GXCommon.setObjectCount(len(functions), bb)
        for k, v in functions:
            bb.setUInt8(DataType.STRUCTURE)
            bb.setUInt8(2)
            bb.setUInt8(DataType.OCTET_STRING)
            _GXCommon.setObjectCount(len(k), bb)
            bb.set(str(k))
            bb.setUInt8(DataType.ARRAY)
            _GXCommon.setObjectCount(len(v), bb)
            for obj in v:
                bb.setUInt8(DataType.STRUCTURE)
                bb.setUInt8(2)
                # Object type.
                bb.setUInt8(DataType.UINT16)
                bb.setUInt16(obj.objectType)
                # LN
                _GXCommon.setData(
                    None,
                    bb,
                    DataType.OCTET_STRING,
                    _GXCommon.logicalNameToBytes(obj.logicalName),
                )
        return bb.array()

    @classmethod
    def __functionListFromByteArray(cls, values):
        """
        Convert function list to byte array.

            Parameters:
                functions: Functions.

            Returns:
                Action bytes.
        """
        # pylint: disable=import-outside-toplevel,unidiomatic-typecheck
        from .._GXObjectFactory import _GXObjectFactory

        functions = []
        for it in values:
            fn = it[0].decode()
            objects = []
            for it2 in it[1]:
                ot = ObjectType(it2[0])
                obj = _GXObjectFactory.createObject(ot)
                obj.logicalName = _GXCommon.toLogicalName(it2[1])
                objects.append(obj)
            functions.append((fn, objects))
        return functions

    def invoke(self, settings, e):
        # pylint: disable=import-outside-toplevel,unidiomatic-typecheck
        from .._GXObjectFactory import _GXObjectFactory

        if e.index == 1:
            functions = self.__functionStatusFromByteArray(e.parameters)
            for k, v in functions:
                for pos in range(0, len(self.__activationStatus) - 1):
                    it = self.__activationStatus[pos]
                    if k == it:
                        it = v
        elif e.index == 2:
            fn = e.parameters[0].decode()
            objects = []
            for it2 in it[1]:
                obj = _GXObjectFactory.CreateObject(it2[0])
                obj.LogicalName = _GXCommon.toLogicalName(it2[1])
                objects.append(obj)
            for it in self.__functionList:
                if it[0] == fn:
                    self.__functionList.remove(it)
            self.__functionList.append((fn, objects))
            self.__activationStatus.append((fn, True))
        elif e.index == 3:
            fn = e.parameters.decode()
            for it in self.__functionList:
                if it[0] == fn:
                    self.__functionList.remove(it)
            for it in self.__activationStatus:
                if it[0] == fn:
                    self.__activationStatus.remove(it)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return None

    def getAttributeIndexToRead(self, all_):
        attributes = []
        # LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        # activation_status
        if all_ or self.canRead(2):
            attributes.append(2)
        # function_list
        if all_ or self.canRead(3):
            attributes.append(3)
        return attributes

    def getNames(self):
        return ("Logical Name", "ActivationStatus", "FunctionList")

    def getMethodNames(self):
        return ("SetFunctionStatus", "AddFunction", "RemoveFunction")

    def getAttributeCount(self):
        return 3

    def getMethodCount(self):
        return 3

    def getValue(self, settings, e):
        if e.index == 1:
            return _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            return self.__functionStatusToByteArray(self.__activationStatus)
        elif e.index == 3:
            return self.__functionListToByteArray(self.__functionList)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return None

    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.__activationStatus = self.__functionStatusFromByteArray(e.value)
        elif e.index == 3:
            self.__functionList = self.__functionListFromByteArray(e.value)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def getValues(self):
        return (self.logicalName, self.__activationStatus, self.__functionList)

    def setFunctionStatus(self, client, functions):
        """
        Adjusts the value of the current credit amount attribute.

            Parameters:
                client: DLMS client.
                functions: Enabled or disabled functions.

            Returns:
                Action bytes.
        """
        return client.method(
            self, 1, self.__functionStatusToByteArray(functions), DataType.ARRAY
        )

    def addFunction(self, client, name, functions):
        """
        Adds a new function to the attribute function list.

            Parameters:
                client: DLMS client.
                functions: Added functions.

            Returns:
                Action bytes.
        """
        bb = GXByteBuffer()
        bb.setUInt8(DataType.STRUCTURE)
        bb.setUInt8(2)
        bb.setUInt8(DataType.OCTET_STRING)
        _GXCommon.setObjectCount(len(name), bb)
        bb.set(name.encode())
        bb.setUInt8(DataType.ARRAY)
        _GXCommon.setObjectCount(len(functions), bb)
        for it in functions:
            bb.setUInt8(DataType.STRUCTURE)
            bb.setUInt8(2)
            _GXCommon.setData(None, bb, DataType.UINT16, it.objectType)
            _GXCommon.setData(
                None,
                bb,
                DataType.OCTET_STRING,
                _GXCommon.logicalNameToBytes(it.logicalName),
            )
        return client.method(self, 2, bb.array(), DataType.ARRAY)

    def removeFunction(self, client, name):
        """
        Removes a function from the attribute function list.

            Parameters:
                client: DLMS client.
                functions: Removed function name.

            Returns:
                Action bytes.
        """
        bb = GXByteBuffer()
        bb.setUInt8(DataType.OCTET_STRING)
        _GXCommon.setObjectCount(len(name), bb)
        bb.set(name.encode())
        return client.method(self, 3, bb.array(), DataType.ARRAY)

    def getDataType(self, index):
        """
        Returns device data type of selected attribute index.

            Parameters:
                index: Attribute index of the object.

            Returns:
                Device data type of the object.
        """
        if index == 1:
            return DataType.OCTET_STRING
        elif index in (2, 3):
            return DataType.ARRAY
        else:
            raise ValueError("GetDataType failed. Invalid attribute index.")

    def load(self, reader):
        # pylint: disable=import-outside-toplevel,unidiomatic-typecheck
        from .._GXObjectFactory import _GXObjectFactory

        if reader.isStartElement("Activations", True):
            self.__activationStatus.clear()
            while reader.isStartElement("Item", True):
                name = reader.readElementContentAsString("Name")
                status = reader.readElementContentAsInt("Status") != 0
                self.__activationStatus.append((name, status))
            reader.readEndElement("Activations")
        if reader.isStartElement("Functions", True):
            self.functionList.clear()
            while reader.isStartElement("Item", True):
                name = reader.readElementContentAsString("Name")
                objects = []
                self.__functionList.append((name, objects))
                if reader.isStartElement("Objects", True):
                    while reader.isStartElement("Object", True):
                        ot = ObjectType(reader.readElementContentAsInt("ObjectType"))
                        ln = reader.readElementContentAsString("LN")
                        obj = _GXObjectFactory.CreateObject(ot)
                        obj.LogicalName = ln
                        objects.Add(obj)
                    reader.readEndElement("Objects")
            reader.readEndElement("Functions")

    def save(self, writer):
        writer.writeStartElement("Activations")
        for k, v in self.__activationStatus:
            writer.writeStartElement("Item")
            writer.writeElementString("Name", k)
            writer.writeElementString("Status", v)
            writer.WriteEndElement()
        writer.WriteEndElement()  # Activations

        writer.writeStartElement("Functions")
        for k, v in self.__functionList:
            writer.writeStartElement("Item")
            writer.writeElementString("Name", k)
            writer.writeStartElement("Objects")
            for obj in v:
                writer.writeStartElement("Object")
                writer.writeElementString("ObjectType", obj.objectType)
                writer.writeElementString("LN", obj.logicalName)
                writer.WriteEndElement()  # Object
            writer.WriteEndElement()  # Objects
            writer.WriteEndElement()  # Item
        writer.WriteEndElement()  # Functions

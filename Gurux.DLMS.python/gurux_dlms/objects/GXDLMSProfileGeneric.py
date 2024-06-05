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
from datetime import timedelta
from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ErrorCode
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from ..GXDateTime import GXDateTime
from ..enums import ObjectType, DataType
from .enums import SortMethod
from .GXDLMSCaptureObject import GXDLMSCaptureObject
from .GXDLMSDemandRegister import GXDLMSDemandRegister
from .GXDLMSRegister import GXDLMSRegister
from ..ValueEventArgs import ValueEventArgs
from ..internal._GXDataInfo import _GXDataInfo


# pylint: disable=too-many-instance-attributes
class GXDLMSProfileGeneric(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSProfileGeneric
    """

    #
    # Constructor.
    #
    # @param ln
    # Logical Name of the object.
    # @param sn
    # Short Name of the object.
    def __init__(self, ln=None, sn=0):
        # pylint: disable=super-with-arguments
        super(GXDLMSProfileGeneric, self).__init__(ObjectType.PROFILE_GENERIC, ln, sn)
        self.version = 1
        self.buffer = []
        self.captureObjects = []
        self.capturePeriod = 0
        self.sortMethod = SortMethod.FIFO
        self.sortObject = None
        self.entriesInUse = 0
        self.profileEntries = 0
        self.sortObjectAttributeIndex = 0
        self.sortObjectDataIndex = 0

    #
    # Clears the buffer.
    #
    # @param client
    # DLMS client.
    # Action bytes.
    def reset(self, client):
        return client.method(self, 1, 0, DataType.INT8)

    # Copies the values of the objects to capture into the buffer by
    #      reading
    # each capture object.
    #
    # @param client
    # DLMS client.
    # Action bytes.
    def capture(self, client):
        return client.method(self, 2, 0, DataType.INT8)

    #
    # Add new capture object (column) to the profile generic.
    #
    def addCaptureObject(self, item, attributeIndex, dataIndex):
        if item is None:
            raise ValueError("Invalid Object")
        # Don't check attributeIndex. Some meters are using -1.
        if dataIndex < 0:
            raise ValueError("Invalid data index")
        co = GXDLMSCaptureObject(attributeIndex, dataIndex)
        self.captureObjects.append((item, co))

    def getValues(self):
        return [
            self.logicalName,
            self.buffer,
            self.captureObjects,
            self.capturePeriod,
            self.sortMethod,
            self.sortObject,
            self.entriesInUse,
            self.profileEntries,
        ]

    def invoke(self, settings, e):
        if e.index == 1:
            #  Reset.
            self.__reset()
        elif e.index == 2:
            #  Capture.
            self.__capture(e.server)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    #
    # Returns collection of attributes to read.
    # If attribute is static and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = []
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  Buffer
        if all_ or not self.isRead(2):
            attributes.append(2)
        #  CaptureObjects
        if all_ or not self.isRead(3):
            attributes.append(3)
        #  CapturePeriod
        if all_ or not self.isRead(4):
            attributes.append(4)
        #  SortMethod
        if all_ or not self.isRead(5):
            attributes.append(5)
        #  SortObject
        if all_ or not self.isRead(6):
            attributes.append(6)
        #  EntriesInUse
        if all_ or not self.isRead(7):
            attributes.append(7)
        #  ProfileEntries
        if all_ or not self.isRead(8):
            attributes.append(8)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 8

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 2

    #
    # Returns captured columns.
    #
    def __getColumns(self, settings):
        cnt = len(self.captureObjects)
        data = GXByteBuffer()
        data.setUInt8(DataType.ARRAY)
        #  Add count
        _GXCommon.setObjectCount(cnt, data)
        for k, v in self.captureObjects:
            data.setUInt8(DataType.STRUCTURE)
            #  Count
            data.setUInt8(4)
            #  ClassID
            _GXCommon.setData(settings, data, DataType.UINT16, k.objectType)
            _GXCommon.setData(
                settings,
                data,
                DataType.OCTET_STRING,
                _GXCommon.logicalNameToBytes(k.logicalName),
            )
            _GXCommon.setData(settings, data, DataType.INT8, v.attributeIndex)
            _GXCommon.setData(settings, data, DataType.UINT16, v.dataIndex)
        return data

    def getData(self, settings, e, table, columns):
        data = GXByteBuffer()
        if settings.index == 0:
            data.setUInt8(DataType.ARRAY)
            if e.rowEndIndex != 0:
                _GXCommon.setObjectCount(e.rowEndIndex - e.rowBeginIndex, data)
            else:
                _GXCommon.setObjectCount(len(table), data)
        types = [None] * len(self.captureObjects)
        pos = 0
        for k, v in self.captureObjects:
            types[pos] = k.getDataType(v.attributeIndex)
            pos += 1
        tp = None
        for row in table:
            items = row
            data.setUInt8(DataType.STRUCTURE)
            if not columns:
                _GXCommon.setObjectCount(0, data)
            else:
                _GXCommon.setObjectCount(len(columns), data)
            pos = 0
            for value in items:
                if columns is None or self.captureObjects[pos] in columns:
                    tp = types[pos]
                    if tp == DataType.NONE:
                        tp = _GXCommon.getDLMSDataType(value)
                        types[pos] = tp
                    _GXCommon.setData(settings, data, tp, value)
                pos += 1
            settings.setIndex(settings.index + 1)
        if e.getRowEndIndex() != 0:
            e.setRowBeginIndex(len(table))
        return data.array()

    def getColumns(self, cols):
        columns = None
        if cols:
            columns = []
            for it in cols:
                ot = ObjectType(it[0])
                ln = _GXCommon.toLogicalName(it[1])
                attributeIndex = it[2]
                dataIndex = it[3]
                for k, v in self.captureObjects:
                    if (
                        k.objectType == ot
                        and v.attributeIndex == attributeIndex
                        and v.dataIndex == dataIndex
                        and k.logicalName == ln
                    ):
                        columns.append((k, v))
                        break
        else:
            colums = []
            colums.append(self.captureObjects)
            return colums
        return columns

    def getSelectedColumns(self, selector, parameters):
        if selector == 0:
            colums = []
            colums.append(self.captureObjects)
            ret = colums
        elif selector == 1:
            ret = self.getColumns((parameters)[3])
        elif selector == 2:
            arr = parameters
            colStart = 1
            colCount = 0
            if len(arr) > 2:
                colStart = arr[2]
            if len(arr) > 3:
                colCount = arr[3]
            elif colStart != 1:
                colCount = len(self.captureObjects)
            if colStart != 1 or colCount != 0:
                return self.captureObjects[colStart - 1 : colStart + colCount - 1]
            colums = []
            colums.append(self.captureObjects)
            ret = colums
        else:
            raise ValueError("Invalid selector.")
        return ret

    def __getProfileGenericData(self, settings, e):
        # pylint: disable=bad-option-value,chained-comparison
        columns = None
        if e.selector == 0 or e.parameters is None or e.getRowEndIndex() != 0:
            return self.getData(settings, e, self.buffer, columns)
        arr = e.parameters
        columns = self.getSelectedColumns(e.selector, arr)
        table = []
        if e.selector == 1:
            info = _GXDataInfo()
            info.type_ = DataType.DATETIME
            start = _GXCommon.getData(settings, GXByteBuffer(arr[1]), info).value
            info.clear()
            info.type_ = DataType.DATETIME
            end = _GXCommon.getData(settings, GXByteBuffer(arr[2]), info).value
            for row in self.buffer:
                tm = None
                tmp = (row)[0]
                if isinstance(tmp, GXDateTime):
                    tm = tmp.value
                else:
                    tm = tmp
                if tm >= start >= 0 and tm <= end:
                    table.append(row)
        elif e.selector == 2:
            start = arr[0]
            if start == 0:
                start = 1
            count = arr[1]
            if count == 0:
                count = len(self.buffer)
            if start + count > len(self.buffer):
                count = len(self.buffer)
            pos = 0
            while pos < count:
                if pos + start - 1 == len(self.buffer):
                    break
                table.append(self.buffer[start + pos - 1])
                pos += 1
        else:
            raise ValueError("Invalid selector.")
        return self.getData(settings, e, table, columns)

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.ARRAY
        elif index == 3:
            ret = DataType.ARRAY
        elif index == 4:
            ret = DataType.UINT32
        elif index == 5:
            ret = DataType.ENUM
        elif index == 6:
            ret = DataType.ARRAY
        elif index == 7:
            ret = DataType.UINT32
        elif index == 8:
            ret = DataType.UINT32
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret

    def getValue(self, settings, e):
        # pylint: disable=bad-option-value,redefined-variable-type
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.__getProfileGenericData(settings, e)
        elif e.index == 3:
            ret = self.__getColumns(settings)
        elif e.index == 4:
            ret = self.capturePeriod
        elif e.index == 5:
            ret = self.sortMethod
        elif e.index == 6:
            data = GXByteBuffer()
            data.setUInt8(DataType.STRUCTURE)
            data.setUInt8(int(4))
            if self.sortObject is None:
                _GXCommon.setData(settings, data, DataType.UINT16, 0)
                _GXCommon.setData(settings, data, DataType.OCTET_STRING, bytearray(6))
                _GXCommon.setData(settings, data, DataType.INT8, 0)
                _GXCommon.setData(settings, data, DataType.UINT16, 0)
            else:
                _GXCommon.setData(
                    settings, data, DataType.UINT16, self.sortObject.objectType
                )
                _GXCommon.setData(
                    settings,
                    data,
                    DataType.OCTET_STRING,
                    _GXCommon.logicalNameToBytes(self.sortObject.logicalName),
                )
                _GXCommon.setData(
                    settings, data, DataType.INT8, self.sortObjectAttributeIndex
                )
                _GXCommon.setData(
                    settings, data, DataType.UINT16, self.sortObjectDataIndex
                )
            ret = data.array()
        elif e.index == 7:
            ret = self.entriesInUse
        elif e.index == 8:
            ret = self.profileEntries
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    def setValue(self, settings, e):
        # pylint: disable=import-outside-toplevel
        from .._GXObjectFactory import _GXObjectFactory

        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.__setBuffer(settings, e)
        elif e.index == 3:
            self.captureObjects = []
            self.buffer = []
            self.entriesInUse = 0
            if e.value:
                for it in e.value:
                    tmp = it
                    if len(tmp) != 4:
                        raise Exception("Invalid structure format.")
                    type_ = tmp[0]
                    ln = _GXCommon.toLogicalName(tmp[1])
                    obj = None
                    if settings and settings.objects:
                        obj = settings.objects.findByLN(type_, ln)
                    if obj is None:
                        obj = _GXObjectFactory.createObject(type_)
                        obj.logicalName = ln
                    index = tmp[2]
                    self.addCaptureObject(obj, index, tmp[3])
        elif e.index == 4:
            if settings and settings.isServer:
                self.__reset()
            if e.value is None:
                self.capturePeriod = 0
            else:
                self.capturePeriod = e.value
        elif e.index == 5:
            # pylint: disable=bad-option-value,redefined-variable-type
            if settings and settings.isServer:
                self.__reset()
            if e.value is None:
                self.sortMethod = SortMethod.FIFO
            else:
                self.sortMethod = SortMethod(e.value)
        elif e.index == 6:
            if settings and settings.isServer:
                self.__reset()
            if e.value is None:
                self.sortObject = None
            else:
                tmp = e.value
                if len(tmp) != 4:
                    raise ValueError("Invalid structure format.")
                type_ = ObjectType(tmp[0])
                ln = _GXCommon.toLogicalName(tmp[1])
                attributeIndex = tmp[2]
                dataIndex = tmp[3]
                self.sortObject = settings.objects.findByLN(type_, ln)
                if self.sortObject is None:
                    self.sortObject = _GXObjectFactory.createObject(type_)
                    self.sortObject.logicalName = ln
                self.sortObjectAttributeIndex = attributeIndex
                self.sortObjectDataIndex = dataIndex
        elif e.index == 7:
            if e.value is None:
                self.entriesInUse = 0
            else:
                self.entriesInUse = e.value
        elif e.index == 8:
            if settings and settings.isServer:
                self.__reset()
            if e.value is None:
                self.profileEntries = 0
            else:
                self.profileEntries = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def __setBuffer(self, settings, e):
        # pylint: disable=broad-except,too-many-nested-blocks,consider-using-enumerate
        cols = e.parameters
        colIndex = 0
        if cols is None:
            cols = self.captureObjects
        if cols is None or not cols:
            raise ValueError("Read capture objects first.")
        if e.value:
            colIndex += 1
            lastDate = None
            types = []
            colIndex = 0
            for k, v in cols:
                types.append(k.getUIDataType(v.attributeIndex))
            for it in e.value:
                row = it
                if len(row) != len(cols):
                    raise ValueError("Number of columns do not match.")
                for colIndex in range(len(row)):
                    data = row[colIndex]
                    type_ = types[colIndex]
                    if type_ != DataType.NONE and isinstance(data, bytearray):
                        data = _GXCommon.changeType(settings, data, type_)
                        if isinstance(data, GXDateTime):
                            lastDate = data.value
                        row[colIndex] = data
                    elif type_ == DataType.DATETIME and data is None:
                        if not lastDate and self.buffer:
                            lastDate = self.buffer[len(self.buffer) - 1][colIndex].value
                        if lastDate:
                            if self.sortMethod in (
                                SortMethod.FIFO,
                                SortMethod.SMALLEST,
                            ):
                                lastDate += timedelta(seconds=self.capturePeriod)
                            else:
                                lastDate -= timedelta(seconds=self.capturePeriod)
                            row[colIndex] = GXDateTime(lastDate)
                    elif type_ == DataType.DATETIME and not isinstance(
                        row[colIndex], GXDateTime
                    ):
                        row[colIndex] = GXDateTime.fromUnixTime(row[colIndex])
                    item = cols[colIndex]
                    if (
                        isinstance(item[0], GXDLMSRegister)
                        and item[1].attributeIndex == 2
                    ):
                        scaler_ = item[0].scaler
                        if scaler_ != 1 and data:
                            try:
                                row[colIndex] = data * scaler_
                            except Exception:
                                print(
                                    "Scalar failed for: {}".format(item[0].logicalName)
                                )
                    elif isinstance(item[0], GXDLMSDemandRegister) and (
                        item[1].attributeIndex == 2 or item[1].attributeIndex == 3
                    ):
                        scaler_ = item[0].scaler
                        if scaler_ != 1 and data:
                            try:
                                row[colIndex] = data * scaler_
                            except Exception:
                                print(
                                    "Scalar failed for: {}".format(item[0].logicalName)
                                )
                    colIndex += 1
                self.buffer.append(row)
            if e.settings.isServer:
                self.entriesInUse = len(self.buffer)

    def __reset(self):
        self.buffer = []
        self.entriesInUse = 0

    def __capture(self, server):
        srv = server
        values = [None] * len(self.captureObjects)
        pos = 0
        args = [ValueEventArgs(srv, self, 2)]
        srv.onPreGet(args)
        if not args[0].handled:
            for k, v in self.captureObjects:
                values[pos] = k.values()[v.attributeIndex - 1]
                pos += 1
            if self.profileEntries:
                self.entriesInUse -= 1
                self.buffer.remove(0)
            self.buffer.append(values)
            self.entriesInUse += 1
        srv.onPostGet(args)
        srv.onAction(args)
        srv.onPostAction(args)

    def load(self, reader):
        # pylint: disable=import-outside-toplevel
        from .._GXObjectFactory import _GXObjectFactory

        self.buffer = []
        if reader.isStartElement("Buffer", True):
            while reader.isStartElement("Row", True):
                row = []
                while reader.isStartElement("Cell", False):
                    row.append(reader.readElementContentAsObject("Cell", None))
                self.buffer.append(row)
            reader.readEndElement("Buffer")
        self.captureObjects = []
        if reader.isStartElement("CaptureObjects", True):
            while reader.isStartElement("Item", True):
                ot = reader.readElementContentAsInt("ObjectType")
                ln = reader.readElementContentAsString("LN")
                ai = reader.readElementContentAsInt("Attribute")
                di = reader.readElementContentAsInt("Data")
                co = GXDLMSCaptureObject(ai, di)
                obj = reader.objects.findByLN(ot, ln)
                if obj is None:
                    obj = _GXObjectFactory.createObject(ot)
                    obj.logicalName = ln
                self.captureObjects.append((obj, co))
            reader.readEndElement("CaptureObjects")
        self.capturePeriod = reader.readElementContentAsInt("CapturePeriod")
        self.sortMethod = SortMethod(reader.readElementContentAsInt("SortMethod"))
        if reader.isStartElement("SortObject", True):
            self.capturePeriod = reader.readElementContentAsInt("CapturePeriod")
            ot = reader.readElementContentAsInt("ObjectType")
            ln = reader.readElementContentAsString("LN")
            self.sortObject = reader.objects.findByLN(ot, ln)
            reader.readEndElement("SortObject")
        self.entriesInUse = reader.readElementContentAsInt("EntriesInUse")
        self.profileEntries = reader.readElementContentAsInt("ProfileEntries")

    def save(self, writer):
        writer.writeStartElement("Buffer")
        if self.buffer:
            for row in self.buffer:
                writer.writeStartElement("Row")
                for it in row:
                    writer.writeElementObject("Cell", it)
                writer.writeEndElement()
        writer.writeEndElement()
        writer.writeStartElement("CaptureObjects")
        if self.captureObjects:
            for k, v in self.captureObjects:
                writer.writeStartElement("Item")
                writer.writeElementString("ObjectType", int(k.objectType))
                writer.writeElementString("LN", k.logicalName)
                writer.writeElementString("Attribute", v.attributeIndex)
                writer.writeElementString("Data", v.dataIndex)
                writer.writeEndElement()
        writer.writeEndElement()
        writer.writeElementString("CapturePeriod", self.capturePeriod)
        writer.writeElementString("SortMethod", int(self.sortMethod))
        if self.sortObject:
            writer.writeStartElement("SortObject")
            writer.writeElementString("ObjectType", int(self.sortObject.objectType))
            writer.writeElementString("LN", self.sortObject.logicalName)
            writer.writeEndElement()
        writer.writeElementString("EntriesInUse", self.entriesInUse)
        writer.writeElementString("ProfileEntries", self.profileEntries)

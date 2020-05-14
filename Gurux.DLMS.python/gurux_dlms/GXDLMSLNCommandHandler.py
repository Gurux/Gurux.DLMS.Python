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
from .ActionRequestType import ActionRequestType
from .internal._GXCommon import _GXCommon
from .enums import Command, ErrorCode, ObjectType
from .ServiceError import ServiceError
from .enums.Service import Service
from .ConfirmedServiceError import ConfirmedServiceError
from .TranslatorTags import TranslatorTags
from .GXByteBuffer import GXByteBuffer
from .enums.AccessServiceCommandType import AccessServiceCommandType
from .internal._GXDataInfo import _GXDataInfo
from .TranslatorOutputType import TranslatorOutputType
from .SingleReadResponse import SingleReadResponse
from .GetCommandType import GetCommandType
from .GXDLMSLNParameters import GXDLMSLNParameters
from .SetRequestType import SetRequestType
from .ValueEventArgs import ValueEventArgs
from .enums.DataType import DataType
from .objects.enums.AssociationStatus import AssociationStatus
from .ConnectionState import ConnectionState
from .objects.GXDLMSAssociationLogicalName import GXDLMSAssociationLogicalName
from .objects.GXDLMSSecuritySetup import GXDLMSSecuritySetup
from .GXDLMS import GXDLMS
from .GXDLMSLongTransaction import GXDLMSLongTransaction
from .enums.AccessMode import AccessMode
from .enums.MethodAccessMode import MethodAccessMode
from .objects.GXDLMSProfileGeneric import GXDLMSProfileGeneric

# pylint: disable=bad-option-value,too-many-locals,too-many-arguments,broad-except,too-many-nested-blocks,old-style-class
class GXDLMSLNCommandHandler:
    #Constructor.
    def __init__(self):
        pass

    # pylint: too-many-arguments
    @classmethod
    def handleGetRequest(cls, settings, server, data, replyData, xml):
        #  Return error if connection is not established.
        if xml is None and not settings.acceptConnection():
            replyData.set(server.generateConfirmedServiceError(ConfirmedServiceError.INITIATE_ERROR, ServiceError.SERVICE, Service.UNSUPPORTED))
            return
        #  Get type.
        type_ = int(data.getUInt8())
        #  Get invoke ID and priority.
        invokeID = data.getUInt8()
        settings.updateInvokeId(invokeID)
        if xml:
            xml.appendStartTag(Command.GET_REQUEST)
            xml.appendStartTag(Command.GET_REQUEST, type_)
            xml.appendLine(TranslatorTags.INVOKE_ID, "Value", xml.integerToHex(invokeID, 2))
        #  GetRequest normal
        if type_ == GetCommandType.NORMAL:
            cls.getRequestNormal(settings, invokeID, server, data, replyData, xml)
        elif type_ == GetCommandType.NEXT_DATA_BLOCK:
            #  Get request for next data block
            cls.getRequestNextDataBlock(settings, invokeID, server, data, replyData, xml, False)
        elif type_ == GetCommandType.WITH_LIST:
            #  Get request with a list.
            cls.getRequestWithList(settings, invokeID, server, data, replyData, xml)
        else:
            bb = GXByteBuffer()
            settings.resetBlockIndex()
            #  Access Error : Device reports a hardware fault.
            bb.setUInt8(ErrorCode.HARDWARE_FAULT)
            GXDLMS.getLNPdu(GXDLMSLNParameters(settings, invokeID, Command.GET_RESPONSE, type_, None, bb, ErrorCode.OK), replyData)
        if xml:
            xml.appendEndTag(Command.GET_REQUEST, type_)
            xml.appendEndTag(Command.GET_REQUEST)

    #
    # Handle set request.
    #
    # Reply to the client.
    #
    @classmethod
    def handleSetRequest(cls, settings, server, data, replyData, xml):
        #  Return error if connection is not established.
        if xml is None and not settings.acceptConnection():
            replyData.set(server.generateConfirmedServiceError(ConfirmedServiceError.INITIATE_ERROR, ServiceError.SERVICE, Service.UNSUPPORTED))
            return
        #  Get type.
        type_ = int(data.getUInt8())
        #  Get invoke ID and priority.
        invoke = data.getUInt8()
        settings.updateInvokeId(invoke)
        #  SetRequest normal or Set Request With First Data Block
        p = GXDLMSLNParameters(settings, invoke, Command.SET_RESPONSE, type_, None, None, 0)
        if xml:
            xml.appendStartTag(Command.SET_REQUEST)
            xml.appendStartTag(Command.SET_REQUEST, type_)
            #  InvokeIdAndPriority
            xml.appendLine(TranslatorTags.INVOKE_ID, "Value", xml.integerToHex(invoke, 2))
        if type_ in (SetRequestType.NORMAL, SetRequestType.FIRST_DATA_BLOCK):
            cls.handleSetRequestNormal(settings, server, data, type_, p, xml)
        elif type_ == SetRequestType.WITH_DATA_BLOCK:
            cls.hanleSetRequestWithDataBlock(settings, server, data, p, xml)
        elif type_ == SetRequestType.WITH_LIST:
            cls.hanleSetRequestWithList(settings, invoke, server, data, xml)
        else:
            settings.resetBlockIndex()
            p.status = ErrorCode.HARDWARE_FAULT
        if xml:
            xml.appendEndTag(Command.SET_REQUEST, type_)
            xml.appendEndTag(Command.SET_REQUEST)
            return
        GXDLMS.getLNPdu(p, replyData)

    @classmethod
    def appendAttributeDescriptor(cls, xml, ci, ln, attributeIndex):
        xml.appendStartTag(TranslatorTags.ATTRIBUTE_DESCRIPTOR)
        if xml.comments:
            ot = ObjectType(ci)
            if ot:
                xml.appendComment(str(ot))
        xml.appendLine(TranslatorTags.CLASS_ID, "Value", xml.integerToHex(ci, 4))
        xml.appendComment(_GXCommon.toLogicalName(ln))
        xml.appendLine(TranslatorTags.INSTANCE_ID, "Value", GXByteBuffer.hex(ln, False))
        xml.appendLine(TranslatorTags.ATTRIBUTE_ID, "Value", xml.integerToHex(attributeIndex, 2))
        xml.appendEndTag(TranslatorTags.ATTRIBUTE_DESCRIPTOR)

    @classmethod
    def appendMethodDescriptor(cls, xml, ci, ln, attributeIndex):
        xml.appendStartTag(TranslatorTags.METHOD_DESCRIPTOR)
        if xml.comments:
            ot = ObjectType(ci)
            if ot:
                xml.appendComment(str(ot))
        xml.appendLine(TranslatorTags.CLASS_ID, "Value", xml.integerToHex(ci, 4))
        xml.appendComment(_GXCommon.toLogicalName(ln))
        xml.appendLine(TranslatorTags.INSTANCE_ID, "Value", GXByteBuffer.hex(ln, False))
        xml.appendLine(TranslatorTags.METHOD_ID, "Value", xml.integerToHex(attributeIndex, 2))
        xml.appendEndTag(TranslatorTags.METHOD_DESCRIPTOR)

    #
    # Handle get request normal command.
    #
    # @param data
    #            Received data.
    #
    @classmethod
    def getRequestNormal(cls, settings, invokeID, server, data, replyData, xml):
        bb = GXByteBuffer()
        e = None
        status = ErrorCode.OK
        settings.setCount(0)
        settings.setIndex(0)
        settings.resetBlockIndex()
        #  CI
        ci = data.getUInt16()
        ln = bytearray(6)
        data.get(ln)
        #  Attribute Id
        attributeIndex = data.getUInt8()
        #  AccessSelection
        selection = data.getUInt8()
        selector = 0
        parameters = None
        info = _GXDataInfo()
        if selection != 0:
            selector = data.getUInt8()
        if xml:
            cls.appendAttributeDescriptor(xml, ci, ln, attributeIndex)
            if selection != 0:
                info.xml = (xml)
                xml.appendStartTag(TranslatorTags.ACCESS_SELECTION)
                xml.appendLine(TranslatorTags.ACCESS_SELECTOR, "Value", xml.integerToHex(selector, 2))
                xml.appendStartTag(TranslatorTags.ACCESS_PARAMETERS)
                _GXCommon.getData(settings, data, info)
                xml.appendEndTag(TranslatorTags.ACCESS_PARAMETERS)
                xml.appendEndTag(TranslatorTags.ACCESS_SELECTION)
            return
        if selection != 0:
            parameters = _GXCommon.getData(settings, data, info)
        ot = ObjectType(ci)
        obj = settings.objects.findByLN(ot, _GXCommon.toLogicalName(ln))
        if obj is None:
            obj = server.onFindObject(ot, 0, _GXCommon.toLogicalName(ln))
        e = ValueEventArgs(server, obj, attributeIndex, selector, parameters)
        if obj is None:
            #  "Access Error : Device reports a undefined object."
            status = ErrorCode.UNDEFINED_OBJECT
        else:
            e.invokeId = (invokeID)
            if server.onGetAttributeAccess(e) == AccessMode.NO_ACCESS:
                #  Read Write denied.
                status = ErrorCode.READ_WRITE_DENIED
            else:
                if isinstance(obj, (GXDLMSProfileGeneric,)) and attributeIndex == 2:
                    dt = None
                    rowsize = 0
                    pg = e.target
                    #  Count how many rows we can fit to one PDU.
                    for k, v in pg.captureObjects:
                        dt = k.getDataType(v.attributeIndex)
                        if dt == DataType.OCTET_STRING:
                            dt = k.getUIDataType(v.attributeIndex)
                            if dt == DataType.DATETIME:
                                rowsize += _GXCommon.getDataTypeSize(DataType.DATETIME)
                            elif dt == DataType.DATE:
                                rowsize += _GXCommon.getDataTypeSize(DataType.DATE)
                            elif dt == DataType.TIME:
                                rowsize += _GXCommon.getDataTypeSize(DataType.TIME)
                        elif dt == DataType.NONE:
                            rowsize += 2
                        else:
                            rowsize += _GXCommon.getDataTypeSize(dt)
                    if rowsize != 0:
                        e.rowToPdu = int(settings.maxPduSize / rowsize)
                server.notifyRead()
                value = None
                if e.handled:
                    value = e.value
                else:
                    settings.setCount(e.rowEndIndex - e.rowBeginIndex)
                    value = obj.getValue(settings, e)
                server.onPostRead()
                if e.byteArray:
                    bb.set(value)
                else:
                    GXDLMS.appendData(settings, obj, attributeIndex, bb, value)
                status = e.error
        GXDLMS.getLNPdu(GXDLMSLNParameters(settings, e.invokeId, Command.GET_RESPONSE, 1, None, bb, status), replyData)
        if settings.count != settings.index or len(bb) != bb.position:
            server.setTransaction(GXDLMSLongTransaction(e, Command.GET_REQUEST, bb))

    #
    # Handle get request next data block command.
    #
    # @param data
    #            Received data.
    #
    @classmethod
    def getRequestNextDataBlock(cls, settings, invokeID, server, data, replyData, xml, streaming):
        bb = GXByteBuffer()
        if not streaming:
            index = int(data.getUInt32())
            #  Get block index.
            if xml:
                xml.appendLine(TranslatorTags.BLOCK_NUMBER, None, xml.integerToHex(index, 8))
                return
            if index != settings.blockIndex:
                GXDLMS.getLNPdu(GXDLMSLNParameters(settings, invokeID, Command.GET_RESPONSE, 2, None, bb, ErrorCode.DATA_BLOCK_NUMBER_INVALID), replyData)
                return
        settings.increaseBlockIndex()
        p = GXDLMSLNParameters(settings, invokeID, Command.GENERAL_BLOCK_TRANSFER if streaming else Command.GET_RESPONSE, 2, None, bb, ErrorCode.OK)
        p.streaming = streaming
        p.windowSize = settings.getWindowSize()
        #  If transaction is not in progress.
        if server.getTransaction() is None:
            p.status = int(ErrorCode.NO_LONG_GET_OR_READ_IN_PROGRESS)
        else:
            bb.set(server.getTransaction().data)
            moreData = settings.index != settings.getCount()
            if moreData:
                #  If there is multiple blocks on the buffer.
                #  This might happen when Max PDU size is very small.
                if len(bb) < settings.getMaxPduSize():
                    value = None
                    for arg in server.transaction.targets:
                        arg.invokeId = (p.invokeId)
                        server.onPreRead([arg])
                        if arg.handled:
                            value = arg.value
                        else:
                            value = arg.target.getValue(settings, arg)
                        p.invokeId = (arg.invokeId)
                        #  Add data.
                        if arg.byteArray:
                            bb.set(int(value))
                        else:
                            GXDLMS.appendData(settings, arg.target, arg.index, bb, value)
                    moreData = settings.index != settings.getCount()
            p.multipleBlocks = True
            GXDLMS.getLNPdu(p, replyData)
            if moreData or len(bb) - bb.position != 0:
                server.getTransaction().setData(bb)
            else:
                server.setTransaction(None)
                settings.resetBlockIndex()

    #
    # Handle get request with list command.
    #
    # @param data
    #            Received data.
    #
    @classmethod
    def getRequestWithList(cls, settings, invokeID, server, data, replyData, xml):
        bb = GXByteBuffer()
        pos = int()
        cnt = _GXCommon.getObjectCount(data)
        _GXCommon.setObjectCount(cnt, bb)
        list_ = list()
        if xml:
            xml.appendStartTag(TranslatorTags.ATTRIBUTE_DESCRIPTOR_LIST, "Qty", xml.integerToHex(cnt, 2))
        while pos != cnt:
            ci = ObjectType(data.getUInt16())
            ln = bytearray(6)
            data.get(ln)
            attributeIndex = data.getUInt8()
            #  AccessSelection
            selection = data.getUInt8()
            selector = 0
            parameters = None
            if selection != 0:
                selector = data.getUInt8()
                i = _GXDataInfo()
                parameters = _GXCommon.getData(settings, data, i)
            if xml:
                xml.appendStartTag(TranslatorTags.ATTRIBUTE_DESCRIPTOR_WITH_SELECTION)
                xml.appendStartTag(TranslatorTags.ATTRIBUTE_DESCRIPTOR)
                if xml.comments:
                    xml.appendComment(ci.__str__())
                xml.appendLine(TranslatorTags.CLASS_ID, "Value", xml.integerToHex(ci.value, 4))
                xml.appendComment(_GXCommon.toLogicalName(ln))
                xml.appendLine(TranslatorTags.INSTANCE_ID, "Value", GXByteBuffer.hex(ln, False))
                xml.appendLine(TranslatorTags.ATTRIBUTE_ID, "Value", xml.integerToHex(attributeIndex, 2))
                xml.appendEndTag(TranslatorTags.ATTRIBUTE_DESCRIPTOR)
                xml.appendEndTag(TranslatorTags.ATTRIBUTE_DESCRIPTOR_WITH_SELECTION)
            else:
                obj = settings.objects.findByLN(ci, _GXCommon.toLogicalName(ln))
                if obj is None:
                    obj = server.onFindObject(ci, 0, _GXCommon.toLogicalName(ln))
                arg = ValueEventArgs(server, obj, attributeIndex, selector, parameters)
                arg.invokeId = (invokeID)
                if obj is None:
                    arg.error = ErrorCode.UNDEFINED_OBJECT
                    list_.append(arg)
                else:
                    if server.onGetAttributeAccess(arg) == AccessMode.NO_ACCESS:
                        #  Read Write denied.
                        arg.error = ErrorCode.READ_WRITE_DENIED
                        list_.append(arg)
                    else:
                        list_.append(arg)
            pos += 1
        if xml:
            xml.appendEndTag(TranslatorTags.ATTRIBUTE_DESCRIPTOR_LIST)
            return
        server.onPreRead(list_)
        value = None
        pos = 0
        p = GXDLMSLNParameters(settings, invokeID, Command.GET_RESPONSE, 3, None, bb, 0xFF)
        for it in list_:
            try:
                if it.handled:
                    value = it.value
                else:
                    value = it.target.getValue(settings, it)
                bb.setUInt8(it.error)
                if it.byteArray:
                    bb.set(value)
                else:
                    GXDLMS.appendData(settings, it.target, it.index, bb, value)
                p.invokeId = it.invokeId
            except Exception:
                bb.setUInt8(ErrorCode.HARDWARE_FAULT)
            if settings.index != settings.count:
                server.setTransaction(GXDLMSLongTransaction(list_, Command.GET_REQUEST, None))
            pos += 1
        server.onPostRead(list_)
        GXDLMS.getLNPdu(p, replyData)

    @classmethod
    def handleSetRequestNormal(cls, settings, server, data, type_, p, xml):
        value = None
        reply = _GXDataInfo()
        #  CI
        ci = data.getInt16()
        ot = ObjectType(ci & 0xFFFF)
        ln = bytearray(6)
        data.get(ln)
        #  Attribute index.
        index = data.getUInt8()
        #  Get Access Selection.
        data.getUInt8()
        if type_ == 2:
            lastBlock = data.getUInt8()
            p.multipleBlocks = lastBlock == 0
            blockNumber = data.getUInt32()
            if blockNumber != settings.blockIndex:
                p.status = ErrorCode.DATA_BLOCK_NUMBER_INVALID
                return
            settings.increaseBlockIndex()
            size = _GXCommon.getObjectCount(data)
            realSize = len(data) - data.position
            if size != realSize:
                p.status = ErrorCode.DATA_BLOCK_UNAVAILABLE
                return
            if xml:
                cls.appendAttributeDescriptor(xml, ci, ln, index)
                xml.appendStartTag(TranslatorTags.DATA_BLOCK)
                xml.appendLine(TranslatorTags.LAST_BLOCK, "Value", xml.integerToHex(lastBlock, 2))
                xml.appendLine(TranslatorTags.BLOCK_NUMBER, "Value", xml.integerToHex(blockNumber, 8))
                xml.appendLine(TranslatorTags.RAW_DATA, "Value", data.remainingHexString(False))
                xml.appendEndTag(TranslatorTags.DATA_BLOCK)
            return
        if xml:
            cls.appendAttributeDescriptor(xml, ci, ln, index)
            xml.appendStartTag(TranslatorTags.VALUE)
            di = _GXDataInfo()
            di.xml = (xml)
            value = _GXCommon.getData(settings, data, di)
            if not di.complete:
                value = GXByteBuffer.hex(data.data, False, data.position, len(data) - data.position)
            elif isinstance(value, bytearray):
                value = GXByteBuffer.hex(value, False)
            xml.appendEndTag(TranslatorTags.VALUE)
            return
        if not p.isMultipleBlocks():
            settings.resetBlockIndex()
            value = _GXCommon.getData(settings, data, reply)
        obj = settings.objects.findByLN(ot, _GXCommon.toLogicalName(ln))
        if obj is None:
            obj = server.onFindObject(ot, 0, _GXCommon.toLogicalName(ln))
        #  If target is unknown.
        if obj is None:
            #  Device reports a undefined object.
            p.setStatus(ErrorCode.UNDEFINED_OBJECT)
        else:
            e = ValueEventArgs(server, obj, index, 0, None)
            e.invokeId = (p.invokeId)
            am = server.onGetAttributeAccess(e)
            #  If write is denied.
            if am not in (AccessMode.WRITE, AccessMode.READ_WRITE):
                #  Read Write denied.
                p.setStatus(ErrorCode.READ_WRITE_DENIED)
            else:
                try:
                    if isinstance(value, bytearray):
                        dt = obj.getDataType(index)
                        if dt not in (DataType.NONE, DataType.OCTET_STRING):
                            value = _GXCommon.changeType(settings, value, dt)
                    e.value = value
                    list_ = list(e)
                    if p.isMultipleBlocks():
                        server.setTransaction(GXDLMSLongTransaction(list_, Command.GET_REQUEST, data))
                    server.onPreWrite(list_)
                    if e.error != ErrorCode.OK:
                        p.status = e.error
                    elif not e.handled and not p.multipleBlocks:
                        obj.setValue(settings, e)
                    server.onPostWrite(list_)
                    p.invokeId = e.invokeId
                except Exception:
                    p.setStatus(ErrorCode.HARDWARE_FAULT)

    @classmethod
    def hanleSetRequestWithDataBlock(cls, settings, server, data, p, xml):
        reply = _GXDataInfo()
        lastBlock = data.getUInt8()
        p.multipleBlocks = lastBlock == 0
        blockNumber = data.getUInt32()
        if xml is None and blockNumber != settings.blockIndex:
            p.status = ErrorCode.DATA_BLOCK_NUMBER_INVALID
        else:
            settings.increaseBlockIndex()
            size = _GXCommon.getObjectCount(data)
            realSize = len(data) - data.position
            if size != realSize:
                p.status = ErrorCode.DATA_BLOCK_UNAVAILABLE
            if xml:
                xml.appendStartTag(TranslatorTags.DATA_BLOCK)
                xml.appendLine(TranslatorTags.LAST_BLOCK, "Value", xml.integerToHex(lastBlock, 2))
                xml.appendLine(TranslatorTags.BLOCK_NUMBER, "Value", xml.integerToHex(blockNumber, 8))
                xml.appendLine(TranslatorTags.RAW_DATA, "Value", data.remainingHexString(False))
                xml.appendEndTag(TranslatorTags.DATA_BLOCK)
                return
            server.getTransaction().data.set(data)
            if not p.isMultipleBlocks():
                try:
                    value = _GXCommon.getData(settings, server.getTransaction().data, reply)
                    if isinstance(value, bytearray):
                        dt = server.transaction.targets[0].target.getDataType(server.transaction.targets[0].index)
                        if dt not in (DataType.NONE, DataType.OCTET_STRING):
                            value = _GXCommon.changeType(settings, value, dt)
                    server.transaction.targets[0].setValue(value)
                    server.onPreWrite(server.transaction.targets)
                    if not server.transaction.targets[0].handled and not p.isMultipleBlocks():
                        server.transaction.targets[0].target.setValue(settings, server.transaction.targets[0])
                    server.onPostWrite(server.transaction.targets)
                except Exception:
                    p.setStatus(ErrorCode.HARDWARE_FAULT)
                finally:
                    server.setTransaction(None)
                settings.resetBlockIndex()
        p.multipleBlocks = True

    @classmethod
    def hanleSetRequestWithList(cls, settings, invokeID, server, data, xml):
        e = None
        cnt = _GXCommon.getObjectCount(data)
        list_ = list()
        if xml:
            xml.appendStartTag(TranslatorTags.ATTRIBUTE_DESCRIPTOR_LIST, "Qty", xml.integerToHex(cnt, 2))
        try:
            pos = 0
            while pos != cnt:
                ci = ObjectType(data.getUInt16())
                ln = bytearray(6)
                data.get(ln)
                attributeIndex = data.getUInt8()
                selection = data.getUInt8()
                selector = 0
                parameters = None
                if selection != 0:
                    selector = data.getUInt8()
                    info = _GXDataInfo()
                    parameters = _GXCommon.getData(settings, data, info)
                if xml:
                    xml.appendStartTag(TranslatorTags.ATTRIBUTE_DESCRIPTOR_WITH_SELECTION)
                    xml.appendStartTag(TranslatorTags.ATTRIBUTE_DESCRIPTOR)
                    xml.appendComment(ci.__str__())
                    xml.appendLine(TranslatorTags.CLASS_ID, "Value", xml.integerToHex(ci.value, 4))
                    xml.appendComment(_GXCommon.toLogicalName(ln))
                    xml.appendLine(TranslatorTags.INSTANCE_ID, "Value", GXByteBuffer.hex(ln, False))
                    xml.appendLine(TranslatorTags.ATTRIBUTE_ID, "Value", xml.integerToHex(attributeIndex, 2))
                    xml.appendEndTag(TranslatorTags.ATTRIBUTE_DESCRIPTOR)
                    xml.appendEndTag(TranslatorTags.ATTRIBUTE_DESCRIPTOR_WITH_SELECTION)
                else:
                    obj = settings.objects.findByLN(ci, _GXCommon.toLogicalName(ln))
                    if obj is None:
                        obj = server.onFindObject(ci, 0, _GXCommon.toLogicalName(ln))
                    if obj is None:
                        e = ValueEventArgs(server, obj, attributeIndex, 0, 0)
                        e.error = ErrorCode.UNDEFINED_OBJECT
                        list_.append(e)
                    else:
                        arg = ValueEventArgs(server, obj, attributeIndex, selector, parameters)
                        arg.invokeId = (invokeID)
                        if server.onGetAttributeAccess(arg) == AccessMode.NO_ACCESS:
                            arg.error = ErrorCode.READ_WRITE_DENIED
                            list_.append(arg)
                        else:
                            list_.append(arg)
                pos += 1
            cnt = _GXCommon.getObjectCount(data)
            if xml:
                xml.appendEndTag(TranslatorTags.ATTRIBUTE_DESCRIPTOR_LIST)
                xml.appendStartTag(TranslatorTags.VALUE_LIST, "Qty", xml.integerToHex(cnt, 2))
            pos = 0
            while pos != cnt:
                di = _GXDataInfo()
                di.xml = xml
                if xml and xml.outputType == TranslatorOutputType.STANDARD_XML:
                    xml.appendStartTag(Command.WRITE_REQUEST, SingleReadResponse.DATA)
                value = _GXCommon.getData(settings, data, di)
                if not di.complete:
                    value = GXByteBuffer.hex(data.data, False, data.position, len(data) - data.position)
                elif isinstance(value, bytearray):
                    value = GXByteBuffer.hex(value, False)
                if xml and xml.outputType == TranslatorOutputType.STANDARD_XML:
                    xml.appendEndTag(Command.WRITE_REQUEST, SingleReadResponse.DATA)
                pos += 1
            if xml:
                xml.appendEndTag(TranslatorTags.VALUE_LIST)
        except Exception as ex:
            if xml is None:
                raise ex

    @classmethod
    def handleMethodRequest(cls, settings, server, data, connectionInfo, replyData, xml):
        error = ErrorCode.OK
        bb = GXByteBuffer()
        type_ = data.getUInt8()
        invokeId = data.getUInt8()
        settings.updateInvokeId(invokeId)
        ci = data.getUInt16()
        ot = ObjectType(ci)
        ln = bytearray(6)
        data.get(ln)
        id_ = data.getUInt8()
        parameters = None
        selection = data.getUInt8()
        if xml:
            xml.appendStartTag(Command.METHOD_REQUEST)
            if type_ == ActionRequestType.NORMAL:
                xml.appendStartTag(Command.METHOD_REQUEST, ActionRequestType.NORMAL)
                xml.appendLine(TranslatorTags.INVOKE_ID, "Value", xml.integerToHex(invokeId, 2))
                cls.appendMethodDescriptor(xml, ci, ln, id_)
                if selection != 0:
                    xml.appendStartTag(TranslatorTags.METHOD_INVOCATION_PARAMETERS)
                    di = _GXDataInfo()
                    di.xml = (xml)
                    _GXCommon.getData(settings, data, di)
                    xml.appendEndTag(TranslatorTags.METHOD_INVOCATION_PARAMETERS)
                xml.appendEndTag(Command.METHOD_REQUEST, ActionRequestType.NORMAL)
            xml.appendEndTag(Command.METHOD_REQUEST)
            return
        if selection != 0:
            info = _GXDataInfo()
            parameters = _GXCommon.getData(settings, data, info)
        obj = settings.objects.findByLN(ot, _GXCommon.toLogicalName(ln))
        if not settings.acceptConnection() and (ci != ObjectType.ASSOCIATION_LOGICAL_NAME or id_ != 1):
            replyData.set(server.generateConfirmedServiceError(ConfirmedServiceError.INITIATE_ERROR, ServiceError.SERVICE, Service.UNSUPPORTED))
            return
        if obj is None:
            obj = server.onFindObject(ot, 0, _GXCommon.toLogicalName(ln))
        if obj is None:
            error = ErrorCode.UNDEFINED_OBJECT
        else:
            e = ValueEventArgs(server, obj, id_, 0, parameters)
            e.invokeId = (invokeId)
            if server.onGetMethodAccess(e) == MethodAccessMode.NO_ACCESS:
                error = ErrorCode.READ_WRITE_DENIED
            else:
                server.onPreAction(list(e))
                if e.handled:
                    actionReply = int(e.value)
                else:
                    actionReply = obj.invoke(settings, e)
                server.onPostAction(list(e))
                if actionReply and e.error == ErrorCode.OK:
                    bb.setUInt8(1)
                    bb.setUInt8(0)
                    if e.byteArray:
                        bb.set(actionReply)
                    else:
                        _GXCommon.setData(settings, bb, _GXCommon.getDLMSDataType(actionReply), actionReply)
                else:
                    error = e.error
                    bb.setUInt8(0)
                invokeId = int(e.invokeId)
        p = GXDLMSLNParameters(settings, invokeId, Command.METHOD_RESPONSE, 1, None, bb, error)
        GXDLMS.getLNPdu(p, replyData)
        if isinstance(obj, (GXDLMSAssociationLogicalName,)) and id_ == 1:
            if obj.getAssociationStatus() == AssociationStatus.ASSOCIATED:
                server.notifyConnected(connectionInfo)
                settings.setConnected(settings.connected | ConnectionState.DLMS)
            else:
                server.onInvalidConnection(connectionInfo)
                settings.setConnected(settings.connected & ~ConnectionState.DLMS)

        #Start to use new keys.
        if e is not None and error == 0 and isinstance(obj, GXDLMSSecuritySetup) and id_ == 2:
            obj.applyKeys(settings, e)

    @classmethod
    def handleAccessRequest(cls, settings, server, data, reply, xml):
        #pylint: disable=bad-option-value,redefined-variable-type
        if xml is None and not settings.acceptConnection():
            reply.set(server.generateConfirmedServiceError(ConfirmedServiceError.INITIATE_ERROR, ServiceError.SERVICE, Service.UNSUPPORTED))
            return
        invokeId = data.getUInt32()
        settings.setLongInvokeID(invokeId)
        len_ = _GXCommon.getObjectCount(data)
        tmp = None
        if len_ != 0:
            tmp = bytearray(len_)
            data.get(tmp)
            if xml is None:
                dt = DataType.DATETIME
                if len_ == 4:
                    dt = DataType.TIME
                elif len_ == 5:
                    dt = DataType.DATE
                info = _GXDataInfo()
                info.type = dt
                _GXCommon.getData(settings, GXByteBuffer(tmp), info)
        cnt = _GXCommon.getObjectCount(data)
        if xml:
            xml.appendStartTag(Command.ACCESS_REQUEST)
            xml.appendLine(TranslatorTags.LONG_INVOKE_ID, "Value", xml.integerToHex(invokeId, 8))
            xml.appendLine(TranslatorTags.DATE_TIME, "Value", GXByteBuffer.hex(tmp, False))
            xml.appendStartTag(TranslatorTags.ACCESS_REQUEST_BODY)
            xml.appendStartTag(TranslatorTags.LIST_OF_ACCESS_REQUEST_SPECIFICATION, "Qty", xml.integerToHex(cnt, 2))
        type_ = 0
        pos = 0
        while pos != cnt:
            type_ = AccessServiceCommandType(data.getUInt8())
            if type_ not in (AccessServiceCommandType.GET, AccessServiceCommandType.SET, AccessServiceCommandType.ACTION):
                raise ValueError("Invalid access service command type.")
            ci = data.getUInt16()
            ln = bytearray(6)
            data.get(ln)
            attributeIndex = data.getUInt8()
            if xml:
                xml.appendStartTag(TranslatorTags.ACCESS_REQUEST_SPECIFICATION)
                xml.appendStartTag(Command.ACCESS_REQUEST, type_)
                cls.appendAttributeDescriptor(xml, ci, ln, attributeIndex)
                xml.appendEndTag(Command.ACCESS_REQUEST, type_)
                xml.appendEndTag(TranslatorTags.ACCESS_REQUEST_SPECIFICATION)
            pos += 1
        if xml:
            xml.appendEndTag(TranslatorTags.LIST_OF_ACCESS_REQUEST_SPECIFICATION)
            xml.appendStartTag(TranslatorTags.ACCESS_REQUEST_LIST_OF_DATA, "Qty", xml.integerToHex(cnt, 2))
        cnt = _GXCommon.getObjectCount(data)
        pos = 0
        while pos != cnt:
            di = _GXDataInfo()
            di.xml = xml
            if xml and xml.outputType == TranslatorOutputType.STANDARD_XML:
                xml.appendStartTag(Command.WRITE_REQUEST, SingleReadResponse.DATA)
            value = _GXCommon.getData(settings, data, di)
            if not di.complete:
                value = GXByteBuffer.hex(data.data, False, data.position, len(data) - data.position)
            elif isinstance(value, bytearray):
                value = GXByteBuffer.hex(value, False)
            if xml and xml.outputType == TranslatorOutputType.STANDARD_XML:
                xml.appendEndTag(Command.WRITE_REQUEST, SingleReadResponse.DATA)
            pos += 1
        if xml:
            xml.appendEndTag(TranslatorTags.ACCESS_REQUEST_LIST_OF_DATA)
            xml.appendEndTag(TranslatorTags.ACCESS_REQUEST_BODY)
            xml.appendEndTag(Command.ACCESS_REQUEST)

    @classmethod
    def handleEventNotification(cls, settings, reply, list_):
        data = reply.data
        reply.time = None
        #Check is date-time available.
        len_ = data.getUInt8()
        tmp = None
        if len_ != 0:
            len_ = data.getUInt8()
            tmp = bytearray(len_)
            data.get(tmp)
            reply.time = _GXCommon.changeType(settings, tmp, DataType.DATETIME)
        if reply.xml:
            reply.xml.appendStartTag(Command.EVENT_NOTIFICATION)
            if reply.time:
                reply.xml.appendComment(str(reply.time))
                reply.xml.appendLine(TranslatorTags.TIME, None, GXByteBuffer.hex(tmp, False))
        ci = data.getUInt16()
        ln = bytearray(6)
        data.get(ln)
        index = data.getUInt8()
        if reply.xml:
            cls.appendAttributeDescriptor(reply.xml, ci, ln, index)
            reply.xml.appendStartTag(TranslatorTags.ATTRIBUTE_VALUE)
        di = _GXDataInfo()
        di.xml = reply.xml
        value = _GXCommon.getData(settings, reply.data, di)
        if reply.xml:
            reply.xml.appendEndTag(TranslatorTags.ATTRIBUTE_VALUE)
            reply.xml.appendEndTag(Command.EVENT_NOTIFICATION)
        else:
            obj = settings.objects.findByLN(ObjectType(ci), _GXCommon.toLogicalName(ln))
            if obj:
                v = ValueEventArgs(obj, index, 0, None)
                v.value = value
                obj.setValue(settings, v)
                list_.append((obj, int(index)))
            else:
                print("InformationReport message. Unknown object : " + str(ObjectType(ci)) + " " + _GXCommon.toLogicalName(ln))

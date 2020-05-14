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
from .TranslatorOutputType import TranslatorOutputType
from .TranslatorTags import TranslatorTags
from .ConfirmedServiceError import ConfirmedServiceError
from .ServiceError import ServiceError
from .enums import Command, ErrorCode, DataType, AccessMode, Service, ObjectType, MethodAccessMode
from .VariableAccessSpecification import VariableAccessSpecification
from .internal._GXCommon import _GXCommon
from .internal._GXDataInfo import _GXDataInfo
from .GXByteBuffer import GXByteBuffer
from .GXDLMS import GXDLMS
from .GXDLMSSNParameters import GXDLMSSNParameters
from .SingleReadResponse import SingleReadResponse
from .GXSNInfo import GXSNInfo
from .ValueEventArgs import ValueEventArgs
from .GXDLMSLongTransaction import GXDLMSLongTransaction
from .SingleWriteResponse import SingleWriteResponse

# pylint: disable=bad-option-value,too-many-locals,too-many-arguments,old-style-class
class GXDLMSSNCommandHandler:
    #Constructor.
    def __init__(self):
        pass

    @classmethod
    def handleRead(cls, settings, server, type_, data, list_, reads, actions, replyData, xml):
        #  GetRequest normal
        sn = data.getInt16()
        if xml:
            if xml.outputType == TranslatorOutputType.STANDARD_XML:
                xml.appendStartTag(TranslatorTags.VARIABLE_ACCESS_SPECIFICATION)
            else:
                sn &= 0xFFFF
            if type_ == VariableAccessSpecification.PARAMETERISED_ACCESS:
                xml.appendStartTag(Command.READ_REQUEST, VariableAccessSpecification.PARAMETERISED_ACCESS)
                xml.appendLine(Command.READ_REQUEST << 8 | VariableAccessSpecification.VARIABLE_NAME, "Value", xml.integerToHex(sn, 4))
                xml.appendLine(TranslatorTags.SELECTOR, "Value", xml.integerToHex(data.getUInt8(), 2))
                di = _GXDataInfo()
                di.xml = xml
                xml.appendStartTag(TranslatorTags.PARAMETER)
                _GXCommon.getData(settings, data, di)
                xml.appendEndTag(TranslatorTags.PARAMETER)
                xml.appendEndTag(Command.READ_REQUEST, VariableAccessSpecification.PARAMETERISED_ACCESS)
            else:
                xml.appendLine(Command.READ_REQUEST << 8 | VariableAccessSpecification.VARIABLE_NAME, "Value", xml.integerToHex(sn, 4))
            if xml.outputType == TranslatorOutputType.STANDARD_XML:
                xml.appendEndTag(TranslatorTags.VARIABLE_ACCESS_SPECIFICATION)
            return
        sn = sn & 0xFFFF
        i = cls.findSNObject(server, server.settings, sn)
        e = ValueEventArgs(server, i.item, i.index, 0, None)
        e.action = i.action
        if type_ == VariableAccessSpecification.PARAMETERISED_ACCESS:
            e.selector = data.getUInt8()
            di = _GXDataInfo()
            e.parameters = _GXCommon.getData(settings, data, di)
        #  Return error if connection is not established.
        if not settings.acceptConnection() and (not e.action or e.target.shortName != 0xFA00 or e.index != 8):
            replyData.set(server.generateConfirmedServiceError(ConfirmedServiceError.INITIATE_ERROR, ServiceError.SERVICE, Service.UNSUPPORTED))
            return
        list_.append(e)
        if not e.action and server.onGetAttributeAccess(e) == AccessMode.NO_ACCESS:
            e.error = ErrorCode.READ_WRITE_DENIED
        elif e.action and server.onGetMethodAccess(e) == MethodAccessMode.NO_ACCESS:
            e.error = ErrorCode.READ_WRITE_DENIED
        else:
            if e.action:
                actions.append(e)
            else:
                reads.append(e)

    #
    # Handle read Block in blocks.
    #
    # @param data
    #            Received data.
    #
    @classmethod
    def handleReadBlockNumberAccess(cls, settings, server, data, replyData, xml):
        blockNumber = data.getUInt16()
        if xml:
            xml.appendStartTag(Command.READ_REQUEST, VariableAccessSpecification.BLOCK_NUMBER_ACCESS)
            xml.appendLine(TranslatorTags.BLOCK_NUMBER, "Value", xml.integerToHex(blockNumber, 4))
            xml.appendEndTag(Command.READ_REQUEST, VariableAccessSpecification.BLOCK_NUMBER_ACCESS)
            return
        bb = GXByteBuffer()
        if blockNumber != settings.blockIndex:
            bb.setUInt8(ErrorCode.DATA_BLOCK_NUMBER_INVALID)
            GXDLMS.getSNPdu(GXDLMSSNParameters(settings, Command.READ_RESPONSE, 1, SingleReadResponse.DATA_ACCESS_ERROR, bb, None), replyData)
            settings.resetBlockIndex()
            return
        if settings.index != settings.count and server.transaction.data.size() < settings.maxPduSize:
            reads = list()
            actions = list()
            for it in server.transaction.targets:
                if it.action:
                    actions.append(it)
                else:
                    reads.append(it)
            if reads:
                server.onPreRead(reads)
            if actions:
                server.onPreAction(actions)
            cls.getReadData(settings, server.transaction.targets, server.transaction.data)
            if reads:
                server.onPostRead(reads)
            if actions:
                server.onPostAction(actions)
        settings.increaseBlockIndex()
        p = GXDLMSSNParameters(settings, Command.READ_RESPONSE, 1, SingleReadResponse.DATA_BLOCK_RESULT, bb, server.transaction.data)
        p.multipleBlocks = True
        GXDLMS.getSNPdu(p, replyData)
        if server.transaction.data.size() == server.transaction.data.position:
            server.transaction = None
            settings.resetBlockIndex()
        else:
            server.transaction.data.strip()

    @classmethod
    def getReadData(cls, settings, list_, data):
        value = None
        first = True
        type_ = SingleReadResponse.DATA
        for e in list_:
            if e.handled:
                value = e.value
            else:
                if e.action:
                    value = e.target.invoke(settings, e)
                else:
                    value = e.target.getValue(settings, e)
            if e.error == ErrorCode.OK:
                if not first and list_:
                    data.setUInt8(SingleReadResponse.DATA)
                if e.action:
                    _GXCommon.setData(settings, data, _GXCommon.getDLMSDataType(value), value)
                else:
                    GXDLMS.appendData(settings, e.target, e.index, data, value)
            else:
                if not first and list_:
                    data.setUInt8(SingleReadResponse.DATA_ACCESS_ERROR)
                data.setUInt8(e.error)
                type_ = SingleReadResponse.DATA_ACCESS_ERROR
            first = False
        return type_

    @classmethod
    def handleReadDataBlockAccess(cls, settings, server, command, data, cnt, replyData, xml):
        bb = GXByteBuffer()
        lastBlock = data.getUInt8()
        blockNumber = data.getUInt16()
        if xml:
            if command == Command.WRITE_RESPONSE:
                xml.appendStartTag(TranslatorTags.WRITE_DATA_BLOCK_ACCESS)
            else:
                xml.appendStartTag(TranslatorTags.READ_DATA_BLOCK_ACCESS)
            xml.appendLine("<LastBlock Value=\"" + xml.integerToHex(lastBlock, 2) + "\" />")
            xml.appendLine("<BlockNumber Value=\"" + xml.integerToHex(blockNumber, 4) + "\" />")
            if command == Command.WRITE_RESPONSE:
                xml.appendEndTag(TranslatorTags.WRITE_DATA_BLOCK_ACCESS)
            else:
                xml.appendEndTag(TranslatorTags.READ_DATA_BLOCK_ACCESS)
            return
        if blockNumber != settings.blockIndex:
            bb.setUInt8(ErrorCode.DATA_BLOCK_NUMBER_INVALID)
            GXDLMS.getSNPdu(GXDLMSSNParameters(settings, command, 1, SingleReadResponse.DATA_ACCESS_ERROR, bb, None), replyData)
            settings.resetBlockIndex()
            return
        count = 1
        type1 = DataType.OCTET_STRING
        if command == Command.WRITE_RESPONSE:
            count = data.getUInt8()
            type1 = data.getUInt8()
        size = _GXCommon.getObjectCount(data)
        realSize = len(data) - data.position
        if count != 1 or type1 != DataType.OCTET_STRING or size != realSize:
            bb.setUInt8(ErrorCode.DATA_BLOCK_UNAVAILABLE)
            GXDLMS.getSNPdu(GXDLMSSNParameters(settings, command, cnt, SingleReadResponse.DATA_ACCESS_ERROR, bb, None), replyData)
            settings.resetBlockIndex()
            return
        if server.transaction is None:
            server.setTransaction(GXDLMSLongTransaction(None, command, data))
        else:
            server.transaction.data.set(data)
        if lastBlock == 0:
            #pylint: disable=bad-option-value,redefined-variable-type
            bb.setUInt16(blockNumber)
            settings.increaseBlockIndex()
            if command == Command.READ_RESPONSE:
                type2 = SingleReadResponse.BLOCK_NUMBER
            else:
                type2 = SingleWriteResponse.BLOCK_NUMBER
            GXDLMS.getSNPdu(GXDLMSSNParameters(settings, command, cnt, type2, None, bb), replyData)
            return
        if server.transaction:
            data.size(0)
            data.set(server.transaction.data)
            server.setTransaction(None)
        if command == Command.READ_RESPONSE:
            cls.handleReadRequest(settings, server, data, replyData, xml)
        else:
            cls.handleWriteRequest(settings, server, data, replyData, xml)
        settings.resetBlockIndex()

    @classmethod
    def handleReadRequest(cls, settings, server, data, replyData, xml):
        bb = GXByteBuffer()
        cnt = 0xFF
        list_ = list()
        if xml is None and not data:
            if server.transaction:
                return
            bb.set(replyData)
            replyData.clear()
            for it in server.transaction.targets:
                list_.append(it)
        else:
            cnt = _GXCommon.getObjectCount(data)
            reads = list()
            actions = list()
            if xml:
                xml.appendStartTag(Command.READ_REQUEST, "Qty", xml.integerToHex(cnt, 2))
            pos = 0
            while pos != cnt:
                type_ = data.getUInt8()
                if type_ in (VariableAccessSpecification.VARIABLE_NAME, VariableAccessSpecification.PARAMETERISED_ACCESS):
                    cls.handleRead(settings, server, type_, data, list_, reads, actions, replyData, xml)
                elif type_ == VariableAccessSpecification.BLOCK_NUMBER_ACCESS:
                    cls.handleReadBlockNumberAccess(settings, server, data, replyData, xml)
                    if xml:
                        xml.appendEndTag(Command.READ_REQUEST)
                    return
                elif type_ == VariableAccessSpecification.READ_DATA_BLOCK_ACCESS:
                    cls.handleReadDataBlockAccess(settings, server, Command.READ_RESPONSE, data, cnt, replyData, xml)
                    if xml:
                        xml.appendEndTag(Command.READ_REQUEST)
                    return
                else:
                    cls.returnSNError(settings, Command.READ_RESPONSE, ErrorCode.READ_WRITE_DENIED, replyData)
                    return
                pos += 1
            if reads:
                server.onPreRead(reads)
            if actions:
                server.onPreAction(actions)
        if xml:
            xml.appendEndTag(Command.READ_REQUEST)
            return
        requestType = cls.getReadData(settings, list_, bb)
        p = GXDLMSSNParameters(settings, Command.READ_RESPONSE, cnt, requestType, None, bb)
        GXDLMS.getSNPdu(p, replyData)
        if server.transaction() is None and (len(bb) != bb.position or settings.count != settings.index):
            reads = list()
            for it in list_:
                reads.append(it)
            if reads:
                server.onPostRead(reads)
            server.setTransaction(GXDLMSLongTransaction(reads, Command.READ_REQUEST, bb))
        elif server.transaction:
            replyData.set(bb)
            return

    @classmethod
    def returnSNError(cls, settings, cmd, error, replyData):
        bb = GXByteBuffer()
        bb.setUInt8(error)
        GXDLMS.getSNPdu(GXDLMSSNParameters(settings, cmd, 1, SingleReadResponse.DATA_ACCESS_ERROR, bb, None), replyData)
        settings.resetBlockIndex()

    @classmethod
    def findSNObject(cls, server, settings, sn):
        i = GXSNInfo()
        offset = [0]
        count = [0]
        for it in settings.objects:
            if sn >= it.shortName:
                if sn < it.shortName + it.getAttributeCount() * 8:
                    i.action = False
                    i.item = it
                    i.index = ((sn - it.shortName) / 8) + 1
                    break
                GXDLMS.getActionInfo(it.objectType, offset, count)
                if sn < it.getShortName() + offset[0] + (8 * count[0]):
                    i.item = it
                    i.action = True
                    i.index = (sn - it.shortName - offset[0]) / 8 + 1
                    break
        if i.item is None and server:
            i.item = server.onFindObject(ObjectType.NONE, sn, None)
        return i

    @classmethod
    def handleWriteRequest(cls, settings, server, data, replyData, xml):
        if xml is None and not settings.acceptConnection:
            replyData.set(server.generateConfirmedServiceError(ConfirmedServiceError.INITIATE_ERROR, ServiceError.SERVICE, Service.UNSUPPORTED))
            return
        type_ = int()
        value = None
        targets = list()
        cnt = _GXCommon.getObjectCount(data)
        if xml:
            xml.appendStartTag(Command.WRITE_REQUEST)
            xml.appendStartTag(TranslatorTags.LIST_OF_VARIABLE_ACCESS_SPECIFICATION, "Qty", xml.integerToHex(cnt, 2))
            if xml.outputType == TranslatorOutputType.STANDARD_XML:
                xml.appendStartTag(TranslatorTags.VARIABLE_ACCESS_SPECIFICATION)
        results = GXByteBuffer(cnt)
        pos = 0
        while pos != cnt:
            type_ = data.getUInt8()
            if type_ == VariableAccessSpecification.VARIABLE_NAME:
                sn = data.getUInt16()
                if xml:
                    xml.appendLine(Command.WRITE_REQUEST << 8 | VariableAccessSpecification.VARIABLE_NAME, "Value", xml.integerToHex(sn, 4))
                else:
                    i = cls.findSNObject(server, server.settings, sn)
                    targets.append(i)
                    if i is None:
                        results.setUInt8(ErrorCode.UNDEFINED_OBJECT)
                    else:
                        results.setUInt8(ErrorCode.OK)
            elif type_ == VariableAccessSpecification.WRITE_DATA_BLOCK_ACCESS:
                cls.handleReadDataBlockAccess(settings, server, Command.WRITE_RESPONSE, data, cnt, replyData, xml)
                if xml is None:
                    return
            else:
                results.setUInt8(ErrorCode.HARDWARE_FAULT)
            pos += 1
        if xml:
            if xml.outputType == TranslatorOutputType.STANDARD_XML:
                xml.appendEndTag(TranslatorTags.VARIABLE_ACCESS_SPECIFICATION)
            xml.appendEndTag(TranslatorTags.LIST_OF_VARIABLE_ACCESS_SPECIFICATION)
        cnt = _GXCommon.getObjectCount(data)
        di = _GXDataInfo()
        if xml:
            di.xml = xml
            xml.appendStartTag(TranslatorTags.LIST_OF_DATA, "Qty", xml.integerToHex(cnt, 2))
        pos = 0
        while pos != cnt:
            di.clear()
            if xml:
                if xml.outputType == TranslatorOutputType.STANDARD_XML:
                    xml.appendStartTag(Command.WRITE_REQUEST << 8 | SingleReadResponse.DATA)
                value = _GXCommon.getData(settings, data, di)
                if not di.complete:
                    value = GXByteBuffer.hex(data.data, False, data.position, len(data) - data.position)
                    xml.appendLine(_GXCommon.DATA_TYPE_OFFSET + di.type, "Value", str(value))
                if xml.outputType == TranslatorOutputType.STANDARD_XML:
                    xml.appendEndTag(Command.WRITE_REQUEST << 8 | SingleReadResponse.DATA)
            elif results.getUInt8(pos) == 0:
                target = targets[pos]
                value = _GXCommon.getData(settings, data, di)
                if isinstance(value, bytearray):
                    dt = target.getItem().getDataType(target.index)
                    if dt not in (DataType.NONE, DataType.OCTET_STRING):
                        value = _GXCommon.changeType(settings, value, dt)
                e = ValueEventArgs(server, target.getItem(), target.index, 0, None)
                am = server.onGetAttributeAccess(e)
                if am not in (AccessMode.WRITE, AccessMode.READ_WRITE):
                    results.setUInt8(pos, ErrorCode.READ_WRITE_DENIED)
                else:
                    e.value = value
                    server.onPreWrite(list(e))
                    if e.error != ErrorCode.OK:
                        results.setUInt8(pos, e.error)
                    elif not e.handled:
                        target.item.setValue(settings, e)
                    server.onPostWrite((e))
            pos += 1
        if xml:
            xml.appendEndTag(TranslatorTags.LIST_OF_DATA)
            xml.appendEndTag(Command.WRITE_REQUEST)
            return
        bb = GXByteBuffer((2 * cnt))
        ret = int()
        pos = 0
        while pos != cnt:
            ret = results.getUInt8(pos)
            if ret != 0:
                bb.setUInt8(1)
            bb.setUInt8(ret)
            pos += 1
        p = GXDLMSSNParameters(settings, Command.WRITE_RESPONSE, cnt, 0xFF, None, bb)
        GXDLMS.getSNPdu(p, replyData)

    @classmethod
    def handleInformationReport(cls, settings, reply, list_):
        data = reply.data
        reply.time = None
        len_ = data.getUInt8()
        tmp = None
        if len_ != 0:
            tmp = bytearray(len_)
            data.get(tmp)
            reply.t = _GXCommon.changeType(settings, tmp, DataType.DATETIME)
        type_ = 0
        ot = TranslatorOutputType.SIMPLE_XML
        if reply.xml:
            ot = reply.xml.outputType
        count = _GXCommon.getObjectCount(reply.data)
        if reply.xml:
            reply.xml.appendStartTag(Command.INFORMATION_REPORT)
            if reply.time:
                reply.xml.appendComment(str(reply.time))
                if ot == TranslatorOutputType.SIMPLE_XML:
                    reply.xml.appendLine(TranslatorTags.CURRENT_TIME, None, GXByteBuffer.hex(tmp, False))
                else:
                    reply.xml.appendLine(TranslatorTags.CURRENT_TIME, None, _GXCommon.generalizedTime(reply.time))
            reply.xml.appendStartTag(TranslatorTags.LIST_OF_VARIABLE_ACCESS_SPECIFICATION, "Qty", reply.xml.integerToHex(count, 2))
        pos = 0
        while pos != count:
            type_ = data.getUInt8()
            if type_ == VariableAccessSpecification.VARIABLE_NAME:
                sn = data.getUInt16()
                if reply.xml:
                    if ot == TranslatorOutputType.STANDARD_XML:
                        reply.xml.appendStartTag(TranslatorTags.VARIABLE_ACCESS_SPECIFICATION)
                    reply.xml.appendLine(Command.WRITE_REQUEST << 8 | VariableAccessSpecification.VARIABLE_NAME, "Value", reply.xml.integerToHex(sn, 4))
                    if ot == TranslatorOutputType.STANDARD_XML:
                        reply.xml.appendEndTag(TranslatorTags.VARIABLE_ACCESS_SPECIFICATION)
                else:
                    info = cls.findSNObject(None, settings, sn)
                    if info.item:
                        list_.append((info.item, info.index))
                    else:
                        print("InformationReport message. Unknown object : " + str(sn))
            pos += 1
        if reply.xml:
            reply.xml.appendEndTag(TranslatorTags.LIST_OF_VARIABLE_ACCESS_SPECIFICATION)
            reply.xml.appendStartTag(TranslatorTags.LIST_OF_DATA, "Qty", reply.xml.integerToHex(count, 2))
        count = _GXCommon.getObjectCount(reply.data)
        di = _GXDataInfo()
        di.xml = (reply.xml)
        pos = 0
        while pos != count:
            di.clear()
            if reply.xml:
                if ot == TranslatorOutputType.STANDARD_XML:
                    reply.xml.appendStartTag(Command.WRITE_REQUEST << 8 | SingleReadResponse.DATA)
                _GXCommon.getData(settings, reply.data, di)
                if ot == TranslatorOutputType.STANDARD_XML:
                    reply.xml.appendEndTag(Command.WRITE_REQUEST << 8 | SingleReadResponse.DATA)
            else:
                v = ValueEventArgs(list_[pos].key, list_[pos].value, 0, None)
                v.value = _GXCommon.getData(settings, reply.data, di)
                list_.get(pos).getKey().setValue(settings, v)
            pos += 1
        if reply.xml:
            reply.xml.appendEndTag(TranslatorTags.LIST_OF_DATA)
            reply.xml.appendEndTag(Command.INFORMATION_REPORT)

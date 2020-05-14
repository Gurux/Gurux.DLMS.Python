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
from abc import ABCMeta, abstractmethod
import datetime
from .GXReplyData import GXReplyData
from .GXDLMSSettings import GXDLMSSettings
from .enums.Command import Command
from .GXDLMSLongTransaction import GXDLMSLongTransaction
from .ServiceError import ServiceError
from .enums.Service import Service
from .ConfirmedServiceError import ConfirmedServiceError
from .internal._GXCommon import _GXCommon
from .enums.InterfaceType import InterfaceType
from .GXDLMS import GXDLMS
from .GXDLMSSNCommandHandler import GXDLMSSNCommandHandler
from .ConnectionState import ConnectionState
from .GXDLMSLNParameters import GXDLMSLNParameters
from .GXDLMSSNParameters import GXDLMSSNParameters
from .GXByteBuffer import GXByteBuffer
from .enums.ErrorCode import ErrorCode
from .GXDLMSConfirmedServiceError import GXDLMSConfirmedServiceError
from .enums.RequestTypes import RequestTypes
from .enums.Authentication import Authentication
from ._HDLCInfo import _HDLCInfo
from .GXSecure import GXSecure
from ._GXAPDU import _GXAPDU
from .GXDLMSException import GXDLMSException
from .enums.AssociationResult import AssociationResult
from .objects.enums.AssociationStatus import AssociationStatus
from .enums.SourceDiagnostic import SourceDiagnostic
from .objects.enums.ApplicationContextName import ApplicationContextName
from .enums.ObjectType import ObjectType
from .ValueEventArgs import ValueEventArgs
from .enums.DataType import DataType
from .objects.GXDLMSAssociationLogicalName import GXDLMSAssociationLogicalName
from .objects.GXDLMSAssociationShortName import GXDLMSAssociationShortName
from .GXDateTime import GXDateTime
from .enums.Conformance import Conformance
from .objects.IGXDLMSBase import IGXDLMSBase
from .enums.Initiate import Initiate
from .enums.Security import Security
from .GXDLMSLNCommandHandler import GXDLMSLNCommandHandler

# pylint: disable=too-many-public-methods,too-many-instance-attributes,useless-object-inheritance
class GXDLMSServer(object):
    __metaclass__ = ABCMeta
    #
    # Constructor.
    # logicalNameReferencing: Is logical name referencing used.
    # interfaceType: Interface type.
    #
    def __init__(self, logicalNameReferencing, interfaceType):
        self.info = GXReplyData()
        # Received data.
        self.receivedData = GXByteBuffer()
        # Reply data.
        self.replyData = GXByteBuffer()
        # Long get or read transaction information.
        self.transaction = None
        # Server settings.
        self.settings = GXDLMSSettings(True)
        # Is server initialized.
        self.initialized = False
        # When data was received last time.
        self.dataReceived = 0
        self.settings.setUseLogicalNameReferencing(logicalNameReferencing)
        self.settings.interfaceType = interfaceType
        self.hdlc = None
        self.wrapper = None
        self.reset()

    def __getItems(self):
        return self.settings.objects

    # List of objects that meter supports.
    items = property(__getItems)

    def __getWindowSize(self):
        return self.settings.windowSize

    def __setWindowSize(self, value):
        self.settings.windowSize = value

    #Window size.
    windowSize = property(__getWindowSize, __setWindowSize)

    def __getPushClientAddress(self):
        return self.settings.pushClientAddress

    def __setPushClientAddress(self, value):
        self.settings.pushClientAddress = value

    #client address for push messages.
    pushClientAddress = property(__getPushClientAddress, __setPushClientAddress)

    def __getLimits(self):
        return self.settings.limits

    # Information from the connection size that server can handle.
    limits = property(__getLimits)

    def __getMaxReceivePDUSize(self):
        return self.maxReceivePDUSize

    def __setMaxReceivePDUSize(self, value):
        self.maxReceivePDUSize = value

    #
    # Retrieves the maximum size of received PDU.  PDU size tells maximum size
    # of PDU packet.  Value can be from 0 to 0xFFFF.  By default the value is
    # 0xFFFF.
    #
    # Maximum size of received PDU.
    #
    maxReceivePDUSize = property(__getMaxReceivePDUSize, __setMaxReceivePDUSize)

    def __getUseLogicalNameReferencing(self):
        return self.settings.getUseLogicalNameReferencing()

    def __setUseLogicalNameReferencing(self, value):
        self.settings.setUseLogicalNameReferencing(value)

    #
    # Determines, whether Logical, or Short name, referencing is used.
    # Referencing depends on the device to communicate with.  Normally, a
    # device
    # supports only either Logical or Short name referencing.  The referencing
    # is defined by the device manufacturer.  If the referencing is wrong, the
    # SNMR message will fail.
    #
    # @see #getMaxReceivePDUSize
    # Is logical name referencing used.
    #
    useLogicalNameReferencing = property(__getUseLogicalNameReferencing, __setUseLogicalNameReferencing)

    def __getConformance(self):
        return self.settings.proposedConformance

    def __setConformance(self, value):
        self.settings.proposedConformance = value

    #
    # What kind of services server is offering.
    #
    conformance = property(__getConformance, __setConformance)

    #
    # Check is data sent to this server.
    #
    # @param serverAddress
    #            Server address.
    # @param clientAddress
    #            Client address.
    # True, if data is sent to this server.
    #
    @abstractmethod
    def isTarget(self, serverAddress, clientAddress):
        raise ValueError("isTarget is called.")

    #
    # Check whether the authentication and password are correct.
    #
    # @param authentication
    #            Authentication level.
    # @param password
    #            Password.
    # Source diagnostic.
    #
    @abstractmethod
    def onValidateAuthentication(self, authentication, password):
        raise ValueError("isTarget is called.")

    #
    # Get selected value(s).  This is called when example profile generic
    # request current value.
    #
    # @param args
    #            Value event arguments.
    #
    @abstractmethod
    def onPreGet(self, args):
        raise ValueError("isTarget is called.")

    #
    # Get selected value(s).  This is called when example profile generic
    # request current value.
    #
    # @param args
    #            Value event arguments.
    #
    @abstractmethod
    def onPostGet(self, args):
        raise ValueError("isTarget is called.")

    #
    # Find object.
    #
    # @param objectType
    #            Object type.
    # @param sn
    #            Short Name.  In Logical name referencing this is not used.
    # @param ln
    #            Logical Name.  In Short Name referencing this is not used.
    # Found object or null if object is not found.
    #
    @abstractmethod
    def onFindObject(self, objectType, sn, ln):
        raise ValueError("isTarget is called.")

    #
    # Called before read is executed.
    #
    # @param args
    #            Handled read requests.
    #
    @abstractmethod
    def onPreRead(self, args):
        raise ValueError("isTarget is called.")

    #
    # Called after read is executed.
    #
    # @param args
    #            Handled read requests.
    #
    @abstractmethod
    def onPostRead(self, args):
        raise ValueError("isTarget is called.")

    #
    # Called before write is executed..
    #
    # @param args
    #            Handled write requests.
    #
    @abstractmethod
    def onPreWrite(self, args):
        raise ValueError("isTarget is called.")

    #
    # Called after write is executed.
    #
    # @param args
    #            Handled write requests.
    #
    @abstractmethod
    def onPostWrite(self, args):
        raise ValueError("isTarget is called.")

    #
    # Accepted connection is made for the server.  All initialization is done
    # here.
    #
    # @param connectionInfo
    #            Connection info.
    #
    @abstractmethod
    def onConnected(self, connectionInfo):
        raise ValueError("isTarget is called.")

    #
    # Client has try to made invalid connection.  Password is incorrect.
    #
    # @param connectionInfo
    #            Connection info.
    #
    @abstractmethod
    def onInvalidConnection(self, connectionInfo):
        raise ValueError("isTarget is called.")

    #
    # Server has close the connection.  All clean up is made here.
    #
    # @param connectionInfo
    #            Connection info.
    #
    @abstractmethod
    def onDisconnected(self, connectionInfo):
        raise ValueError("isTarget is called.")

    #
    # Get attribute access mode.
    #
    # @param arg
    #            Value event argument.
    # Access mode.
    #
    @abstractmethod
    def onGetAttributeAccess(self, arg):
        raise ValueError("isTarget is called.")

    #
    # Get method access mode.
    #
    # @param arg
    #            Value event argument.
    # Method access mode.
    #
    @abstractmethod
    def onGetMethodAccess(self, arg):
        raise ValueError("onGetMethodAccess is called.")

    #
    # Called before action is executed.
    #
    # @param args
    #            Handled action requests.
    #
    @abstractmethod
    def onPreAction(self, args):
        raise ValueError("onPreAction is called.")

    #
    # Called after action is executed.
    #
    # @param args
    #            Handled action requests.
    #
    @abstractmethod
    def onPostAction(self, args):
        raise ValueError("onPostAction is called.")

    #
    # Add value of COSEM object to byte buffer.  AddData method can be used
    # with
    # GetDataNotificationMessage -method.  DLMS specification do not specify
    # the
    # structure of Data-Notification body.  So each manufacture can sent
    # different data.
    #
    # @param obj
    #            COSEM object.
    # @param index
    #            Attribute index.
    # @param buff
    #            Byte buffer.
    #
    def addData(self, obj, index, buff):
        dt = None
        e = ValueEventArgs(obj, index, 0, None)
        value = obj.getValue(self.settings, e)
        dt = obj.getDataType(index)
        if dt == DataType.NONE and value:
            dt = _GXCommon.getDLMSDataType(value)
        _GXCommon.setData(self.settings, buff, dt, value)

    #
    # Generates data notification message.
    #
    # @param time
    #            Date time.  Set Date(0) if not added.
    # @param data
    #            Notification body.
    # Generated data notification message(s).
    #
    def generateDataNotificationMessages(self, time, data):
        if self.useLogicalNameReferencing:
            p = GXDLMSLNParameters(self.settings, 0, Command.DATA_NOTIFICATION, 0, None, data, 0xff)
            if time is None:
                p.time = None
            else:
                p.time = GXDateTime(time)
            reply = GXDLMS.getLnMessages(p)
        else:
            p2 = GXDLMSSNParameters(self.settings, Command.DATA_NOTIFICATION, 1, 0, data, None)
            reply = GXDLMS.getSnMessages(p2)
        if (self.settings.negotiatedConformance & Conformance.GENERAL_BLOCK_TRANSFER) == 0 and len(reply) != 1:
            raise ValueError("Data is not fit to one PDU. Use general block transfer.")
        return reply

    def generatePushSetupMessages(self, date, push):
        if push is None:
            raise ValueError("push")
        buff = GXByteBuffer()
        buff.setUInt8(DataType.STRUCTURE)
        _GXCommon.setObjectCount(len(push.pushObjectList), buff)
        for k, v in push.pushObjectList:
            self.addData(k, v.attributeIndex, buff)
        return self.generateDataNotificationMessages(date, buff)

    def __getStoCChallenge(self):
        return self.settings.stoCChallenge

    def __setStoCChallenge(self, value):
        self.settings.useCustomChallenge = value is not None
        self.settings.stoCChallenge = value

    #
    # Server to Client custom challenge.  This is for debugging
    #      purposes.  Reset
    # custom challenge settings StoCChallenge to null.
    # @param value Server to Client challenge.
    #
    stoCChallenge = property(__getStoCChallenge, __setStoCChallenge)

    #
    # Interface type.
    #
    def getInterfaceType(self):
        return self.settings.interfaceType


    def __getStartingPacketIndex(self):
        return self.settings.blockIndex

    def __setStartingPacketIndex(self, value):
        self.settings.blockIndex = value

    #
    # Set starting packet index.  Default is One based, but some meters
    #      use Zero
    # based value.  Usually this is not used.
    # @param value Zero based starting index.
    #
    startingPacketIndex = property(__getStartingPacketIndex, __setStartingPacketIndex)

    def __getInvokeID(self):
        return self.settings.invokeId

    def __setInvokeID(self, value):
        self.settings.invokeID = value

    # Invoke ID.
    invokeID = property(__getInvokeID, __setInvokeID)

    def __getServiceClass(self):
        return self.settings.serviceClass

    def __setServiceClass(self, value):
        self.settings.serviceClass = value

    # Used service class.
    serviceClass = property(__getServiceClass, __setServiceClass)

    def __getPriority(self):
        return self.settings.priority

    def __setPriority(self, value):
        self.settings.priority = value

    # Used priority.
    priority = property(__getPriority, __setPriority)

    #
    # Initialize server.  This must call after server objects are set.
    #
    def initialize(self):
        associationObject = None
        self.initialized = True
        pos = 0
        while pos != len(self.settings.objects):
            it = self.settings.objects[pos]
            if not it.logicalName:
                raise ValueError("Invalid Logical Name.")
            it.start = self
            if isinstance(it, (GXDLMSAssociationShortName,)) and not self.useLogicalNameReferencing:
                if (it).objectList.size() == 0:
                    (it).objectList.append(self.items)
                associationObject = it
            elif isinstance(it, (GXDLMSAssociationLogicalName,)) and self.useLogicalNameReferencing:
                ln = it
                if ln.objectList.size() == 0:
                    ln.objectList.append(self.items)
                associationObject = it
                ln.xDLMSContextInfo.maxReceivePduSize = self.settings.maxServerPDUSize
                ln.xDLMSContextInfo.maxSendPduSize = self.settings.maxServerPDUSize
            elif not isinstance(it, IGXDLMSBase):
                self.settings.objects.remove(pos)
                pos -= 1
            pos += 1
        if not associationObject:
            if self.useLogicalNameReferencing:
                it = GXDLMSAssociationLogicalName()
                it.xDLMSContextInfo.maxReceivePduSize = self.settings.maxServerPDUSize
                it.xDLMSContextInfo.maxSendPduSize = self.settings.maxServerPDUSize
                self.items.append(it)
                it.objectList.append(self.items)
            else:
                it2 = GXDLMSAssociationShortName()
                self.items.append(it2)
                it2.objectList.append(self.items)
        if not self.useLogicalNameReferencing:
            self.updateShortNames(False)

    def updateShortNames(self, force):
        sn = 0xA0
        offset = [0]
        count = [0]
        for it in self.settings.objects:
            if not isinstance(it, (GXDLMSAssociationShortName, GXDLMSAssociationLogicalName)):
                if force or it.shortName == 0:
                    it.setShortName(sn)
                    GXDLMS.getActionInfo(it.objectType, offset, count)
                    if count[0] != 0:
                        sn += offset[0] + (8 * count[0])
                    else:
                        sn += 8 * it.getAttributeCount()
                else:
                    sn = it.shortName

    def handleAarqRequest(self, data, connectionInfo):
        # pylint: disable=too-many-nested-blocks
        result = AssociationResult.ACCEPTED
        error = None
        self.settings.setCtoSChallenge(None)
        if self.settings.cipher:
            self.settings.cipher.setDedicatedKey(None)
        if self.settings.interfaceType == InterfaceType.WRAPPER:
            self.reset(True)
        diagnostic = SourceDiagnostic.NO_REASON_GIVEN
        try:
            diagnostic = _GXAPDU.parsePDU(self.settings, self.settings.cipher, data, None)
            if self.settings.negotiatedConformance == Conformance.NONE:
                result = AssociationResult.PERMANENT_REJECTED
                diagnostic = SourceDiagnostic.NO_REASON_GIVEN
                error = GXByteBuffer()
                error.setUInt8(0xE)
                error.setUInt8(ConfirmedServiceError.INITIATE_ERROR)
                error.setUInt8(ServiceError.INITIATE)
                error.setUInt8(Initiate.INCOMPATIBLE_CONFORMANCE)
            elif self.settings.maxPduSize < 64:
                result = AssociationResult.PERMANENT_REJECTED
                diagnostic = SourceDiagnostic.NO_REASON_GIVEN
                error = GXByteBuffer()
                error.setUInt8(0xE)
                error.setUInt8(ConfirmedServiceError.INITIATE_ERROR)
                error.setUInt8(ServiceError.INITIATE)
                error.setUInt8(Initiate.PDU_SIZE_TOO_SHORT)
            elif self.settings.dlmsVersion != 6:
                self.settings.dlmsVersion = 6
                result = AssociationResult.PERMANENT_REJECTED
                diagnostic = SourceDiagnostic.NO_REASON_GIVEN
                error = GXByteBuffer()
                error.setUInt8(0xE)
                error.setUInt8(ConfirmedServiceError.INITIATE_ERROR)
                error.setUInt8(ServiceError.INITIATE)
                error.setUInt8(Initiate.DLMS_VERSION_TOO_LOW)
            elif diagnostic != SourceDiagnostic.NONE:
                result = AssociationResult.PERMANENT_REJECTED
                diagnostic = SourceDiagnostic.NOT_SUPPORTED
                self.onInvalidConnection(connectionInfo)
            else:
                diagnostic = self.onValidateAuthentication(self.settings.authentication, self.settings.password)
                if diagnostic != SourceDiagnostic.NONE:
                    result = AssociationResult.PERMANENT_REJECTED
                elif self.settings.authentication > Authentication.LOW:
                    result = AssociationResult.ACCEPTED
                    diagnostic = SourceDiagnostic.AUTHENTICATION_REQUIRED
                    if self.useLogicalNameReferencing:
                        ln = self.items.findByLN(ObjectType.ASSOCIATION_LOGICAL_NAME, "0.0.40.0.0.255")
                        if ln:
                            if self.settings.cipher is None or self.settings.cipher.security == Security.NONE:
                                ln.applicationContextName.contextId = ApplicationContextName.LOGICAL_NAME
                            else:
                                ln.applicationContextName.contextId = ApplicationContextName.LOGICAL_NAME_WITH_CIPHERING
                            ln.authenticationMechanismName.mechanismId = self.settings.authentication
                            ln.associationStatus = AssociationStatus.ASSOCIATION_PENDING
                else:
                    if self.useLogicalNameReferencing:
                        ln = self.items.findByLN(ObjectType.ASSOCIATION_LOGICAL_NAME, "0.0.40.0.0.255")
                        if ln:
                            if self.settings.cipher is None or self.settings.cipher.security == Security.NONE:
                                ln.applicationContextName.contextId = ApplicationContextName.LOGICAL_NAME
                            else:
                                ln.applicationContextName.contextId = ApplicationContextName.LOGICAL_NAME_WITH_CIPHERING
                            ln.authenticationMechanismName.mechanismId = self.settings.authentication
                            ln.associationStatus = AssociationStatus.ASSOCIATED
                    self.settings.connected = self.settings.connected | ConnectionState.DLMS
        except GXDLMSConfirmedServiceError as e:
            result = AssociationResult.PERMANENT_REJECTED
            diagnostic = SourceDiagnostic.NO_REASON_GIVEN
            error = GXByteBuffer()
            error.setUInt8(0xE)
            error.setUInt8(e.confirmedServiceError)
            error.setUInt8(e.serviceError)
            error.setUInt8(e.serviceErrorValue)
        except GXDLMSException as e:
            result = e.result
            diagnostic = e.diagnostic
        if self.settings.interfaceType == InterfaceType.HDLC:
            self.replyData.set(_GXCommon.LLC_REPLY_BYTES)
        if self.settings.authentication > Authentication.LOW:
            self.settings.setStoCChallenge(GXSecure.generateChallenge())
        _GXAPDU.generateAARE(self.settings, self.replyData, result, diagnostic, self.settings.cipher, error, None)

    def handleReleaseRequest(self, data):
        # pylint: disable=unused-argument
        if self.settings.interfaceType == InterfaceType.HDLC:
            self.replyData.set(0, _GXCommon.LLC_REPLY_BYTES)
        tmp = _GXAPDU.getUserInformation(self.settings, self.settings.cipher)
        self.replyData.setUInt8(0x63)
        self.replyData.setUInt8(int((len(tmp))))
        self.replyData.setUInt8(0x80)
        self.replyData.setUInt8(0x01)
        self.replyData.setUInt8(0x00)
        self.replyData.setUInt8(0xBE)
        self.replyData.setUInt8(1 + len(tmp))
        self.replyData.setUInt8(4)
        self.replyData.setUInt8(len(tmp))
        self.replyData.set(tmp)

    def handleSnrmRequest(self, data):
        GXDLMS.parseSnrmUaResponse(data, self.settings.limits)
        self.reset(True)
        self.replyData.setUInt8(0x81)
        self.replyData.setUInt8(0x80)
        self.replyData.setUInt8(0)
        if self.hdlc:
            if self.settings.limits.maxInfoTX > self.hdlc.maximumInfoLengthReceive:
                self.settings.limits.maxInfoTX = self.hdlc.maximumInfoLengthReceive
            if self.settings.limits.maxInfoRX > self.hdlc.maximumInfoLengthTransmit:
                self.settings.limits.maxInfoRX = self.hdlc.maximumInfoLengthTransmit
            if self.settings.limits.maxInfoRX > self.hdlc.maximumInfoLengthTransmit:
                self.settings.limits.windowSizeTX = self.hdlc.windowSizeReceive
            if self.settings.limits.maxInfoRX > self.hdlc.maximumInfoLengthTransmit:
                self.settings.limits.windowSizeRX = self.hdlc.windowSizeTransmit
        self.replyData.setUInt8(_HDLCInfo.MAX_INFO_TX)
        GXDLMS.appendHdlcParameter(self.replyData, self.limits.maxInfoTX)
        self.replyData.setUInt8(_HDLCInfo.MAX_INFO_RX)
        GXDLMS.appendHdlcParameter(self.replyData, self.limits.maxInfoRX)
        self.replyData.setUInt8(_HDLCInfo.WINDOW_SIZE_TX)
        self.replyData.setUInt8(4)
        self.replyData.setUInt32(self.limits.getWindowSizeTX())
        self.replyData.setUInt8(_HDLCInfo.WINDOW_SIZE_RX)
        self.replyData.setUInt8(4)
        self.replyData.setUInt32(self.limits.getWindowSizeRX())
        self.replyData.setUInt8(2, len(self.replyData) - 3)
        self.settings.connected = ConnectionState.HDLC

    def generateDisconnectRequest(self):
        self.replyData.setUInt8(0x81)
        self.replyData.setUInt8(0x80)
        self.replyData.setUInt8(0)
        self.replyData.setUInt8(_HDLCInfo.MAX_INFO_TX)
        self.replyData.setUInt8(1)
        self.replyData.setUInt8(self.limits.maxInfoTX)
        self.replyData.setUInt8(_HDLCInfo.MAX_INFO_RX)
        self.replyData.setUInt8(1)
        self.replyData.setUInt8(self.limits.maxInfoRX)
        self.replyData.setUInt8(_HDLCInfo.WINDOW_SIZE_TX)
        self.replyData.setUInt8(4)
        self.replyData.setUInt32(self.limits.windowSizeTX)
        self.replyData.setUInt8(_HDLCInfo.WINDOW_SIZE_RX)
        self.replyData.setUInt8(4)
        self.replyData.setUInt32(self.limits.windowSizeRX)
        self.replyData.setUInt8(2, len(self.replyData) - 3)


    def reset(self, connect=False):
        if not connect:
            self.info.clear()
            self.settings.serverAddress = 0
            self.settings.clientAddress = 0
        self.settings.protocolVersion = None
        self.settings.ctoSChallenge = None
        self.settings.stoCChallenge = None
        self.receivedData.clear()
        self.transaction = None
        self.settings.count = 0
        self.settings.index = 0
        self.settings.connected = ConnectionState.NONE
        self.replyData.clear()
        self.settings.authentication = Authentication.NONE
        if self.settings.cipher:
            self.settings.cipher.reset()

    def reset_0(self):
        self.reset(False)

    def handleRequest(self, sr):
        #pylint: disable=too-many-return-statements,broad-except
        """
        Handles client request.

        buff: Received data from the client.
        Returns Response to the request. Response is null if request packet is not complete.
        """
        if not sr.isStreaming() and not sr.data:
            return
        if not self.initialized:
            raise ValueError("Server not Initialized.")
        try:
            if not sr.isStreaming():
                self.receivedData.set(sr.data)
                first = self.settings.serverAddress == 0 and self.settings.clientAddress == 0
                try:
                    GXDLMS.getData(self.settings, self.receivedData, self.info, None)
                except Exception:
                    self.dataReceived = datetime.datetime.now()
                    self.receivedData.size = 0
                    sr.setReply(GXDLMS.getHdlcFrame(self.settings, Command.UNACCEPTABLE_FRAME, self.replyData))
                    return
                if not self.info.complete:
                    return
                self.receivedData.clear()
                if self.info.command == Command.DISCONNECT_REQUEST and (self.settings.connected == ConnectionState.NONE):
                    sr.setReply(GXDLMS.getHdlcFrame(self.settings, Command.DISCONNECT_MODE, self.replyData))
                    self.info.clear()
                    return
                if first or self.info.command == Command.SNRM or (self.settings.interfaceType == InterfaceType.WRAPPER and self.info.command == Command.AARQ):
                    if not self.isTarget(self.settings.serverAddress, self.settings.clientAddress):
                        self.info.clear()
                        return
                if (self.info.moreData & RequestTypes.FRAME) == RequestTypes.FRAME:
                    self.dataReceived = datetime.datetime.now()
                    sr.setReply(GXDLMS.getHdlcFrame(self.settings, self.settings.getReceiverReady(), self.replyData))
                    return
                if self.info.command == Command.NONE:
                    if self.transaction:
                        self.info.command = (self.transaction.command)
                    elif not self.replyData:
                        sr.setReply(GXDLMS.getHdlcFrame(self.settings, self.settings.getReceiverReady(), self.replyData))
                        return
                if self.hdlc and self.hdlc.inactivityTimeout != 0:
                    if self.info.command != Command.SNRM:
                        elapsed = int((datetime.datetime.now() - self.dataReceived)) / 1000
                        if elapsed >= self.hdlc.inactivityTimeout:
                            self.reset()
                            self.dataReceived = 0
                            return
                elif self.wrapper and self.wrapper.inactivityTimeout != 0:
                    if self.info.command != Command.AARQ:
                        elapsed = int((datetime.datetime.now() - self.dataReceived)) / 1000
                        if elapsed >= self.wrapper.inactivityTimeout:
                            self.reset()
                            self.dataReceived = 0
                            return
            else:
                self.info.command = (Command.GENERAL_BLOCK_TRANSFER)
            try:
                sr.setReply(self.handleCommand(self.info.command, self.info.data, sr))
            except Exception:
                self.receivedData.size(0)
                sr.setReply(GXDLMS.getHdlcFrame(self.settings, Command.UNACCEPTABLE_FRAME, self.replyData))
            self.dataReceived = datetime.datetime.now()
            self.info.clear()
        except Exception as e:
            if isinstance(e, (GXDLMSConfirmedServiceError,)):
                sr.setReply(self.reportConfirmedServiceError(e))
                self.transaction = None
                self.settings.setCount(0)
                self.settings.setIndex(0)
                self.info.clear()
                self.receivedData.clear()
            elif self.info.command != Command.NONE:
                sr.setReply(self.reportError(self.info.command, ErrorCode.HARDWARE_FAULT))
                self.transaction = None
                self.settings.setCount(0)
                self.settings.setIndex(0)
                self.info.clear()
                self.receivedData.clear()
            else:
                self.reset()
                if (self.settings.connected & ConnectionState.DLMS) != 0:
                    self.settings.connected = self.settings.connected & ~ConnectionState.DLMS
                    self.onDisconnected(sr.connectionInfo)

    def reportConfirmedServiceError(self, e):
        self.replyData.clear()
        if self.settings.interfaceType == InterfaceType.HDLC:
            GXDLMS.addLLCBytes(self.settings, self.replyData)
        self.replyData.setUInt8(Command.CONFIRMED_SERVICE_ERROR)
        self.replyData.setUInt8(e.confirmedServiceError)
        self.replyData.setUInt8(e.serviceError)
        self.replyData.setUInt8(e.serviceErrorValue)
        if self.settings.interfaceType == InterfaceType.WRAPPER:
            return GXDLMS.getWrapperFrame(self.settings, Command.CONFIRMED_SERVICE_ERROR, self.replyData)
        return GXDLMS.getHdlcFrame(self.settings, int(0), self.replyData)

    def reportError(self, command, error):
        cmd = 0
        if command == Command.READ_REQUEST:
            cmd = Command.READ_RESPONSE
        elif command == Command.WRITE_REQUEST:
            cmd = Command.WRITE_RESPONSE
        elif command == Command.GET_REQUEST:
            cmd = Command.GET_RESPONSE
        elif command == Command.SET_REQUEST:
            cmd = Command.SET_RESPONSE
        elif command == Command.METHOD_REQUEST:
            cmd = Command.METHOD_RESPONSE
        else:
            cmd = Command.NONE
        if self.settings.getUseLogicalNameReferencing():
            p = GXDLMSLNParameters(self.settings, 0, cmd, 1, None, None, error)
            GXDLMS.getLNPdu(p, self.replyData)
        else:
            bb = GXByteBuffer()
            bb.setUInt8(error)
            p2 = GXDLMSSNParameters(self.settings, cmd, 1, 1, None, bb)
            GXDLMS.getSNPdu(p2, self.replyData)
        if self.settings.interfaceType == InterfaceType.WRAPPER:
            return GXDLMS.getWrapperFrame(self.settings, command, self.replyData)
        return GXDLMS.getHdlcFrame(self.settings, int(0), self.replyData)

    def handleCommand(self, cmd, data, sr):
        frame_ = 0
        if self.replyData:
            frame_ = self.settings.getNextSend(False)
        if cmd == Command.ACCESS_REQUEST:
            GXDLMSLNCommandHandler.handleAccessRequest(self.settings, self, data, self.replyData, None)
        elif cmd == Command.SET_REQUEST:
            GXDLMSLNCommandHandler.handleSetRequest(self.settings, self, data, self.replyData, None)
        elif cmd == Command.WRITE_REQUEST:
            GXDLMSSNCommandHandler.handleWriteRequest(self.settings, self, data, self.replyData, None)
        elif cmd == Command.GET_REQUEST:
            if data:
                GXDLMSLNCommandHandler.handleGetRequest(self.settings, self, data, self.replyData, None)
        elif cmd == Command.READ_REQUEST:
            GXDLMSSNCommandHandler.handleReadRequest(self.settings, self, data, self.replyData, None)
        elif cmd == Command.METHOD_REQUEST:
            GXDLMSLNCommandHandler.handleMethodRequest(self.settings, self, data, sr.getConnectionInfo(), self.replyData, None)
        elif cmd == Command.SNRM:
            self.handleSnrmRequest(data)
            frame_ = int(Command.UA)
        elif cmd == Command.AARQ:
            self.handleAarqRequest(data, sr.getConnectionInfo())
            if (self.settings.connected & ConnectionState.DLMS) != 0:
                self.onConnected(sr.getConnectionInfo())
        elif cmd == Command.RELEASE_REQUEST:
            self.handleReleaseRequest(data)
            if (self.settings.connected & ConnectionState.DLMS) != 0:
                self.settings.connected = self.settings.connected & ~ConnectionState.DLMS
                self.onDisconnected(sr.getConnectionInfo())
        elif cmd == Command.DISCONNECT_REQUEST:
            self.generateDisconnectRequest()
            if (self.settings.connected & ConnectionState.DLMS) != 0:
                self.onDisconnected(sr.getConnectionInfo())
            self.settings.connected = ConnectionState.HDLC
            frame_ = Command.UA
        elif cmd == Command.GENERAL_BLOCK_TRANSFER:
            if not self.handleGeneralBlockTransfer(data, sr):
                return None
        elif cmd == Command.NONE:
            pass
        else:
            raise Exception("Invalid command: " + str(cmd))
        if self.settings.interfaceType == InterfaceType.WRAPPER:
            reply = GXDLMS.getWrapperFrame(self.settings, cmd, self.replyData)
        else:
            reply = GXDLMS.getHdlcFrame(self.settings, frame_, self.replyData)
        if cmd == Command.DISCONNECT_REQUEST or (self.settings.interfaceType == InterfaceType.WRAPPER and cmd == Command.RELEASE_REQUEST):
            self.reset()
        return reply

    def handleGeneralBlockTransfer(self, data, sr):
        if self.transaction:
            if self.transaction.command == Command.GET_REQUEST:
                if sr.count == 0:
                    self.settings.setBlockNumberAck(self.settings.blockNumberAck + 1)
                    sr.setCount(self.settings.windowSize)
                GXDLMSLNCommandHandler.getRequestNextDataBlock(self.settings, 0, self, data, self.replyData, None, True)
                if sr.count != 0:
                    sr.setCount(sr.getCount() - 1)
                if not self.transaction:
                    sr.setCount(0)
            else:
                bc = data.getUInt8()
                blockNumber = data.getUInt16()
                blockNumberAck = data.getUInt16()
                len_ = _GXCommon.getObjectCount(data)
                if len_ > len(data) - data.position:
                    self.replyData.set(self.generateConfirmedServiceError(ConfirmedServiceError.INITIATE_ERROR, ServiceError.SERVICE, Service.UNSUPPORTED))
                else:
                    self.transaction.data.set(data)
                    igonoreAck = (bc & 0x40) != 0 and (blockNumberAck * self.settings.windowSize) + 1 > blockNumber
                    windowSize = self.settings.windowSize
                    bn = self.settings.blockIndex
                    if (bc & 0x80) != 0:
                        self.handleCommand(self.transaction.command, self.transaction.data, sr)
                        self.transaction = None
                        igonoreAck = False
                        windowSize = 1
                    if igonoreAck:
                        return False
                    self.replyData.setUInt8(Command.GENERAL_BLOCK_TRANSFER)
                    self.replyData.setUInt8(int((0x80 | windowSize)))
                    self.settings.blockIndex = self.settings.blockIndex + 1
                    self.replyData.setUInt16(bn)
                    self.replyData.setUInt16(blockNumber)
                    self.replyData.setUInt8(0)
        else:
            bc = data.getUInt8()
            blockNumber = data.getUInt16()
            blockNumberAck = data.getUInt16()
            len_ = _GXCommon.getObjectCount(data)
            if len_ > len(data) - data.position:
                self.replyData.set(self.generateConfirmedServiceError(ConfirmedServiceError.INITIATE_ERROR, ServiceError.SERVICE, Service.UNSUPPORTED))
            else:
                self.transaction = GXDLMSLongTransaction(None, data.getUInt8(), data)
                self.replyData.setUInt8(Command.GENERAL_BLOCK_TRANSFER)
                self.replyData.setUInt8((0x80 | self.settings.windowSize))
                self.replyData.setUInt16(blockNumber)
                blockNumberAck += 1
                self.replyData.setUInt16(blockNumberAck)
                self.replyData.setUInt8(0)
        return True

    @classmethod
    def generateConfirmedServiceError(cls, service, type_, code_):
        return [Command.CONFIRMED_SERVICE_ERROR, service, type_, code_]

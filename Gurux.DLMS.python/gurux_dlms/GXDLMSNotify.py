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
from .GXDLMSSettings import GXDLMSSettings
from .ValueEventArgs import ValueEventArgs
from .GXDateTime import GXDateTime
from .internal._GXCommon import _GXCommon
from .enums.Command import Command
from .GXDLMS import GXDLMS
from .GXDLMSLNParameters import GXDLMSLNParameters
from .GXByteBuffer import GXByteBuffer
from .GXDLMSSNParameters import GXDLMSSNParameters
from .VariableAccessSpecification import VariableAccessSpecification
from .enums.DataType import DataType
from .enums.Conformance import Conformance

#pylint: disable=bad-option-value,useless-object-inheritance
class GXDLMSNotify(object):
    """This class is used to send data notify and push messages to the clients."""

    #
    # Constructor.
    #
    # @param useLogicalNameReferencing
    #            Is Logical Name referencing used.
    # @param clientAddress
    #            Server address.
    # @param serverAddress
    #            Client address.
    # @param interfaceType
    #            Object type.
    #
    def __init__(self, useLogicalNameReferencing, clientAddress, serverAddress, interfaceType):
        # DLMS settings.
        self.settings = GXDLMSSettings(True)
        self.useLogicalNameReferencing = useLogicalNameReferencing
        self.settings.clientAddress = clientAddress
        self.settings.serverAddress = serverAddress
        self.settings.interfaceType = interfaceType

    def __getConformance(self):
        return self.settings.negotiatedConformance

    def __setConformance(self, value):
        self.settings.negotiatedConformance = value

    # What kind of services are used.
    conformance = property(__getConformance, __setConformance)

    #
    # @param value
    #            Cipher interface that is used to cipher PDU.
    #
    def setCipher(self, value):
        self.settings.ipher = value

    def __getObjects(self):
        return self.settings.objects

    # Get list of meter's objects.
    objects = property(__getObjects)

    #
    #
    def __getLimits(self):
        return self.settings.limits
    # Information from the connection size that server can handle.
    limits = property(__getLimits)

    def __getMaxReceivePDUSize(self):
        return self.settings.maxPduSize

    def __setMaxReceivePDUSize(self, value):
        self.settings.maxPduSize = value

    #
    # Retrieves the maximum size of received PDU.  PDU size tells maximum size
    # of PDU packet.  Value can be from 0 to 0xFFFF.  By default the value is
    # 0xFFFF.
    #
    # @see GXDLMSClient#clientAddress
    # @see GXDLMSClient#serverAddress
    # @see GXDLMSClient#useLogicalNameReferencing
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
    # Is Logical Name referencing used.
    #
    useLogicalNameReferencing = property(__getUseLogicalNameReferencing, __setUseLogicalNameReferencing)

    def __getPriority(self):
        return self.settings.priority

    def __setPriority(self, value):
        self.settings.priority = value

    #
    # Used Priority.
    #
    priority = property(__getPriority, __setPriority)

    def __getServiceClass(self):
        return self.settings.serviceClass

    def __setServiceClass(self, value):
        self.settings.serviceClass = value

    #
    # Used service class.
    #
    serviceClass = property(__getServiceClass, __setServiceClass)

    def __getInvokeID(self):
        return self.settings.invokeId

    def __setInvokeID(self, value):
        self.settings.invokeID = value

    #
    # Invoke ID.
    #
    invokeID = property(__getInvokeID, __setInvokeID)

    #
    # Removes the HDLC frame from the packet, and returns COSEM data only.
    #
    # @param reply
    #            The received data from the device.
    # @param data
    #            Information from the received data.
    # Is frame complete.
    #
    def getData(self, reply, data):
        return GXDLMS.getData(self.settings, reply, data, None)

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
        e = ValueEventArgs(self.settings, obj, index, 0, None)
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
        reply = None
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
        if self.settings.negotiatedConformance & Conformance.GENERAL_BLOCK_TRANSFER == 0 and len(reply) != 1:
            raise ValueError("Data is not fit to one PDU. Use general block transfer.")
        return reply

    #
    # Generates push setup message.
    #
    # @param date
    #            Date time.  Set to null or Date(0) if not used.
    # @param push
    #            Target Push object.
    # Generated data notification message(s).
    #
    def generatePushSetupMessages(self, date, push):
        if push is None:
            raise ValueError("push")
        buff = GXByteBuffer()
        buff.setUInt8(DataType.STRUCTURE)
        _GXCommon.setObjectCount(len(push.pushObjectList), buff)
        for k, v in push.pushObjectList:
            self.addData(k, v.attributeIndex, buff)
        return self.generateDataNotificationMessages(date, buff)

    def generateReport(self, time, list_):
        #pylint: disable=bad-option-value,redefined-variable-type
        if not list_:
            raise ValueError("list")
        if self.useLogicalNameReferencing and len(list_) != 1:
            raise ValueError("Only one object can send with Event Notification request.")
        buff = GXByteBuffer()
        reply = None
        if self.useLogicalNameReferencing:
            for k, v in list_:
                buff.setUInt16(k.objectType)
                buff.set(_GXCommon.logicalNameToBytes(k.logicalName))
                buff.setUInt8(v)
                self.addData(k, v, buff)
            p = GXDLMSLNParameters(self.settings, 0, Command.EVENT_NOTIFICATION, 0, None, buff, 0xff)
            p.time = time
            reply = GXDLMS.getLnMessages(p)
        else:
            p = GXDLMSSNParameters(self.settings, Command.INFORMATION_REPORT, len(list_), 0xFF, None, buff)
            for k, v in list_:
                buff.setUInt8(VariableAccessSpecification.VARIABLE_NAME)
                sn = k.shortName
                sn += (v - 1) * 8
                buff.setUInt16(sn)
            _GXCommon.setObjectCount(len(list_), buff)
            for k, v in list_:
                self.addData(k, v, buff)
            reply = GXDLMS.getSnMessages(p)
        return reply

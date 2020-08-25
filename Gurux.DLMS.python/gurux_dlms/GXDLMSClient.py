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
from .GXDLMSSettings import GXDLMSSettings
from .enums import Authentication, InterfaceType, SourceDiagnostic, DataType, Conformance
from .ConnectionState import ConnectionState
from .GXByteBuffer import GXByteBuffer
from .GXDLMSLimits import GXDLMSLimits
from .enums import Command, ObjectType
from .GXDLMS import GXDLMS
from ._GXAPDU import _GXAPDU
from ._HDLCInfo import _HDLCInfo
from .GXDLMSLNParameters import GXDLMSLNParameters
from .ActionRequestType import ActionRequestType
from .internal._GXCommon import _GXCommon
from .GetCommandType import GetCommandType
from .objects import GXDLMSObject, GXDLMSObjectCollection, GXDLMSData
from .internal._GXDataInfo import _GXDataInfo
from .ValueEventArgs import ValueEventArgs
from .GXDateTime import GXDateTime
from .SetRequestType import SetRequestType
from .GXDLMSSNParameters import GXDLMSSNParameters
from .VariableAccessSpecification import VariableAccessSpecification
from .GXSecure import GXSecure
from .GXDLMSConverter import GXDLMSConverter
from .GXDLMSLNCommandHandler import GXDLMSLNCommandHandler
from .GXDLMSSNCommandHandler import GXDLMSSNCommandHandler
from .enums.AccessServiceCommandType import AccessServiceCommandType
from .enums.ErrorCode import ErrorCode
from .GXDLMSTranslatorStructure import GXDLMSTranslatorStructure
from .enums.RequestTypes import RequestTypes
from .SerialnumberCounter import SerialNumberCounter
from ._GXObjectFactory import _GXObjectFactory

#pylint:disable=bad-option-value,too-many-instance-attributes,too-many-arguments,too-many-public-methods,useless-object-inheritance
class GXDLMSClient(object):
    """
    GXDLMS implements methods to communicate with DLMS/COSEM metering devices.
    """

    #
    # Constructor.
    #
    # useLogicalNameReferencing: Is Logical Name referencing used.
    # clientAddress: Server address.
    # serverAddress: Client address.
    # forAuthentication: Authentication type.
    # password: Password if authentication is used.
    # interfaceType: Interface type.
    def __init__(self, useLogicalNameReferencing=True, clientAddress=16, serverAddress=1, forAuthentication=Authentication.NONE, password=None, interfaceType=InterfaceType.HDLC):
        # DLMS settings.
        self.settings = GXDLMSSettings(False)
        self.settings.setUseLogicalNameReferencing(useLogicalNameReferencing)
        self.clientAddress = clientAddress
        self.serverAddress = serverAddress
        self.authentication = forAuthentication
        if not password:
            self.password = None
        elif isinstance(password, str):
            self.password = _GXCommon.getBytes(password)
        elif isinstance(password, (bytes, bytearray)):
            self.password = password
        self.interfaceType = interfaceType
        self.translator = None
        self.throwExceptions = True
        self.obisCodes = None
        # Is authentication required.
        self.isAuthenticationRequired = False
        # Auto increase Invoke ID.
        self.autoIncreaseInvokeID = False
        #If protected release is used release is including a ciphered xDLMS Initiate request.
        self.useProtectedRelease = False

    def __getObjects(self):
        return self.settings.objects

    objects = property(__getObjects)

    #
    # Set starting packet index.  Default is One based, but some meters
    #      use Zero
    # based value.  Usually this is not used.
    #
    # value
    # Zero based starting index.
    #
    def setStartingPacketIndex(self, value):
        self.settings.setStartingPacketIndex(value)

    def __getUserId(self):
        return self.settings.userId

    def __setUserId(self, value):
        if value < -1 or value > 255:
            raise ValueError("Invalid user Id.")
        self.settings.userId = value

    #
    # User id is the identifier of the user.  This value is used if user
    # list on Association LN is used.
    userId = property(__getUserId, __setUserId)

    def __getClientAddress(self):
        return self.settings.clientAddress

    def __setClientAddress(self, value):
        self.settings.clientAddress = value

    #
    # Client address.
    #
    clientAddress = property(__getClientAddress, __setClientAddress)


    def __getServerAddress(self):
        return self.settings.serverAddress

    def __setServerAddress(self, value):
        self.settings.serverAddress = value
    #
    # Server Address.
    #
    serverAddress = property(__getServerAddress, __setServerAddress)

    def __getServerAddressSize(self):
        return self.settings.serverAddressSize

    def __setServerAddressSize(self, value):
        self.settings.serverAddressSize = value

    #
    # Server address size in bytes.  If it is Zero it is counted
    # automatically.
    #
    serverAddressSize = property(__getServerAddressSize, __setServerAddressSize)

    def __getSourceSystemTitle(self):
        return self.settings.sourceSystemTitle

    #
    # Source system title.
    # Meter returns system title when ciphered connection is made or GMAC
    # authentication is used.
    #
    sourceSystemTitle = property(__getSourceSystemTitle, None)

    def __getWindowSize(self):
        return self.settings.windowSize

    def __setWindowSize(self, value):
        self.settings.windowSize = value

    #
    # GBT window size.
    #
    windowSize = property(__getWindowSize, __setWindowSize)

    def __getMaxReceivePDUSize(self):
        return self.settings.maxPduSize

    def __setMaxReceivePDUSize(self, value):
        self.settings.maxPduSize = value

    #
    # Retrieves the maximum size of received PDU.  PDU size tells
    #      maximum size
    # of PDU packet.  Value can be from 0 to 0xFFFF.  By default the
    #      value is
    # 0xFFFF.
    #
    # @see GXDLMSClient.clientAddress
    # @see GXDLMSClient.serverAddress
    # @see GXDLMSClient.useLogicalNameReferencing
    # Maximum size of received PDU.
    #
    maxReceivePDUSize = property(__getMaxReceivePDUSize, __setMaxReceivePDUSize)

    def __getUseLogicalNameReferencing(self):
        return self.settings.getUseLogicalNameReferencing()

    def __setUseLogicalNameReferencing(self, value):
        self.settings.setUseLogicalNameReferencing(value)

    #
    # Determines, whether Logical, or Short name, referencing is used.
    # Referencing depends on the device to communicate with.  Normally,
    #      a device
    # supports only either Logical or Short name referencing.  The
    #      referencing
    # is defined by the device manufacturer.  If the referencing is
    #      wrong, the
    # SNMR message will fail.
    #
    # Is Logical Name referencing used.
    #
    useLogicalNameReferencing = property(__getUseLogicalNameReferencing, __setUseLogicalNameReferencing)

    def __getCtoSChallenge(self):
        return self.settings.ctoSChallenge

    def __setCtoSChallenge(self, value):
        self.settings.useCustomChallenge = value is not None
        self.settings.ctoSChallenge = value

    #
    # Client to Server custom challenge.
    # This is for debugging purposes.  Reset custom challenge settings
    # CtoSChallenge to null.
    #
    # Client to Server custom challenge.
    #
    # Client to Server custom challenge.
    #
    ctoSChallenge = property(__getCtoSChallenge, __setCtoSChallenge)

    def __getUseUtc2NormalTime(self):
        return self.settings.useUtc2NormalTime

    def __setUseUtc2NormalTime(self, value):
        self.settings.useUtc2NormalTime = value

    #
    # Standard says that Time zone is from normal time to UTC in minutes.
    # If meter is configured to use UTC time (UTC to normal time) set this to true.
    #
    # True, if UTC time is used.
    #
    useUtc2NormalTime = property(__getUseUtc2NormalTime, __setUseUtc2NormalTime)

    def __getIncreaseInvocationCounterForGMacAuthentication(self):
        return self.settings.increaseInvocationCounterForGMacAuthentication

    def __setIncreaseInvocationCounterForGMacAuthentication(self, value):
        self.settings.increaseInvocationCounterForGMacAuthentication = value

    increaseInvocationCounterForGMacAuthentication = property(__getIncreaseInvocationCounterForGMacAuthentication, __setIncreaseInvocationCounterForGMacAuthentication)
    """Some meters expect that Invocation Counter is increased for GMAC Authentication when connection is established."""

    def __getDateTimeSkips(self):
        return self.settings.dateTimeSkips

    def __setDateTimeSkips(self, value):
        self.settings.dateTimeSkips = value

    dateTimeSkips = property(__getDateTimeSkips, __setDateTimeSkips)
    """Skipped date time fields. This value can be used if meter can't handle deviation or status."""


    def __getStandard(self):
        return self.settings.standard

    def __setStandard(self, value):
        self.settings.standard = value

    #
    # Used standard.
    #
    standard = property(__getStandard, __setStandard)

    def __getPassword(self):
        return self.settings.password

    def __setPassword(self, value):
        self.settings.password = value

    #
    # Retrieves the password that is used in communication.  If
    #      authentication
    # is set to none, password is not used.
    #
    # @see GXDLMSClient#getAuthentication
    # Used password.
    #
    password = property(__getPassword, __setPassword)

    def __getNegotiatedConformance(self):
        return self.settings.negotiatedConformance

    def __setNegotiatedConformance(self, value):
        self.settings.negotiatedConformance = value

    #
    # Functionality what server offers.
    #
    negotiatedConformance = property(__getNegotiatedConformance, __setNegotiatedConformance)


    def __getProposedConformance(self):
        return self.settings.proposedConformance

    def __setProposedConformance(self, value):
        self.settings.proposedConformance = value
    #
    # When connection is made client tells what kind of services
    # it want's to use.
    #
    proposedConformance = property(__getProposedConformance, __setProposedConformance)

    def __getAuthentication(self):
        return self.settings.authentication

    def __setAuthentication(self, value):
        self.settings.authentication = value

    #
    # Retrieves the authentication used in communicating with the
    #      device.  By
    # default authentication is not used.  If authentication is used,
    #      set the
    # password with the Password property.
    #
    # @see GXDLMSClient#getPassword
    # @see GXDLMSClient#getClientAddress
    # Used authentication.
    #
    authentication = property(__getAuthentication, __setAuthentication)

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

    def __getInterfaceType(self):
        return self.settings.interfaceType

    def __setInterfaceType(self, value):
        self.settings.interfaceType = value

    #
    # Interface type.
    #
    interfaceType = property(__getInterfaceType, __setInterfaceType)
    """Interface type."""

    #
    # Information from the connection size that server can
    #      handle.
    #
    @property
    def limits(self):
        return self.settings.limits

    def __getGateway(self):
        return self.settings.gateway

    def __setGateway(self, value):
        self.settings.gateway = value

    #
    # Gateway settings.
    #
    gateway = property(__getGateway, __setGateway)

    def __getProtocolVersion(self):
        return self.settings.protocolVersion

    def __setProtocolVersion(self, value):
        self.settings.protocolVersion = value

    #
    # Protocol version.
    #
    protocolVersion = property(__getProtocolVersion, __setProtocolVersion)

    #
    # Generates SNRM request.  his method is used to generate send
    #      SNRMRequest.
    # Before the SNRM request can be generated, at least the following
    # properties must be set:
    # <ul>
    # <li>ClientAddress</li>
    # <li>ServerAddress</li>
    # </ul>
    # <b>Note!  </b>According to IEC 62056-47: when communicating using
    #      TCP/IP,
    # the SNRM request is not send.
    #
    # @see GXDLMSClient#getClientAddress
    # @see GXDLMSClient#getServerAddress
    # @see GXDLMSClient#parseUAResponse
    # SNRM request as byte array.
    #
    def snrmRequest(self):
        self.settings.connected = ConnectionState.NONE
        self.isAuthenticationRequired = False
        #  SNRM request is not used in network connections.
        if self.interfaceType == InterfaceType.WRAPPER:
            return None
        data = GXByteBuffer(25)
        data.setUInt8(0x81)
        #  FromatID
        data.setUInt8(0x80)
        #  GroupID
        data.setUInt8(0)
        #  Length.
        #  If custom HDLC parameters are used.
        if GXDLMSLimits.DEFAULT_MAX_INFO_TX != self.limits.maxInfoTX:
            data.setUInt8(_HDLCInfo.MAX_INFO_TX)
            GXDLMS.appendHdlcParameter(data, self.limits.maxInfoTX)
        if GXDLMSLimits.DEFAULT_MAX_INFO_RX != self.limits.maxInfoRX:
            data.setUInt8(_HDLCInfo.MAX_INFO_RX)
            GXDLMS.appendHdlcParameter(data, self.limits.maxInfoRX)
        if GXDLMSLimits.DEFAULT_WINDOWS_SIZE_TX != self.limits.windowSizeTX:
            data.setUInt8(_HDLCInfo.WINDOW_SIZE_TX)
            data.setUInt8(4)
            data.setUInt32(self.limits.windowSizeTX)
        if GXDLMSLimits.DEFAULT_WINDOWS_SIZE_RX != self.limits.windowSizeRX:
            data.setUInt8(_HDLCInfo.WINDOW_SIZE_RX)
            data.setUInt8(4)
            data.setUInt32(self.limits.windowSizeRX)
        #  If default HDLC parameters are not used.
        if data.size != 3:
            data.setUInt8(len(data) - 3, 2)
        else:
            data = None
        return GXDLMS.getHdlcFrame(self.settings, Command.SNRM, data)

    #
    # Parses UAResponse from byte array.
    #
    # data: # Received message from the server.
    # @see GXDLMSClient#snrmRequest
    #
    def parseUAResponse(self, data):
        if not isinstance(data, GXByteBuffer):
            data = GXByteBuffer(data)

        GXDLMS.parseSnrmUaResponse(data, self.settings.limits)
        self.settings.connected = ConnectionState.HDLC

    #
    # Generate AARQ request.  Because all_ meters can't read all_ data in
    #      one
    # packet, the packet must be split first, by using
    #      SplitDataToPackets
    # method.
    #
    # AARQ request as byte array.
    # @see GXDLMSClient#parseAareResponse
    #
    def aarqRequest(self):
        #pylint: disable=bad-option-value,redefined-variable-type
        self.settings.connected = self.settings.connected & ~ConnectionState.DLMS
        buff = GXByteBuffer(20)
        self.settings.resetBlockIndex()
        GXDLMS.checkInit(self.settings)
        self.settings.setStoCChallenge(None)
        if self.autoIncreaseInvokeID:
            self.settings.setInvokeID(0)
        else:
            self.settings.setInvokeID(1)
        #  If authentication or ciphering is used.
        if self.authentication > Authentication.LOW:
            if not self.settings.useCustomChallenge:
                self.settings.ctoSChallenge = GXSecure.generateChallenge()
        else:
            self.settings.setCtoSChallenge(None)
        _GXAPDU.generateAarq(self.settings, self.settings.cipher, None, buff)
        reply = None
        if self.settings.getUseLogicalNameReferencing():
            p = GXDLMSLNParameters(self.settings, 0, Command.AARQ, 0, buff, None, 0xff)
            reply = GXDLMS.getLnMessages(p)
        else:
            p = GXDLMSSNParameters(self.settings, Command.AARQ, 0, 0, None, buff)
            reply = GXDLMS.getSnMessages(p)
        return reply

    #
    # Parses the AARE response.  Parse method will update the following
    #      data:
    # <ul>
    # <li>DLMSVersion</li>
    # <li>MaxReceivePDUSize</li>
    # <li>UseLogicalNameReferencing</li>
    # <li>LNSettings or SNSettings</li>
    # </ul>
    # LNSettings or SNSettings will be updated, depending on the
    #      referencing,
    # Logical name or Short name.
    #
    # reply
    # Received data.
    # @see GXDLMSClient#aarqRequest
    # @see GXDLMSClient#useLogicalNameReferencing
    # @see GXDLMSClient#negotiatedConformance
    # @see GXDLMSClient#proposedConformance
    #
    def parseAareResponse(self, reply):
        self.isAuthenticationRequired = _GXAPDU.parsePDU(self.settings, self.settings.cipher, reply, None) == SourceDiagnostic.AUTHENTICATION_REQUIRED
        if self.settings.dlmsVersion != 6:
            raise ValueError("Invalid DLMS version number.")
        if not self.isAuthenticationRequired:
            self.settings.connected = self.settings.connected | ConnectionState.DLMS

    #
    # Is authentication Required.
    #
    def getIsAuthenticationRequired(self):
        return self.isAuthenticationRequired

    #
    # Get challenge request if HLS authentication is used.
    #
    def getApplicationAssociationRequest(self):
        if self.settings.authentication != Authentication.HIGH_ECDSA and self.settings.authentication != Authentication.HIGH_GMAC and not self.settings.password:
            raise ValueError("Password is invalid.")
        self.settings.resetBlockIndex()
        pw = []
        if self.settings.authentication == Authentication.HIGH_GMAC:
            pw = self.settings.cipher.systemTitle
        elif self.settings.authentication == Authentication.HIGH_SHA256:
            tmp = GXByteBuffer()
            tmp.set(self.settings.password)
            tmp.set(self.settings.cipher.systemTitle)
            tmp.set(self.settings.sourceSystemTitle)
            tmp.set(self.settings.stoCChallenge)
            tmp.set(self.settings.ctoSChallenge)
            pw = tmp.array()
        else:
            pw = self.settings.password
        if self.settings.cipher and self.settings.increaseInvocationCounterForGMacAuthentication:
            self.settings.cipher.invocationCounter += 1
        challenge = GXSecure.secure(self.settings, self.settings.cipher, self.settings.cipher.invocationCounter, self.settings.getStoCChallenge(), pw)
        if self.useLogicalNameReferencing:
            return self.__method("0.0.40.0.0.255", ObjectType.ASSOCIATION_LOGICAL_NAME, 1, challenge, DataType.OCTET_STRING)
        return self.__method(0xFA00, ObjectType.ASSOCIATION_SHORT_NAME, 8, challenge, DataType.OCTET_STRING)

    #
    # Parse server's challenge if HLS authentication is used.
    #
    # reply
    # Received reply from the server.
    #
    def parseApplicationAssociationResponse(self, reply):
        info = _GXDataInfo()
        equals = False
        ic = 0
        value = _GXCommon.getData(self.settings, reply, info)
        if value:
            if self.settings.authentication == Authentication.HIGH_ECDSA:
                raise ValueError("ECDSA is not supported.")
            if self.settings.authentication == Authentication.HIGH_GMAC:
                secret = self.settings.sourceSystemTitle
                bb = GXByteBuffer(value)
                bb.getUInt8()
                ic = bb.getUInt32()
            elif self.settings.authentication == Authentication.HIGH_SHA256:
                tmp2 = GXByteBuffer()
                tmp2.set(self.settings.password)
                tmp2.set(self.settings.sourceSystemTitle)
                tmp2.set(self.settings.cipher.systemTitle)
                tmp2.set(self.settings.ctoSChallenge)
                tmp2.set(self.settings.stoCChallenge)
                secret = tmp2.array()
            else:
                secret = self.settings.password
            tmp = GXSecure.secure(self.settings, self.settings.cipher, ic, self.settings.getCtoSChallenge(), secret)
            challenge = GXByteBuffer(tmp)
            equals = challenge.compare(value)
            if not equals:
                print("Invalid StoC:" + GXByteBuffer.hex(value, True) + "-" + GXByteBuffer.hex(tmp, True))
        else:
            print("Server did not accept CtoS.")
        if not equals:
            raise Exception("parseApplicationAssociationResponse failed. " + " Server to Client do not match.")
        self.settings.connected |= ConnectionState.DLMS

    def releaseRequest(self):
        if (self.settings.connected & ConnectionState.DLMS) == 0:
            return None
        buff = GXByteBuffer()
        buff.setUInt8(3)
        buff.setUInt8(0x80)
        buff.setUInt8(1)
        buff.setUInt8(00)
        if self.useProtectedRelease:
            #Increase IC.
            if self.settings.cipher and self.settings.cipher.isCiphered:
                self.settings.cipher.invocationCounter = self.settings.cipher.invocationCounter + 1
            _GXAPDU.generateUserInformation(self.settings, self.settings.cipher, None, buff)
            buff.setUInt8(len(buff) - 1, 0)
        if self.useLogicalNameReferencing:
            p = GXDLMSLNParameters(self.settings, 0, Command.RELEASE_REQUEST, 0, buff, None, 0xff)
            reply = GXDLMS.getLnMessages(p)
        else:
            reply = GXDLMS.getSnMessages(GXDLMSSNParameters(self.settings, Command.RELEASE_REQUEST, 0xFF, 0xFF, None, buff))
        self.settings.connected = self.settings.connected & ~ConnectionState.DLMS
        return reply

    def disconnectRequest(self, force=False):
        self.settings.maxPduSize = 0xFFFF
        if not force and self.settings.connected == ConnectionState.NONE:
            return None
        if self.interfaceType == InterfaceType.HDLC:
            self.settings.connected = ConnectionState.NONE
            return GXDLMS.getHdlcFrame(self.settings, Command.DISCONNECT_REQUEST, None)
        reply = self.releaseRequest()
        if reply is None:
            return None
        return reply[0]

    @classmethod
    def __createDLMSObject(cls, classID, version, baseName, ln, accessRights):
        type_ = classID
        obj = cls.createObject(type_)
        cls.__updateObjectData(obj, type_, version, baseName, ln, accessRights)
        return obj

    def parseSNObjects(self, buff, onlyKnownObjects, ignoreInactiveObjects):
        # pylint: disable=unidiomatic-typecheck
        buff.position = 0
        size = buff.getUInt8()
        if size != 0x01:
            raise Exception("Invalid response.")
        items = GXDLMSObjectCollection(self)
        cnt = _GXCommon.getObjectCount(buff)
        info = _GXDataInfo()
        objPos = 0
        while objPos != cnt:
            if buff.position == len(buff):
                break
            info.count = 0
            info.index = 0
            info.type_ = DataType.NONE
            objects = _GXCommon.getData(self.settings, buff, info)
            if len(objects) != 4:
                raise Exception("Invalid structure format.")
            classID = objects[1]
            baseName = int(objects[0]) & 0xFFFF
            comp = self.__createDLMSObject(classID, objects[2], baseName, objects[3], None)
            if (not onlyKnownObjects or type(comp) != GXDLMSObject):
                if not ignoreInactiveObjects or comp.logicalName != "0.0.127.0.0.0":
                    items.append(comp)
            else:
                print("Unknown object : " + str(classID) + " " + str(baseName))
            objPos += 1
        return items

    @classmethod
    def __updateObjectData(cls, obj, objectType, version, baseName, logicalName, accessRights):
        obj.objectType = objectType
        if accessRights:
            for attributeAccess in accessRights[0]:
                id_ = attributeAccess[0]
                if id_ > 0:
                    mode = attributeAccess[1]
                    obj.setAccess(id_, mode)
            for methodAccess in accessRights[1]:
                id_ = methodAccess[0]
                tmp = 0
                if isinstance(methodAccess[1], bool):
                    if bool((methodAccess)[1]):
                        tmp = 1
                    else:
                        tmp = 0
                else:
                    tmp = methodAccess[1]
                obj.setMethodAccess(id_, tmp)
        if baseName is not None:
            obj.shortName = int(baseName)
        if version is not None:
            obj.version = int(version)
        obj.logicalName = _GXCommon.toLogicalName(logicalName)

    def parseObjects(self, data, onlyKnownObjects=True, ignoreInactiveObjects=True):
        if not data:
            raise Exception("Invalid parameter.")
        objects = None
        if self.useLogicalNameReferencing:
            objects = self.parseLNObjects(data, onlyKnownObjects, ignoreInactiveObjects)
        else:
            objects = self.parseSNObjects(data, onlyKnownObjects, ignoreInactiveObjects)
        self.settings.objects = objects

        c = GXDLMSConverter(self.standard)
        c.updateOBISCodeInformation(objects)
        return objects

    def parseLNObjects(self, buff, onlyKnownObjects, ignoreInactiveObjects):
        # pylint: disable=unidiomatic-typecheck
        size = buff.getInt8()
        if size != 0x01:
            raise Exception("Invalid response.")
        items = GXDLMSObjectCollection(self)
        info = _GXDataInfo()
        cnt = _GXCommon.getObjectCount(buff)
        objPos = 0
        while objPos != cnt:
            if buff.position == len(buff):
                break
            info.type_ = DataType.NONE
            info.index = 0
            info.count = 0
            objects = _GXCommon.getData(self.settings, buff, info)
            if len(objects) != 4:
                raise Exception("Invalid structure format.")
            classID = objects[0]
            if classID > 0:
                comp = self.__createDLMSObject(classID, objects[1], 0, objects[2], objects[3])
                if (not onlyKnownObjects or type(comp) != GXDLMSObject):
                    if not ignoreInactiveObjects or comp.logicalName != "0.0.127.0.0.0":
                        items.append(comp)
                else:
                    print("Unknown object : " + str(classID) + " " + _GXCommon.toLogicalName(objects[2]))
            objPos += 1
        return items

    def updateValue(self, target, attributeIndex, value, parameters=None):
        if isinstance(value, (bytes, bytearray)):
            type_ = target.getUIDataType(attributeIndex)
            if type_ == DataType.DATETIME and len(value) == 4:
                type_ = DataType.DATE
                target.setUIDataType(attributeIndex, type_)
            if type_ != DataType.NONE:
                value = self.changeType(value, type_, self.settings.useUtc2NormalTime)
        e = ValueEventArgs(self.settings, target, attributeIndex, 0, parameters)
        e.value = value
        target.setValue(self.settings, e)
        return target.getValues()[attributeIndex - 1]

    @classmethod
    def getValue(cls, data, useUtc):
        settings = GXDLMSSettings(False)
        settings.useUtc2NormalTime = useUtc
        info = _GXDataInfo()
        return _GXCommon.getData(settings, data, info)


    def updateValues(self, list_, values):
        pos = 0
        for k, v in list_:
            e = ValueEventArgs(self.settings, k, v, 0, None)
            e.value = values[pos]
            k.setValue(self.settings, e)
            pos += 1

    @classmethod
    def changeType(cls, value, type_, useUtc=False):
        settings = GXDLMSSettings(False)
        settings.useUtc2NormalTime = useUtc
        return _GXCommon.changeType(settings, value, type_)

    def getObjectsRequest(self):
        #pylint: disable=bad-option-value,redefined-variable-type
        self.settings.resetBlockIndex()
        if self.useLogicalNameReferencing:
            name = "0.0.40.0.0.255"
        else:
            name = int(0xFA00)
        return self._read(name, ObjectType.ASSOCIATION_LOGICAL_NAME, 2)[0]


    def method(self, item, index, data, type_):
        return self.__method(item.name, item.objectType, index, data, type_)

    def __method(self, name, objectType, methodIndex, value, dataType=DataType.NONE):
        #pylint:
        #disable=bad-option-value,redefined-variable-type,too-many-locals
        if not name or methodIndex < 1:
            raise ValueError("Invalid parameter")
        self.settings.resetBlockIndex()
        if self.autoIncreaseInvokeID:
            self.settings.setInvokeID(int(((self.settings.invokeId + 1) & 0xF)))
        index = methodIndex
        type_ = dataType
        if type_ == DataType.NONE:
            raise Exception("Invalid parameter. In python value type must give.")
        reply = None
        data = GXByteBuffer()
        attributeDescriptor = GXByteBuffer()
        _GXCommon.setData(self.settings, data, type_, value)
        if self.useLogicalNameReferencing:
            attributeDescriptor.setUInt16(objectType)
            attributeDescriptor.set(_GXCommon.logicalNameToBytes(str(name)))
            attributeDescriptor.setUInt8(int(methodIndex))
            if type_ == DataType.NONE:
                attributeDescriptor.setUInt8(0)
            else:
                attributeDescriptor.setUInt8(1)
            p = GXDLMSLNParameters(self.settings, 0, Command.METHOD_REQUEST, ActionRequestType.NORMAL, attributeDescriptor, data, 0xff)
            reply = GXDLMS.getLnMessages(p)
        else:
            ind = [0]
            count = [0]
            GXDLMS.getActionInfo(objectType, ind, count)
            if index > count[0]:
                raise ValueError("methodIndex")
            sn = name
            index = (ind[0] + (index - 1) * 0x8)
            sn += index
            attributeDescriptor.setUInt16(sn)
            if type_ != DataType.NONE:
                attributeDescriptor.setUInt8(1)
            else:
                attributeDescriptor.setUInt8(0)
            p = GXDLMSSNParameters(self.settings, Command.WRITE_REQUEST, 1, VariableAccessSpecification.VARIABLE_NAME, attributeDescriptor, data)
            reply = GXDLMS.getSnMessages(p)
        return reply


    def write(self, item, index):
        e = ValueEventArgs(self.settings, item, index, 0, None)
        value = item.getValue(self.settings, e)
        type_ = item.getDataType(index)
        if type_ == DataType.OCTET_STRING and isinstance(value, (str,)):
            ui = item.getUIDataType(index)
            if ui == DataType.STRING:
                return self.__write(item.name, str(value).encode(), type_, item.objectType, index)
        return self.__write(item.name, value, type_, item.objectType, index)

    def __write(self, name, value, dataType, objectType, index):
        #pylint: disable=bad-option-value,redefined-variable-type
        if index < 1:
            raise Exception("Invalid parameter")
        self.settings.resetBlockIndex()
        if self.autoIncreaseInvokeID:
            self.settings.setInvokeID(int(((self.settings.invokeId + 1) & 0xF)))
        type_ = dataType
        if value is not None and type_ == DataType.NONE:
            raise Exception("Invalid parameter. In python value type must give.")
        reply = None
        data = GXByteBuffer()
        attributeDescriptor = GXByteBuffer()
        _GXCommon.setData(self.settings, data, type_, value)
        if self.useLogicalNameReferencing:
            attributeDescriptor.setUInt16(objectType)
            attributeDescriptor.set(_GXCommon.logicalNameToBytes(str(name)))
            attributeDescriptor.setUInt8(index)
            attributeDescriptor.setUInt8(0)
            p = GXDLMSLNParameters(self.settings, 0, Command.SET_REQUEST, SetRequestType.NORMAL, attributeDescriptor, data, 0xff)
            p.blockIndex = self.settings.blockIndex
            p.blockNumberAck = self.settings.blockNumberAck
            p.streaming = False
            reply = GXDLMS.getLnMessages(p)
        else:
            sn = name
            sn += (index - 1) * 8
            attributeDescriptor.setUInt16(sn)
            attributeDescriptor.setUInt8(1)
            p = GXDLMSSNParameters(self.settings, Command.WRITE_REQUEST, 1, VariableAccessSpecification.VARIABLE_NAME, attributeDescriptor, data)
            reply = GXDLMS.getSnMessages(p)
        return reply

    def writeList(self, list_):
        if not list_:
            raise ValueError("Invalid parameter.")
        value = None
        reply = None
        self.settings.resetBlockIndex()
        data = GXByteBuffer()
        bb = GXByteBuffer()
        if self.useLogicalNameReferencing:
            bb.setUInt8(len(list_))
            for it in list_:
                bb.setUInt16(it.target.objectType)
                bb.set(_GXCommon.logicalNameToBytes(it.target.logicalName))
                bb.setUInt8(it.index)
                bb.setUInt8(0)
        else:
            for it in list_:
                bb.setUInt8(2)
                sn = it.target.shortName
                sn += (it.index - 1) * 8
                bb.setUInt16(sn)
        _GXCommon.setObjectCount(len(list_), bb)
        for it in list_:
            e = ValueEventArgs(self.settings, it.target, it.index, it.selector, it.parameters)
            value = it.target.getValue(self.settings, e)
            type_ = it.getDataType()
            if (type_ is None or type_ == DataType.NONE) and value:
                type_ = it.target.getDataType(it.index)
                if type_ == DataType.NONE:
                    raise Exception("Invalid parameter. In python value type must give.")
            _GXCommon.setData(self.settings, data, type_, value)
        if self.useLogicalNameReferencing:
            p = GXDLMSLNParameters(self.settings, 0, Command.SET_REQUEST, SetRequestType.WITH_LIST, bb, data, 0xff)
            reply = GXDLMS.getLnMessages(p)
        else:
            p2 = GXDLMSSNParameters(self.settings, Command.WRITE_REQUEST, len(list_), 4, bb, data)
            reply = GXDLMS.getSnMessages(p2)
        return reply


    def _read(self, name, objectType, attributeOrdinal, data=None):
        if attributeOrdinal < 1:
            raise ValueError("Invalid parameter")
        attributeDescriptor = GXByteBuffer()
        reply = None
        self.settings.resetBlockIndex()
        if self.autoIncreaseInvokeID:
            self.settings.setInvokeID(int(((self.settings.invokeId + 1) & 0xF)))
        if self.useLogicalNameReferencing:
            attributeDescriptor.setUInt16(int(objectType))
            attributeDescriptor.set(_GXCommon.logicalNameToBytes(str(name)))
            attributeDescriptor.setUInt8(attributeOrdinal)
            if not data:
                attributeDescriptor.setUInt8(0)
            else:
                attributeDescriptor.setUInt8(1)
            p = GXDLMSLNParameters(self.settings, 0, Command.GET_REQUEST, GetCommandType.NORMAL, attributeDescriptor, data, 0xFF)
            reply = GXDLMS.getLnMessages(p)
        else:
            #pylint: disable=bad-option-value,redefined-variable-type
            sn = name
            sn += (attributeOrdinal - 1) * 8
            attributeDescriptor.setUInt16(sn)
            if data:
                requestType = VariableAccessSpecification.PARAMETERISED_ACCESS
            else:
                requestType = VariableAccessSpecification.VARIABLE_NAME
            p = GXDLMSSNParameters(self.settings, Command.READ_REQUEST, 1, requestType, attributeDescriptor, data)
            reply = GXDLMS.getSnMessages(p)
        return reply

    def read(self, item, attributeOrdinal):
        return self._read(item.name, item.objectType, attributeOrdinal)

    def readList(self, list_):
        if not list_:
            raise ValueError("Invalid parameter.")
        if self.negotiatedConformance & Conformance.MULTIPLE_REFERENCES == 0:
            raise ValueError("Meter doesn't support multiple objects reading with one request.")

        messages = list()
        data = GXByteBuffer()
        self.settings.resetBlockIndex()
        if self.useLogicalNameReferencing:
            p = GXDLMSLNParameters(self.settings, 0, Command.GET_REQUEST, GetCommandType.WITH_LIST, data, None, 0xff)
            pos = 0
            count = (self.settings.maxPduSize - 12) / 10
            if len(list_) < count:
                count = len(list_)
            if count > 10:
                count = 10
            _GXCommon.setObjectCount(count, data)
            for k, v in list_:
                data.setUInt16(k.objectType)
                data.set(_GXCommon.logicalNameToBytes(k.logicalName))
                data.setUInt8(v)
                data.setUInt8(0)
                pos += 1
                if pos % count == 0 and len(list_) != pos:
                    messages.append(GXDLMS.getLnMessages(p))
                    data.clear()
                    if len(list_) - pos < count:
                        _GXCommon.setObjectCount(len(list_) - pos, data)
                    else:
                        _GXCommon.setObjectCount(count, data)
            messages.append(GXDLMS.getLnMessages(p))
        else:
            p2 = GXDLMSSNParameters(self.settings, Command.READ_REQUEST, len(list_), 0xFF, data, None)
            for k, v in list_:
                data.setUInt8(VariableAccessSpecification.VARIABLE_NAME)
                sn = k.shortName
                sn += (v - 1) * 8
                data.setUInt16(sn)
            messages.append(GXDLMS.getSnMessages(p2))
        return messages

    def keepAlive(self):
        if self.interfaceType == InterfaceType.WRAPPER:
            return None
        return GXDLMS.getHdlcFrame(self.settings, self.settings.getReceiverReady(), None)


    def readRowsByEntry(self, pg, index, count, columns=None):
        if index < 0:
            raise ValueError("index")
        if count < 0:
            raise ValueError("count")
        pg.buffer = list()
        buff = GXByteBuffer(19)
        buff.setUInt8(0x02)
        buff.setUInt8(DataType.STRUCTURE)
        buff.setUInt8(0x04)
        _GXCommon.setData(self.settings, buff, DataType.UINT32, index)
        if count == 0:
            _GXCommon.setData(self.settings, buff, DataType.UINT32, count)
        else:
            _GXCommon.setData(self.settings, buff, DataType.UINT32, index + count - 1)
        columnIndex = 1
        columnCount = 0
        pos = 0
        if columns:
            if not pg.captureObjects:
                raise ValueError("Read capture objects first.")
            columnIndex = len(pg.captureObjects)
            columnCount = 1
            for c in columns:
                pos = 0
                found = False
                for k, v in pg.captureObjects:
                    pos += 1
                    if k.objectType == k.objectType and k.logicalName == c[0].logicalName and v.attributeIndex == c[1].attributeIndex and v.dataIndex == c[1].dataIndex:
                        found = True
                        if pos < columnIndex:
                            columnIndex = pos
                        columnCount = pos - columnIndex + 1
                        break
                if not found:
                    raise ValueError("Invalid column: " + c.logicalName)
        _GXCommon.setData(self.settings, buff, DataType.UINT16, columnIndex)
        _GXCommon.setData(self.settings, buff, DataType.UINT16, columnCount)
        return self._read(pg.name, ObjectType.PROFILE_GENERIC, 2, buff)

    def readRowsByRange(self, pg, start, end, columns=None):
        pg.buffer = list()
        self.settings.resetBlockIndex()
        if not isinstance(start, GXDateTime):
            start = GXDateTime(start)
        if not isinstance(end, GXDateTime):
            end = GXDateTime(end)
        sort = pg.sortObject
        if not sort and pg.captureObjects:
            sort = pg.captureObjects[0][0]
        buff = GXByteBuffer(51)
        buff.setUInt8(0x01)
        buff.setUInt8(DataType.STRUCTURE)
        buff.setUInt8(0x04)
        buff.setUInt8(DataType.STRUCTURE)
        buff.setUInt8(0x04)
        _GXCommon.setData(self.settings, buff, DataType.UINT16, sort.objectType)
        _GXCommon.setData(self.settings, buff, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(sort.logicalName))
        _GXCommon.setData(self.settings, buff, DataType.INT8, 2)
        _GXCommon.setData(self.settings, buff, DataType.UINT16, sort.version)
        if sort and isinstance(sort, GXDLMSData) and sort.logicalName == "0.0.1.1.0.255":
            _GXCommon.setData(self.settings, buff, DataType.UINT32, GXDateTime.toUnixTime(start))
            _GXCommon.setData(self.settings, buff, DataType.UINT32, GXDateTime.toUnixTime(end))
        else:
            _GXCommon.setData(self.settings, buff, DataType.OCTET_STRING, start)
            _GXCommon.setData(self.settings, buff, DataType.OCTET_STRING, end)
        buff.setUInt8(DataType.ARRAY)
        if not columns:
            buff.setUInt8(0x00)
        else:
            _GXCommon.setObjectCount(len(columns), buff)
            for it in columns:
                buff.setUInt8(DataType.STRUCTURE)
                buff.setUInt8(4)
                _GXCommon.setData(self.settings, buff, DataType.UINT16, it[0].objectType)
                _GXCommon.setData(self.settings, buff, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(it[0].logicalName))
                _GXCommon.setData(self.settings, buff, DataType.INT8, it[1].attributeIndex)
                _GXCommon.setData(self.settings, buff, DataType.INT16, it[1].dataIndex)
        return self._read(pg.name, ObjectType.PROFILE_GENERIC, 2, buff)

    @classmethod
    def createObject(cls, type_):
        return _GXObjectFactory.createObject(type_)

    def receiverReady(self, type_):
        return GXDLMS.receiverReady(self.settings, type_)

    def getData(self, reply, data, notify=None):
        # pylint: disable=broad-except
        data.xml = None
        ret = False
        if isinstance(reply, bytearray):
            reply = GXByteBuffer(reply)
        elif isinstance(reply, bytes):
            reply = GXByteBuffer(reply)
        try:
            ret = GXDLMS.getData(self.settings, reply, data, notify)
        except Exception as ex:
            if self.translator is None or self.throwExceptions:
                raise ex
            ret = True
        if ret and self.translator and data.moreData == RequestTypes.NONE:
            if data.xml is None:
                data.xml = (GXDLMSTranslatorStructure(self.translator.outputType, self.translator.isOmitXmlNameSpace(), self.translator.isHex(), self.translator.getShowStringAsHex(), self.translator.comments, self.translator.tags))
            pos = data.data.position
            try:
                data2 = data.data
                if data.command == Command.GET_RESPONSE:
                    tmp = GXByteBuffer((4 + data.data.size))
                    tmp.setUInt8(data.command)
                    tmp.setUInt8(GetCommandType.NORMAL)
                    tmp.setUInt8(int(data.invokeId))
                    tmp.setUInt8(0)
                    tmp.set(data.data)
                    data.setData(tmp)
                elif data.command == Command.METHOD_RESPONSE:
                    tmp = GXByteBuffer((6 + data.data.size))
                    tmp.setUInt8(data.command)
                    tmp.setUInt8(GetCommandType.NORMAL)
                    tmp.setUInt8(int(data.invokeId))
                    tmp.setUInt8(0)
                    tmp.setUInt8(1)
                    tmp.setUInt8(0)
                    tmp.set(data.data)
                    data.setData(tmp)
                elif data.command == Command.READ_RESPONSE:
                    tmp = GXByteBuffer(3 + data.data.size)
                    tmp.setUInt8(data.command)
                    tmp.setUInt8(VariableAccessSpecification.VARIABLE_NAME)
                    tmp.setUInt8(int(data.invokeId))
                    tmp.setUInt8(0)
                    tmp.set(data.data)
                    data.setData(tmp)
                data.data.position = 0
                if data.command == Command.SNRM or data.command == Command.UA:
                    data.xml.appendStartTag(data.command)
                    if data.data.size != 0:
                        self.translator.pduToXml(data.xml, data.data, self.translator.omitXmlDeclaration, self.translator.omitXmlNameSpace, True)
                    data.xml.appendEndTag(data.command)
                else:
                    if data.data.size != 0:
                        self.translator.pduToXml(data.xml, data.data, self.translator.omitXmlDeclaration, self.translator.omitXmlNameSpace, True)
                    data.setData(data2)
            finally:
                data.data.position = pos
        return ret

    @classmethod
    def getServerAddress(cls, serialNumber, formula=None):
        if not formula:
            return 0x4000 | SerialNumberCounter.count(serialNumber, "SN % 10000 + 1000")
        return 0x4000 | SerialNumberCounter.count(serialNumber, formula)

    @classmethod
    def getServerAddress2(cls, logicalAddress, physicalAddress, addressSize):
        if addressSize < 4 and physicalAddress < 0x80 and logicalAddress < 0x80:
            return logicalAddress << 7 | physicalAddress
        if physicalAddress < 0x4000 and logicalAddress < 0x4000:
            return logicalAddress << 14 | physicalAddress
        raise ValueError("Invalid logical or physical address.")

    def accessRequest(self, time, list_):
        bb = GXByteBuffer()
        _GXCommon.setObjectCount(len(list_), bb)
        for it in list_:
            bb.setUInt8(it.command)
            bb.setUInt16(it.target.objectType)
            items = ".".split(it.target.logicalName)
            if len(items) != 6:
                raise ValueError("Invalid Logical Name.")
            for it2 in items:
                bb.setUInt8(it2)
            bb.setUInt8(it.index)
        _GXCommon.setObjectCount(len(list_), bb)
        for it in list_:
            if it.command == AccessServiceCommandType.GET:
                bb.setUInt8(0)
            else:
                value = (it.target).getValue(self.settings, ValueEventArgs(it.target, it.index, 0, None))
                type_ = it.target.getDataType(it.index)
                if type_ == DataType.NONE:
                    raise Exception("Invalid parameter. In python value type must give.")
                _GXCommon.setData(self.settings, bb, type_, value)
        p = GXDLMSLNParameters(self.settings, 0, Command.ACCESS_REQUEST, 0xFF, None, bb, 0xff)
        if time:
            p.time = GXDateTime(time)
        return GXDLMS.getLnMessages(p)

    def parseAccessResponse(self, list_, data):
        pos = int()
        info = _GXDataInfo()
        cnt = _GXCommon.getObjectCount(data)
        if len(list_) != cnt:
            raise ValueError("List size and values size do not match.")
        values_ = list(cnt)
        reply = list(cnt)
        while pos != cnt:
            info.clear()
            value = _GXCommon.getData(self.settings, data, info)
            values_.append(value)
            pos += 1
        cnt = _GXCommon.getObjectCount(data)
        if len(values_) != cnt:
            raise ValueError("List size and values size do not match.")
        for it in values_:
            data.getUInt8()
            reply.append((it, ErrorCode(data.getUInt8())))
        pos = 0
        for it in list_:
            if it.command == AccessServiceCommandType.GET and reply[pos].value == ErrorCode.OK:
                ve = ValueEventArgs(self.settings, it.target, it.index, 0, None)
                ve.value = values_[pos]
                (it.target).setValue(self.settings, ve)
            pos += 1
        return reply

    @classmethod
    def getInitialConformance(cls, useLogicalNameReferencing):
        return GXDLMSSettings.getInitialConformance(useLogicalNameReferencing)

    def parseReport(self, reply, list_):
        if reply.command == Command.EVENT_NOTIFICATION:
            GXDLMSLNCommandHandler.handleEventNotification(self.settings, reply, list_)
            return None
        if reply.command == Command.INFORMATION_REPORT:
            GXDLMSSNCommandHandler.handleInformationReport(self.settings, reply, list_)
            return None
        if reply.command == Command.DATA_NOTIFICATION:
            return reply.value
        raise ValueError("Invalid command. " + reply.command)

    def parsePushObjects(self, data):
        objects = list()
        if data:
            c = GXDLMSConverter(self.standard)
            for it in data:
                tmp = it
                classID = tmp[0]
                if classID > 0:
                    comp = None
                    comp = self.objects.findByLN(classID, _GXCommon.toLogicalName(tmp[1]))
                    if comp is None:
                        comp = self.__createDLMSObject(classID, 0, 0, tmp[1], None)
                        self.settings.objects.append(comp)
                        c.updateOBISCodeInformation(comp)
                    if comp.__class__ != GXDLMSObject.__class__:
                        objects.append((comp, tmp[2]))
                    else:
                        print("Unknown object: " + str(classID) + " " + _GXCommon.toLogicalName(tmp[1]))
        return objects

    def getFrameSize(self, data):
        if self.interfaceType == InterfaceType.WRAPPER:
            if data.available() < 8 or data.getUInt16(data.position) != 1:
                return 8 - data.available()
            return data.getUInt16(data.position + 6)
        return 1

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
import os
import datetime
import time
import traceback
from gurux_common.enums import TraceLevel
from gurux_common.io import Parity, StopBits
from gurux_common import ReceiveParameters, GXCommon, TimeoutException
from gurux_dlms import (
    GXByteBuffer,
    GXReplyData,
    GXDLMSTranslator,
    GXDLMSException,
    GXDLMSAccessItem,
)
from gurux_dlms.enums import (
    InterfaceType,
    ObjectType,
    Authentication,
    Conformance,
    DataType,
    Security,
    AssociationResult,
    SourceDiagnostic,
    AccessServiceCommandType,
)
from gurux_dlms.objects import (
    GXDLMSObject,
    GXDLMSObjectCollection,
    GXDLMSData,
    GXDLMSRegister,
    GXDLMSDemandRegister,
    GXDLMSProfileGeneric,
    GXDLMSExtendedRegister,
    GXDLMSSecuritySetup,
)
from gurux_dlms import GXDateTime
from gurux_dlms.enums import DateTimeSkips

from gurux_net import GXNet
from gurux_serial import GXSerial
from gurux_dlms.ecdsa.enums.Ecc import Ecc
from gurux_dlms.objects.enums.CertificateType import CertificateType
from gurux_dlms.objects.enums.SecuritySuite import SecuritySuite
from gurux_dlms.asn.GXAsn1Converter import GXAsn1Converter
from gurux_dlms.ecdsa.GXEcdsa import GXEcdsa
from gurux_dlms.asn.GXPkcs8 import GXPkcs8
from gurux_dlms.asn.GXPkcs10 import GXPkcs10
from gurux_dlms.asn.GXx509Certificate import GXx509Certificate
from gurux_dlms.asn.GXCertificateRequest import GXCertificateRequest
from gurux_dlms.objects.enums.CertificateEntity import CertificateEntity
from gurux_dlms.GXDLMSConverter import GXDLMSConverter

from gurux_dlms.objects import *


class GXDLMSReader:
    # pylint: disable=too-many-public-methods, too-many-instance-attributes
    def __init__(self, client, media, trace, invocationCounter):
        # pylint: disable=too-many-arguments
        self.replyBuff = bytearray(8 + 1024)
        self.waitTime = 5000
        self.logFile = open("logFile.txt", "w")
        self.trace = trace
        self.media = media
        self.invocationCounter = invocationCounter
        self.client = client
        if self.trace > TraceLevel.WARNING:
            print("Authentication: " + str(self.client.authentication))
            print("ClientAddress: " + hex(self.client.clientAddress))
            print("ServerAddress: " + hex(self.client.serverAddress))

    def disconnect(self):
        # pylint: disable=broad-except
        if self.media and self.media.isOpen():
            print("DisconnectRequest")
            reply = GXReplyData()
            self.readDLMSPacket(self.client.disconnectRequest(), reply)

    def release(self):
        # pylint: disable=broad-except
        if self.media and self.media.isOpen():
            print("DisconnectRequest")
            reply = GXReplyData()
            try:
                # Release is call only for secured connections.
                # All meters are not supporting Release and it's causing
                # problems.
                if (
                    self.client.interfaceType == InterfaceType.WRAPPER
                    or self.client.ciphering.security != Security.NONE
                ):
                    self.readDataBlock(self.client.releaseRequest(), reply)
            except Exception:
                pass
                #  All meters don't support release.

    def close(self):
        # pylint: disable=broad-except
        if self.media and self.media.isOpen():
            print("DisconnectRequest")
            reply = GXReplyData()
            try:
                # Release is call only for secured connections.
                # All meters are not supporting Release and it's causing
                # problems.
                if (
                    self.client.interfaceType == InterfaceType.WRAPPER
                    or self.client.ciphering.security != Security.NONE
                ):
                    self.readDataBlock(self.client.releaseRequest(), reply)
            except Exception:
                pass
                #  All meters don't support release.
            reply.clear()
            self.readDLMSPacket(self.client.disconnectRequest(), reply)
            self.media.close()

    @classmethod
    def now(cls):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def writeTrace(self, line, level):
        if self.trace >= level:
            print(line)
        self.logFile.write(line + "\n")

    def readDLMSPacket(self, data, reply=None):
        if not reply:
            reply = GXReplyData()
        if isinstance(data, bytearray):
            self.readDLMSPacket2(data, reply)
        elif data:
            for it in data:
                reply.clear()
                self.readDLMSPacket2(it, reply)

    def readDLMSPacket2(self, data, reply):
        if not data:
            return
        notify = GXReplyData()
        reply.error = 0
        eop = 0x7E
        # In network connection terminator is not used.
        if self.client.interfaceType == InterfaceType.WRAPPER and isinstance(
            self.media, GXNet
        ):
            eop = None
        p = ReceiveParameters()
        p.eop = eop
        p.allData = True
        p.waitTime = self.waitTime
        if eop is None:
            p.Count = 8
        else:
            p.Count = 5
        self.media.eop = eop
        rd = GXByteBuffer()
        with self.media.getSynchronous():
            if not reply.isStreaming():
                self.writeTrace(
                    "TX: " + self.now() + "\t" + GXByteBuffer.hex(data),
                    TraceLevel.VERBOSE,
                )
                self.media.send(data)
            pos = 0
            try:
                while not self.client.getData(rd, reply, notify):
                    if notify.data.size != 0:
                        if not notify.isMoreData():
                            t = GXDLMSTranslator()
                            xml = t.dataToXml(notify.data)
                            print(xml)
                            notify.clear()
                        continue
                    if not p.eop:
                        p.count = self.client.getFrameSize(rd)
                    while not self.media.receive(p):
                        pos += 1
                        if pos == 3:
                            raise TimeoutException(
                                "Failed to receive reply from the device in given time."
                            )
                        print("Data send failed.  Try to resend " + str(pos) + "/3")
                        self.media.send(data, None)
                    rd.set(p.reply)
                    p.reply = None
            except Exception as e:
                self.writeTrace("RX: " + self.now() + "\t" + str(rd), TraceLevel.ERROR)
                raise e
            self.writeTrace("RX: " + self.now() + "\t" + str(rd), TraceLevel.VERBOSE)
            if reply.error != 0:
                raise GXDLMSException(reply.error)

    def readDataBlock(self, data, reply):
        if data:
            if isinstance(data, (list)):
                for it in data:
                    reply.clear()
                    self.readDataBlock(it, reply)
                return reply.error == 0
            else:
                self.readDLMSPacket(data, reply)
                while reply.isMoreData():
                    if reply.isStreaming():
                        data = None
                    else:
                        data = self.client.receiverReady(reply)
                    self.readDLMSPacket(data, reply)

    def initializeOpticalHead(self):
        if self.client.interfaceType == InterfaceType.HDLC_WITH_MODE_E:
            p = ReceiveParameters()
            p.allData = True
            p.eop = "\n"
            p.waitTime = self.waitTime
            with self.media.getSynchronous():
                data = "/?!\r\n"
                self.writeTrace("TX: " + self.now() + "\t" + data, TraceLevel.VERBOSE)
                self.media.send(data)
                if not self.media.receive(p):
                    raise Exception("Failed to received reply from the media.")

                self.writeTrace(
                    "RX: " + self.now() + "\t" + str(p.reply), TraceLevel.VERBOSE
                )
                # If echo is used.
                if data.encode() == p.reply:
                    p.reply = None
                    if not self.media.receive(p):
                        raise Exception("Failed to received reply from the media.")
                    self.writeTrace(
                        "RX: " + self.now() + "\t" + str(p.reply), TraceLevel.VERBOSE
                    )

            if not p.reply or p.reply[0] != ord("/"):
                raise Exception("Invalid responce : " + str(p.reply))
            baudrate = chr(p.reply[4])
            if baudrate == "0":
                bitrate = 300
            elif baudrate == "1":
                bitrate = 600
            elif baudrate == "2":
                bitrate = 1200
            elif baudrate == "3":
                bitrate = 2400
            elif baudrate == "4":
                bitrate = 4800
            elif baudrate == "5":
                bitrate = 9600
            elif baudrate == "6":
                bitrate = 19200
            else:
                raise Exception("Unknown baud rate.")

            print("Bitrate is : " + str(bitrate))
            # Send ACK
            # Send Protocol control character
            controlCharacter = ord("2")
            # "2" HDLC protocol procedure (Mode E)
            # Mode control character
            # "2" //(HDLC protocol procedure) (Binary mode)
            modeControlCharacter = ord("2")
            # Set mode E.
            tmp = bytearray(
                [0x06, controlCharacter, ord(baudrate), modeControlCharacter, 13, 10]
            )
            p.reply = None
            with self.media.getSynchronous():
                self.media.send(tmp)
                # This sleep make sure that all meters can be read.
                time.sleep(1)
                self.writeTrace(
                    "TX: " + self.now() + "\t" + GXCommon.toHex(tmp), TraceLevel.VERBOSE
                )
                p.waitTime = 200
                if self.media.receive(p):
                    self.writeTrace(
                        "RX: " + self.now() + "\t" + str(p.reply), TraceLevel.VERBOSE
                    )
                self.media.dataBits = 8
                self.media.parity = Parity.NONE
                self.media.stopBits = StopBits.ONE
                self.media.baudRate = bitrate
                # This sleep make sure that all meters can be read.
                time.sleep(1)

    def updateFrameCounter(self):
        if (
            self.invocationCounter
            and self.client.ciphering is not None
            and self.client.ciphering.security != Security.NONE
        ):
            self.initializeOpticalHead()
            self.client.proposedConformance |= Conformance.GENERAL_PROTECTION
            add = self.client.clientAddress
            auth = self.client.authentication
            security = self.client.ciphering.security
            challenge = self.client.ctoSChallenge
            try:
                self.client.clientAddress = 16
                self.client.authentication = Authentication.NONE
                self.client.ciphering.security = Security.NONE
                reply = GXReplyData()
                data = self.client.snrmRequest()
                if data:
                    self.readDLMSPacket(data, reply)
                    self.client.parseUAResponse(reply.data)
                    size = self.client.hdlcSettings.maxInfoTX + 40
                    self.replyBuff = bytearray(size)
                reply.clear()
                self.readDataBlock(self.client.aarqRequest(), reply)
                self.client.parseAareResponse(reply.data)
                reply.clear()
                d = GXDLMSData(self.invocationCounter)
                self.read(d, 2)
                self.client.ciphering.invocationCounter = 1 + d.value
                print(
                    "Invocation counter: "
                    + str(self.client.ciphering.invocationCounter)
                )
                self.disconnect()
                # except Exception as ex:
            finally:
                self.client.clientAddress = add
                self.client.authentication = auth
                self.client.ciphering.security = security
                self.client.ctoSChallenge = challenge

    def initializeConnection(self):
        print("Standard: " + str(self.client.standard))
        if self.client.ciphering.security != Security.NONE:
            print("Security Suite: " + str(self.client.ciphering.securitySuite))
            print("Security: " + str(self.client.ciphering.security))
            print("System title: " + GXCommon.toHex(self.client.ciphering.systemTitle))
            print(
                "Authentication key: "
                + GXCommon.toHex(self.client.ciphering.authenticationKey)
            )
            print(
                "Block cipher key: "
                + GXCommon.toHex(self.client.ciphering.blockCipherKey)
            )
            if self.client.ciphering.dedicatedKey:
                print(
                    "Dedicated key: "
                    + GXCommon.toHex(self.client.ciphering.dedicatedKey)
                )
        self.updateFrameCounter()
        self.initializeOpticalHead()
        reply = GXReplyData()
        data = self.client.snrmRequest()
        if data:
            self.readDLMSPacket(data, reply)
            self.client.parseUAResponse(reply.data)
            size = self.client.hdlcSettings.maxInfoTX + 40
            self.replyBuff = bytearray(size)
        reply.clear()
        self.readDataBlock(self.client.aarqRequest(), reply)
        self.client.parseAareResponse(reply.data)
        reply.clear()
        if self.client.authentication > Authentication.LOW:
            try:
                for it in self.client.getApplicationAssociationRequest():
                    self.readDLMSPacket(it, reply)
                self.client.parseApplicationAssociationResponse(reply.data)
            except GXDLMSException as ex:
                # Invalid password.
                raise GXDLMSException(
                    AssociationResult.PERMANENT_REJECTED,
                    SourceDiagnostic.AUTHENTICATION_FAILURE,
                )

    def read(self, item, attributeIndex):
        data = self.client.read(item, attributeIndex)[0]
        reply = GXReplyData()
        self.readDataBlock(data, reply)
        # Update data type on read.
        if item.getDataType(attributeIndex) == DataType.NONE:
            item.setDataType(attributeIndex, reply.valueType)
        return self.client.updateValue(item, attributeIndex, reply.value)

    def readList(self, list_):
        if list_:
            data = self.client.readList(list_)
            reply = GXReplyData()
            values = list()
            for it in data:
                self.readDataBlock(it, reply)
                if reply.value:
                    values.extend(reply.value)
                reply.clear()
            if len(values) != len(list_):
                raise ValueError("Invalid reply. Read items count do not match.")
            self.client.updateValues(list_, values)

    def write(self, item, attributeIndex):
        data = self.client.write(item, attributeIndex)
        self.readDLMSPacket(data)

    def readRowsByEntry(self, pg, index, count):
        data = self.client.readRowsByEntry(pg, index, count)
        reply = GXReplyData()
        self.readDataBlock(data, reply)
        return self.client.updateValue(pg, 2, reply.value)

    def readRowsByRange(self, pg, start, end):
        reply = GXReplyData()
        data = self.client.readRowsByRange(pg, start, end)
        self.readDataBlock(data, reply)
        return self.client.updateValue(pg, 2, reply.value)

    # Read values using Access request.
    def readByAccess(self, list_):
        if list_:
            reply = GXReplyData()
            data = self.client.accessRequest(None, list_)
            self.readDataBlock(data, reply)
            self.client.parseAccessResponse(list_, reply.data)

    def readScalerAndUnits(self):
        # pylint: disable=broad-except
        objs = self.client.objects.getObjects(
            [
                ObjectType.REGISTER,
                ObjectType.EXTENDED_REGISTER,
                ObjectType.DEMAND_REGISTER,
            ]
        )
        list_ = list()
        try:
            if self.client.negotiatedConformance & Conformance.ACCESS != 0:
                for it in objs:
                    if isinstance(it, (GXDLMSRegister, GXDLMSExtendedRegister)):
                        if it.canRead(3):
                            list_.append(
                                GXDLMSAccessItem(AccessServiceCommandType.GET, it, 3)
                            )
                    elif isinstance(it, (GXDLMSDemandRegister)):
                        if it.canRead(4):
                            list_.append(
                                GXDLMSAccessItem(AccessServiceCommandType.GET, it, 4)
                            )
                self.readByAccess(list_)
                return
        except Exception:
            print("Failed to read scalers and units with access.")
        try:
            if self.client.negotiatedConformance & Conformance.MULTIPLE_REFERENCES != 0:
                for it in objs:
                    if isinstance(it, (GXDLMSRegister, GXDLMSExtendedRegister)):
                        if it.canRead(3):
                            list_.append((it, 3))
                    elif isinstance(it, (GXDLMSDemandRegister,)):
                        if it.canRead(4):
                            list_.append((it, 4))
                self.readList(list_)
        except Exception:
            self.client.negotiatedConformance &= ~Conformance.MULTIPLE_REFERENCES
        if self.client.negotiatedConformance & Conformance.MULTIPLE_REFERENCES == 0:
            for it in objs:
                try:
                    if isinstance(it, (GXDLMSRegister,)):
                        if it.canRead(3):
                            self.read(it, 3)
                    elif isinstance(it, (GXDLMSDemandRegister,)):
                        if it.canRead(4):
                            self.read(it, 4)
                except Exception:
                    pass

    def getProfileGenericColumns(self):
        # pylint: disable=broad-except
        profileGenerics = self.client.objects.getObjects(ObjectType.PROFILE_GENERIC)
        for pg in profileGenerics:
            self.writeTrace(
                "Profile Generic " + str(pg.name) + "Columns:", TraceLevel.INFO
            )
            try:
                if pg.canRead(3):
                    self.read(pg, 3)
                if self.trace > TraceLevel.WARNING:
                    sb = ""
                    for k, _ in pg.captureObjects:
                        if sb:
                            sb += " | "
                        sb += str(k.name)
                        sb += " "
                        desc = k.description
                        if desc:
                            sb += desc
                    self.writeTrace(sb, TraceLevel.INFO)
            except Exception as ex:
                self.writeTrace(
                    "Err! Failed to read columns:" + str(ex), TraceLevel.ERROR
                )

    def getReadOut(self):
        # pylint: disable=unidiomatic-typecheck, broad-except
        for it in self.client.objects:
            if type(it) == GXDLMSObject:
                print("Unknown Interface: " + it.objectType.__str__())
                continue
            if isinstance(it, GXDLMSProfileGeneric):
                continue

            self.writeTrace(
                "-------- Reading "
                + str(it.objectType)
                + " "
                + str(it.name)
                + " "
                + it.description,
                TraceLevel.INFO,
            )
            for pos in it.getAttributeIndexToRead(True):
                try:
                    if it.canRead(pos):
                        val = self.read(it, pos)
                        self.showValue(pos, val)
                    else:
                        self.writeTrace(
                            "Attribute" + str(pos) + " is not readable.",
                            TraceLevel.INFO,
                        )
                except Exception as ex:
                    self.writeTrace(
                        "Error! Index: " + str(pos) + " " + str(ex), TraceLevel.ERROR
                    )
                    self.writeTrace(str(ex), TraceLevel.ERROR)
                    if not isinstance(ex, (GXDLMSException, TimeoutException)):
                        traceback.print_exc()

    def showValue(self, pos, val):
        if isinstance(val, (bytes, bytearray)):
            val = GXByteBuffer(val)
        elif isinstance(val, list):
            str_ = ""
            for tmp in val:
                if str_:
                    str_ += ", "
                if isinstance(tmp, bytes):
                    str_ += GXByteBuffer.hex(tmp)
                else:
                    str_ += str(tmp)
            val = str_
        self.writeTrace("Index: " + str(pos) + " Value: " + str(val), TraceLevel.INFO)

    def getProfileGenerics(self):
        # pylint: disable=broad-except,too-many-nested-blocks
        cells = []
        profileGenerics = self.client.objects.getObjects(ObjectType.PROFILE_GENERIC)
        for it in profileGenerics:
            self.writeTrace(
                "-------- Reading "
                + str(it.objectType)
                + " "
                + str(it.name)
                + " "
                + it.description,
                TraceLevel.INFO,
            )
            entriesInUse = self.read(it, 7)
            entries = self.read(it, 8)
            self.writeTrace(
                "Entries: " + str(entriesInUse) + "/" + str(entries), TraceLevel.INFO
            )
            pg = it
            if entriesInUse == 0 or not pg.captureObjects:
                continue
            try:
                cells = self.readRowsByEntry(pg, 1, 1)
                if self.trace > TraceLevel.WARNING:
                    for rows in cells:
                        for cell in rows:
                            if isinstance(cell, bytearray):
                                self.writeTrace(
                                    GXByteBuffer.hex(cell) + " | ", TraceLevel.INFO
                                )
                            else:
                                self.writeTrace(str(cell) + " | ", TraceLevel.INFO)
                        self.writeTrace("", TraceLevel.INFO)
            except Exception as ex:
                self.writeTrace(
                    "Error! Failed to read first row: " + str(ex), TraceLevel.ERROR
                )
                if not isinstance(ex, (GXDLMSException, TimeoutException)):
                    traceback.print_exc()
            try:
                start = datetime.datetime.now()
                end = start
                start = start.replace(hour=0, minute=0, second=0, microsecond=0)
                end = end.replace(minute=0, second=0, microsecond=0)
                cells = self.readRowsByRange(it, start, end)
                for rows in cells:
                    row = ""
                    for cell in rows:
                        if row:
                            row += " | "
                        if isinstance(cell, bytearray):
                            row += GXByteBuffer.hex(cell)
                        else:
                            row += str(cell)
                    self.writeTrace(row, TraceLevel.INFO)
            except Exception as ex:
                self.writeTrace(
                    "Error! Failed to read last day: " + str(ex), TraceLevel.ERROR
                )

    def getAssociationView(self):
        reply = GXReplyData()
        self.readDataBlock(self.client.getObjectsRequest(), reply)
        self.client.parseObjects(reply.data, True, False)
        # Access rights must read differently when short Name referencing is used.
        if not self.client.useLogicalNameReferencing:
            sn = self.client.objects.findBySN(0xFA00)
            if sn and sn.version > 0:
                try:
                    self.read(sn, 3)
                except GXDLMSException:
                    self.writeTrace(
                        "Access rights are not implemented for the meter.",
                        TraceLevel.INFO,
                    )

    @classmethod
    def __getPath(cls, securitySuite, type_, path, systemTitle):
        if securitySuite == SecuritySuite.Suite2:
            path = os.path.join(path, "384")
        if not systemTitle:
            return path
        if type_ == CertificateType.DigitalSignature:
            pre = "D"
        elif type_ == CertificateType.KeyAgreement:
            pre = "A"
        else:
            raise Exception("Invalid type.")
        return os.path.join(
            path, pre + GXDLMSTranslator.ToHex(systemTitle, False) + ".pem"
        )

    def generateCertificates(self, logicalName):
        """
        Generates a new server and client public/private keys and register them and import certificates to the meter.

            Parameters:
                logicalName: Logical name of the security setup object.
        """

        if not os.path.exists("Keys"):
            os.mkdir("Keys")
        if not os.path.exists("Certificates"):
            os.mkdir("Certificates")
        if not os.path.exists("Keys384"):
            os.mkdir("Keys384")
        if not os.path.exists("Certificates384"):
            os.mkdir("Certificates384")
        address = "https://certificates.gurux.fi/api/CertificateGenerator"
        certs = []
        if self.client.authentication < Authentication.LOW:
            raise Exception(
                "High authentication must be used to change the certificate keys."
            )
        reply = GXReplyData()
        self.initializeConnection()
        ss = GXDLMSSecuritySetup(logicalName)
        certifications = []
        # Read used security suite.
        self.read(ss, 3)
        # Read client system title.
        self.read(ss, 4)
        # Read server system title.
        self.read(ss, 5)
        clientST = ss.clientSystemTitle
        if len(clientST) != 8:
            clientST = self.client.ciphering.systemTitle

        # Get client subject.
        subject = GXAsn1Converter.systemTitleToSubject(clientST)
        # Generate new digital signature for the client. In this example P-256 keys are used.
        kp = GXEcdsa.generateKeyPair(Ecc.P256)
        # Save private key in PKCS #8 format.
        key = GXPkcs8(kp)
        key.save(
            GXPkcs8.getFilePath(Ecc.P256, CertificateType.DIGITAL_SIGNATURE, clientST)
        )
        # Generate x509 certificates.
        pkc10 = GXPkcs10.createCertificateSigningRequest(kp, subject)

        # All certigicates are generated with one request.
        certifications.append(
            GXCertificateRequest(CertificateType.DIGITAL_SIGNATURE, pkc10)
        )

        # Generate new key agreement for the client. In this example P-256 keys are used.
        kp = GXEcdsa.generateKeyPair(Ecc.P256)
        # Save private key in PKCS #8 format.
        key = GXPkcs8(kp)
        key.save(GXPkcs8.getFilePath(Ecc.P256, CertificateType.KEY_AGREEMENT, clientST))
        # Generate x509 certificates.
        pkc10 = GXPkcs10.createCertificateSigningRequest(kp, subject)
        # All certigicates are generated with one request.
        certifications.append(
            GXCertificateRequest(CertificateType.KEY_AGREEMENT, pkc10)
        )

        # Generate public/private key for digital signature.
        if not self.readDataBlock(
            ss.generateKeyPair(self.client, CertificateType.DIGITAL_SIGNATURE), reply
        ):
            raise GXDLMSException(reply.error)

        reply.clear()
        # Generate public/private key for key agreement.
        if not self.readDataBlock(
            ss.generateKeyPair(self.client, CertificateType.KEY_AGREEMENT), reply
        ):
            raise GXDLMSException(reply.error)
        reply.clear()
        # Generate certification request.
        if not self.readDataBlock(
            ss.generateCertificate(self.client, CertificateType.DIGITAL_SIGNATURE),
            reply,
        ):
            raise GXDLMSException(reply.error)

        # Generate server certification.
        pkc10 = GXPkcs10(reply.value)
        subject = GXAsn1Converter.systemTitleToSubject(ss.serverSystemTitle)
        # Validate subject.
        if pkc10.subject.find(subject) == -1:
            raise Exception(
                "Server system title '"
                + GXDLMSTranslator.toHex(ss.serverSystemTitle)
                + "' is not the same as in the generated certificate request '",
                +GXAsn1Converter.hexSystemTitleFromSubject(pkc10.subject) + "'.",
            )
        certifications.append(
            GXCertificateRequest(CertificateType.DIGITAL_SIGNATURE, pkc10)
        )
        reply.clear()

        # Generate certification request for key agreement.
        if not self.readDataBlock(
            ss.generateCertificate(self.client, CertificateType.KEY_AGREEMENT), reply
        ):
            raise GXDLMSException(reply.error)

        # Generate server certification.
        pkc10 = GXPkcs10(reply.value)
        # Validate subject.
        if pkc10.subject.find(subject) == -1:
            raise Exception(
                "Server system title '"
                + GXDLMSTranslator.toHex(ss.serverSystemTitle)
                + "' is not the same as in the generated certificate request '",
                +GXAsn1Converter.hexSystemTitleFromSubject(pkc10.subject) + "'.",
            )
        certifications.append(
            GXCertificateRequest(CertificateType.KEY_AGREEMENT, pkc10)
        )
        reply.clear()

        # Note! There is a limit how many request you can do in a day.
        certs = GXPkcs10.getCertificate(address, certifications)
        # Save server certificates.
        for it in certs:
            it.save(GXx509Certificate.getFilePath(it))
        reply.clear()
        # Import server certificates.
        for it in certs:
            if not self.readDataBlock(ss.importCertificate(self.client, it), reply):
                raise GXDLMSException(reply.error)
            reply.clear()

        # Export server certificates and verify it.
        for it in certs:
            if (
                it.subject.find(
                    GXAsn1Converter.systemTitleToSubject(ss.serverSystemTitle)
                )
                != -1
            ):
                st = ss.serverSystemTitle
                entity = CertificateEntity.SERVER
            elif it.subject.find(GXAsn1Converter.systemTitleToSubject(clientST)) != -1:
                st = clientST
                entity = CertificateEntity.CLIENT
            else:
                # This is another certificate.
                continue

            if not self.readDataBlock(
                ss.exportCertificateByEntity(
                    self.client,
                    entity,
                    GXDLMSConverter.keyUsageToCertificateType(it.keyUsage),
                    st,
                ),
                reply,
            ):
                raise GXDLMSException(reply.error)
            # Verify certificate.
            exported = GXx509Certificate(reply.value)
            if exported != it:
                raise Exception("Invalid server certificate.")
            reply.clear()

        # Export server certificates using serial number and verify it.
        for it in certs:
            if not self.readDataBlock(
                ss.exportCertificateBySerial(
                    self.client, it.serialNumber, it.issuerRaw
                ),
                reply,
            ):
                raise GXDLMSException(reply.error)
            # Verify certificate.
            exported = GXx509Certificate(reply.value)
            if exported != it:
                raise Exception("Invalid server certificate.")
            reply.clear()

    def exportMeterCertificates(self, logicalName):
        """
        Export client and server certificates from the meter.

            Parameters:
                logicalName: Logical name of the security setup object.
        """
        try:
            self.initializeConnection()
            ss = GXDLMSSecuritySetup(logicalName)
            # Read used security suite.
            self.read(ss, 3)
            # Client private keys are saved to this directory.
            # Client might be different system title for each meter.
            if not os.path.exists("Keys"):
                os.mkdir("Keys")
            if not os.path.exists("Certificates"):
                os.mkdir("Certificates")
            if not os.path.exists("Keys384"):
                os.mkdir("Keys384")
            if not os.path.exists("Certificates384"):
                os.mkdir("Certificates384")

            # Read server system title.
            self.read(ss, 5)
            # Read certificates.
            self.read(ss, 6)
            # Export meter certificates and save them.
            reply = GXReplyData()
            for it in ss.certificates:
                reply.clear()
                # Export certification and verify it.
                if not self.readDataBlock(
                    ss.exportCertificateBySerial(
                        self.client, it.serialNumber, it.issuerRaw
                    ),
                    reply,
                ):
                    raise GXDLMSException(reply.error)
                cert = GXx509Certificate(reply.value)
                path = GXx509Certificate.getFilePath(cert)
                cert.save(path)
        finally:
            self.close()

    def readAll(self, outputFile):
        try:
            read = False
            self.initializeConnection()
            if outputFile and os.path.exists(outputFile):
                try:
                    c = GXDLMSObjectCollection.load(outputFile)
                    self.client.objects.extend(c)
                    if self.client.objects:
                        read = True
                except Exception:
                    read = False
            if not read:
                self.getAssociationView()
                self.readScalerAndUnits()
                self.getProfileGenericColumns()
            self.getReadOut()
            self.getProfileGenerics()
            if outputFile:
                self.client.objects.save(outputFile)
        except (KeyboardInterrupt, SystemExit):
            # Don't send anything if user is closing the app.
            self.media = None
            raise
        finally:
            self.close()

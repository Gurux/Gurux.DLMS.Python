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
from gurux_dlms.enums import InterfaceType, Authentication, Security, Standard
from gurux_dlms import GXDLMSClient
from gurux_dlms.secure import GXDLMSSecureClient
from gurux_dlms.GXByteBuffer import GXByteBuffer
from gurux_dlms.objects import GXDLMSObject
from gurux_common.enums import TraceLevel
from gurux_common.io import Parity, StopBits, BaudRate
from gurux_net.enums import NetworkType
from gurux_net import GXNet
from gurux_serial.GXSerial import GXSerial
from GXCmdParameter import GXCmdParameter

class GXSettings:
    #
    # Constructor.
    #
    def __init__(self):
        self.media = None
        self.trace = TraceLevel.INFO
        self.iec = False
        self.invocationCounter = None
        self.client = GXDLMSSecureClient(True)
        #  Objects to read.
        self.readObjects = []
        self.outputFile = None

    #
    # Show help.
    #
    @classmethod
    def showHelp(cls):
        print("GuruxDlmsSample reads data from the DLMS/COSEM device.")
        print("GuruxDlmsSample -h [Meter IP Address] -p [Meter Port No] -c 16 -s 1 -r SN")
        print(" -h \t host name or IP address.")
        print(" -p \t port number or name (Example: 1000).")
        print(" -S \t serial port. (Example: COM1 or COM1:9600:8None1)")
        print(" -i IEC is a start protocol.")
        print(" -a \t Authentication (None, Low, High).")
        print(" -P \t Password for authentication.")
        print(" -c \t Client address. (Default: 16)")
        print(" -s \t Server address. (Default: 1)")
        print(" -n \t Server address as serial number.")
        print(" -r [sn, ln]\t Short name or Logical Name (default) referencing is used.")
        print(" -w WRAPPER profile is used. HDLC is default.")
        print(" -t [Error, Warning, Info, Verbose] Trace messages.")
        print(" -g \"0.0.1.0.0.255:1; 0.0.1.0.0.255:2\" Get selected object(s) with given attribute index.")
        print(" -C Security Level. (None, Authentication, Encrypted, AuthenticationEncryption)")
        print(" -v Invocation counter data object Logical Name. Ex. 0.0.43.1.0.255")
        print(" -I \t Auto increase invoke ID")
        print(" -o \t Cache association view to make reading faster. Ex. -o C:\\device.xml")
        print(" -T \t System title that is used with chiphering. Ex -D 4775727578313233")
        print(" -A \t Authentication key that is used with chiphering. Ex -D D0D1D2D3D4D5D6D7D8D9DADBDCDDDEDF")
        print(" -B \t Block cipher key that is used with chiphering. Ex -D 000102030405060708090A0B0C0D0E0F")
        print(" -D \t Dedicated key that is used with chiphering. Ex -D 00112233445566778899AABBCCDDEEFF")
        print(" -d \t Used DLMS standard. Ex -d India (DLMS, India, Italy, Saudi_Arabia, IDIS)")
        print("Example:")
        print("Read LG device using TCP/IP connection.")
        print("GuruxDlmsSample -r SN -c 16 -s 1 -h [Meter IP Address] -p [Meter Port No]")
        print("Read LG device using serial port connection.")
        print("GuruxDlmsSample -r SN -c 16 -s 1 -sp COM1 -i")
        print("Read Indian device using serial port connection.")
        print("GuruxDlmsSample -S COM1 -c 16 -s 1 -a Low -P [password]")
        print("------------------------------------------------------")
        print("Available serial ports:")
        print(GXSerial.getPortNames())

    # Returns command line parameters.
    #
    # @param args
    #            Command line parameters.
    # @param optstring
    #            Expected option tags.
    # @return List of command line parameters
    #
    @classmethod
    def __getParameters(cls, args, optstring):
        list_ = list()
        skipNext = False
        for index in range(1, len(args)):
            if skipNext:
                skipNext = False
            else:
                if args[index][0] != '-' and args[index][0] != '/':
                    raise ValueError("Invalid parameter: " + args[index])

                pos = optstring.index(args[index][1])
                if pos == - 1:
                    raise ValueError("Invalid parameter: " + args[index])

                c = GXCmdParameter()
                c.tag = args[index][1]
                list_.append(c)
                if pos < len(optstring) - 1 and optstring[1 + pos] == ':':
                    skipNext = True
                    if len(args) <= index:
                        c.missing = True
                    c.value = args[1 + index]
        return list_


    def getParameters(self, args):
        parameters = GXSettings.__getParameters(args, "h:p:c:s:r:iIt:a:p:wP:g:S:n:C:v:o:T:A:B:D:d:")
        defaultBaudRate = True
        for it in parameters:
            if it.tag == 'w':
                self.client.interfaceType = InterfaceType.WRAPPER
            elif it.tag == 'r':
                if it.value == "sn":
                    self.client.useLogicalNameReferencing = False
                elif it.value == "ln":
                    self.client.useLogicalNameReferencing = True
                else:
                    raise ValueError("Invalid reference option.")
            elif it.tag == 'h':
                #  Host address.
                if not self.media:
                    self.media = GXNet(NetworkType.TCP, it.value, 0)
                else:
                    self.media.hostName = it.value
            elif it.tag == 't':
                #  Trace.
                if it.value == "Off":
                    self.trace = TraceLevel.OFF
                elif it.value == "Error":
                    self.trace = TraceLevel.ERROR
                elif it.value == "Warning":
                    self.trace = TraceLevel.WARNING
                elif it.value == "Info":
                    self.trace = TraceLevel.INFO
                elif it.value == "Verbose":
                    self.trace = TraceLevel.VERBOSE
                else:
                    raise ValueError("Invalid trace level(Off, Error, Warning, Info, Verbose).")
            elif it.tag == 'p':
                #  Port.
                if not self.media:
                    self.media = GXNet(NetworkType.TCP, None, int(it.value))
                else:
                    self.media.port = int(it.value)
            elif it.tag == 'P':
                #  Password
                self.client.password = it.value
            elif it.tag == 'i':
                #  IEC.
                self.iec = True
                if not defaultBaudRate:
                    self.media.baudrate = BaudRate.BAUD_RATE_300
                    self.media.bytesize = 7
                    self.media.parity = Parity.EVEN
                    self.media.stopbits = StopBits.ONE
            elif it.tag == 'I':
                #AutoIncreaseInvokeID.
                self.client.autoIncreaseInvokeID = True
            elif it.tag == 'v':
                self.invocationCounter = it.value
                GXDLMSObject.validateLogicalName(self.invocationCounter)
            elif it.tag == 'g':
                #  Get (read) selected objects.
                for o in it.value.split(";,"):
                    tmp = o.split(":")
                    if len(tmp) != 2:
                        raise ValueError("Invalid Logical name or attribute index.")
                    self.readObjects.append((tmp[0].strip(), int(tmp[1].strip())))
            elif it.tag == 'S':#Serial Port
                self.media = GXSerial(None)
                tmp = it.value.split(':')
                self.media.port = tmp[0]
                if len(tmp) > 1:
                    defaultBaudRate = False
                    self.media.baudRate = int(tmp[1])
                    self.media.dataBits = int(tmp[2][0: 1])
                    self.media.parity = Parity[tmp[2][1: len(tmp[2]) - 1].upper()]
                    self.media.stopBits = int(tmp[2][len(tmp[2]) - 1:]) - 1
                else:
                    self.media.baudrate = BaudRate.BAUD_RATE_9600
                    self.media.bytesize = 8
                    self.media.parity = Parity.NONE
                    self.media.stopbits = StopBits.ONE
            elif it.tag == 'a':
                try:
                    if it.value == "None":
                        self.client.authentication = Authentication.NONE
                    elif it.value == "Low":
                        self.client.authentication = Authentication.LOW
                    elif it.value == "High":
                        self.client.authentication = Authentication.HIGH
                    elif it.value == "HighMd5":
                        self.client.authentication = Authentication.HIGH_MD5
                    elif it.value == "HighSha1":
                        self.client.authentication = Authentication.HIGH_SHA1
                    elif it.value == "HighGMac":
                        self.client.authentication = Authentication.HIGH_GMAC
                    elif it.value == "HighSha256":
                        self.client.authentication = Authentication.HIGH_SHA256
                except Exception:
                    raise ValueError("Invalid Authentication option: '" + it.value + "'. (None, Low, High, HighMd5, HighSha1, HighGMac, HighSha256)")
            elif it.tag == 'C':
                if it.value == "None":
                    self.client.ciphering.security = Security.NONE
                elif it.value == "Authentication":
                    self.client.ciphering.security = Security.AUTHENTICATION
                elif it.value == "Encryption":
                    self.client.ciphering.security = Security.ENCRYPTION
                elif it.value == "AuthenticationEncryption":
                    self.client.ciphering.security = Security.AUTHENTICATION_ENCRYPTION
                else:
                    raise ValueError("Invalid Ciphering option: '" + it.value + "'. (None, Authentication, Encryption, AuthenticationEncryption)")
            elif it.tag == 'T':
                self.client.ciphering.systemTitle = GXByteBuffer.hexToBytes(it.value)
            elif it.tag == 'A':
                self.client.ciphering.authenticationKey = GXByteBuffer.hexToBytes(it.value)
            elif it.tag == 'B':
                self.client.ciphering.blockCipherKey = GXByteBuffer.hexToBytes(it.value)
            elif it.tag == 'D':
                self.client.ciphering.dedicatedKey = GXByteBuffer.hexToBytes(it.value)
            elif it.tag == 'o':
                self.outputFile = it.value
            elif it.tag == 'd':
                if it.value == "DLMS":
                    self.client.standard = Standard.DLMS
                elif it.value == "India":
                    self.client.standard = Standard.INDIA
                elif it.value == "Italy":
                    self.client.standard = Standard.ITALY
                elif it.value == "SaudiArabia":
                    self.client.standard = Standard.SAUDI_ARABIA
                elif it.value == "IDIS":
                    self.client.standard = Standard.IDIS
                else:
                    raise ValueError("Invalid DLMS standard option: '" + it.value + "'. (DLMS, India, Italy, SaudiArabia, IDIS)")
            elif it.tag == 'c':
                self.client.clientAddress = int(it.value)
            elif it.tag == 's':
                self.client.serverAddress = int(it.value)
            elif it.tag == 'n':
                self.client.serverAddress = GXDLMSClient.getServerAddress(int(it.value))
            elif it.tag == '?':
                if it.tag == 'c':
                    raise ValueError("Missing mandatory client option.")
                if it.tag == 's':
                    raise ValueError("Missing mandatory server option.")
                if it.tag == 'h':
                    raise ValueError("Missing mandatory host name option.")
                if it.tag == 'p':
                    raise ValueError("Missing mandatory port option.")
                if it.tag == 'r':
                    raise ValueError("Missing mandatory reference option.")
                if it.tag == 'a':
                    raise ValueError("Missing mandatory authentication option.")
                if it.tag == 'S':
                    raise ValueError("Missing mandatory Serial port option.\n")
                if it.tag == 't':
                    raise ValueError("Missing mandatory trace option.\n")
                if it.tag == 'g':
                    raise ValueError("Missing mandatory OBIS code option.")
                if it.tag == 'C':
                    raise ValueError("Missing mandatory Ciphering option.")
                if it.tag == 'v':
                    raise ValueError("Missing mandatory invocation counter logical name option.")
                if it.tag == 'T':
                    raise ValueError("Missing mandatory system title option.")
                if it.tag == 'A':
                    raise ValueError("Missing mandatory authentication key option.")
                if it.tag == 'B':
                    raise ValueError("Missing mandatory block cipher key option.")
                if it.tag == 'D':
                    raise ValueError("Missing mandatory dedicated key option.")
                if it.tag == 'd':
                    raise ValueError("Missing mandatory DLMS standard option.")
                self.showHelp()
                return 1
            else:
                self.showHelp()
                return 1

        if not self.media:
            GXSettings.showHelp()
            return 1
        return 0

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
from gurux_dlms.GXByteBuffer import GXByteBuffer
from gurux_dlms.objects import GXDLMSObject
from gurux_dlms.GXDLMSXmlClient import GXDLMSXmlClient
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
        self.invocationCounter = None
        self.client = GXDLMSXmlClient()
        #cache file.
        self.outputFile = None
        self.path = None
    #
    # Show help.
    #
    @classmethod
    def showHelp(cls):
        print("Gurux.DLMS.XmlClient reads data from the DLMS/COSEM device.")
        print("python main.py -h [Meter IP Address] -p [Meter Port No] -c 16 -s 1 -r SN")
        print(" -h \t host name or IP address.")
        print(" -p \t port number or name (Example: 1000).")
        print(" -S [COM1:9600:8None1]\t serial port.")
        print(" -i IEC is a start protocol.")
        print(" -a \t Authentication (None, Low, High).")
        print(" -P \t Password for authentication.")
        print(" -c \t Client address. (Default: 16)")
        print(" -s \t Server address. (Default: 1)")
        print(" -n \t Server address as serial number.")
        print(" -l \t Logical Server address.")
        print(" -r [sn, ln]\t Short name or Logical Name (default) referencing is used.")
        print(" -w WRAPPER profile is used. HDLC is default.")
        print(" -t [Error, Warning, Info, Verbose] Trace messages.")
        print(" -C \t Security Level. (None, Authentication, Encrypted, AuthenticationEncryption)")
        print(" -v \t Invocation counter data object Logical Name. Ex. 0.0.43.1.1.255")
        print(" -I \t Auto increase invoke ID")
        print(" -o \t Cache association view to make reading faster. Ex. -o C:\\device.xml")
        print(" -T \t System title that is used with chiphering. Ex -D 4775727578313233")
        print(" -A \t Authentication key that is used with chiphering. Ex -D D0D1D2D3D4D5D6D7D8D9DADBDCDDDEDF")
        print(" -B \t Block cipher key that is used with chiphering. Ex -D 000102030405060708090A0B0C0D0E0F")
        print(" -D \t Dedicated key that is used with chiphering. Ex -D 00112233445566778899AABBCCDDEEFF")
        print(" -F \t Initial Frame Counter (Invocation counter) value.")
        print(" -d \t Used DLMS standard. Ex -d India (DLMS, India, Italy, SaudiArabia, IDIS)")
        print(" -x input XML file.")
        print("Example:")
        print("Read LG device using TCP/IP connection.")
        print("python main.py -r SN -c 16 -s 1 -h [Meter IP Address] -p [Meter Port No]")
        print("Read LG device using serial port connection.")
        print("python main.py -r SN -c 16 -s 1 -sp COM1 -i")
        print("Read Indian device using serial port connection.")
        print("python main.py -S COM1 -c 16 -s 1 -a Low -P [password]")
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
        parameters = GXSettings.__getParameters(args, "h:p:c:s:r:i:It:a:p:P:S:n:C:v:o:T:A:B:D:d:l:W:w:f:L:x:")
        modeEDefaultValues = True
        for it in parameters:
            if it.tag == 'x':
                self.path = it.value
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
                if it.value.startswith("0x"):
                    self.client.password = GXByteBuffer.hexToBytes(it.value[2:])
                else:
                    self.client.password = it.value
            elif it.tag == 'i':
                if it.value == "HDLC":
                    self.client.interfaceType = InterfaceType.HDLC
                elif it.value == "WRAPPER":
                    self.client.interfaceType = InterfaceType.WRAPPER
                elif it.value == "HdlcWithModeE":
                    self.client.interfaceType = InterfaceType.HDLC_WITH_MODE_E
                elif it.value == "Plc":
                    self.client.interfaceType = InterfaceType.PLC
                elif it.value == "PlcHdlc":
                    self.client.interfaceType = InterfaceType.PLC_HDLC
                else:
                    raise ValueError("Invalid interface type option." + it.value + " (HDLC, WRAPPER, HdlcWithModeE, Plc, PlcHdlc)")
                if modeEDefaultValues and self.client.interfaceType == InterfaceType.HDLC_WITH_MODE_E and isinstance(self.media, GXSerial):
                    self.media.baudRate = BaudRate.BAUD_RATE_300
                    self.media.dataBits = 7
                    self.media.parity = Parity.EVEN
                    self.media.stopbits = StopBits.ONE
            elif it.tag == 'I':
                #AutoIncreaseInvokeID.
                self.client.autoIncreaseInvokeID = True
            elif it.tag == 'v':
                self.invocationCounter = it.value
                GXDLMSObject.validateLogicalName(self.invocationCounter)
            elif it.tag == 'S':#Serial Port
                self.media = GXSerial(None)
                tmp = it.value.split(':')
                self.media.port = tmp[0]
                if len(tmp) > 1:
                    modeEDefaultValues = False
                    self.media.baudRate = int(tmp[1])
                    self.media.dataBits = int(tmp[2][0: 1])
                    self.media.parity = Parity[tmp[2][1: len(tmp[2]) - 1].upper()]
                    self.media.stopBits = int(tmp[2][len(tmp[2]) - 1:]) - 1
                else:
                    if self.client.interfaceType == InterfaceType.HDLC_WITH_MODE_E:
                        self.media.baudRate = BaudRate.BAUD_RATE_300
                        self.media.dataBits = 7
                        self.media.parity = Parity.EVEN
                        self.media.stopbits = StopBits.ONE
                    else:
                        self.media.baudRate = BaudRate.BAUD_RATE_9600
                        self.media.dataBits = 8
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
                    self.client.useUtc2NormalTime = True
                elif it.value == "Italy":
                    self.client.standard = Standard.ITALY
                    self.client.useUtc2NormalTime = True
                elif it.value == "SaudiArabia":
                    self.client.standard = Standard.SAUDI_ARABIA
                    self.client.useUtc2NormalTime = True
                elif it.value == "IDIS":
                    self.client.standard = Standard.IDIS
                else:
                    raise ValueError("Invalid DLMS standard option: '" + it.value + "'. (DLMS, India, Italy, SaudiArabia, IDIS)")
            elif it.tag == 'c':
                self.client.clientAddress = int(it.value)
            elif it.tag == 's':
                if self.client.serverAddress != 1:
                    self.client.serverAddress = GXDLMSClient.getServerAddress(self.client.serverAddress, int(it.value))
                else:
                    self.client.serverAddress = int(it.value)
            elif it.tag == 'l':
                self.client.serverAddress = GXDLMSClient.getServerAddress(int(it.value), self.client.serverAddress)
            elif it.tag == 'n':
                self.client.serverAddress = GXDLMSClient.getServerAddressFromSerialNumber(int(it.value))
            elif it.tag == 'W':
                self.client.gbtWindowSize = int(it.value)
            elif it.tag == 'w':
                self.client.hdlcSettings.WindowSizeRX = self.client.hdlcSettings.WindowSizeTX = int(it.value)
            elif it.tag == 'f':
                self.client.hdlcSettings.MaxInfoRX = self.client.hdlcSettings.MaxInfoTX = int(it.value)
            elif it.tag == 'L':
                self.client.manufacturerId = it.value
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

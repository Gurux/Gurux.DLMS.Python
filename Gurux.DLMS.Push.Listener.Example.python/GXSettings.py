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
from gurux_dlms.enums import InterfaceType
from gurux_dlms.secure import GXDLMSSecureClient
from gurux_dlms.GXByteBuffer import GXByteBuffer

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
        self.client = GXDLMSSecureClient(True)

    #
    # Show help.
    #
    @classmethod
    def showHelp(cls):
        print("Gurux.DLMS.Push.Listener.Example waits notify messages from the DLMS/COSEM device.")
        print("python main -h localhost -p [Meter Port No] -c 16 -s 1 -r SN")
        print(" -p \t port number or name (Example: 1000).")
        print(" -i \t Used communication interface. Ex. -i WRAPPER.")
        print(" -S \t serial port. (Example: COM1 or COM1:9600:8None1)")
        print(" -r [sn, ln]\t Short name or Logical Name (default) referencing is used.")
        print(" -t [Error, Warning, Info, Verbose] Trace messages.")
        print(" -T \t System title that is used with chiphering. Ex -T 4775727578313233")
        print(" -A \t Authentication key that is used with chiphering. Ex -A D0D1D2D3D4D5D6D7D8D9DADBDCDDDEDF")
        print(" -B \t Block cipher key that is used with chiphering. Ex -B 000102030405060708090A0B0C0D0E0F")
        print(" -D \t Dedicated key that is used with chiphering. Ex -D 00112233445566778899AABBCCDDEEFF")
        print("Example:")
        print("Start listener using TCP/IP connection.")
        print("python main -p [Meter Port No] -i WRAPPER")
        print("Start listener using serial port connection.")
        print("python main -S COM1:9600:8None1")
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
        parameters = GXSettings.__getParameters(args, "p:S:r:i:t:T:A:B:D:")
        for it in parameters:
            if it.tag == 'r':
                if it.value == "sn":
                    self.client.useLogicalNameReferencing = False
                elif it.value == "ln":
                    self.client.useLogicalNameReferencing = True
                else:
                    raise ValueError("Invalid reference option.")
            elif it.tag == 'i':
                if it.value == "HDLC":
                    self.client.interfaceType = InterfaceType.HDLC
                elif it.value == "WRAPPER":
                    self.client.interfaceType = InterfaceType.WRAPPER
                elif it.value == "HdlcWithModeE":
                    self.client.interfaceType = InterfaceType.HDLC_WITH_MODE_E
                elif it.value == "Plc":
                    self.clientinterfaceType = InterfaceType.PLC
                elif it.value == "PlcHdlc":
                    self.clientinterfaceType = InterfaceType.PLC_HDLC
                else:
                    raise ValueError("Invalid interface type option." + it.value + " (HDLC, WRAPPER, HdlcWithModeE, Plc, PlcHdlc)");
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
                    self.media.server = True
                else:
                    self.media.port = int(it.value)
            elif it.tag == 'S':#Serial Port
                self.media = GXSerial(None)
                tmp = it.value.split(':')
                self.media.port = tmp[0]
                if len(tmp) > 1:
                    self.media.baudRate = int(tmp[1])
                    self.media.dataBits = int(tmp[2][0: 1])
                    self.media.parity = Parity[tmp[2][1: len(tmp[2]) - 1].upper()]
                    self.media.stopBits = int(tmp[2][len(tmp[2]) - 1:]) - 1
                else:
                    self.media.baudrate = BaudRate.BAUD_RATE_9600
                    self.media.bytesize = 8
                    self.media.parity = Parity.NONE
                    self.media.stopbits = StopBits.ONE
            elif it.tag == 'T':
                self.client.ciphering.systemTitle = GXByteBuffer.hexToBytes(it.value)
            elif it.tag == 'A':
                self.client.ciphering.authenticationKey = GXByteBuffer.hexToBytes(it.value)
            elif it.tag == 'B':
                self.client.ciphering.blockCipherKey = GXByteBuffer.hexToBytes(it.value)
            elif it.tag == 'D':
                self.client.ciphering.dedicatedKey = GXByteBuffer.hexToBytes(it.value)
            elif it.tag == '?':
                if it.tag == 'p':
                    raise ValueError("Missing mandatory port option.")
                if it.tag == 'r':
                    raise ValueError("Missing mandatory reference option.")
                if it.tag == 'S':
                    raise ValueError("Missing mandatory Serial port option.\n")
                if it.tag == 't':
                    raise ValueError("Missing mandatory trace option.\n")
                self.showHelp()
                return 1
            else:
                self.showHelp()
                return 1

        if not self.media:
            GXSettings.showHelp()
            return 1
        return 0

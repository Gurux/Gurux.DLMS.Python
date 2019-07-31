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
# ignore serial for now.  import serial
import socket
import sys
from gurux_dlms import InterfaceType, Authentication
from gurux_dlms.secure import GXDLMSSecureClient
from TraceLevel import TraceLevel
from GXCmdParameter import GXCmdParameter

class GXSettings:
    #
    # Constructor.
    #
    def __init__(self):
        self.media = None
        self.trace = TraceLevel.INFO
        self.iec = False
        self.client = GXDLMSSecureClient(True)
        #  Objects to read.
        self.readObjects = []

    #
    # Show help.
    #
    @classmethod
    def showHelp(self):
        print("GuruxDlmsSample reads data from the DLMS/COSEM device.")
        print("GuruxDlmsSample -h [Meter IP Address] -p [Meter Port No] -c 16 -s 1 -r SN")
        print(" -h \t host name or IP address.")
        print(" -p \t port number or name (Example: 1000).")
        print(" -S \t serial port.")
        print(" -i IEC is a start protocol.")
        print(" -a \t Authentication (None, Low, High).")
        print(" -P \t Password for authentication.")
        print(" -c \t Client address. (Default: 16)")
        print(" -s \t Server address. (Default: 1)")
        print(" -n \t Server address as serial number.")
        print(" -r [sn, sn]\t Short name or Logican Name (default) referencing is used.")
        print(" -w WRAPPER profile is used. HDLC is default.")
        print(" -t [Error, Warning, Info, Verbose] Trace messages.")
        print(" -g \"0.0.1.0.0.255:1; 0.0.1.0.0.255:2\" Get selected object(s) with given attribute index.")
        print("Example:")
        print("Read LG device using TCP/IP connection.")
        print("GuruxDlmsSample -r SN -c 16 -s 1 -h [Meter IP Address] -p [Meter Port No]")
        print("Read LG device using serial port connection.")
        print("GuruxDlmsSample -r SN -c 16 -s 1 -sp COM1 -i")
        print("Read Indian device using serial port connection.")
        print("GuruxDlmsSample -S COM1 -c 16 -s 1 -a Low -P [password]")

    # Returns command line parameters.
    #
    # @param args
    #            Command line parameters.
    # @param optstring
    #            Expected option tags.
    # @return List of command line parameters
    #
    @classmethod
    def __getParameters(self,args, optstring):
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
                        c.missing(True)
                    c.value = args[1 + index]
        return list_


    def getParameters(self, args):
        parameters = GXSettings.__getParameters(args, "h:p:c:s:r:it:a:p:wP:g:")
        hostName = None
        port = 0
        for it in parameters:
            if it.tag == 'w':
                self.client.interfaceType = InterfaceType.WRAPPER
            elif it.tag == 'r':
                if it.value == "sn":
                    self.client.setUseLogicalNameReferencing(False)
                elif it.value == "ln":
                    self.client.setUseLogicalNameReferencing(True)
                else:
                    raise ValueError("Invalid reference option.")
            elif it.tag == 'h':
                #  Host address.
                hostName = it.value
            elif it.tag == 't':
                #  Trace.
                self.trace = TraceLevel[it.value.upper()]
            elif it.tag == 'p':
                #  Port.
                port = int(it.value)
            elif it.tag == 'P':
                #  Password
                self.client.password = it.value
            elif it.tag == 'i':
                #  IEC.
                self.iec = True
            elif it.tag == 'g':
                #  Get (read) selected objects.
                for o in it.value.split(";,"):
                    tmp = o.split(":")
                    if len(tmp):
                        raise ValueError("Invalid Logical name or attribute index.")
                    self.readObjects.append((tmp[0].strip(), int(tmp[1].strip())))
            elif it.tag == 'S':
                self.media = serial.Serial(it.value)
            elif it.tag == 'a':
                try:
                    it.value = it.value.upper()
                    if it.value.startswith("HIGH"):
                        it.value ="HIGH_" + it.value[4:]
                    self.client.authentication = Authentication[it.value]
                except Exception as e:
                    #raise ValueError("Invalid Authentication option: '" + it.value + "'. (None, Low, High, HighMd5, HighSha1, HighGmac, HighSha256)")
                    raise ValueError("Invalid Authentication option: '" + it.value + "'. (None, Low, HighGmac)")
            elif it.tag == 'o':
                pass
            elif it.tag == 'c':
                self.client.clientAddress = int(it.value)
            elif it.tag == 's':
                self.client.serverAddress = int(it.value)
            elif it.tag == '?':
                if it.tag == 'c':
                    raise ValueError("Missing mandatory client option.")
                elif it.tag == 's':
                    raise ValueError("Missing mandatory server option.")
                elif it.tag == 'h':
                    raise ValueError("Missing mandatory host name option.")
                elif it.tag == 'p':
                    raise ValueError("Missing mandatory port option.")
                elif it.tag == 'r':
                    raise ValueError("Missing mandatory reference option.")
                elif it.tag == 'a':
                    raise ValueError("Missing mandatory authentication option.")
                elif it.tag == 'S':
                    raise ValueError("Missing mandatory Serial port option.\n")
                elif it.tag == 't':
                    raise ValueError("Missing mandatory trace option.\n")
                else:
                    self.showHelp()
                    return 1
            else:
                self.showHelp()
                return 1

        if hostName != None and port != 0:
            self.media = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (hostName, port)
            self.media.connect(server_address)

        if self.media == None:
            GXSettings.showHelp()
            return 1
        return 0

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
import os.path
import sys
import traceback
from gurux_common.enums import TraceLevel
from gurux_common.GXCommon import GXCommon
from gurux_serial import GXSerial
from gurux_net import GXNet
from gurux_dlms import GXDLMSException, GXDLMSExceptionResponse, GXDLMSConfirmedServiceError
from gurux_dlms import GXReplyData
from gurux_dlms.enums import InterfaceType, Command
from GXSettings import GXSettings
from GXDLMSReader import GXDLMSReader

try:
    import pkg_resources
    #pylint: disable=broad-except
except Exception:
    #It's OK if this fails.
    print("pkg_resources not found")

#pylint: disable=too-few-public-methods,broad-except
class sampleclient():

    #Returns True, is command is in XML file.
    @classmethod
    def ___containsCommand(cls, actions, command):
        for it in actions:
            if it.command == command:
                return True

        return False

    # Handle meter reply.
    # reply: Received reply.
    @classmethod
    def handleReply(cls, reply):
        if isinstance(reply.value, (bytes, bytearray)):
            print(GXCommon.toHex(reply.value))
            print(str(reply))
        else:
            print(str(reply))

    @classmethod
    def main(cls, args):
        try:
            print("gurux_dlms version: " + pkg_resources.get_distribution("gurux_dlms").version)
            print("gurux_net version: " + pkg_resources.get_distribution("gurux_net").version)
            print("gurux_serial version: " + pkg_resources.get_distribution("gurux_serial").version)
        except Exception:
            #It's OK if this fails.
            print("pkg_resources not found")

        # args: the command line arguments
        reader = None
        settings = GXSettings()
        try:
            # //////////////////////////////////////
            #  Handle command line parameters.
            ret = settings.getParameters(args)
            if ret != 0:
                return
            # //////////////////////////////////////
            #  Initialize connection settings.
            if not isinstance(settings.media, (GXSerial, GXNet)):
                raise Exception("Unknown media type.")
            # //////////////////////////////////////
            if not settings.path:
                if settings.client.useLogicalNameReferencing:
                    settings.path = "Messages\\LN"
                else:
                    settings.path = "Messages\\SN"
            if os.path.isdir(settings.path):
                #files = os.listdir(settings.path)
                files = [os.path.join(settings.path, name) for name in os.listdir(settings.path)]
            else:
                files = []
                files.append(settings.path)
            #Execute messages.
            for file in files:
                name = os.path.splitext(file)[0]
                if settings.trace > TraceLevel.WARNING:
                    print("------------------------------------------------------------")
                    print(name)
                actions = settings.client.load(file)
                #If there aren't actions in the file.
                if not actions:
                    continue
                try:
                    settings.media.open()
                    reader = GXDLMSReader(settings.client, settings.media, settings.trace, settings.invocationCounter)
                    reply = GXReplyData()
                    #Send SNRM if not in xml.
                    if settings.client.interfaceType == InterfaceType.HDLC:
                        if not sampleclient.___containsCommand(actions, Command.SNRM):
                            reader.snrmRequest()

                    #Send AARQ if not in xml.
                    if not sampleclient.___containsCommand(actions, Command.AARQ):
                        if not sampleclient.___containsCommand(actions, Command.SNRM):
                            reader.aarqRequest()

                    for it in actions:
                        if it.command == Command.SNRM and settings.client.interfaceType == InterfaceType.WRAPPER:
                            continue
                        if it.command == Command.DISCONNECT_REQUEST and settings.client.interfaceType == InterfaceType.WRAPPER:
                            break
                        #Send
                        reply.clear()
                        if settings.trace > TraceLevel.WARNING:
                            print("------------------------------------------------------------")
                            print(str(it))

                        if it.isRequest():
                            reader.readDataBlock(settings.client.pduToMessages(it), reply)
                            cls.handleReply(reply)
                except (ValueError, GXDLMSException, GXDLMSExceptionResponse, GXDLMSConfirmedServiceError) as ex:
                    print(ex)
        except (KeyboardInterrupt, SystemExit, Exception) as ex:
            traceback.print_exc()
            if settings.media:
                settings.media.close()
            reader = None
        finally:
            if reader:
                try:
                    #Send disconnect if not in xml.
                    if not sampleclient.___containsCommand(actions, Command.DISCONNECT_REQUEST):
                        reader.disconnect()
                    else:
                        settings.media.close()
                        reader.close()
                except Exception:
                    traceback.print_exc()
            print("Ended. Press any key to continue.")

if __name__ == '__main__':
    sampleclient.main(sys.argv)

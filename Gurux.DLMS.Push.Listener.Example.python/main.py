#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename: $HeadURL$
#
#  Version: $Revision$,
#                $Date$
#                $Author$
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
import time
import sys
import traceback
import pkg_resources
from gurux_common.GXCommon import GXCommon
from gurux_common.IGXMediaListener import IGXMediaListener
from gurux_common.enums.TraceLevel import TraceLevel
from gurux_serial.GXSerial import GXSerial
from GXSettings import GXSettings
from gurux_dlms.enums.InterfaceType import InterfaceType
from gurux_dlms.GXDLMSTranslator import GXDLMSTranslator
from gurux_dlms.GXReplyData import GXReplyData
from gurux_dlms.GXByteBuffer import GXByteBuffer

# ---------------------------------------------------------------------------
# This example wait push notifications from the serial port or TCP/IP port.
# ---------------------------------------------------------------------------
#pylint: disable=no-self-argument
class sampleclient(IGXMediaListener):
    def __init__(self, args):
        try:
            print("gurux_dlms version: " + pkg_resources.get_distribution("gurux_dlms").version)
            print("gurux_net version: " + pkg_resources.get_distribution("gurux_net").version)
            print("gurux_serial version: " + pkg_resources.get_distribution("gurux_serial").version)
        except Exception:
            #It's OK if this fails.
            print("pkg_resources not found")
        settings = GXSettings()
        ret = settings.getParameters(args)
        if ret != 0:
            return

        #There might be several notify messages in GBT.
        self.notify = GXReplyData()
        self.client = settings.client
        self.translator = GXDLMSTranslator()
        self.reply = GXByteBuffer()
        settings.media.trace = settings.trace
        print(settings.media)

        #Start to listen events from the media.
        settings.media.addListener(self)
        #Set EOP for the media.
        if settings.client.interfaceType == InterfaceType.HDLC:
            settings.media.eop = 0x7e
        try:
            print("Press any key to close the application.")
            #Open the connection.
            settings.media.open()
            #Wait input.
            input()
            print("Closing")
        except (KeyboardInterrupt, SystemExit, Exception) as ex:
            print(ex)
        settings.media.close()
        settings.media.removeListener(self)

    def onError(self, sender, ex):
        """
        Represents the method that will handle the error event of a Gurux
        component.

        sender :  The source of the event.
        ex : An Exception object that contains the event data.
        """
        print("Error has occured. " + str(ex))

    @classmethod
    def printData(cls, value, offset):
        sb = ' ' * 2 * offset
        if isinstance(value, list):
            print(sb + "{")
            offset = offset + 1
            #Print received data.
            for it in value:
                cls.printData(it, offset)
            print(sb + "}")
            offset = offset - 1
        elif isinstance(value, bytearray):
            #Print value.
            print(sb + GXCommon.toHex(value))
        else:
            #Print value.
            print(sb + str(value))

    def onReceived(self, sender, e):
        """Media component sends received data through this method.

        sender : The source of the event.
        e : Event arguments.
        """
        if sender.trace == TraceLevel.VERBOSE:
            print("New data is received. " + GXCommon.toHex(e.data))
        #Data might come in fragments.
        self.reply.set(e.data)
        data = GXReplyData()
        try:
            if not self.client.getData(self.reply, data, self.notify):
                #If all data is received.
                if self.notify.complete:
                    if not self.notify.isMoreData():
                        #Show received data as XML.
                        try:
                            xml = self.translator.dataToXml(self.notify.data)
                            print(xml)
                            #Print received data.
                            self.printData(self.notify.value, 0)

                            #Example is sending list of push messages in first parameter.
                            if isinstance(self.notify.value, list):
                                objects = self.client.parsePushObjects(self.notify.value[0])
                                #Remove first item because it's not needed anymore.
                                objects.pop(0)
                                Valueindex = 1
                                for obj, index in objects:
                                    self.client.updateValue(obj, index, self.notify.value[Valueindex])
                                    Valueindex += 1
                                    #Print value
                                    print(str(obj.objectType) + " " + obj.logicalName + " " + str(index) + ": " + str(obj.getValues()[index - 1]))
                            print("Server address:" + str(self.notify.serverAddress) + " Client Address:" + str(self.notify.clientAddress))
                        except Exception:
                            self.reply.position = 0
                            xml = self.translator.messageToXml(self.reply)
                            print(xml)
                        self.notify.clear()
                        self.reply.clear()
        except Exception as ex:
            print(ex)
            self.notify.clear()
            self.reply.clear()

    def onMediaStateChange(self, sender, e):
        """Media component sends notification, when its state changes.
        sender : The source of the event.
        e : Event arguments.
        """
        print("Media state changed. " + str(e))

    def onTrace(self, sender, e):
        """Called when the Media is sending or receiving data.

        sender : The source of the event.
        e : Event arguments.
        """
        print("trace:" + str(e))

    def onPropertyChanged(self, sender, e):
        """
        Event is raised when a property is changed on a component.

        sender : The source of the event.
        e : Event arguments.
        """
        print("Property {!r} has hanged.".format(str(e)))

if __name__ == '__main__':
    sampleclient(sys.argv)

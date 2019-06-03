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
import sys
import socket
import locale
import re
import calendar
from GXSettings import GXSettings
from GXDLMSReader import GXDLMSReader
from gurux_dlms import *
from gurux_dlms.manufacturersettings import *
from gurux_dlms.enums import *
from gurux_dlms.objects import *

class sampleclient(object):
    @classmethod
    def main(self, args):
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
            # ignore serial for now.
            # if isinstance(settings.media, serial.Serial):
            #     if settings.iec:
            #        with serial.Serial() as settings.media:
            #         settings.media.baudrate = 300
            #         settings.media.bytesize = 7
            #         settings.media.parity = 'E'
            #         settings.media.stopbits = 1
            #      else:
            #         settings.media.baudrate = 9600
            #         settings.media.bytesize = 8
            #         settings.media.parity = 'N'
            #         settings.media.stopbits = 1
            if not isinstance(settings.media, socket.socket):
                raise Exception("Unknown media type.")
            # //////////////////////////////////////
            reader = GXDLMSReader(settings.client, settings.media, settings.trace)
            if len(settings.readObjects) != 0:
                reader.initializeConnection()
                reader.getAssociationView()
                for it in settings.readObjects:
                    val = reader.read(settings.client.objects.findByLN(ObjectType.NONE, it.getKey()), it.getValue())
                    reader.showValue(it.getValue(), val)
            else:
                reader.readAll()
        except Exception as ex:
            print(ex)
        finally:
            if reader != None:
                try:
                    reader.close()
                except Exception as e:
                    print(e)
            print("Ended. Press any key to continue.")

if __name__ == '__main__':
    sampleclient.main(sys.argv)

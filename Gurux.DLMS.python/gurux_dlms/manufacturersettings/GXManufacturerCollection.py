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
import xml.etree.cElementTree as ET
import datetime
import sys
from os import listdir
from os.path import isfile, join
import os.path
from tempfile import NamedTemporaryFile
from .GXManufacturer import GXManufacturer
from .GXObisCode import GXObisCode
from .GXAuthentication import GXAuthentication
from .GXServerAddress import GXServerAddress
from .GXDLMSAttribute import GXDLMSAttribute
from .InactivityMode import InactivityMode
from .StartProtocolType import StartProtocolType
from .HDLCAddressType import HDLCAddressType
from ..enums import Authentication, DataType, ObjectType
if sys.version_info >= (3, 0):
    import urllib.request

#
class GXManufacturerCollection(list):
    #
    # * Find manufacturer settings by manufacturer id.
    #
    # @param id
    #            Manufacturer id.
    # found manufacturer or null.
    #
    def findByIdentification(self, id_):
        for it in self:
            if it.identification == id_:
                return it
        return None

    #
    # @param path
    #            Is this first run.
    # Settings directory.
    #
    @classmethod
    def isFirstRun(cls, path):
        if not os.path.isdir(path):
            os.mkdir(path)
            return True
        if not os.path.isfile(os.path.join(path, "files.xml")):
            return True
        return False

    #
    # Check if there are any updates available in Gurux www server.
    #
    # @param path
    #            Settings directory.
    # Returns true if there are any updates available.
    #
    @classmethod
    def isUpdatesAvailable(cls, path):
        if sys.version_info < (3, 0):
            return False
        # pylint: disable=broad-except
        if not os.path.isfile(os.path.join(path, "files.xml")):
            return True
        try:
            available = dict()
            for it in ET.parse(os.path.join(path, "files.xml")).iter():
                if it.tag == "File":
                    available[it.text] = datetime.datetime.strptime(it.attrib["Modified"], "%d-%m-%Y")

            path = NamedTemporaryFile()
            path.close()
            urllib.request.urlretrieve("https://www.gurux.fi/obis/files.xml", path.name)
            for it in ET.parse(path.name).iter():
                if it.tag == "File":
                    tmp = datetime.datetime.strptime(it.attrib["Modified"], "%d-%m-%Y")
                    if not it.text in available or available[it.text] != tmp:
                        return True
        except Exception as e:
            print(e)
            return True
        return False

    @classmethod
    def updateManufactureSettings(cls, directory):
        #
        # Update manufacturer settings from the Gurux www server.
        #
        # directory: Target directory.
        #
        if sys.version_info >= (3, 0):
            return
        if not os.path.isdir(directory):
            os.mkdir(directory)
            if not os.path.isdir(directory):
                return
        path = os.path.join(directory, "files.xml")
        urllib.request.urlretrieve("https://www.gurux.fi/obis/files.xml", path)
        for it in ET.parse(path).iter():
            if it.tag == "File":
                path = os.path.join(directory, it.text)
                urllib.request.urlretrieve("https://www.gurux.fi/obis/" + it.text, path)

    @classmethod
    def readManufacturerSettings(cls, manufacturers, path):
        # pylint: disable=broad-except
        manufacturers = []
        files = [f for f in listdir(path) if isfile(join(path, f))]
        if files:
            for it in files:
                if it.endswith(".obx"):
                    try:
                        manufacturers.append(cls.__parse(os.path.join(path, it)))
                    except Exception as e:
                        print(e)
                        continue

    #
    # Serialize manufacturer from the xml.
    #
    # @param in
    #            Input stream.
    # Serialized manufacturer.
    #
    @classmethod
    def __parse(cls, file):
        man = None
        authentication = None
        for it in ET.parse(file).iter():
            if it.tag == "GXManufacturer":
                man = GXManufacturer()
            elif it.tag == "GXObisCode":
                obisCode = GXObisCode()
                man.obisCodes.append(obisCode)
            elif it.tag == "GXAuthentication":
                authentication = GXAuthentication()
                man.settings.append(authentication)
            elif it.tag == "GXServerAddress":
                serveraddress = GXServerAddress()
                man.serverSettings.append(serveraddress)
            elif it.tag == "GXDLMSAttributeSettings":
                att = GXDLMSAttribute()
                obisCode.attributes.append(att)
            elif it.tag == "Identification":
                man.identification = it.text
            elif it.tag == "Name":
                man.name = it.text
            elif it.tag == "UseLN":
                man.useLogicalNameReferencing = bool(it.text)
            elif it.tag == "UseIEC47":
                man.useIEC47 = bool(it.text)
            elif it.tag == "ClientAddress":
                if authentication:
                    authentication.clientAddress = int(it.text)
            elif it.tag == "PhysicalAddress":
                if serveraddress:
                    serveraddress.physicalAddress = int(it.text)
            elif it.tag == "LogicalAddress":
                if serveraddress:
                    serveraddress.logicalAddress = int(it.text)
            elif it.tag == "Formula":
                if serveraddress:
                    serveraddress.formula = it.text
            elif it.tag == "HDLCAddress":
                if serveraddress:
                    serveraddress.HDLCAddress = (HDLCAddressType(int(it.text)))
            elif it.tag == "Selected":
                #  Old functionality.
                continue
            elif it.tag == "InactivityMode":
                man.inactivityMode = InactivityMode[it.text.upper()]
            elif it.tag == "Type":
                if authentication:
                    str_ = it.text.upper().replace("HIGH", "HIGH_")
                    if str_ == "HIGH_":
                        str_ = "HIGH"
                    authentication.type_ = Authentication[str_]
                else:
                    if it.text == "BinaryCodedDesimal":
                        att.type_ = DataType.BCD
                    elif it.text == "OctetString":
                        att.type_ = DataType.OCTET_STRING
                    else:
                        att.type_ = DataType[it.text.upper()]
            elif it.tag == "UIType":
                if it.text == "BinaryCodedDesimal":
                    att.uiType = DataType.BCD
                elif it.text == "OctetString":
                    att.uiType = DataType.OCTET_STRING
                else:
                    att.uiType = DataType[it.text.upper()]
            elif it.tag == "GXAuthentication":
                authentication = None
            elif it.tag == "LogicalName":
                obisCode.logicalName = it.text
            elif it.tag == "Description":
                obisCode.description = it.text
            elif it.tag == "ObjectType":
                obisCode.objectType = ObjectType(int(it.text))
            elif it.tag == "Interface":
                #  Old way.  ObjectType is used now.
                continue
            elif it.tag == "Index":
                att.index = int(it.text)
            elif it.tag == "StartProtocol":
                man.startProtocol = StartProtocolType[it.text]
            elif it.tag == "WebAddress":
                man.webAddress = it.text
            elif it.tag == "Info":
                man.info = it.text
        return man

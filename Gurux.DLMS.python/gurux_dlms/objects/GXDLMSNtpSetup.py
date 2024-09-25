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
from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ErrorCode
from ..internal._GXCommon import _GXCommon
from ..enums import ObjectType, DataType
from .enums.NtpAuthenticationMethod import NtpAuthenticationMethod
from ..GXByteBuffer import GXByteBuffer
# pylint: disable=too-many-instance-attributes
class GXDLMSNtpSetup(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSNtpSetup
    """

    def __init__(self, ln="0.0.25.10.0.255", sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.NTP_SETUP, ln, sn)
        self.value = None
        #Is NTP time synchronisation active.
        self.activated = False
        # NTP server address.
        self.serverAddress = None
        # UDP port related to this protocol.
        self.port = 123
         # Authentication method.
        self.authentication = NtpAuthenticationMethod.NO_SECURITY
         # Symmetric keys for authentication.
        self.keys = {}
         #Client key (NTP server public key).
        self.clientKey = None

    def getValues(self):
        return [self.logicalName,
                self.activated, self.serverAddress, self.port,
                self.authentication, self.keys, self.clientKey]

    # Synchronizes the time of the DLMS server with the NTP server.
    # client: DLMS client.
    # Returns Action bytes.
    def synchronize(self, client):
        return client.method(self, 1, 0, DataType.INT8)

    # Adds a new symmetric authentication key to authentication key array.
    # client: DLMS client.
    # id_: Authentication key Id.
    # authentication Key.
    # Returns Action bytes.
    def addAuthenticationKey(self, client, id_, key):
        bb = GXByteBuffer()
        bb.setUInt8(DataType.STRUCTURE)
        bb.setUInt8(2)
        bb.setUInt8(DataType.UINT32)
        bb.setUInt32(id_)
        bb.setUInt8(DataType.OCTET_STRING)
        _GXCommon.setObjectCount(key.length, bb)
        bb.set(key)
        return client.method(self, 2, bb.array(), DataType.STRUCTURE)

    # Remove symmetric authentication key.
    # client: DLMS client.
    # id_: Authentication key Id.
    # Returns Action bytes.
    def deleteAuthenticationKey(self, client, id_):
        return client.method(self, 3, id_, DataType.INT8)

    #
    # Returns collection of attributes to read.  If attribute is static and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = []
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  Activated
        if all_ or self.canRead(2):
            attributes.append(2)
        # ServerAddress
        if all_ or self.canRead(3):
            attributes.append(3)
        # Port
        if all_ or self.canRead(4):
            attributes.append(4)
        # Authentication
        if all_ or self.canRead(5):
            attributes.append(5)
        # Keys
        if all_ or self.canRead(6):
            attributes.append(6)
        # ClientKey
        if all_ or self.canRead(7):
            attributes.append(7)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 7

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 3

    def getUIDataType(self, index):
        if index == 3:
            return DataType.STRING
        #pylint:disable=super-with-arguments
        return super(GXDLMSNtpSetup, self).getUIDataType(index)

    def getDataType(self, index):
        if index == 1:
            dt = DataType.OCTET_STRING
        elif index == 2:
            dt = DataType.BOOLEAN
        elif index == 3:
            dt = DataType.OCTET_STRING
        elif index == 4:
            dt = DataType.UINT16
        elif index == 5:
            dt = DataType.ENUM
        elif index == 6:
            dt = DataType.ARRAY
        elif index == 7:
            dt = DataType.OCTET_STRING
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return dt


    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.activated
        elif e.index == 3:
            ret = self.serverAddress
        elif e.index == 4:
            ret = self.port
        elif e.index == 5:
            ret = self.authentication
        elif e.index == 6:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.ARRAY)
            #Add count
            _GXCommon.setObjectCount(len(self.keys), bb)
            for it in self.keys:
                bb.setUInt8(DataType.STRUCTURE)
                #Count
                bb.setUInt8(2)
                bb.setUInt8(DataType.UINT32)
                bb.setUInt32(it.key)
                bb.setUInt8(DataType.OCTET_STRING)
                _GXCommon.setObjectCount(len(it.value), bb)
                bb.set(it.value)
            ret = bb.array()
        elif e.index == 7:
            ret = self.clientKey
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
            ret = None
        return ret

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.activated = e.value
        elif e.index == 3:
            if isinstance(e.value, bytearray):
                self.serverAddress = str(e.value)
            elif isinstance(e.value, str):
                self.serverAddress = e.value
            else:
                self.serverAddress = None
        elif e.index == 4:
            self.port = e.value
        elif e.index == 5:
            self.authentication = NtpAuthenticationMethod(e.value)
        elif e.index == 6:
            self.keys.clear()
            if e.value:
                for it in e.value:
                    self.keys[it[0]] = it[1]
        elif e.index == 7:
            self.clientKey = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.activated = reader.readElementContentAsInt("Activated", 1) != 0
        self.serverAddress = reader.readElementContentAsString("ServerAddress", None)
        self.port = reader.readElementContentAsInt("Port", 0)
        self.authentication = NtpAuthenticationMethod(reader.readElementContentAsInt("Authentication", 0))
        self.keys.clear()
        if reader.isStartElement("Keys", True):
            while reader.isStartElement("Item", True):
                id_ = reader.readElementContentAsLong("ID")
                key = GXByteBuffer.hexToBytes(reader.readElementContentAsString("Key"))
                self.keys[id_] = key
        self.clientKey = GXByteBuffer.hexToBytes(reader.readElementContentAsString("ClientKey", None))

    def save(self, writer):
        writer.writeElementString("Activated", self.activated)
        writer.writeElementString("ServerAddress", self.serverAddress)
        writer.writeElementString("Port", self.port)
        writer.writeElementString("Authentication", int(self.authentication))
        writer.writeStartElement("Keys")
        for it in self.keys:
            writer.writeStartElement("Item")
            writer.writeElementString("ID", str(it.key))
            writer.writeElementString("Key", GXByteBuffer.hex(it.value, False))
            writer.writeEndElement()
        writer.writeEndElement()
        #Keys
        writer.writeElementString("ClientKey", GXByteBuffer.hex(self.clientKey, False))

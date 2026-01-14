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
#  Gurux Device Framework is Open Source software you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http:#www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http:#www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
from gurux_dlms.objects import GXDLMSData
from ..enums import ObjectType
from ..internal._GXCommon import _GXCommon
from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ErrorCode
from ..enums.DataType import DataType
from .enums.ProtectionMode import ProtectionMode
from .enums.ProtectionStatus import ProtectionStatus
from ..internal._GXLocalizer import _GXLocalizer


# pylint: disable=too-many-instance-attributes too-many-public-methods
class GXDLMSCommunicationPortProtection(GXDLMSObject, IGXDLMSBase):
    """
    Represents a DLMS/COSEM Communication Port Protection object that manages access control and lockout mechanisms
    for a communication port based on failed authentication attempts.


    This class provides configuration and status information for communication port protection,
    including lockout timing, allowed failed attempts, and the current protection status. It is typically used in
    metering or device management scenarios to prevent unauthorized access by disabling the port after a
    configurable number of failed attempts. The protection behavior can be customized using properties such as
    ProtectionMode, AllowedFailedAttempts, and SteepnessFactor. The associated port is referenced via the Port
    property.


    Online help:
    https://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSCommunicationPortProtection
    """

    __protectionMode = ProtectionMode.LOCKED_ON_FAILED_ATTEMPTS
    __allowedFailedAttempts = None
    __initialLockoutTime = None
    __steepnessFactor = 1
    __maxLockoutTime = None
    __port = None
    __protectionStatus = ProtectionStatus.UNLOCKED
    __failedAttempts = None
    __cumulativeFailedAttempts = None

    def invoke(self, settings, e):
        """See IGXDLMSBase.invoke."""
        if e.index == 1:
            self.__failedAttempts = 0
            if self.__protectionMode == ProtectionMode.LOCKED_ON_FAILED_ATTEMPTS:
                self.__protectionStatus = ProtectionStatus.UNLOCKED
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def getAttributeIndexToRead(self, all_):
        """See IGXDLMSBase.getAttributeIndexToRead."""
        attributes = []
        # LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        # ProtectionMode
        if all_ or self.canRead(2):
            attributes.append(2)
        # AllowedFailedAttempts
        if all_ or self.canRead(3):
            attributes.append(3)
        # InitialLockoutTime
        if all_ or self.canRead(4):
            attributes.append(4)
        # SteepnessFactor
        if all_ or self.canRead(5):
            attributes.append(5)
        # MaxLockoutTime
        if all_ or self.canRead(6):
            attributes.append(6)
        # Port
        if all_ or self.canRead(7):
            attributes.append(7)
        # ProtectionStatus
        if all_ or self.canRead(8):
            attributes.append(8)
        # FailedAttempts
        if all_ or self.canRead(9):
            attributes.append(9)
        # CumulativeFailedAttempts
        if all_ or self.canRead(10):
            attributes.append(10)
        return attributes

    def getNames(self):
        """See IGXDLMSBase.getNames."""
        return (
            _GXLocalizer.gettext("Logical name"),
            _GXLocalizer.gettext("Protection mode"),
            _GXLocalizer.gettext("Allowed failed attempts"),
            _GXLocalizer.gettext("Initial lockout time"),
            _GXLocalizer.gettext("Steepness factor"),
            _GXLocalizer.gettext("Max lockout time"),
            _GXLocalizer.gettext("Port"),
            _GXLocalizer.gettext("Protection status"),
            _GXLocalizer.gettext("Failed attempts"),
            _GXLocalizer.gettext("Cumulative failed attempts"),
        )

    def getMethodNames(self):
        """See IGXDLMSBase.getMethodNames."""
        return "Reset"

    def getAttributeCount(self):
        """See IGXDLMSBase.getAttributeCount."""
        return 10

    def getMethodCount(self):
        """See IGXDLMSBase.getMethodCount."""
        return 1

    def getValue(self, settings, e):
        """See IGXDLMSBase.getValue."""
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.__protectionMode
        elif e.index == 3:
            ret = self.__allowedFailedAttempts
        elif e.index == 4:
            ret = self.__initialLockoutTime
        elif e.index == 5:
            ret = self.__steepnessFactor
        elif e.index == 6:
            ret = self.__maxLockoutTime
        elif e.index == 7:
            if self.__port is None:
                ret = _GXCommon.logicalNameToBytes(None)
            else:
                ret = _GXCommon.logicalNameToBytes(self.__port.logicalName)
        elif e.index == 8:
            ret = self.__protectionStatus
        elif e.index == 9:
            ret = self.__failedAttempts
        elif e.index == 10:
            ret = self.__cumulativeFailedAttempts
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
            ret = None
        return ret

    def setValue(self, settings, e):
        """See IGXDLMSBase.setValue."""
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.__protectionMode = ProtectionMode(int(e.value) & 0xFF)
        elif e.index == 3:
            self.__allowedFailedAttempts = int(e.value) & 0xFFFF
        elif e.index == 4:
            self.__initialLockoutTime = int(e.value) & 0xFFFFFFFF
        elif e.index == 5:
            self.__steepnessFactor = int(e.value) & 0xFF
        elif e.index == 6:
            self.__maxLockoutTime = int(e.value) & 0xFFFFFFFF
        elif e.index == 7:
            ln = _GXCommon.toLogicalName(e.value)
            self.__port = settings.objects.findByLN(ObjectType.NONE, ln)
        elif e.index == 8:
            self.__protectionStatus = ProtectionStatus(int(e.value) & 0xFF)
        elif e.index == 9:
            self.__failedAttempts = int(e.value) & 0xFFFFFFFF
        elif e.index == 10:
            self.__cumulativeFailedAttempts = int(e.value) & 0xFFFFFFFF
        else:
            e.Error = ErrorCode.READ_WRITE_DENIED

    @property
    def protectionMode(self):
        """
        Controls the protection mode.
        """
        return self.__protectionMode

    @protectionMode.setter
    def protectionMode(self, value):
        self.__protectionMode = value

    @property
    def allowedFailedAttempts(self):
        """
        Number of allowed failed communication attempts before port is disabled.
        """
        return self.__allowedFailedAttempts

    @allowedFailedAttempts.setter
    def allowedFailedAttempts(self, value):
        self.__allowedFailedAttempts = value

    @property
    def initialLockoutTime(self):
        """
        The lockout time.
        """
        return self.__initialLockoutTime

    @initialLockoutTime.setter
    def initialLockoutTime(self, value):
        self.__initialLockoutTime = value

    @property
    def steepnessFactor(self):
        """
        Holds a factor that controls how the lockout time is increased with
         each failed attempt.
        """
        return self.__steepnessFactor

    @steepnessFactor.setter
    def steepnessFactor(self, value):
        self.__steepnessFactor = value

    @property
    def maxLockoutTime(self):
        """
        The lockout time.
        """
        return self.__maxLockoutTime

    @maxLockoutTime.setter
    def maxLockoutTime(self, value):
        self.__maxLockoutTime = value

    @property
    def port(self):
        """
        The communication port being protected
        """
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value

    @property
    def protectionStatus(self):
        """
        Current protection status.
        """
        return self.__protectionStatus

    @protectionStatus.setter
    def protectionStatus(self, value):
        self.__protectionStatus = value

    @property
    def failedAttempts(self):
        """
        Failed attempts.
        """
        return self.__failedAttempts

    @failedAttempts.setter
    def failedAttempts(self, value):
        self.__failedAttempts = value

    @property
    def cumulativeFailedAttempts(self):
        """
        Total failed attempts.
        """
        return self.__cumulativeFailedAttempts

    @cumulativeFailedAttempts.setter
    def cumulativeFailedAttempts(self, value):
        self.__cumulativeFailedAttempts = value

    def reset(self, client):
        """
        Resets failed attempts and current lockout time to zero.
        Protection status is set to unlocked.
        """
        return client.method(self, 1, 0)

    def getValues(self):
        """See IGXDLMSBase.getValues."""
        return (
            self.logicalName,
            self.protectionMode,
            self.allowedFailedAttempts,
            self.initialLockoutTime,
            self.steepnessFactor,
            self.maxLockoutTime,
            self.port,
            self.protectionStatus,
            self.failedAttempts,
            self.cumulativeFailedAttempts,
        )

    def getDataType(self, index):
        """See IGXDLMSBase.getDataType."""
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.ENUM
        elif index == 3:
            ret = DataType.UINT16
        elif index == 4:
            ret = DataType.UINT32
        elif index == 5:
            ret = DataType.UINT8
        elif index == 6:
            ret = DataType.UINT32
        elif index == 7:
            ret = DataType.OCTET_STRING
        elif index == 8:
            ret = DataType.ENUM
        elif index == 9:
            ret = DataType.UINT32
        elif index == 10:
            ret = DataType.UINT32
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret

    def __init__(self, ln=None, sn=0):
        """
        Constructor.

        ln : Logical Name of the object.
        sn : Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.COMMUNICATION_PORT_PROTECTION, ln, sn)

    def load(self, reader):
        """See IGXDLMSBase.load."""
        self.__protectionMode = ProtectionMode(
            reader.readElementContentAsInt("ProtectionMode")
        )
        self.__allowedFailedAttempts = reader.readElementContentAsInt(
            "AllowedFailedAttempts"
        )
        self.__initialLockoutTime = reader.readElementContentAsLong(
            "InitialLockoutTime"
        )
        self.__steepnessFactor = reader.readElementContentAsInt("SteepnessFactor")
        self.__maxLockoutTime = reader.readElementContentAsLong("MaxLockoutTime")
        port = reader.readElementContentAsString("Port")
        if not port:
            self.__port = None
        else:
            self.__port = reader.objects.findByLN(ObjectType.NONE, port)
            # Save port object for data object if it's not loaded yet.
            if self.__port is None:
                self.__port = GXDLMSClient.createObject(ObjectType.DATA)
                self.__port.Version = 0
                self.__port.LogicalName = port

        self.__protectionStatus = ProtectionStatus(
            reader.readElementContentAsInt("ProtectionStatus")
        )
        self.__failedAttempts = reader.readElementContentAsLong("FailedAttempts")
        self.__cumulativeFailedAttempts = reader.readElementContentAsLong(
            "CumulativeFailedAttempts"
        )

    def save(self, writer):
        """See IGXDLMSBase.save."""
        writer.writeElementString("ProtectionMode", int(self.__protectionMode))
        writer.writeElementString("AllowedFailedAttempts", self.__allowedFailedAttempts)
        writer.writeElementString("InitialLockoutTime", self.__initialLockoutTime)
        writer.writeElementString("SteepnessFactor", self.__steepnessFactor)
        writer.writeElementString("MaxLockoutTime", self.__maxLockoutTime)
        if self.__port is None:
            writer.writeElementString("Port", "", 7)
        else:
            writer.writeElementString("Port", self.__port.LogicalName, 7)

        writer.writeElementString("ProtectionStatus", int(self.__protectionStatus), 8)
        writer.writeElementString("FailedAttempts", self.__failedAttempts, 9)
        writer.writeElementString(
            "CumulativeFailedAttempts", self.__cumulativeFailedAttempts, 10
        )

    def postLoad(self, reader):
        """See IGXDLMSBase.postLoad."""
        if isinstance(self.__port, GXDLMSData):
            self.__port = reader.objects.findByLN(
                ObjectType.NONE, self.__port.LogicalName
            )

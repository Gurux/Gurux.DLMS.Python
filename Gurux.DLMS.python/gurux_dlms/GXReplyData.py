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
from .GXByteBuffer import GXByteBuffer
from .enums import DataType, RequestTypes, Command
from .GXDLMSException import GXDLMSException

# pylint: disable=bad-option-value,old-style-class,too-few-public-methods,too-many-instance-attributes
class GXReplyData:
    #
    #      Constructor.
    #
    #      @param more
    #                 Is more data available.
    #      @param cmd
    #                 Received command.
    #      @param buff
    #                 Received data.
    #      @param forComplete
    #                 Is frame complete.
    #      @param err
    #                 Received error ID.
    # pylint: disable=too-many-arguments
    def __init__(self, more=RequestTypes.NONE, cmd=Command.NONE, buff=None, forComplete=False, err=0):
        # Is more data available.
        self.moreData = more
        # Received command.
        self.command = cmd
        # Received data.
        self.data = buff
        if not self.data:
            self.data = GXByteBuffer()
        # Is frame complete.
        self.complete = forComplete
        # Received error.
        self.error = err
        self.value = None
        # Is received frame echo.
        self.echo = False
        # Received command type.
        self.commandType = 0
        # HDLC frame ID.
        self.frameId = 0
        # Read value.
        self.dataValue = None
        # Expected count of element in the array.
        self.totalCount = 0
        # Last read position.  This is used in peek to solve how far data
        # is read.
        self.readPosition = 0
        # Packet length.
        self.packetLength = 0
        # Try get value.
        self.peek = False
        # Cipher index is position where data is decrypted.
        self.cipherIndex = 0
        # Data notification date time.
        self.time = None
        # XML settings.
        self.xml = None
        # Invoke ID.
        self.invokeId = 0
        # GBT block number.
        self.blockNumber = 0
        # GBT block number ACK.
        self.blockNumberAck = 0
        # Is GBT streaming in use.
        self.streaming = False
        # GBT Window size.  This is for internal use.
        self.windowSize = 0
        # Client address of the notification message.  Notification
        # message sets
        # this.
        self.clientAddress = 0
        # Server address of the notification message.  Notification
        # message sets
        # this.
        self.serverAddress = 0
        # Gateway information.
        self.gateway = None
        # Data type.
        self.valueType = DataType.NONE

    def clear(self):
        """"
        Reset data values to default.
        """
        self.moreData = RequestTypes.NONE
        self.command = Command.NONE
        self.commandType = 0
        self.data.capacity = 0
        self.complete = False
        self.error = 0
        self.totalCount = 0
        self.dataValue = None
        self.readPosition = 0
        self.packetLength = 0
        self.valueType = DataType.NONE
        self.cipherIndex = 0
        self.time = None
        if self.xml:
            self.xml.xml = ""
        self.invokeId = 0
        self.value = None

    def isMoreData(self):
        """
        Is more data available.
        """
        return self.moreData != RequestTypes.NONE and self.error == 0

    #
    # Is notify message.
    #
    def isNotify(self):
        return self.command == Command.EVENT_NOTIFICATION or self.command == Command.DATA_NOTIFICATION or self.command == Command.INFORMATION_REPORT

    #
    #      Is frame complete.
    #
    # Returns true if frame is complete or false if bytes is
    #      missing.
    #
    def isComplete(self):
        return self.complete

    #
    #      Get Received error.  Value is zero if no error has occurred.
    #
    # Received error.
    #
    def getError(self):
        return self.error

    def getErrorMessage(self):
        return GXDLMSException.getDescription(self.error)

    #
    #      Get total count of element in the array.  If this method is used
    #      peek must
    #      be set true.
    #
    # Count of element in the array.
    #      @see #setPeek
    #      @see #getCount
    #
    def getTotalCount(self):
        return self.totalCount

    #
    #      Get count of read elements.  If this method is used peek must be set
    #      true.
    #
    # Count of read elements.
    #      @see #setPeek
    #      @see #getTotalCount
    #
    def getCount(self):
        if isinstance(self.dataValue, list):
            return len(self.dataValue)
        return 0

    #
    # Is GBT streaming.
    #
    def isStreaming(self):
        return self.streaming and (self.blockNumberAck * self.windowSize) + 1 > self.blockNumber

    def __str__(self):
        if self.xml:
            return self.xml
        if self.data is None:
            return ""
        return str(self.data)

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
#  More information of Gurux products: http:#www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http:#www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
class GXDLMSBroadcastLogTable:
    '''
    Broadcast log table
    '''

    __sourceAddress = None
    "Source address of a broadcast packet."

    __sequenceNumber = 0
    "The sequence number contained in the BC0 header"

    __validTime = None
    "Remaining time in minutes until when this entry in the broadcast log table is considered valid."

    @property
    def sourceAddress(self):
        '''
        Source address of a broadcast packet.
        '''
        return self.__sourceAddress

    @sourceAddress.setter
    def sourceAddress(self, value):
        self.__sourceAddress = value
    @property
    def sequenceNumber(self):
        '''
        The sequence number contained in the BC0 header
        '''
        return self.__sequenceNumber

    @sequenceNumber.setter
    def sequenceNumber(self, value):
        self.__sequenceNumber = value
    @property
    def validTime(self):
        '''
        Remaining time in minutes until when this entry in the broadcast log table is considered valid.
        '''
        return self.__validTime

    @validTime.setter
    def validTime(self, value):
        self.__validTime = value

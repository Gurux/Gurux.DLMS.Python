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
class GXDLMSContextInformationTable:
    '''
    Contains the context information associated to each CID extension field.
    '''

    __cID = ""
    "Corresponds to the 4-bit context information used for source and destination addresses (SCI, DCI)."

    __context = bytearray()
    "Context."

    __compression = None
    "Indicates if the context is valid for use in compression."

    __validLifetime = None
    "Remaining time in minutes during which the context information table is considered valid. It is updated upon reception of the advertised context."

    @property
    def cID(self):
        '''
        Corresponds to the 4-bit context information used for source and destination addresses (SCI, DCI).
        '''
        return self.__cID

    @cID.setter
    def cID(self, value):
        self.__cID = value
    @property
    def context(self):
        '''
        Context.
        '''
        return self.__context

    @context.setter
    def context(self, value):
        self.__context = value
    @property
    def compression(self):
        '''
        Indicates if the context is valid for use in compression.
        '''
        return self.__compression

    @compression.setter
    def compression(self, value):
        self.__compression = value
    @property
    def validLifetime(self):
        '''
        Remaining time in minutes during which the context information table is considered valid. It is updated upon reception of the advertised context.
        '''
        return self.__validLifetime

    @validLifetime.setter
    def validLifetime(self, value):
        self.__validLifetime = value

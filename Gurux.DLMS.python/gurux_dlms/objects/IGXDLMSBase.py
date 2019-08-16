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
from abc import ABCMeta, abstractmethod

ABC = ABCMeta('ABC', (object,), {'__slots__': ()})

class IGXDLMSBase(ABC):

    # Returns collection of attributes to read.  If attribute is static and
    # already read or device is returned HW error it is not returned.
    #
    # @param all_
    #            All are attributes get.
    # @return Collection of attributes to read.
    @abstractmethod
    def getAttributeIndexToRead(self, all_):
        """ This is interface method """

    # @return Amount of attributes.
    @abstractmethod
    def getAttributeCount(self):
        """ This is interface method """

    # @return Amount of methods.
    @abstractmethod
    def getMethodCount(self):
        """ This is interface method """

    # Returns value of given attribute.
    #
    # @param settings
    #            DLMS settings.
    # @param e
    #            Get parameter.
    # @return Returned value.
    @abstractmethod
    def getValue(self, settings, e):
        """ This is interface method """

    # Set value of given attribute.
    #
    # @param settings
    #            DLMS settings.
    # @param e
    #            Set parameter.
    @abstractmethod
    def setValue(self, settings, e):
        """ This is interface method """

    # Server calls invoke method.
    #
    # @param settings
    #            Server settings.
    # @param e
    #            Invoke parameter.
    # @return Reply for the client.
    @abstractmethod
    def invoke(self, settings, e):
        """ This is interface method """

    # Load object content from XML.
    #
    # @param reader
    #            XML reader.
    @abstractmethod
    def load(self, reader):
        """ This is interface method """

    # Save object content to XML.
    #
    # @param writer
    #            XML writer.
    @abstractmethod
    def save(self, writer):
        """ This is interface method """

    # Handle actions after Load.
    #
    # @param reader
    #            XML reader.
    def postLoad(self, reader):
        """ This is interface method """

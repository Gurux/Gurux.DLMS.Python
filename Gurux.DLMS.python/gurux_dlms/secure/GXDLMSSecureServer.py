#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename:        $HeadURL$
#
#  Version:         $Revision$,
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
from ..GXDLMSServer import GXDLMSServer
from ..GXCiphering import GXCiphering

class GXDLMSSecureServer(GXDLMSServer):
    __metaclass__ = ABCMeta
    """
    Implements secured DLMS server.
    """

    def __init__(self, association, interfaceType):
        """
        # Constructor.
        #
        # association: Association logical name.
        # type: Interface type.
        """
        #pylint:disable=super-with-arguments
        super(GXDLMSSecureServer, self).__init__(association, interfaceType)
        self.settings.ciphering = GXCiphering("ABCDEFGH".encode())
        self.kek = None

    def getCiphering(self):
        return self.settings.ciphering

    def getKek(self):
        return self.settings.kek

    def setKek(self, value):
        self.settings.kek = value

    kek = property(getKek, setKek, None, "Key Encrypting Key, also known as Master key.")

     #
    # Check is data sent to this server.
    #
    # @param serverAddress
    #            Server address.
    # @param clientAddress
    #            Client address.
    # True, if data is sent to this server.
    #
    @abstractmethod
    def isTarget(self, serverAddress, clientAddress):
        raise ValueError("isTarget is called.")

    #
    # Check whether the authentication and password are correct.
    #
    # @param authentication
    #            Authentication level.
    # @param password
    #            Password.
    # Source diagnostic.
    #
    @abstractmethod
    def onValidateAuthentication(self, authentication, password):
        raise ValueError("isTarget is called.")

    #
    # Get selected value(s).  This is called when example profile generic
    # request current value.
    #
    # @param args
    #            Value event arguments.
    #
    @abstractmethod
    def onPreGet(self, args):
        raise ValueError("isTarget is called.")

    #
    # Get selected value(s).  This is called when example profile generic
    # request current value.
    #
    # @param args
    #            Value event arguments.
    #
    @abstractmethod
    def onPostGet(self, args):
        raise ValueError("isTarget is called.")

    #
    # Find object.
    #
    # @param objectType
    #            Object type.
    # @param sn
    #            Short Name.  In Logical name referencing this is not used.
    # @param ln
    #            Logical Name.  In Short Name referencing this is not used.
    # Found object or null if object is not found.
    #
    @abstractmethod
    def onFindObject(self, objectType, sn, ln):
        raise ValueError("isTarget is called.")

    #
    # Called before read is executed.
    #
    # @param args
    #            Handled read requests.
    #
    @abstractmethod
    def onPreRead(self, args):
        raise ValueError("isTarget is called.")

    #
    # Called after read is executed.
    #
    # @param args
    #            Handled read requests.
    #
    @abstractmethod
    def onPostRead(self, args):
        raise ValueError("isTarget is called.")

    #
    # Called before write is executed..
    #
    # @param args
    #            Handled write requests.
    #
    @abstractmethod
    def onPreWrite(self, args):
        raise ValueError("isTarget is called.")

    #
    # Called after write is executed.
    #
    # @param args
    #            Handled write requests.
    #
    @abstractmethod
    def onPostWrite(self, args):
        raise ValueError("isTarget is called.")

    #
    # Accepted connection is made for the server.  All initialization is done
    # here.
    #
    # @param connectionInfo
    #            Connection info.
    #
    @abstractmethod
    def onConnected(self, connectionInfo):
        raise ValueError("isTarget is called.")

    #
    # Client has try to made invalid connection.  Password is incorrect.
    #
    # @param connectionInfo
    #            Connection info.
    #
    @abstractmethod
    def onInvalidConnection(self, connectionInfo):
        raise ValueError("isTarget is called.")

    #
    # Server has close the connection.  All clean up is made here.
    #
    # @param connectionInfo
    #            Connection info.
    #
    @abstractmethod
    def onDisconnected(self, connectionInfo):
        raise ValueError("isTarget is called.")

    #
    # Get attribute access mode.
    #
    # @param arg
    #            Value event argument.
    # Access mode.
    #
    @abstractmethod
    def onGetAttributeAccess(self, arg):
        raise ValueError("isTarget is called.")

    #
    # Get method access mode.
    #
    # @param arg
    #            Value event argument.
    # Method access mode.
    #
    @abstractmethod
    def onGetMethodAccess(self, arg):
        raise ValueError("onGetMethodAccess is called.")

    #
    # Called before action is executed.
    #
    # @param args
    #            Handled action requests.
    #
    @abstractmethod
    def onPreAction(self, args):
        raise ValueError("onPreAction is called.")

    #
    # Called after action is executed.
    #
    # @param args
    #            Handled action requests.
    #
    @abstractmethod
    def onPostAction(self, args):
        raise ValueError("onPostAction is called.")

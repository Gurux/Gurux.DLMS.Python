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
import abc

ABC = abc.ABCMeta("ABC", (object,), {"__slots__": ()})

class IGXCryptoNotifier(ABC):
    """
    The server uses this interface to notify client connections.
    """

    __metaclass__ = abc.ABCMeta
    """Network Server component will notify events throught this interface."""

    @abc.abstractmethod
    def onPduEventHandler(self, sender, complete, data):
        """Notifies un-ciphered PDU..

        sender : The source of the event.
        complete : Is all data received.
        data : Un-ciphered PDU.
        """

    @abc.abstractmethod
    def onKey(self, sender, args):
        """Called when the public or private key is needed 
        and it's unknown.

        sender : The source of the event.
        args : Event arguments.
        """

    @abc.abstractmethod
    def onCrypto(self, sender, args):
        """Called to encrypt or decrypt the data using 
        external Hardware Security Module.

        sender : The source of the event.
        args : Event arguments.
        """

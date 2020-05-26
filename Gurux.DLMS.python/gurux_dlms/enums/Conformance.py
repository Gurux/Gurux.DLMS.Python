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
from ..GXIntFlag import GXIntFlag

class Conformance(GXIntFlag):
    """Enumerates all conformance bits.
    Client is using conformance to tell what kind of services it's interested
    and server is using conformance to tell what kind of services it can offer.

    All services enumerated here are not necessary supported by the client or the
    server.
    https://www.gurux.fi/Gurux.DLMS.Conformance
    """
    #pylint: disable=too-few-public-methods

    #None conformace is reserved for internal use.
    NONE = 0x0

    #Reserved zero conformance bit.
    #Not used at the moment.
    RESERVED_ZERO = 0x1

    #Is General Protection supported by the meter or is client interested from
    #General Protection.
    #General Protection is used to secure connection between client and the
    #meter using Symmetric or ASymmetric ciphering or General Signing.
    GENERAL_PROTECTION = 0x2

    #General Block Transfer mechanism is used to transport data that size is
    #longer than PDU size.
    GENERAL_BLOCK_TRANSFER = 0x4

    #Is Read supported by the meter or is client interested from Read.
    #Read is used with Short Name Referencing to read value from the meter.
    READ = 0x8

    #Is Write supported by the meter or is client interested from write data
    #to the meter.
    #Write is used with Short Name Referencing to write value to the meter.
    WRITE = 0x10

    #Is Unconfirmed Write supported by the meter or is client interested from
    #write unconfirmed data to the meter.
    #Unconfirmed Write is used with Short Name Referencing to write value
    #without confirmation from success to the meter.
    UN_CONFIRMED_WRITE = 0x20

    #Reserved six conformance bit.
    #Not used at the moment.
    RESERVED_SIX = 0x40

    #Reserved seven conformance bit.
    #Not used at the moment.
    RESERVED_SEVEN = 0x80

    #Is Attribute Set supported by the meter or is client interested from
    #write data with Attribute 0 to the meter.
    #Attribute 0 Set means that all COSEM object's attributes can be write
    #with one message.
    ATTRIBUTE_0_SUPPORTED_WITH_SET = 0x100

    #Is Priority Management supported by the meter or is client interested
    #from Priority Management.
    #Priority Management is used by Logical Name referencing to handle urgent
    #messages.
    PRIORITY_MGMT_SUPPORTED = 0x200

    #Is Attribute get supported by the meter or is client interested from read
    #data with Attribute 0 from the meter.
    #Attribute 0 Get means that all COSEM object's attributes can be read with
    #one message.
    ATTRIBUTE_0_SUPPORTED_WITH_GET = 0x400

    #Is Block transfer supported by the meter or is client interested from
    #read data with blocks from the meter.
    #Read Block transfer is used to read data from the meter that is not fit
    #to one PDU.  Example reading historical data might take more than one PDU
    #and then block transfer is used.
    BLOCK_TRANSFER_WITH_GET_OR_READ = 0x800

    #Is Block transfer supported by the meter or is client interested from
    #writing data with blocks to the meter.
    #Write Block transfer is used to write data from the meter that is not fit
    #to one PDU.  Example updating image =Firmware) might take more than one
    #PDU and then block transfer is used.
    BLOCK_TRANSFER_WITH_SET_OR_WRITE = 0x1000

    #Is Block with action transfer supported by the meter or is client
    #interested from sending action data with blocks to the meter.
    #Action Block transfer is used to send action data from the meter that is
    #not fit to one PDU.  Example Public Key transfer might take more than one
    #PDU and then block transfer with action is used.
    BLOCK_TRANSFER_WITH_ACTION = 0x2000

    #Is multiple references supported by the meter or is client interested
    #from multiple references.
    #Multiple references is used when reading or writing several object with
    #one message.  Example ReadByList is using it.
    MULTIPLE_REFERENCES = 0x4000

    #Is Information reports supported by the meter.
    #Information reports is used with Short Name Referencing
    #
    #@see DATA_NOTIFICATION
    #@see EVENT_NOTIFICATION
    INFORMATION_REPORT = 0x8000

    #Is Data Notification supported by the meter.
    #
    #@see INFORMATION_REPORT
    #@see EVENT_NOTIFICATION
    DATA_NOTIFICATION = 0x10000

    #Is Access service supported by the meter or is client interested from
    #Access service.
    #Using Access service client can make several Read, Write or Action
    #requests with one command.
    ACCESS = 0x20000

    #Is parameterized access supported by the meter or is client interested
    #from parameterized access.
    #Parameterized access is used with Short Name Referencing example if
    #Profile Generic is read by range or entry.
    #
    #@see SELECTIVE_ACCESS
    PARAMETERIZED_ACCESS = 0x40000

    #Is Get supported by the meter or is client interested from Get.
    #Get is used with Logical Name Referencing to read value from the meter.
    GET = 0x80000

    #Is Set supported by the meter or is client interested from Set.
    #Set is used with Logical Name Referencing to write value to the meter.
    SET = 0x100000

    #Is selective access supported by the meter or is client interested from
    #selective access.
    #Selective access is used with Logical Name Referencing example if Profile
    #Generic is read by range or entry.
    #
    #@see PARAMETERIZED_ACCESS
    SELECTIVE_ACCESS = 0x200000

    #Is Event Notification supported by the meter.
    #Meter is using Event Notifications with Logical Name referencing to send
    #events for given target.  Example if power down occurred.  Note!  Client
    #do
    #not need to have connection to the server when event notification is
    #send.
    #
    EVENT_NOTIFICATION = 0x400000

    #Is actions supported by the meter or is client interested from actions.
    #
    #Actions are used example to reset historical data.
    ACTION = 0x800000

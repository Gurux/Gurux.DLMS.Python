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
from ..GXIntEnum import GXIntEnum


class ObjectType(GXIntEnum):
    """ObjectType enumerates the usable types of DLMS objects in GuruxDLMS."""

    # pylint: disable=too-few-public-methods

    # When communicating with a meter, the application may demand periodical
    # actions.  If these actions are not linked to tariffication =
    # ActivityCalendar or Schedule, use an object of type ActionSchedule =
    # 0x16.
    ACTION_SCHEDULE = 22

    # When handling tariffication structures, you can use an object of type
    # ActivityCalendar.  It determines, when to activate specified scripts to
    # perform certain activities in the meter.  The activities, simply said,
    # scheduled actions, are operations that are carried out on a specified
    # day, at a specified time.  ActivityCalendar can be used together with a
    # more general object type, Schedule, and they can even overlap.  If
    # multiple actions are timed to the same moment, the actions determined in
    # the Schedule are executed first, and then the ones determined in the
    # ActivityCalendar.  If using object type SpecialDaysTable, with
    # ActivityCalendar, simultaneous actions determined in SpecialDaysTable are
    # executed over the ones determined in ActivityCalendar.  <p /> <b>Note:
    # </b>To make sure that tariffication is correct after a power failure,
    # only the latest missed action from ActivityCalendar is executed, with a
    # delay.  In a case of power failure, if a Schedule object coexists, the
    # latest missed action from ActivityCalendar has to be executed at the
    # correct time, sequentially with actions determined in the Schedule.
    ACTIVITY_CALENDAR = 20

    # All object types are used.
    NONE = 0

    # AssociationLogicalName object type is used with meters that utilize
    # Logical Name associations within a COSEM.
    ASSOCIATION_LOGICAL_NAME = 15

    # AssociationShortName object type is used with meters that utilize Short
    # Name associations within a COSEM.
    ASSOCIATION_SHORT_NAME = 12

    # To determine auto answering settings = for data transfer between device
    # and modem = s to answer incoming calls, use AutoAnswer object.
    AUTO_ANSWER = 28

    # To determine auto connecting settings = for data transfer from the meter
    # to defined destinations, use AutoConnect = previously known as AutoDial
    # object.
    AUTO_CONNECT = 29

    # An object of type Clock is used to handle the information of a date =
    # day, month and year and/or a time = hundredths of a second, seconds,
    # minutes and hours.
    CLOCK = 8

    # An object of type Data typically stores manufacturer specific information
    # of the meter, for example configuration data and logical name.
    DATA = 1

    # An object of type DemandRegister stores a value, information of the item,
    # which the value belongs to, the status of the item, and the time of the
    # value.  DemandRegister object type enables both current, and last
    # average,
    # it supports both block, and sliding demand calculation, and it also
    # provides resetting the value average, and periodic averages.
    DEMAND_REGISTER = 5

    # MAC address of the physical device.  The name and the use of this
    # interface class has been changed from Ethernet setup to MAC address setup
    # to allow a more general use.
    MAC_ADDRESS_SETUP = 43

    # ExtendedRegister stores a value, and understands the type of the value.
    # Refer to an object of this type by its logical name, using the OBIS
    # identification code.
    EXTENDED_REGISTER = 4

    # To determine the GPRS settings, use GprsSetup object.
    GPRS_SETUP = 45

    # To determine the HDLC = High-level Data Link Control settings, use the
    # IecHdlcSetup object.
    IEC_HDLC_SETUP = 23

    # To determine the Local Port settings, use the IecLocalPortSetup object.
    IEC_LOCAL_PORT_SETUP = 19

    # To determine the Twisted Pair settings, use the IecTwistedPairSetup
    # object.
    IEC_TWISTED_PAIR_SETUP = 24

    # To determine the IP 4 settings, use the Ip4Setup object.
    IP4_SETUP = 42

    GSM_DIAGNOSTIC = 47

    # To determine the IP 6 settings, use the Ip6Setup object.
    IP6_SETUP = 48

    # To determine the M-BUS settings, use the MbusSetup object.
    MBUS_SLAVE_PORT_SETUP = 25

    # To determine modem settings, use ModemConfiguration object.
    MODEM_CONFIGURATION = 27

    # To determine PPP = Point-to-Point Protocol settings, use the PppSetup
    # object.
    PPP_SETUP = 44

    # ProfileGeneric determines a general way of gathering values from a
    # profile.  The data is retrieved either by a period of time, or by an
    # occuring event.  When gathering values from a profile, you need to
    # understand the concept of the profile buffer, in which the profile data
    # is stored.  The buffer may be sorted by a register, or by a clock, within
    # the profile, or the data can be just piled in it, in order: last in,
    # first out.  You can retrieve a part of the buffer, within a certain range
    # of values, or by a range of entry numbers.  You can also determine
    # objects, whose values are to be retained.  To determine, what to
    # retrieve,
    # and what to retain, you need to assign the objects to the profile.  You
    # can use static assignments, as all entries in a buffer are alike = same
    # size, same structure.  <p /> <b>Note: </b>When you modify any assignment,
    # the buffer of the corresponding profile is cleared, and all other
    # profiles, using the modified one, will be cleared too.  This is to make
    # sure that their entries stay alike by size and structure.
    PROFILE_GENERIC = 7

    # Register stores a value, and understands the type of the value.  Refer to
    # an object of this type by its logical name, using the OBIS identification
    # code.
    REGISTER = 3

    # When handling tariffication structures, you can use RegisterActivation to
    # determine, what objects to enable, when activating a certain activation
    # mask.  The objects, assigned to the register, but not determined in the
    # mask, are disabled.  <p /> <b>Note: </b>If an object is not assigned to
    # any register, it is, by default, enabled.
    REGISTER_ACTIVATION = 6

    # RegisterMonitor allows you to determine scripts to execute, when a
    # register value crosses a specified threshold.  To use RegisterMonitor,
    # also ScriptTable needs to be instantiated in the same logical device.
    REGISTER_MONITOR = 21

    # Instances of the Disconnect control IC manage an internal or external
    # disconnect unit of the meter.
    DISCONNECT_CONTROL = 70

    LIMITER = 71

    MBUS_CLIENT = 72

    PUSH_SETUP = 40

    COMPACT_DATA = 62

    PARAMETER_MONITOR = 65
    WIRELESS_MODE_Q_CHANNEL = 73
    MBUS_MASTER_PORT_SETUP = 74

    #
    # Addresses that are provided by the base node during the opening of the
    # convergence layer.
    #
    LLC_SSCS_SETUP = 80

    #
    # Counters related to the physical layers exchanges.
    #
    PRIME_NB_OFDM_PLC_PHYSICAL_LAYER_COUNTERS = 81

    #
    # A necessary parameters to set up and manage the PRIME NB OFDM PLC MAC
    # layer.
    #
    PRIME_NB_OFDM_PLC_MAC_SETUP = 82

    #
    # Functional behaviour of MAC.
    #
    PRIME_NB_OFDM_PLC_MAC_FUNCTIONAL_PARAMETERS = 83

    #
    # Statistical information on the operation of the MAC layer for management
    # purposes.
    #
    PRIME_NB_OFDM_PLC_MAC_COUNTERS = 84

    #
    # Parameters related to the management of the devices connected to the
    # network.
    #
    PRIME_NB_OFDM_PLC_MAC_NETWORK_ADMINISTRATION_DATA = 85

    #
    # Identification information related to administration and maintenance of
    # PRIME NB OFDM PLC devices.
    #
    PRIME_NB_OFDM_PLC_APPLICATIONS_IDENTIFICATION = 86

    # RegisterTable stores identical attributes of objects, in a selected
    # collection of objects.  All the objects in the collection need to be of
    # the same type.  Also, the value in value groups A to D and F in their
    # logical name = OBIS identification code needs to be identical.  <p />
    # Clause 5 determines the possible values in value group E, as a table,
    # where header = the common part, and each cell = a possible E value, of
    # the OBIS code.

    REGISTER_TABLE = 61
    # NTP Setup is used for time synchronisation.
    NTP_SETUP = 100

    #
    # Configure a ZigBee PRO device with information necessary to create or
    # join the network.
    ZIG_BEE_SAS_STARTUP = 101

    #
    # Configure the behavior of a ZigBee PRO device on joining or loss of
    # connection to the network.
    ZIG_BEE_SAS_JOIN = 102

    #
    # Configure the fragmentation feature of ZigBee PRO transport layer.
    ZIG_BEE_SAS_APS_FRAGMENTATION = 103
    ZIG_BEE_NETWORK_CONTROL = 104

    DATA_PROTECTION = 30

    ACCOUNT = 111

    CREDIT = 112

    CHARGE = 113

    TOKEN_GATEWAY = 115

    IEC_6205541_Attributes = 116

    # Allow managing attributes of type array of other interface objects.
    ARRAY_MANAGER = 123

    # SapAssigment stores information of assignment of the logical devices to
    # their SAP = Service Access Points.
    SAP_ASSIGNMENT = 17

    # Instances of the Image transfer IC model the mechanism of transferring
    # binary files, called firmware Images to COSEM servers.
    IMAGE_TRANSFER = 18

    # To handle time and date driven actions, use Schedule, with an object of
    # type SpecialDaysTable.
    SCHEDULE = 10

    # To trigger a set of actions with an execute method, use object type
    # ScriptTable.  Each table entry = script includes a unique identifier, and
    # a set of action specifications, which either execute a method, or modify
    # the object attributes, within the logical device.  The script can be
    # triggered by other objects = within the same logical device, or from the
    # outside.
    SCRIPT_TABLE = 9

    # To determine the SMTP protocol settings, use the SmtpSetup object.
    SMTP_SETUP = 2

    # With SpecialDaysTable you can determine dates to override a preset
    # behaviour, for specific days = data item day_id.  SpecialDaysTable works
    # together with objects of Schedule, or Activity Calendar.
    SPECIAL_DAYS_TABLE = 11

    # StatusMapping object stores status words with mapping.  Each bit in the
    # status word is mapped to position = s in referencing status table.
    STATUS_MAPPING = 63

    SECURITY_SETUP = 64

    # To determine Internet TCP/UDP protocol settings, use the TcpUdpSetup
    # object.
    TCP_UDP_SETUP = 41

    # In an object of type UtilityTables each "Table" = ANSI C12.19:1997 table
    # data is represented as an instance, and identified by its logical name.
    UTILITY_TABLES = 26

    #
    # S-FSK Phy MAC Setup
    SFSK_PHY_MAC_SETUP = 50

    # S-FSK Active initiator.
    SFSK_ACTIVE_INITIATOR = 51

    # S-FSK MAC synchronization timeouts
    SFSK_MAC_SYNCHRONIZATION_TIMEOUTS = 52

    # S-FSK MAC Counters.
    SFSK_MAC_COUNTERS = 53

    # IEC 61334-4-32 LLC setup
    IEC_61334_4_32_LLC_SETUP = 55

    # S-FSK Reporting system list.
    S_FSK_REPORTING_SYSTEM_LIST = 56

    # Arbitrator.
    ARBITRATOR = 68

    # G3-PLC MAC layer counters
    G3_PLC_MAC_LAYER_COUNTERS = 90

    # G3-PLC MAC setup.
    G3_PLC_MAC_SETUP = 91

    # G3-PLC 6LoWPAN.
    G3_PLC6_LO_WPAN = 92

    # Function control.
    FUNCTION_CONTROL = 122

    # Communication port protection.
    COMMUNICATION_PORT_PROTECTION = 124

    # LTE monitoring.
    LTE_MONITORING = 151

    # CoAP setup.
    CoAPSetup = 152

    # CoAP diagnostic.
    COAP_DIAGNOSTIC = 153

    # G3-PLC Hybrid RF MAC layer counters.
    G3_PLC_HYBRID_RF_MAC_LAYER_COUNTERS = 160

    # G3-PLC Hybrid RF MAC setup.
    G3_PLC_HYBRID_RF_MAC_SETUP = 161

    # G3-PLC Hybrid 6LoWPAN adaptation layer setup.
    G3_PLC_HYBRID_6LOWPAN_ADAPTATION_LAYER_SETUP = 162
    #
    # Tariff Plan =Piano Tariffario) is used in Italian standard UNI/TS
    # 11291-11.
    TARIFF_PLAN = 8192

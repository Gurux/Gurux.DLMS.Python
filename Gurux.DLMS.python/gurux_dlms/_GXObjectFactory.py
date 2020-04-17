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
from .enums import ObjectType
#pylint: disable=bad-option-value,too-many-locals,
#cyclic-import,old-style-class,too-few-public-methods
from .objects.GXDLMSAssociationLogicalName import GXDLMSAssociationLogicalName
from .objects.GXDLMSObject import GXDLMSObject
from .objects.GXDLMSActionSchedule import GXDLMSActionSchedule
from .objects.GXDLMSActivityCalendar import GXDLMSActivityCalendar
from .objects.GXDLMSAssociationShortName import GXDLMSAssociationShortName
from .objects.GXDLMSAutoAnswer import GXDLMSAutoAnswer
from .objects.GXDLMSAutoConnect import GXDLMSAutoConnect
from .objects.GXDLMSClock import GXDLMSClock
from .objects.GXDLMSData import GXDLMSData
from .objects.GXDLMSDemandRegister import GXDLMSDemandRegister
from .objects.GXDLMSMacAddressSetup import GXDLMSMacAddressSetup
from .objects.GXDLMSRegister import GXDLMSRegister
from .objects.GXDLMSExtendedRegister import GXDLMSExtendedRegister
from .objects.GXDLMSGprsSetup import GXDLMSGprsSetup
from .objects.GXDLMSHdlcSetup import GXDLMSHdlcSetup
from .objects.GXDLMSIECLocalPortSetup import GXDLMSIECLocalPortSetup
from .objects.GXDLMSIecTwistedPairSetup import GXDLMSIecTwistedPairSetup
from .objects.GXDLMSIp4Setup import GXDLMSIp4Setup
from .objects.GXDLMSIp6Setup import GXDLMSIp6Setup
from .objects.GXDLMSMBusSlavePortSetup import GXDLMSMBusSlavePortSetup
from .objects.GXDLMSImageTransfer import GXDLMSImageTransfer
from .objects.GXDLMSSecuritySetup import GXDLMSSecuritySetup
from .objects.GXDLMSDisconnectControl import GXDLMSDisconnectControl
from .objects.GXDLMSLimiter import GXDLMSLimiter

from .objects.GXDLMSMBusClient import GXDLMSMBusClient
from .objects.GXDLMSModemConfiguration import GXDLMSModemConfiguration
from .objects.GXDLMSPppSetup import GXDLMSPppSetup
from .objects.GXDLMSProfileGeneric import GXDLMSProfileGeneric
from .objects.GXDLMSRegisterMonitor import GXDLMSRegisterMonitor
from .objects.GXDLMSRegisterActivation import GXDLMSRegisterActivation
from .objects.GXDLMSSapAssignment import GXDLMSSapAssignment
from .objects.GXDLMSSchedule import GXDLMSSchedule
from .objects.GXDLMSScriptTable import GXDLMSScriptTable
from .objects.GXDLMSSpecialDaysTable import GXDLMSSpecialDaysTable
from .objects.GXDLMSTcpUdpSetup  import GXDLMSTcpUdpSetup
from .objects.GXDLMSPushSetup import GXDLMSPushSetup
from .objects.GXDLMSMBusMasterPortSetup import GXDLMSMBusMasterPortSetup
from .objects.GXDLMSGSMDiagnostic import GXDLMSGSMDiagnostic
from .objects.GXDLMSAccount import GXDLMSAccount
from .objects.GXDLMSCredit import GXDLMSCredit
from .objects.GXDLMSCharge import GXDLMSCharge
from .objects.GXDLMSTokenGateway import GXDLMSTokenGateway
from .objects.GXDLMSParameterMonitor import GXDLMSParameterMonitor
from .objects.GXDLMSUtilityTables import GXDLMSUtilityTables
from .objects.GXDLMSLlcSscsSetup import GXDLMSLlcSscsSetup
from .objects.GXDLMSPrimeNbOfdmPlcPhysicalLayerCounters import GXDLMSPrimeNbOfdmPlcPhysicalLayerCounters
from .objects.GXDLMSPrimeNbOfdmPlcMacSetup import GXDLMSPrimeNbOfdmPlcMacSetup
from .objects.GXDLMSPrimeNbOfdmPlcMacFunctionalParameters import GXDLMSPrimeNbOfdmPlcMacFunctionalParameters
from .objects.GXDLMSPrimeNbOfdmPlcMacCounters import GXDLMSPrimeNbOfdmPlcMacCounters
from .objects.GXDLMSPrimeNbOfdmPlcMacNetworkAdministrationData import GXDLMSPrimeNbOfdmPlcMacNetworkAdministrationData
from .objects.GXDLMSPrimeNbOfdmPlcApplicationsIdentification import GXDLMSPrimeNbOfdmPlcApplicationsIdentification

class _GXObjectFactory:
    #Reserved for internal use.

    #
    # Constructor.
    def __init__(self):
        pass

    @classmethod
    def createObject(cls, ot):
        #pylint: disable=bad-option-value,redefined-variable-type
        #  If IC is manufacturer specific or unknown.
        if ot is None:
            raise ValueError("Invalid object type.")

        if ot == ObjectType.ACTION_SCHEDULE:
            ret = GXDLMSActionSchedule()
        elif ot == ObjectType.ACTIVITY_CALENDAR:
            ret = GXDLMSActivityCalendar()
        elif ot == ObjectType.ASSOCIATION_LOGICAL_NAME:
            ret = GXDLMSAssociationLogicalName()
        elif ot == ObjectType.ASSOCIATION_SHORT_NAME:
            ret = GXDLMSAssociationShortName()
        elif ot == ObjectType.AUTO_ANSWER:
            ret = GXDLMSAutoAnswer()
        elif ot == ObjectType.AUTO_CONNECT:
            ret = GXDLMSAutoConnect()
        elif ot == ObjectType.CLOCK:
            ret = GXDLMSClock()
        elif ot == ObjectType.DATA:
            ret = GXDLMSData()
        elif ot == ObjectType.DEMAND_REGISTER:
            ret = GXDLMSDemandRegister()
        elif ot == ObjectType.MAC_ADDRESS_SETUP:
            ret = GXDLMSMacAddressSetup()
        elif ot == ObjectType.REGISTER:
            ret = GXDLMSRegister()
        elif ot == ObjectType.EXTENDED_REGISTER:
            ret = GXDLMSExtendedRegister()
        elif ot == ObjectType.GPRS_SETUP:
            ret = GXDLMSGprsSetup()
        elif ot == ObjectType.IEC_HDLC_SETUP:
            ret = GXDLMSHdlcSetup()
        elif ot == ObjectType.IEC_LOCAL_PORT_SETUP:
            ret = GXDLMSIECLocalPortSetup()
        elif ot == ObjectType.IEC_TWISTED_PAIR_SETUP:
            ret = GXDLMSIecTwistedPairSetup()
        elif ot == ObjectType.IP4_SETUP:
            ret = GXDLMSIp4Setup()
        elif ot == ObjectType.IP6_SETUP:
            ret = GXDLMSIp6Setup()
        elif ot == ObjectType.MBUS_SLAVE_PORT_SETUP:
            ret = GXDLMSMBusSlavePortSetup()
        elif ot == ObjectType.IMAGE_TRANSFER:
            ret = GXDLMSImageTransfer()
        elif ot == ObjectType.SECURITY_SETUP:
            ret = GXDLMSSecuritySetup()
        elif ot == ObjectType.DISCONNECT_CONTROL:
            ret = GXDLMSDisconnectControl()
        elif ot == ObjectType.LIMITER:
            ret = GXDLMSLimiter()
        elif ot == ObjectType.MBUS_CLIENT:
            ret = GXDLMSMBusClient()
        elif ot == ObjectType.MODEM_CONFIGURATION:
            ret = GXDLMSModemConfiguration()
        elif ot == ObjectType.PPP_SETUP:
            ret = GXDLMSPppSetup()
        elif ot == ObjectType.PROFILE_GENERIC:
            ret = GXDLMSProfileGeneric()
        elif ot == ObjectType.REGISTER_MONITOR:
            ret = GXDLMSRegisterMonitor()
        elif ot == ObjectType.REGISTER_ACTIVATION:
            ret = GXDLMSRegisterActivation()
        elif ot == ObjectType.REGISTER_TABLE:
            ret = GXDLMSObject(ot)
        elif ot == ObjectType.ZIG_BEE_SAS_STARTUP:
            ret = GXDLMSObject(ot)
        elif ot == ObjectType.ZIG_BEE_SAS_JOIN:
            ret = GXDLMSObject(ot)
        elif ot == ObjectType.SAP_ASSIGNMENT:
            ret = GXDLMSSapAssignment()
        elif ot == ObjectType.SCHEDULE:
            ret = GXDLMSSchedule()
        elif ot == ObjectType.SCRIPT_TABLE:
            ret = GXDLMSScriptTable()
        elif ot == ObjectType.SPECIAL_DAYS_TABLE:
            ret = GXDLMSSpecialDaysTable()
        elif ot == ObjectType.STATUS_MAPPING:
            ret = GXDLMSObject(ot)
        elif ot == ObjectType.TCP_UDP_SETUP:
            ret = GXDLMSTcpUdpSetup()
        elif ot == ObjectType.ZIG_BEE_SAS_APS_FRAGMENTATION:
            ret = GXDLMSObject(ot)
        elif ot == ObjectType.UTILITY_TABLES:
            ret = GXDLMSUtilityTables()
        elif ot == ObjectType.PUSH_SETUP:
            ret = GXDLMSPushSetup()
        elif ot == ObjectType.MBUS_MASTER_PORT_SETUP:
            ret = GXDLMSMBusMasterPortSetup()
        elif ot == ObjectType.GSM_DIAGNOSTIC:
            ret = GXDLMSGSMDiagnostic()
        elif ot == ObjectType.ACCOUNT:
            ret = GXDLMSAccount()
        elif ot == ObjectType.CREDIT:
            ret = GXDLMSCredit()
        elif ot == ObjectType.CHARGE:
            ret = GXDLMSCharge()
        elif ot == ObjectType.TOKEN_GATEWAY:
            ret = GXDLMSTokenGateway()
        elif ot == ObjectType.PARAMETER_MONITOR:
            ret = GXDLMSParameterMonitor()
        elif ot == ObjectType.LLC_SSCS_SETUP:
            ret = GXDLMSLlcSscsSetup()
        elif ot == ObjectType.PRIME_NB_OFDM_PLC_PHYSICAL_LAYER_COUNTERS:
            ret = GXDLMSPrimeNbOfdmPlcPhysicalLayerCounters()
        elif ot == ObjectType.PRIME_NB_OFDM_PLC_MAC_SETUP:
            ret = GXDLMSPrimeNbOfdmPlcMacSetup()
        elif ot == ObjectType.PRIME_NB_OFDM_PLC_MAC_FUNCTIONAL_PARAMETERS:
            ret = GXDLMSPrimeNbOfdmPlcMacFunctionalParameters()
        elif ot == ObjectType.PRIME_NB_OFDM_PLC_MAC_COUNTERS:
            ret = GXDLMSPrimeNbOfdmPlcMacCounters()
        elif ot == ObjectType.PRIME_NB_OFDM_PLC_MAC_NETWORK_ADMINISTRATION_DATA:
            ret = GXDLMSPrimeNbOfdmPlcMacNetworkAdministrationData()
        elif ot == ObjectType.PRIME_NB_OFDM_PLC_APPLICATIONS_IDENTIFICATION:
            ret = GXDLMSPrimeNbOfdmPlcApplicationsIdentification()
        else:
            ret = GXDLMSObject(ot)
        return ret

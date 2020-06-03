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
from __future__ import print_function
import pkg_resources
from .enums import Standard, ObjectType, DataType
from .GXStandardObisCodeCollection import GXStandardObisCodeCollection
from .GXStandardObisCode import GXStandardObisCode
from .internal._GXCommon import _GXCommon
from .GXEnum import GXEnum
from .GXInt8 import GXInt8
from .GXInt16 import GXInt16
from .GXInt32 import GXInt32
from .GXInt64 import GXInt64
from .GXUInt8 import GXUInt8
from .GXUInt16 import GXUInt16
from .GXUInt32 import GXUInt32
from .GXUInt64 import GXUInt64
from .GXDate import GXDate
from .GXDateTime import GXDateTime
from .GXTime import GXTime
from .GXByteBuffer import GXByteBuffer
from .manufacturersettings.GXObisCode import GXObisCode

###Python 2 requires this
#pylint: disable=bad-option-value,old-style-class
class GXDLMSConverter:
    #
    # Constructor.
    #
    # value: Used standard.
    #
    def __init__(self, value=Standard.DLMS):
        self.standard = value
        # Collection of standard OBIS codes.
        self.codes = GXStandardObisCodeCollection()

    #
    # Get OBIS code description.
    #
    # @param logicalName
    # Logical name (OBIS code).
    # @param type
    # Object type.
    # @param description
    # Description filter.
    # Array of descriptions that match given OBIS code.
    #
    def getDescription(self, logicalName, type_=ObjectType.NONE, description=None):
        if not self.codes:
            self.__readStandardObisInfo(self.standard, self.codes)
        list_ = list()
        all_ = not logicalName
        for it in self.codes.find(logicalName, type_):
            if description and not it.description.lower().contains(description.lower()):
                continue
            if all_:
                list_.append("A=" + it.getOBIS()[0] + ", B=" + it.getOBIS()[1] + ", C=" + it.getOBIS()[2] + ", D=" + it.getOBIS()[3] + ", E=" + it.getOBIS()[4] + ", F=" + it.getOBIS()[5] + "\r\n" + it.description)
            else:
                list_.append(it.description)
        return list_

    #pylint: disable=too-many-boolean-expressions
    @classmethod
    def __updateOBISCodeInfo(cls, codes, it, standard):
        ln = it.logicalName
        list_ = codes.find(ln, it.objectType)
        code_ = list_[0]
        if code_:
            if not it.description:
                it.description = code_.description
            #Update data type from DLMS standard.
            if standard != Standard.DLMS:
                d = list_[len(list_) - 1]
                code_.dataType = d.dataType
            if not code_.uiDataType:
                if "10" in code_.dataType:
                    code_.uiDataType = "10"
                elif "25" in code_.dataType or "26" in code_.dataType:
                    code_.uiDataType = "25"
                elif "9" in code_.dataType:
                    if (GXStandardObisCodeCollection.equalsMask2("0.0-64.96.7.10-14.255", ln) or GXStandardObisCodeCollection.equalsMask2("0.0-64.0.1.5.0-99,255", ln) or GXStandardObisCodeCollection.equalsMask2("0.0-64.0.1.2.0-99,255", ln) or GXStandardObisCodeCollection.equalsMask2("1.0-64.0.1.2.0-99,255", ln) or GXStandardObisCodeCollection.equalsMask2("1.0-64.0.1.5.0-99,255", ln) or GXStandardObisCodeCollection.equalsMask2("1.0-64.0.9.0.255", ln) or GXStandardObisCodeCollection.equalsMask2("1.0-64.0.9.6.255", ln) or GXStandardObisCodeCollection.equalsMask2("1.0-64.0.9.7.255", ln) or GXStandardObisCodeCollection.equalsMask2("1.0-64.0.9.13.255", ln) or GXStandardObisCodeCollection.equalsMask2("1.0-64.0.9.14.255", ln) or GXStandardObisCodeCollection.equalsMask2("1.0-64.0.9.15.255", ln)):
                        code_.uiDataType = "25"
                    #Local time
                    elif GXStandardObisCodeCollection.equalsMask2("1.0-64.0.9.1.255", ln):
                        code_.uiDataType = "27"
                    #Local date
                    elif GXStandardObisCodeCollection.equalsMask2("1.0-64.0.9.2.255", ln):
                        code_.uiDataType = "26"
                    #Active firmware identifier
                    elif GXStandardObisCodeCollection.equalsMask2("1.0.0.2.0.255", ln):
                        code_.uiDataType = "10"
                #Unix time
                elif it.objectType == ObjectType.DATA and GXStandardObisCodeCollection.equalsMask2("0.0.1.1.0.255", it.logicalName):
                    code_.uiDataType = "25"

            if not code_.dataType == "*" and not code_.dataType == "" and "," not in code_.dataType:
                tp = int(code_.dataType)
                if it.objectType in (ObjectType.DATA, ObjectType.REGISTER, ObjectType.REGISTER_ACTIVATION, ObjectType.EXTENDED_REGISTER):
                    it.setDataType(2, tp)
            if code_.uiDataType:
                tp = int(code_.uiDataType)
                if it.objectType in (ObjectType.DATA, ObjectType.REGISTER, ObjectType.REGISTER_ACTIVATION, ObjectType.EXTENDED_REGISTER):
                    it.setUIDataType(2, tp)
        else:
            print("Unknown OBIS Code: " + it.logicalName + " Type: " + it.objectType)

    def updateOBISCodeInformation(self, objects):
        if not self.codes:
            self.__readStandardObisInfo(self.standard, self.codes)
        if isinstance(objects, list):
            for it in objects:
                self.__updateOBISCodeInfo(self.codes, it, self.standard)
        else:
            self.__updateOBISCodeInfo(self.codes, objects, self.standard)

    @classmethod
    def __getObjects(cls, standard):
        codes = list()
        if standard == Standard.ITALY:
            str_ = pkg_resources.resource_string(__name__, "Italy.txt").decode("utf-8")
        elif standard == Standard.INDIA:
            str_ = pkg_resources.resource_string(__name__, "India.txt").decode("utf-8")
        elif standard == Standard.SAUDI_ARABIA:
            str_ = pkg_resources.resource_string(__name__, "SaudiArabia.txt").decode("utf-8")
        if not str_:
            return None
        str_ = str_.replace("\n", "\r")
        rows = str_.split('\r')
        for it in rows:
            if it and not it.startswith("#"):
                items = it.split(';')
                if len(items) > 1:
                    ot = int(items[0])
                    ln = _GXCommon.toLogicalName(_GXCommon.logicalNameToBytes(items[1]))
                    version = int(items[2])
                    desc = items[3]
                    code_ = GXObisCode(ln, ot, 0, desc)
                    code_.version = version
                    if len(items) > 4:
                        code_.uiDataType = items[4]
                    codes.append(code_)
        return codes

    @classmethod
    def __readStandardObisInfo(cls, standard, codes):
        if standard != Standard.DLMS:
            for it in cls.__getObjects(standard):
                tmp = GXStandardObisCode(it.logicalName.split('.'))
                tmp.interfaces = str(it.objectType)
                tmp.description = it.description
                tmp.uiDataType = it.uiDataType
                codes.append(tmp)

        str_ = pkg_resources.resource_string(__name__, "OBISCodes.txt").decode("utf-8")
        str_ = str_.replace("\n", "\r")
        rows = str_.split('\r')
        for it in rows:
            if it and not it.startswith("#"):
                items = it.split(';')
                obis = items[0].split('.')
                try:
                    code_ = GXStandardObisCode(obis, str(items[3]) + "; " + str(items[4]) + "; " + str(items[5]) + "; " + str(items[6]) + "; " + str(items[7]), str(items[1]), str(items[2]))
                    codes.append(code_)
                except UnicodeEncodeError:
                    pass

    @classmethod
    def changeType(cls, value, type_):
        if _GXCommon.getDLMSDataType(value) == type_:
            return value
        if type_ == DataType.ARRAY:
            raise ValueError("Can't change array types.")
        if type_ == DataType.BCD:
            ret = int(value)
        elif type_ == DataType.BOOLEAN:
            ret = bool(value)
        elif type_ == DataType.COMPACT_ARRAY:
            raise ValueError("Can't change compact array types.")
        elif type_ == DataType.DATE:
            ret = GXDate(value)
        elif type_ == DataType.DATETIME:
            ret = GXDateTime(value)
        elif type_ == DataType.ENUM:
            ret = GXEnum(value)
        elif type_ == DataType.FLOAT32:
            ret = float(value)
        elif type_ == DataType.FLOAT64:
            ret = float(value)
        elif type_ == DataType.INT16:
            ret = GXInt16(value)
        elif type_ == DataType.INT32:
            ret = GXInt32(value)
        elif type_ == DataType.INT64:
            ret = GXInt64(value)
        elif type_ == DataType.INT8:
            ret = GXInt8(value)
        elif type_ == DataType.NONE:
            ret = None
        elif type_ == DataType.OCTET_STRING:
            if isinstance(value, str):
                ret = GXByteBuffer.hexToBytes(str(value))
            else:
                raise ValueError("Can't change octect string type.")
        elif type_ == DataType.STRING:
            ret = str(value)
        elif type_ == DataType.BITSTRING:
            ret = str(value)
        elif type_ == DataType.STRING_UTF8:
            ret = str(value)
        elif type_ == DataType.STRUCTURE:
            raise ValueError("Can't change structure types.")
        elif type_ == DataType.TIME:
            ret = GXTime(value)
        elif type_ == DataType.UINT16:
            ret = GXUInt16(value)
        elif type_ == DataType.UINT32:
            ret = GXUInt32(value)
        elif type_ == DataType.UINT64:
            ret = GXUInt64(value)
        elif type_ == DataType.UINT8:
            ret = GXUInt8(value)
        else:
            raise ValueError('Invalid data type.')
        return ret

    @classmethod
    def objectTypeToString(cls, ot):
        if ot == ObjectType.ACTION_SCHEDULE:
            ret = "ActionSchedule"
        elif ot == ObjectType.ACTIVITY_CALENDAR:
            ret = "ActivityCalendar"
        elif ot == ObjectType.ASSOCIATION_LOGICAL_NAME:
            ret = "AssociationLogicalName"
        elif ot == ObjectType.ASSOCIATION_SHORT_NAME:
            ret = "AssociationShortName"
        elif ot == ObjectType.AUTO_ANSWER:
            ret = "AutoAnswer"
        elif ot == ObjectType.AUTO_CONNECT:
            ret = "AutoConnect"
        elif ot == ObjectType.CLOCK:
            ret = "Clock"
        elif ot == ObjectType.DATA:
            ret = "Data"
        elif ot == ObjectType.DEMAND_REGISTER:
            ret = "DemandRegister"
        elif ot == ObjectType.MAC_ADDRESS_SETUP:
            ret = "MacAddressSetup"
        elif ot == ObjectType.EXTENDED_REGISTER:
            ret = "ExtendedRegister"
        elif ot == ObjectType.GPRS_SETUP:
            ret = "GprsSetup"
        elif ot == ObjectType.SECURITY_SETUP:
            ret = "SecuritySetup"
        elif ot == ObjectType.IEC_HDLC_SETUP:
            ret = "IecHdlcSetup"
        elif ot == ObjectType.IEC_LOCAL_PORT_SETUP:
            ret = "IecLocalPortSetup"
        elif ot == ObjectType.IEC_TWISTED_PAIR_SETUP:
            ret = "IEC_TWISTED_PAIR_SETUP"
        elif ot == ObjectType.IP4_SETUP:
            ret = "Ip4Setup"
        elif ot == ObjectType.MBUS_SLAVE_PORT_SETUP:
            ret = "MBusSlavePortSetup"
        elif ot == ObjectType.IMAGE_TRANSFER:
            ret = "ImageTransfer"
        elif ot == ObjectType.DISCONNECT_CONTROL:
            ret = "DisconnectControl"
        elif ot == ObjectType.LIMITER:
            ret = "Limiter"
        elif ot == ObjectType.MBUS_CLIENT:
            ret = "MBusClient"
        elif ot == ObjectType.MODEM_CONFIGURATION:
            ret = "ModemConfiguration"
        elif ot == ObjectType.PPP_SETUP:
            ret = "PppSetup"
        elif ot == ObjectType.PROFILE_GENERIC:
            ret = "ProfileGeneric"
        elif ot == ObjectType.REGISTER:
            ret = "Register"
        elif ot == ObjectType.REGISTER_ACTIVATION:
            ret = "RegisterActivation"
        elif ot == ObjectType.REGISTER_MONITOR:
            ret = "RegisterMonitor"
        elif ot == ObjectType.REGISTER_TABLE:
            ret = "RegisterTable"
        elif ot == ObjectType.ZIG_BEE_SAS_STARTUP:
            ret = "ZigBeeSasStartup"
        elif ot == ObjectType.ZIG_BEE_SAS_JOIN:
            ret = "ZigBeeSasJoin"
        elif ot == ObjectType.ZIG_BEE_SAS_APS_FRAGMENTATION:
            ret = "ZigBeeSasApsFragmentation"
        elif ot == ObjectType.ZIG_BEE_NETWORK_CONTROL:
            ret = "ZigBeeNetworkControl"
        elif ot == ObjectType.SAP_ASSIGNMENT:
            ret = "SapAssignment"
        elif ot == ObjectType.SCHEDULE:
            ret = "Schedule"
        elif ot == ObjectType.SCRIPT_TABLE:
            ret = "ScriptTable"
        elif ot == ObjectType.SMTP_SETUP:
            ret = "SMTPSetup"
        elif ot == ObjectType.SPECIAL_DAYS_TABLE:
            ret = "SpecialDaysTable"
        elif ot == ObjectType.STATUS_MAPPING:
            ret = "StatusMapping"
        elif ot == ObjectType.TCP_UDP_SETUP:
            ret = "TcpUdpSetup"
        elif ot == ObjectType.UTILITY_TABLES:
            ret = "UtilityTables"
        elif ot == ObjectType.MBUS_MASTER_PORT_SETUP:
            ret = "MBusMasterPortSetup"
        elif ot == ObjectType.PUSH_SETUP:
            ret = "PushSetup"
        elif ot == ObjectType.ACCOUNT:
            ret = "Account"
        elif ot == ObjectType.CREDIT:
            ret = "Credit"
        elif ot == ObjectType.CHARGE:
            ret = "Charge"
        elif ot == ObjectType.PARAMETER_MONITOR:
            ret = "ParameterMonitor"
        elif ot == ObjectType.TOKEN_GATEWAY:
            ret = "Token"
        elif ot == ObjectType.GSM_DIAGNOSTIC:
            ret = "GSMDiagnostic"
        elif ot == ObjectType.COMPACT_DATA:
            ret = "CompactData"
        elif ot == ObjectType.IP6_SETUP:
            ret = "Ip6Setup"
        elif ot == ObjectType.LLC_SSCS_SETUP:
            ret = "LlcSscsSetup"
        elif ot == ObjectType.PRIME_NB_OFDM_PLC_PHYSICAL_LAYER_COUNTERS:
            ret = "PrimeNbOfdmPlcPhysicalLayerCounters"
        elif ot == ObjectType.PRIME_NB_OFDM_PLC_MAC_SETUP:
            ret = "PrimeNbOfdmPlcMacSetup"
        elif ot == ObjectType.PRIME_NB_OFDM_PLC_MAC_FUNCTIONAL_PARAMETERS:
            ret = "PrimeNbOfdmPlcMacFunctionalParameters"
        elif ot == ObjectType.PRIME_NB_OFDM_PLC_MAC_COUNTERS:
            ret = "PrimeNbOfdmPlcMacCounters"
        elif ot == ObjectType.PRIME_NB_OFDM_PLC_MAC_NETWORK_ADMINISTRATION_DATA:
            ret = "PrimeNbOfdmPlcMacNetworkAdministrationData"
        elif ot == ObjectType.PRIME_NB_OFDM_PLC_APPLICATIONS_IDENTIFICATION:
            ret = "PrimeNbOfdmPlcApplicationsIdentification"
        else:
            ret = "Manufacture spesific."
        return ret

    @classmethod
    def valueOfObjectType(cls, value):
        if value == "ActionSchedule":
            ot = ObjectType.ACTION_SCHEDULE
        elif value == "ActivityCalendar":
            ot = ObjectType.ACTIVITY_CALENDAR
        elif value == "AssociationLogicalName":
            ot = ObjectType.ASSOCIATION_LOGICAL_NAME
        elif value == "AssociationShortName":
            ot = ObjectType.ASSOCIATION_SHORT_NAME
        elif value == "AutoAnswer":
            ot = ObjectType.AUTO_ANSWER
        elif value == "AutoConnect":
            ot = ObjectType.AUTO_CONNECT
        elif value == "Clock":
            ot = ObjectType.CLOCK
        elif value == "Data":
            ot = ObjectType.DATA
        elif value == "DemandRegister":
            ot = ObjectType.DEMAND_REGISTER
        elif value == "MacAddressSetup":
            ot = ObjectType.MAC_ADDRESS_SETUP
        elif value == "ExtendedRegister":
            ot = ObjectType.EXTENDED_REGISTER
        elif value == "GprsSetup":
            ot = ObjectType.GPRS_SETUP
        elif value == "SecuritySetup":
            ot = ObjectType.SECURITY_SETUP
        elif value in ("IecHdlcSetup", "HdlcSetup"):
            ot = ObjectType.IEC_HDLC_SETUP
        elif value in ("IecLocalPortSetup", "IecOpticalPortSetup"):
            ot = ObjectType.IEC_LOCAL_PORT_SETUP
        elif value == "IEC_TWISTED_PAIR_SETUP":
            ot = ObjectType.IEC_TWISTED_PAIR_SETUP
        elif value == "Ip4Setup":
            ot = ObjectType.IP4_SETUP
        elif value == "MBusSlavePortSetup":
            ot = ObjectType.MBUS_SLAVE_PORT_SETUP
        elif value == "ImageTransfer":
            ot = ObjectType.IMAGE_TRANSFER
        elif value == "DisconnectControl":
            ot = ObjectType.DISCONNECT_CONTROL
        elif value == "Limiter":
            ot = ObjectType.LIMITER
        elif value == "MBusClient":
            ot = ObjectType.MBUS_CLIENT
        elif value == "ModemConfiguration":
            ot = ObjectType.MODEM_CONFIGURATION
        elif value == "PppSetup":
            ot = ObjectType.PPP_SETUP
        elif value == "ProfileGeneric":
            ot = ObjectType.PROFILE_GENERIC
        elif value == "Register":
            ot = ObjectType.REGISTER
        elif value == "RegisterActivation":
            ot = ObjectType.REGISTER_ACTIVATION
        elif value == "RegisterMonitor":
            ot = ObjectType.REGISTER_MONITOR
        elif value == "RegisterTable":
            ot = ObjectType.REGISTER_TABLE
        elif value == "ZigBeeSasStartup":
            ot = ObjectType.ZIG_BEE_SAS_STARTUP
        elif value == "ZigBeeSasJoin":
            ot = ObjectType.ZIG_BEE_SAS_JOIN
        elif value == "ZigBeeSasApsFragmentation":
            ot = ObjectType.ZIG_BEE_SAS_APS_FRAGMENTATION
        elif value == "ZigBeeNetworkControl":
            ot = ObjectType.ZIG_BEE_NETWORK_CONTROL
        elif value == "SapAssignment":
            ot = ObjectType.SAP_ASSIGNMENT
        elif value == "Schedule":
            ot = ObjectType.SCHEDULE
        elif value == "ScriptTable":
            ot = ObjectType.SCRIPT_TABLE
        elif value == "SMTPSetup":
            ot = ObjectType.SMTP_SETUP
        elif value == "SpecialDaysTable":
            ot = ObjectType.SPECIAL_DAYS_TABLE
        elif value == "StatusMapping":
            ot = ObjectType.STATUS_MAPPING
        elif value == "TcpUdpSetup":
            ot = ObjectType.TCP_UDP_SETUP
        elif value == "UtilityTables":
            ot = ObjectType.UTILITY_TABLES
        elif value == "MBusMasterPortSetup":
            ot = ObjectType.MBUS_MASTER_PORT_SETUP
        elif value == "PushSetup":
            ot = ObjectType.PUSH_SETUP
        elif value == "Account":
            ot = ObjectType.ACCOUNT
        elif value == "Credit":
            ot = ObjectType.CREDIT
        elif value == "Charge":
            ot = ObjectType.CHARGE
        elif value == "ParameterMonitor":
            ot = ObjectType.PARAMETER_MONITOR
        elif value in ("Token", "TokenGateway"):
            ot = ObjectType.TOKEN_GATEWAY
        elif value == "GSMDiagnostic":
            ot = ObjectType.GSM_DIAGNOSTIC
        elif value == "CompactData":
            ot = ObjectType.COMPACT_DATA
        elif value == "Ip6Setup":
            ot = ObjectType.IP6_SETUP
        elif value == "LlcSscsSetup":
            ot = ObjectType.LLC_SSCS_SETUP
        elif value == "PrimeNbOfdmPlcPhysicalLayerCounters":
            ot = ObjectType.PRIME_NB_OFDM_PLC_PHYSICAL_LAYER_COUNTERS
        elif value == "PrimeNbOfdmPlcMacSetup":
            ot = ObjectType.PRIME_NB_OFDM_PLC_MAC_SETUP
        elif value == "PrimeNbOfdmPlcMacFunctionalParameters":
            ot = ObjectType.PRIME_NB_OFDM_PLC_MAC_FUNCTIONAL_PARAMETERS
        elif value == "PrimeNbOfdmPlcMacCounters":
            ot = ObjectType.PRIME_NB_OFDM_PLC_MAC_COUNTERS
        elif value == "PrimeNbOfdmPlcMacNetworkAdministrationData":
            ot = ObjectType.PRIME_NB_OFDM_PLC_MAC_NETWORK_ADMINISTRATION_DATA
        elif value == "PrimeNbOfdmPlcApplicationsIdentification":
            ot = ObjectType.PRIME_NB_OFDM_PLC_APPLICATIONS_IDENTIFICATION
        else:
            ot = ObjectType.NONE
        return ot

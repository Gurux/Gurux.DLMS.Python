from .ActionRequestType import ActionRequestType
from .enums import Command, DataType, Initiate, LoadDataSet, Task, Access, Definition, ApplicationReference, HardwareResource, VdeStateError, StateError, ExceptionServiceError
from .TranslatorGeneralTags import TranslatorGeneralTags
from .TranslatorTags import TranslatorTags
from .SingleReadResponse import SingleReadResponse
from .VariableAccessSpecification import VariableAccessSpecification
from .GetCommandType import GetCommandType
from .SetRequestType import SetRequestType
from .ActionResponseType import ActionResponseType
from .SetResponseType import SetResponseType
from .enums import AccessServiceCommandType, Conformance, ErrorCode
from .internal._GXCommon import _GXCommon
from .ServiceError import ServiceError
from .enums.Service import Service
from .ReleaseResponseReason import ReleaseResponseReason
from .ReleaseRequestReason import ReleaseRequestReason

#pylint: disable=bad-option-value,old-style-class,too-many-public-methods
class TranslatorSimpleTags:
    # Constructor.
    def __init__(self):
        pass

    #
    # Get general tags.
    #
    # @param type
    # @param list
    @classmethod
    def getGeneralTags(cls, list_):
        list_[Command.SNRM] = "Snrm"
        list_[Command.UNACCEPTABLE_FRAME] = "UnacceptableFrame"
        list_[Command.DISCONNECT_MODE] = "DisconnectMode"
        list_[Command.UA] = "Ua"
        list_[Command.AARQ] = "AssociationRequest"
        list_[Command.AARE] = "AssociationResponse"
        list_[TranslatorGeneralTags.APPLICATION_CONTEXT_NAME] = "ApplicationContextName"
        list_[Command.INITIATE_RESPONSE] = "InitiateResponse"
        list_[Command.INITIATE_REQUEST] = "InitiateRequest"
        list_[TranslatorGeneralTags.NEGOTIATED_QUALITY_OF_SERVICE] = "NegotiatedQualityOfService"
        list_[TranslatorGeneralTags.PROPOSED_QUALITY_OF_SERVICE] = "ProposedQualityOfService"
        list_[TranslatorGeneralTags.PROPOSED_DLMS_VERSION_NUMBER] = "ProposedDlmsVersionNumber"
        list_[TranslatorGeneralTags.PROPOSED_MAX_PDU_SIZE] = "ProposedMaxPduSize"
        list_[TranslatorGeneralTags.PROPOSED_CONFORMANCE] = "ProposedConformance"
        list_[TranslatorGeneralTags.VAA_NAME] = "VaaName"
        list_[TranslatorGeneralTags.NEGOTIATED_CONFORMANCE] = "NegotiatedConformance"
        list_[TranslatorGeneralTags.NEGOTIATED_DLMS_VERSION_NUMBER] = "NegotiatedDlmsVersionNumber"
        list_[TranslatorGeneralTags.NEGOTIATED_MAX_PDU_SIZE] = "NegotiatedMaxPduSize"
        list_[TranslatorGeneralTags.CONFORMANCE_BIT] = "ConformanceBit"
        list_[TranslatorGeneralTags.SENDER_ACSE_REQUIREMENTS] = "SenderACSERequirements"
        list_[TranslatorGeneralTags.RESPONDER_ACSE_REQUIREMENT] = "ResponderACSERequirement"
        list_[TranslatorGeneralTags.RESPONDING_MECHANISM_NAME] = "MechanismName"
        list_[TranslatorGeneralTags.CALLING_MECHANISM_NAME] = "MechanismName"
        list_[TranslatorGeneralTags.CALLING_AUTHENTICATION] = "CallingAuthentication"
        list_[TranslatorGeneralTags.RESPONDING_AUTHENTICATION] = "RespondingAuthentication"
        list_[Command.RELEASE_REQUEST] = "ReleaseRequest"
        list_[Command.RELEASE_RESPONSE] = "ReleaseResponse"
        list_[Command.DISCONNECT_REQUEST] = "DisconnectRequest"
        list_[TranslatorGeneralTags.ASSOCIATION_RESULT] = "AssociationResult"
        list_[TranslatorGeneralTags.RESULT_SOURCE_DIAGNOSTIC] = "ResultSourceDiagnostic"
        list_[TranslatorGeneralTags.ACSE_SERVICE_USER] = "ACSEServiceUser"
        list_[TranslatorGeneralTags.CALLING_AP_TITLE] = "CallingAPTitle"
        list_[TranslatorGeneralTags.RESPONDING_AP_TITLE] = "RespondingAPTitle"
        list_[TranslatorGeneralTags.DEDICATED_KEY] = "DedicatedKey"
        list_[Command.CONFIRMED_SERVICE_ERROR] = "ConfirmedServiceError"
        list_[Command.INFORMATION_REPORT] = "InformationReportRequest"
        list_[Command.EVENT_NOTIFICATION] = "EventNotificationRequest"
        list_[Command.EXCEPTION_RESPONSE] = "ExceptionResponse"
        list_[TranslatorTags.STATE_ERROR] = "StateError"
        list_[TranslatorTags.SERVICE_ERROR] = "ServiceError"

    #
    # Get SN tags.
    #
    # @param type
    # @param list
    #
    @classmethod
    def getSnTags(cls, list_):
        list_[Command.READ_REQUEST] = "ReadRequest"
        list_[Command.WRITE_REQUEST] = "WriteRequest"
        list_[Command.WRITE_REQUEST << 8 | SingleReadResponse.DATA] = "VariableName"
        list_[Command.WRITE_RESPONSE] = "WriteResponse"
        list_[Command.READ_REQUEST << 8 | VariableAccessSpecification.VARIABLE_NAME] = "VariableName"
        list_[Command.READ_REQUEST << 8 | VariableAccessSpecification.PARAMETERISED_ACCESS] = "ParameterisedAccess"
        list_[Command.READ_REQUEST << 8 | VariableAccessSpecification.BLOCK_NUMBER_ACCESS] = "BlockNumberAccess"
        list_[Command.WRITE_REQUEST << 8 | VariableAccessSpecification.VARIABLE_NAME] = "VariableName"
        list_[Command.READ_RESPONSE] = "ReadResponse"
        list_[Command.READ_RESPONSE << 8 | SingleReadResponse.DATA_BLOCK_RESULT] = "DataBlockResult"
        list_[Command.READ_RESPONSE << 8 | SingleReadResponse.DATA] = "Data"
        list_[Command.READ_RESPONSE << 8 | SingleReadResponse.DATA_ACCESS_ERROR] = "DataAccessError"

    #
    # Get LN tags.
    #
    # @param type
    # @param list
    #
    @classmethod
    def getLnTags(cls, list_):
        list_[Command.GET_REQUEST] = "GetRequest"
        list_[Command.GET_REQUEST << 8 | GetCommandType.NORMAL] = "GetRequestNormal"
        list_[Command.GET_REQUEST << 8 | GetCommandType.NEXT_DATA_BLOCK] = "GetRequestForNextDataBlock"
        list_[Command.GET_REQUEST << 8 | GetCommandType.WITH_LIST] = "GetRequestWithList"
        list_[Command.SET_REQUEST] = "SetRequest"
        list_[Command.SET_REQUEST << 8 | SetRequestType.NORMAL] = "SetRequestNormal"
        list_[Command.SET_REQUEST << 8 | SetRequestType.FIRST_DATA_BLOCK] = "SetRequestFirstDataBlock"
        list_[Command.SET_REQUEST << 8 | SetRequestType.WITH_DATA_BLOCK] = "SetRequestWithDataBlock"
        list_[Command.SET_REQUEST << 8 | SetRequestType.WITH_LIST] = "SetRequestWithList"
        list_[Command.METHOD_REQUEST] = "ActionRequest"
        list_[Command.METHOD_REQUEST << 8 | ActionRequestType.NORMAL] = "ActionRequestNormal"
        list_[Command.METHOD_REQUEST << 8 | ActionRequestType.NEXT_BLOCK] = "ActionRequestForNextDataBlock"
        list_[Command.METHOD_REQUEST << 8 | ActionRequestType.WITH_LIST] = "ActionRequestWithList"
        list_[Command.METHOD_RESPONSE] = "ActionResponse"
        list_[Command.METHOD_RESPONSE << 8 | ActionResponseType.NORMAL] = "ActionResponseNormal"
        list_[Command.METHOD_RESPONSE << 8 | ActionResponseType.WITH_FIRST_BLOCK] = "ActionResponseWithFirstBlock"
        list_[Command.METHOD_RESPONSE << 8 | ActionResponseType.WITH_LIST] = "ActionResponseWithList"
        list_[int(Command.DATA_NOTIFICATION)] = "DataNotification"
        list_[Command.GET_RESPONSE] = "GetResponse"
        list_[Command.GET_RESPONSE << 8 | GetCommandType.NORMAL] = "GetResponseNormal"
        list_[Command.GET_RESPONSE << 8 | GetCommandType.NEXT_DATA_BLOCK] = "GetResponsewithDataBlock"
        list_[Command.GET_RESPONSE << 8 | GetCommandType.WITH_LIST] = "GetResponseWithList"
        list_[Command.SET_RESPONSE] = "SetResponse"
        list_[Command.SET_RESPONSE << 8 | SetResponseType.NORMAL] = "SetResponseNormal"
        list_[Command.SET_RESPONSE << 8 | SetResponseType.DATA_BLOCK] = "SetResponseDataBlock"
        list_[Command.SET_RESPONSE << 8 | SetResponseType.LAST_DATA_BLOCK] = "SetResponseWithLastDataBlock"
        list_[Command.SET_RESPONSE << 8 | SetResponseType.WITH_LIST] = "SetResponseWithList"
        list_[Command.ACCESS_REQUEST] = "AccessRequest"
        list_[(Command.ACCESS_REQUEST) << 8 | AccessServiceCommandType.GET] = "AccessRequestGet"
        list_[(Command.ACCESS_REQUEST) << 8 | AccessServiceCommandType.SET] = "AccessRequestSet"
        list_[(Command.ACCESS_REQUEST) << 8 | AccessServiceCommandType.ACTION] = "AccessRequestAction"
        list_[Command.ACCESS_RESPONSE] = "AccessResponse"
        list_[(Command.ACCESS_RESPONSE) << 8 | AccessServiceCommandType.GET] = "AccessResponseGet"
        list_[(Command.ACCESS_RESPONSE) << 8 | AccessServiceCommandType.SET] = "AccessResponseSet"
        list_[(Command.ACCESS_RESPONSE) << 8 | AccessServiceCommandType.ACTION] = "AccessResponseAction"
        list_[TranslatorTags.ACCESS_REQUEST_BODY] = "AccessRequestBody"
        list_[TranslatorTags.LIST_OF_ACCESS_REQUEST_SPECIFICATION] = "AccessRequestSpecification"
        list_[TranslatorTags.ACCESS_REQUEST_SPECIFICATION] = "_AccessRequestSpecification"
        list_[TranslatorTags.ACCESS_REQUEST_LIST_OF_DATA] = "AccessRequestListOfData"
        list_[TranslatorTags.ACCESS_RESPONSE_BODY] = "AccessResponseBody"
        list_[TranslatorTags.LIST_OF_ACCESS_RESPONSE_SPECIFICATION] = "AccessResponseSpecification"
        list_[TranslatorTags.ACCESS_RESPONSE_SPECIFICATION] = "_AccessResponseSpecification"
        list_[TranslatorTags.ACCESS_RESPONSE_LIST_OF_DATA] = "AccessResponseListOfData"
        list_[TranslatorTags.SERVICE] = "Service"
        list_[TranslatorTags.SERVICE_ERROR] = "ServiceError"
        list_[Command.GENERAL_BLOCK_TRANSFER] = "GeneralBlockTransfer"
        list_[TranslatorGeneralTags.CALLING_AE_INVOCATION_ID] = "CallingAEInvocationId"
        list_[TranslatorGeneralTags.CALLED_AE_INVOCATION_ID] = "CalledAEInvocationId"
        list_[TranslatorGeneralTags.RESPONDING_AE_INVOCATION_ID] = "RespondingAEInvocationId"
        list_[Command.GATEWAY_REQUEST] = "GatewayRequest"
        list_[Command.GATEWAY_RESPONSE] = "GatewayResponse"

    #
    # Get glo tags.
    #
    # @param type
    # @param list
    #
    @classmethod
    def getGloTags(cls, list_):
        list_[Command.GLO_INITIATE_REQUEST] = "glo_InitiateRequest"
        list_[Command.GLO_INITIATE_RESPONSE] = "glo_InitiateResponse"
        list_[Command.GLO_GET_REQUEST] = "glo_GetRequest"
        list_[Command.GLO_GET_RESPONSE] = "glo_GetResponse"
        list_[Command.GLO_SET_REQUEST] = "glo_SetRequest"
        list_[Command.GLO_SET_RESPONSE] = "glo_SetResponse"
        list_[Command.GLO_METHOD_REQUEST] = "glo_ActionRequest"
        list_[Command.GLO_METHOD_RESPONSE] = "glo_ActionResponse"
        list_[Command.GLO_READ_REQUEST] = "glo_ReadRequest"
        list_[Command.GLO_READ_RESPONSE] = "glo_ReadResponse"
        list_[Command.GLO_WRITE_REQUEST] = "glo_WriteRequest"
        list_[Command.GLO_WRITE_RESPONSE] = "glo_WriteResponse"
        list_[Command.GENERAL_GLO_CIPHERING] = "GeneralGloCiphering"
        list_[Command.GENERAL_CIPHERING] = "GeneralCiphering"
        list_[Command.GLO_CONFIRMED_SERVICE_ERROR] = "glo_GloConfirmedServiceError"

    #
    # Get ded tags.
    #
    # @param type
    # @param list
    #
    @classmethod
    def getDedTags(cls, list_):
        list_[Command.DED_GET_REQUEST] = "ded_GetRequest"
        list_[Command.DED_GET_RESPONSE] = "ded_GetResponse"
        list_[Command.DED_SET_REQUEST] = "ded_SetRequest"
        list_[Command.DED_SET_RESPONSE] = "ded_SetResponse"
        list_[Command.DED_METHOD_REQUEST] = "ded_ActionRequest"
        list_[Command.DED_METHOD_RESPONSE] = "ded_ActionResponse"
        list_[Command.GENERAL_DED_CIPHERING] = "GeneralDedCiphering"
        list_[Command.DED_CONFIRMED_SERVICE_ERROR] = "ded_GloConfirmedServiceError"
    #
    # Get translator tags.
    #
    # @param type
    # @param list
    #
    @classmethod
    def getTranslatorTags(cls, list_):
        list_[TranslatorTags.WRAPPER] = "Wrapper"
        list_[TranslatorTags.HDLC] = "Hdlc"
        list_[TranslatorTags.PDU_DLMS] = "Pdu"
        list_[TranslatorTags.TARGET_ADDRESS] = "TargetAddress"
        list_[TranslatorTags.SOURCE_ADDRESS] = "SourceAddress"
        list_[TranslatorTags.FRAME_TYPE] = "FrameType"
        list_[TranslatorTags.LIST_OF_VARIABLE_ACCESS_SPECIFICATION] = "ListOfVariableAccessSpecification"
        list_[TranslatorTags.LIST_OF_DATA] = "ListOfData"
        list_[TranslatorTags.SUCCESS] = "Success"
        list_[TranslatorTags.DATA_ACCESS_ERROR] = "DataAccessError"
        list_[TranslatorTags.ATTRIBUTE_DESCRIPTOR] = "AttributeDescriptor"
        list_[TranslatorTags.CLASS_ID] = "ClassId"
        list_[TranslatorTags.INSTANCE_ID] = "InstanceId"
        list_[TranslatorTags.ATTRIBUTE_ID] = "AttributeId"
        list_[TranslatorTags.METHOD_INVOCATION_PARAMETERS] = "MethodInvocationParameters"
        list_[TranslatorTags.SELECTOR] = "Selector"
        list_[TranslatorTags.PARAMETER] = "Parameter"
        list_[TranslatorTags.LAST_BLOCK] = "LastBlock"
        list_[TranslatorTags.BLOCK_NUMBER] = "BlockNumber"
        list_[TranslatorTags.RAW_DATA] = "RawData"
        list_[TranslatorTags.METHOD_DESCRIPTOR] = "MethodDescriptor"
        list_[TranslatorTags.METHOD_ID] = "MethodId"
        list_[TranslatorTags.RESULT] = "Result"
        list_[TranslatorTags.RETURN_PARAMETERS] = "ReturnParameters"
        list_[TranslatorTags.ACCESS_SELECTION] = "AccessSelection"
        list_[TranslatorTags.VALUE] = "Value"
        list_[TranslatorTags.ACCESS_SELECTOR] = "AccessSelector"
        list_[TranslatorTags.ACCESS_PARAMETERS] = "AccessParameters"
        list_[TranslatorTags.ATTRIBUTE_DESCRIPTOR_LIST] = "AttributeDescriptorList"
        list_[TranslatorTags.ATTRIBUTE_DESCRIPTOR_WITH_SELECTION] = "AttributeDescriptorWithSelection"
        list_[TranslatorTags.READ_DATA_BLOCK_ACCESS] = "ReadDataBlockAccess"
        list_[TranslatorTags.WRITE_DATA_BLOCK_ACCESS] = "WriteDataBlockAccess"
        list_[TranslatorTags.DATA] = "Data"
        list_[TranslatorTags.INVOKE_ID] = "InvokeIdAndPriority"
        list_[TranslatorTags.LONG_INVOKE_ID] = "LongInvokeIdAndPriority"
        list_[TranslatorTags.DATE_TIME] = "DateTime"
        list_[TranslatorTags.CURRENT_TIME] = "CurrentTime"
        list_[TranslatorTags.TIME] = "Time"
        list_[TranslatorTags.REASON] = "Reason"
        list_[TranslatorTags.NOTIFICATION_BODY] = "NotificationBody"
        list_[TranslatorTags.DATA_VALUE] = "DataValue"
        list_[TranslatorTags.CIPHERED_SERVICE] = "CipheredService"
        list_[TranslatorTags.SYSTEM_TITLE] = "SystemTitle"
        list_[TranslatorTags.DATA_BLOCK] = "DataBlock"
        list_[TranslatorTags.TRANSACTION_ID] = "TransactionId"
        list_[TranslatorTags.ORIGINATOR_SYSTEM_TITLE] = "OriginatorSystemTitle"
        list_[TranslatorTags.RECIPIENT_SYSTEM_TITLE] = "RecipientSystemTitle"
        list_[TranslatorTags.OTHER_INFORMATION] = "OtherInformation"
        list_[TranslatorTags.KEY_INFO] = "KeyInfo"
        list_[TranslatorTags.CIPHERED_CONTENT] = "CipheredContent"
        list_[TranslatorTags.AGREED_KEY] = "AgreedKey"
        list_[TranslatorTags.KEY_PARAMETERS] = "KeyParameters"
        list_[TranslatorTags.KEY_CIPHERED_DATA] = "KeyCipheredData"
        list_[TranslatorTags.ATTRIBUTE_VALUE] = "AttributeValue"
        list_[TranslatorTags.MAX_INFO_RX] = "MaxInfoRX"
        list_[TranslatorTags.MAX_INFO_TX] = "MaxInfoTX"
        list_[TranslatorTags.WINDOW_SIZE_RX] = "WindowSizeRX"
        list_[TranslatorTags.WINDOW_SIZE_TX] = "WindowSizeTX"
        list_[TranslatorTags.VALUE_LIST] = "ValueList"
        list_[TranslatorTags.DATA_ACCESS_RESULT] = "DataAccessResult"
        list_[TranslatorTags.BLOCK_CONTROL] = "BlockControl"
        list_[TranslatorTags.BLOCK_NUMBER_ACK] = "BlockNumberAck"
        list_[TranslatorTags.BLOCK_DATA] = "BlockData"
        list_[TranslatorTags.CONTENTS_DESCRIPTION] = "ContentsDescription"
        list_[TranslatorTags.ARRAY_CONTENTS] = "ArrayContents"
        list_[TranslatorTags.NETWORK_ID] = "NetworkId"
        list_[TranslatorTags.PHYSICAL_DEVICE_ADDRESS] = "PhysicalDeviceAddress"
        list_[TranslatorTags.PROTOCOL_VERSION] = "ProtocolVersion"
        list_[TranslatorTags.CALLED_AP_TITLE] = "CalledAPTitle"
        list_[TranslatorTags.CALLED_AP_INVOCATION_ID] = "CalledAPInvocationId"
        list_[TranslatorTags.CALLED_AE_INVOCATION_ID] = "CalledAEInvocationId"
        list_[TranslatorTags.CALLING_AP_INVOCATION_ID] = "CallingApInvocationId"
        list_[TranslatorTags.CALLED_AE_QUALIFIER] = "CalledAEQualifier"

    @classmethod
    def getDataTypeTags(cls, list_):
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.NONE] = "None"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.ARRAY] = "Array"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.BCD] = "BCD"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.BITSTRING] = "BitString"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.BOOLEAN] = "Boolean"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.COMPACT_ARRAY] = "CompactArray"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.DATE] = "Date"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.DATETIME] = "DateTime"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.ENUM] = "Enum"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.FLOAT32] = "Float32"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.FLOAT64] = "Float64"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.INT16] = "Int16"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.INT32] = "Int32"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.INT64] = "Int64"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.INT8] = "Int8"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.OCTET_STRING] = "OctetString"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.STRING] = "String"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.STRING_UTF8] = "StringUTF8"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.STRUCTURE] = "Structure"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.TIME] = "Time"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.UINT16] = "UInt16"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.UINT32] = "UInt32"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.UINT64] = "UInt64"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.UINT8] = "UInt8"

    @classmethod
    def errorCodeToString(cls, value):
        value = ErrorCode(value)
        str_ = None
        if value == ErrorCode.ACCESS_VIOLATED:
            str_ = "AccessViolated"
        elif value == ErrorCode.DATA_BLOCK_NUMBER_INVALID:
            str_ = "DataBlockNumberInvalid"
        elif value == ErrorCode.DATA_BLOCK_UNAVAILABLE:
            str_ = "DataBlockUnavailable"
        elif value == ErrorCode.HARDWARE_FAULT:
            str_ = "HardwareFault"
        elif value == ErrorCode.INCONSISTENT_CLASS:
            str_ = "InconsistentClass"
        elif value == ErrorCode.LONG_GET_OR_READ_ABORTED:
            str_ = "LongGetOrReadAborted"
        elif value == ErrorCode.LONG_SET_OR_WRITE_ABORTED:
            str_ = "LongSetOrWriteAborted"
        elif value == ErrorCode.NO_LONG_GET_OR_READ_IN_PROGRESS:
            str_ = "NoLongGetOrReadInProgress"
        elif value == ErrorCode.NO_LONG_SET_OR_WRITE_IN_PROGRESS:
            str_ = "NoLongSetOrWriteInProgress"
        elif value == ErrorCode.OK:
            str_ = "Success"
        elif value == ErrorCode.OTHER_REASON:
            str_ = "OtherReason"
        elif value == ErrorCode.READ_WRITE_DENIED:
            str_ = "ReadWriteDenied"
        elif value == ErrorCode.TEMPORARY_FAILURE:
            str_ = "TemporaryFailure"
        elif value == ErrorCode.UNAVAILABLE_OBJECT:
            str_ = "UnavailableObject"
        elif value == ErrorCode.UNDEFINED_OBJECT:
            str_ = "UndefinedObject"
        elif value == ErrorCode.UNMATCHED_TYPE:
            str_ = "UnmatchedType"
        else:
            raise ValueError("Error code: " + str(value))
        return str_

    @classmethod
    def value_ofErrorCode(cls, value):
        v = None
        if "AccessViolated".lower() == value.lower():
            v = ErrorCode.ACCESS_VIOLATED
        elif "DataBlockNumberInvalid".lower() == value.lower():
            v = ErrorCode.DATA_BLOCK_NUMBER_INVALID
        elif "DataBlockUnavailable".lower() == value.lower():
            v = ErrorCode.DATA_BLOCK_UNAVAILABLE
        elif "HardwareFault".lower() == value.lower():
            v = ErrorCode.HARDWARE_FAULT
        elif "InconsistentClass".lower() == value.lower():
            v = ErrorCode.INCONSISTENT_CLASS
        elif "LongGetOrReadAborted".lower() == value.lower():
            v = ErrorCode.LONG_GET_OR_READ_ABORTED
        elif "LongSetOrWriteAborted".lower() == value.lower():
            v = ErrorCode.LONG_SET_OR_WRITE_ABORTED
        elif "NoLongGetOrReadInProgress".lower() == value.lower():
            v = ErrorCode.NO_LONG_GET_OR_READ_IN_PROGRESS
        elif "NoLongSetOrWriteInProgress".lower() == value.lower():
            v = ErrorCode.NO_LONG_SET_OR_WRITE_IN_PROGRESS
        elif "Success".lower() == value.lower():
            v = ErrorCode.OK
        elif "OtherReason".lower() == value.lower():
            v = ErrorCode.OTHER_REASON
        elif "ReadWriteDenied".lower() == value.lower():
            v = ErrorCode.READ_WRITE_DENIED
        elif "TemporaryFailure".lower() == value.lower():
            v = ErrorCode.TEMPORARY_FAILURE
        elif "UnavailableObject".lower() == value.lower():
            v = ErrorCode.UNAVAILABLE_OBJECT
        elif "UndefinedObject".lower() == value.lower():
            v = ErrorCode.UNDEFINED_OBJECT
        elif "UnmatchedType".lower() == value.lower():
            v = ErrorCode.UNMATCHED_TYPE
        else:
            raise ValueError("Error code: " + value)
        return v

    @classmethod
    def __getServiceErrors(cls):
        list_ = dict()
        list_[ServiceError.APPLICATION_REFERENCE] = "ApplicationReference"
        list_[ServiceError.HARDWARE_RESOURCE] = "HardwareResource"
        list_[ServiceError.VDE_STATE_ERROR] = "VdeStateError"
        list_[ServiceError.SERVICE] = "Service"
        list_[ServiceError.DEFINITION] = "Definition"
        list_[ServiceError.ACCESS] = "Access"
        list_[ServiceError.INITIATE] = "Initiate"
        list_[ServiceError.LOAD_DATASET] = "LoadDataSet"
        list_[ServiceError.TASK] = "Task"
        return list_

    @classmethod
    def __getApplicationReference(cls):
        list_ = dict()
        list_[ApplicationReference.APPLICATION_CONTEXT_UNSUPPORTED] = "ApplicationContextUnsupported"
        list_[ApplicationReference.APPLICATION_REFERENCE_INVALID] = "ApplicationReferenceInvalid"
        list_[ApplicationReference.APPLICATION_UNREACHABLE] = "ApplicationUnreachable"
        list_[ApplicationReference.DECIPHERING_ERROR] = "DecipheringError"
        list_[ApplicationReference.OTHER] = "Other"
        list_[ApplicationReference.PROVIDER_COMMUNICATION_ERROR] = "ProviderCommunicationError"
        list_[ApplicationReference.TIME_ELAPSED] = "TimeElapsed"
        return list_

    @classmethod
    def __getHardwareResource(cls):
        list_ = dict()
        list_[HardwareResource.MASS_STORAGE_UNAVAILABLE] = "MassStorageUnavailable"
        list_[HardwareResource.MEMORY_UNAVAILABLE] = "MemoryUnavailable"
        list_[HardwareResource.OTHER] = "Other"
        list_[HardwareResource.OTHER_RESOURCE_UNAVAILABLE] = "OtherResourceUnavailable"
        list_[HardwareResource.PROCESSOR_RESOURCE_UNAVAILABLE] = "ProcessorResourceUnavailable"
        return list_

    @classmethod
    def __getVdeStateError(cls):
        list_ = dict()
        list_[VdeStateError.LOADING_DATASET] = "LoadingDataSet"
        list_[VdeStateError.NO_DLMS_CONTEXT] = "NoDlmsContext"
        list_[VdeStateError.OTHER] = "Other"
        list_[VdeStateError.STATUS_INOPERABLE] = "StatusInoperable"
        list_[VdeStateError.STATUS_NO_CHANGE] = "StatusNochange"
        return list_

    @classmethod
    def __getService(cls):
        list_ = dict()
        list_[Service.OTHER] = "Other"
        list_[Service.PDU_SIZE] = "PduSize"
        list_[Service.UNSUPPORTED] = "ServiceUnsupported"
        return list_

    @classmethod
    def __getDefinition(cls):
        list_ = dict()
        list_[Definition.OBJECT_ATTRIBUTE_INCONSISTENT] = "ObjectAttributeInconsistent"
        list_[Definition.OBJECT_CLASS_INCONSISTENT] = "ObjectClassInconsistent"
        list_[Definition.OBJECT_UNDEFINED] = "ObjectUndefined"
        list_[Definition.OTHER] = "Other"
        return list_

    @classmethod
    def __getAccess(cls):
        list_ = dict()
        list_[Access.HARDWARE_FAULT] = "HardwareFault"
        list_[Access.OBJECT_ACCESS_INVALID] = "ObjectAccessInvalid"
        list_[Access.OBJECT_UNAVAILABLE] = "ObjectUnavailable"
        list_[Access.OTHER] = "Other"
        list_[Access.SCOPE_OF_ACCESS_VIOLATED] = "ScopeOfAccessViolated"
        return list_

    @classmethod
    def __getInitiate(cls):
        list_ = dict()
        list_[Initiate.DLMS_VERSION_TOO_LOW] = "DlmsVersionTooLow"
        list_[Initiate.INCOMPATIBLE_CONFORMANCE] = "IncompatibleConformance"
        list_[Initiate.OTHER] = "Other"
        list_[Initiate.PDU_SIZE_TOO_SHORT] = "PduSizeTooShort"
        list_[Initiate.REFUSED_BY_THE_VDE_HANDLER] = "RefusedByTheVDEHandler"
        return list_

    @classmethod
    def __getLoadDataSet(cls):
        list_ = dict()
        list_[LoadDataSet.DATASET_NOT_READY] = "DataSetNotReady"
        list_[LoadDataSet.DATASET_SIZE_TOO_LARGE] = "DatasetSizeTooLarge"
        list_[LoadDataSet.INTERPRETATION_FAILURE] = "InterpretationFailure"
        list_[LoadDataSet.NOT_AWAITED_SEGMENT] = "NotAwaitedSegment"
        list_[LoadDataSet.NOT_LOADABLE] = "NotLoadable"
        list_[LoadDataSet.OTHER] = "Other"
        list_[LoadDataSet.PRIMITIVE_OUT_OF_SEQUENCE] = "PrimitiveOutOfSequence"
        list_[LoadDataSet.STORAGE_FAILURE] = "StorageFailure"
        return list_

    @classmethod
    def __getTask(cls):
        list_ = dict()
        list_[Task.NO_REMOTE_CONTROL] = "NoRemoteControl"
        list_[Task.OTHER] = "Other"
        list_[Task.TI_RUNNING] = "tiRunning"
        list_[Task.TI_STOPPED] = "tiStopped"
        list_[Task.TI_UNUSABLE] = "tiUnusable"
        return list_

    @classmethod
    def getServiceErrorValue(cls, error, value):
        if error == ServiceError.APPLICATION_REFERENCE:
            str_ = cls.__getApplicationReference().get(ApplicationReference(value))
        elif error == ServiceError.HARDWARE_RESOURCE:
            str_ = cls.__getHardwareResource().get(HardwareResource(value))
        elif error == ServiceError.VDE_STATE_ERROR:
            str_ = cls.__getVdeStateError().get(VdeStateError(value))
        elif error == ServiceError.SERVICE:
            str_ = cls.__getService().get(Service(value))
        elif error == ServiceError.DEFINITION:
            str_ = cls.__getDefinition().get(Definition(value))
        elif error == ServiceError.ACCESS:
            str_ = cls.__getAccess().get(Access(value))
        elif error == ServiceError.INITIATE:
            str_ = cls.__getInitiate().get(Initiate(value))
        elif error == ServiceError.LOAD_DATASET:
            str_ = cls.__getLoadDataSet().get(LoadDataSet(value))
        elif error == ServiceError.TASK:
            str_ = cls.__getTask().get(Task(value))
        elif error == ServiceError.OTHER_ERROR:
            str_ = str(value)
        else:
            str_ = ""
        return str_

    #
    # @param error
    # Service error enumeration value.
    # Service error simple XML tag.
    #
    @classmethod
    def serviceErrorToString(cls, error):
        return cls.__getServiceErrors().get(error)

    @classmethod
    def __getApplicationReferenceByValue(cls, value):
        ret = None
        for k, v in cls.__getApplicationReference().items():
            if value == v:
                ret = k
                break
        if ret is None:
            raise ValueError()
        return ret

    #
    # @param value
    # Service error simple XML tag.
    # Service error enumeration value.
    #
    @classmethod
    def getServiceError(cls, value):
        error = None
        for k, v in cls.__getServiceErrors().items():
            if value == v:
                error = k
                break
        if error is None:
            raise ValueError()
        return error

    @classmethod
    def __getHardwareResourceByValue(cls, value):
        ret = None
        for k, v in cls.__getHardwareResource().items():
            if value == v:
                ret = k
                break
        if ret is None:
            raise ValueError()
        return ret

    @classmethod
    def __getVdeStateErrorByValue(cls, value):
        ret = None
        for k, v in cls.__getVdeStateError().items():
            if value == v:
                ret = k
                break
        if ret is None:
            raise ValueError()
        return ret

    @classmethod
    def __getServiceByValue(cls, value):
        ret = None
        for k, v in cls.__getService().items():
            if value == v:
                ret = k
                break
        if ret is None:
            raise ValueError()
        return ret

    @classmethod
    def __getDefinitionByValue(cls, value):
        ret = None
        for k, v in cls.__getDefinition().items():
            if value == v:
                ret = k
                break
        if ret is None:
            raise ValueError()
        return ret

    @classmethod
    def __getAccessByValue(cls, value):
        ret = None
        for k, v in cls.__getAccess().items():
            if value == v:
                ret = k
                break
        if ret is None:
            raise ValueError()
        return ret

    @classmethod
    def getInitiateByValue(cls, value):
        ret = None
        for k, v in cls.__getInitiate().items():
            if value == v:
                ret = k
                break
        if ret is None:
            raise ValueError()
        return ret

    @classmethod
    def __getLoadDataSetByValue(cls, value):
        ret = None
        for k, v in cls.__getLoadDataSet().items():
            if value == v:
                ret = k
                break
        if ret is None:
            raise ValueError()
        return ret

    @classmethod
    def __getTaskByValue(cls, value):
        ret = None
        for k, v in cls.__getTask().items():
            if value == v:
                ret = k
                break
        if ret is None:
            raise ValueError()
        return ret

    @classmethod
    def getError(cls, serviceError, value):
        ret = 0
        if serviceError == ServiceError.APPLICATION_REFERENCE:
            ret = cls.__getApplicationReferenceByValue(value)
        elif serviceError == ServiceError.HARDWARE_RESOURCE:
            ret = cls.__getHardwareResourceByValue(value)
        elif serviceError == ServiceError.VDE_STATE_ERROR:
            ret = cls.__getVdeStateErrorByValue(value)
        elif serviceError == ServiceError.SERVICE:
            ret = cls.__getServiceByValue(value)
        elif serviceError == ServiceError.DEFINITION:
            ret = cls.__getDefinitionByValue(value)
        elif serviceError == ServiceError.ACCESS:
            ret = cls.__getAccessByValue(value)
        elif serviceError == ServiceError.INITIATE:
            ret = cls.getInitiateByValue(value)
        elif serviceError == ServiceError.LOAD_DATASET:
            ret = cls.__getLoadDataSetByValue(value)
        elif serviceError == ServiceError.TASK:
            ret = cls.__getTaskByValue(value)
        elif serviceError == ServiceError.OTHER_ERROR:
            ret = int(value)
        return ret

    @classmethod
    def conformancetoString(cls, value):
        str_ = None
        if value == Conformance.ACCESS:
            str_ = "Access"
        elif value == Conformance.ACTION:
            str_ = "Action"
        elif value == Conformance.ATTRIBUTE_0_SUPPORTED_WITH_GET:
            str_ = "Attribute0SupportedWithGet"
        elif value == Conformance.ATTRIBUTE_0_SUPPORTED_WITH_SET:
            str_ = "Attribute0SupportedWithSet"
        elif value == Conformance.BLOCK_TRANSFER_WITH_ACTION:
            str_ = "BlockTransferWithAction"
        elif value == Conformance.BLOCK_TRANSFER_WITH_GET_OR_READ:
            str_ = "BlockTransferWithGetOrRead"
        elif value == Conformance.BLOCK_TRANSFER_WITH_SET_OR_WRITE:
            str_ = "BlockTransferWithSetOrWrite"
        elif value == Conformance.DATA_NOTIFICATION:
            str_ = "DataNotification"
        elif value == Conformance.EVENT_NOTIFICATION:
            str_ = "EventNotification"
        elif value == Conformance.GENERAL_BLOCK_TRANSFER:
            str_ = "GeneralBlockTransfer"
        elif value == Conformance.GENERAL_PROTECTION:
            str_ = "GeneralProtection"
        elif value == Conformance.GET:
            str_ = "Get"
        elif value == Conformance.INFORMATION_REPORT:
            str_ = "InformationReport"
        elif value == Conformance.MULTIPLE_REFERENCES:
            str_ = "MultipleReferences"
        elif value == Conformance.PARAMETERIZED_ACCESS:
            str_ = "ParameterizedAccess"
        elif value == Conformance.PRIORITY_MGMT_SUPPORTED:
            str_ = "PriorityMgmtSupported"
        elif value == Conformance.READ:
            str_ = "Read"
        elif value == Conformance.RESERVED_SEVEN:
            str_ = "ReservedSeven"
        elif value == Conformance.RESERVED_SIX:
            str_ = "ReservedSix"
        elif value == Conformance.RESERVED_ZERO:
            str_ = "ReservedZero"
        elif value == Conformance.SELECTIVE_ACCESS:
            str_ = "SelectiveAccess"
        elif value == Conformance.SET:
            str_ = "Set"
        elif value == Conformance.UN_CONFIRMED_WRITE:
            str_ = "UnconfirmedWrite"
        elif value == Conformance.WRITE:
            str_ = "Write"
        else:
            raise ValueError(str(value))
        return str_

    @classmethod
    def value_ofConformance(cls, value):
        ret = None
        if "Access".lower() == value.lower():
            ret = Conformance.ACCESS
        elif "Action".lower() == value.lower():
            ret = Conformance.ACTION
        elif "Attribute0SupportedWithGet".lower() == value.lower():
            ret = Conformance.ATTRIBUTE_0_SUPPORTED_WITH_GET
        elif "Attribute0SupportedWithSet".lower() == value.lower():
            ret = Conformance.ATTRIBUTE_0_SUPPORTED_WITH_SET
        elif "BlockTransferWithAction".lower() == value.lower():
            ret = Conformance.BLOCK_TRANSFER_WITH_ACTION
        elif "BlockTransferWithGetOrRead".lower() == value.lower():
            ret = Conformance.BLOCK_TRANSFER_WITH_GET_OR_READ
        elif "BlockTransferWithSetOrWrite".lower() == value.lower():
            ret = Conformance.BLOCK_TRANSFER_WITH_SET_OR_WRITE
        elif "DataNotification".lower() == value.lower():
            ret = Conformance.DATA_NOTIFICATION
        elif "EventNotification".lower() == value.lower():
            ret = Conformance.EVENT_NOTIFICATION
        elif "GeneralBlockTransfer".lower() == value.lower():
            ret = Conformance.GENERAL_BLOCK_TRANSFER
        elif "GeneralProtection".lower() == value.lower():
            ret = Conformance.GENERAL_PROTECTION
        elif "Get".lower() == value.lower():
            ret = Conformance.GET
        elif "InformationReport".lower() == value.lower():
            ret = Conformance.INFORMATION_REPORT
        elif "MultipleReferences".lower() == value.lower():
            ret = Conformance.MULTIPLE_REFERENCES
        elif "ParameterizedAccess".lower() == value.lower():
            ret = Conformance.PARAMETERIZED_ACCESS
        elif "PriorityMgmtSupported".lower() == value.lower():
            ret = Conformance.PRIORITY_MGMT_SUPPORTED
        elif "Read".lower() == value.lower():
            ret = Conformance.READ
        elif "ReservedSeven".lower() == value.lower():
            ret = Conformance.RESERVED_SEVEN
        elif "ReservedSix".lower() == value.lower():
            ret = Conformance.RESERVED_SIX
        elif "ReservedZero".lower() == value.lower():
            ret = Conformance.RESERVED_ZERO
        elif "SelectiveAccess".lower() == value.lower():
            ret = Conformance.SELECTIVE_ACCESS
        elif "Set".lower() == value.lower():
            ret = Conformance.SET
        elif "UnconfirmedWrite".lower() == value.lower():
            ret = Conformance.UN_CONFIRMED_WRITE
        elif "Write".lower() == value.lower():
            ret = Conformance.WRITE
        else:
            raise ValueError(value)
        return ret

    @classmethod
    def releaseResponseReasonToString(cls, value):
        str_ = None
        if value == ReleaseResponseReason.NORMAL:
            str_ = "Normal"
        elif value == ReleaseResponseReason.NOT_FINISHED:
            str_ = "NotFinished"
        elif value == ReleaseResponseReason.USER_DEFINED:
            str_ = "UserDefined"
        else:
            raise ValueError(str(value))
        return str_

    @classmethod
    def value_ofReleaseResponseReason(cls, value):
        ret = None
        if "Normal".lower() == value.lower():
            ret = ReleaseResponseReason.NORMAL
        elif "NotFinished".lower() == value.lower():
            ret = ReleaseResponseReason.NOT_FINISHED
        elif "UserDefined".lower() == value.lower():
            ret = ReleaseResponseReason.USER_DEFINED
        else:
            raise ValueError(value)
        return ret

    @classmethod
    def releaseRequestReasonToString(cls, value):
        str_ = None
        if value == ReleaseRequestReason.NORMAL:
            str_ = "Normal"
        elif value == ReleaseRequestReason.URGENT:
            str_ = "Urgent"
        elif value == ReleaseRequestReason.USER_DEFINED:
            str_ = "UserDefined"
        else:
            raise ValueError(str(value))
        return str_

    @classmethod
    def value_ofReleaseRequestReason(cls, value):
        ret = None
        if "Normal".lower() == value.lower():
            ret = ReleaseRequestReason.NORMAL
        elif "Urgent".lower() == value.lower():
            ret = ReleaseRequestReason.URGENT
        elif "UserDefined".lower() == value.lower():
            ret = ReleaseRequestReason.USER_DEFINED
        else:
            raise ValueError(value)
        return ret

    @classmethod
    def stateErrorToString(cls, value):
        if value == StateError.SERVICE_NOT_ALLOWED:
            ret = "ServiceNotAllowed"
        elif value == StateError.SERVICE_UNKNOWN:
            ret = "ServiceUnknown"
        else:
            raise ValueError(value)
        return ret

    @classmethod
    def exceptionServiceErrorToString(cls, value):
        if value == ExceptionServiceError.OPERATION_NOT_POSSIBLE:
            ret = "OperationNotPossible"
        elif value == ExceptionServiceError.SERVICE_NOT_SUPPORTED:
            ret = "ServiceNotSupported"
        elif value == ExceptionServiceError.OTHER_REASON:
            ret = "OtherReason"
        else:
            raise ValueError(value)
        return ret

    @classmethod
    def valueofStateError(cls, value):
        if "ServiceNotAllowed".lower() == value.lower():
            ret = StateError.SERVICE_NOT_ALLOWED
        elif "ServiceUnknown".lower() == value.lower():
            ret = StateError.SERVICE_UNKNOWN
        else:
            raise ValueError(value)
        return ret

    @classmethod
    def valueOfExceptionServiceError(cls, value):
        if "OperationNotPossible".lower() == value.lower():
            ret = ExceptionServiceError.OPERATION_NOT_POSSIBLE
        elif "ServiceNotSupported".lower() == value.lower():
            ret = ExceptionServiceError.SERVICE_NOT_SUPPORTED
        elif "OtherReason".lower() == value.lower():
            ret = ExceptionServiceError.OTHER_REASON
        else:
            raise ValueError(value)
        return ret

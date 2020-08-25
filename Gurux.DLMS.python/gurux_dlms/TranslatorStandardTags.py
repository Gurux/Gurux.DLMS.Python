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
class TranslatorStandardTags:
    # Constructor.
    def __init__(self):
        pass

    #
    # Get general tags.
    #
    # @param type
    # @param list
    #
    @classmethod
    def getGeneralTags(cls, list_):
        list_[Command.SNRM] = "Snrm"
        list_[Command.UNACCEPTABLE_FRAME] = "UnacceptableFrame"
        list_[Command.DISCONNECT_MODE] = "DisconnectMode"
        list_[Command.UA] = "Ua"
        list_[Command.AARQ] = "aarq"
        list_[Command.AARE] = "aare"
        list_[TranslatorGeneralTags.APPLICATION_CONTEXT_NAME] = "application-context-name"
        list_[Command.INITIATE_RESPONSE] = "initiateResponse"
        list_[Command.INITIATE_REQUEST] = "initiateRequest"
        list_[TranslatorGeneralTags.NEGOTIATED_QUALITY_OF_SERVICE] = "negotiated-quality-of-service"
        list_[TranslatorGeneralTags.PROPOSED_QUALITY_OF_SERVICE] = "proposed-quality-of-service"
        list_[TranslatorGeneralTags.PROPOSED_DLMS_VERSION_NUMBER] = "proposed-dlms-version-number"
        list_[TranslatorGeneralTags.PROPOSED_MAX_PDU_SIZE] = "client-max-receive-pdu-size"
        list_[TranslatorGeneralTags.PROPOSED_CONFORMANCE] = "proposed-conformance"
        list_[TranslatorGeneralTags.VAA_NAME] = "vaa-name"
        list_[TranslatorGeneralTags.NEGOTIATED_CONFORMANCE] = "negotiated-conformance"
        list_[TranslatorGeneralTags.NEGOTIATED_DLMS_VERSION_NUMBER] = "negotiated-dlms-version-number"
        list_[TranslatorGeneralTags.NEGOTIATED_MAX_PDU_SIZE] = "server-max-receive-pdu-size"
        list_[TranslatorGeneralTags.CONFORMANCE_BIT] = "ConformanceBit"
        list_[TranslatorGeneralTags.SENDER_ACSE_REQUIREMENTS] = "sender-acse-requirements"
        list_[TranslatorGeneralTags.RESPONDER_ACSE_REQUIREMENT] = "responder-acse-requirements"
        list_[TranslatorGeneralTags.RESPONDING_MECHANISM_NAME] = "mechanism-name"
        list_[TranslatorGeneralTags.CALLING_MECHANISM_NAME] = "mechanism-name"
        list_[TranslatorGeneralTags.CALLING_AUTHENTICATION] = "calling-authentication-value"
        list_[TranslatorGeneralTags.RESPONDING_AUTHENTICATION] = "responding-authentication-value"
        list_[Command.RELEASE_REQUEST] = "rlrq"
        list_[Command.RELEASE_RESPONSE] = "rlre"
        list_[Command.DISCONNECT_REQUEST] = "Disc"
        list_[TranslatorGeneralTags.ASSOCIATION_RESULT] = "result"
        list_[TranslatorGeneralTags.RESULT_SOURCE_DIAGNOSTIC] = "result-source-diagnostic"
        list_[TranslatorGeneralTags.ACSE_SERVICE_USER] = "acse-service-user"
        list_[TranslatorGeneralTags.CALLING_AP_TITLE] = "CallingAPTitle"
        list_[TranslatorGeneralTags.RESPONDING_AP_TITLE] = "RespondingAPTitle"
        list_[TranslatorGeneralTags.CHAR_STRING] = "charstring"
        list_[TranslatorGeneralTags.DEDICATED_KEY] = "dedicated-key"
        list_[TranslatorTags.RESPONSE_ALLOWED] = "response-allowed"
        list_[TranslatorGeneralTags.USER_INFORMATION] = "user-information"
        list_[Command.CONFIRMED_SERVICE_ERROR] = "confirmedServiceError"
        list_[Command.INFORMATION_REPORT] = "informationReportRequest"
        list_[Command.EVENT_NOTIFICATION] = "event-notification-request"
        list_[TranslatorGeneralTags.CALLING_AE_INVOCATION_ID] = "calling-AE-invocation-id"
        list_[TranslatorGeneralTags.CALLED_AE_INVOCATION_ID] = "called-AE-invocation-id"
        list_[TranslatorGeneralTags.RESPONDING_AE_INVOCATION_ID] = "responding-AE-invocation-id"
        list_[Command.EXCEPTION_RESPONSE] = "exception-response"
        list_[TranslatorTags.STATE_ERROR] = "state-error"
        list_[TranslatorTags.SERVICE_ERROR] = "service-error"

    #
    # Get SN tags.
    #
    # @param type
    # @param list
    #
    @classmethod
    def getSnTags(cls, list_):
        list_[Command.READ_REQUEST] = "readRequest"
        list_[Command.WRITE_REQUEST] = "writeRequest"
        list_[Command.WRITE_RESPONSE] = "writeResponse"
        list_[Command.WRITE_REQUEST << 8 | SingleReadResponse.DATA] = "Data"
        list_[Command.READ_REQUEST << 8 | VariableAccessSpecification.VARIABLE_NAME] = "variable-name"
        list_[Command.READ_REQUEST << 8 | VariableAccessSpecification.PARAMETERISED_ACCESS] = "parameterized-access"
        list_[Command.READ_REQUEST << 8 | VariableAccessSpecification.BLOCK_NUMBER_ACCESS] = "BlockNumberAccess"
        list_[Command.WRITE_REQUEST << 8 | VariableAccessSpecification.VARIABLE_NAME] = "variable-name"
        list_[Command.READ_RESPONSE] = "readResponse"
        list_[Command.READ_RESPONSE << 8 | SingleReadResponse.DATA_BLOCK_RESULT] = "DataBlockResult"
        list_[Command.READ_RESPONSE << 8 | SingleReadResponse.DATA] = "data"
        list_[Command.WRITE_RESPONSE << 8 | SingleReadResponse.DATA] = "data"
        list_[Command.READ_RESPONSE << 8 | SingleReadResponse.DATA_ACCESS_ERROR] = "data-access-error"

    #
    # Get LN tags.
    #
    # @param type
    # @param list
    #
    @classmethod
    def getLnTags(cls, list_):
        list_[Command.GET_REQUEST] = "get-request"
        list_[Command.GET_REQUEST << 8 | GetCommandType.NORMAL] = "get-request-normal"
        list_[Command.GET_REQUEST << 8 | GetCommandType.NEXT_DATA_BLOCK] = "get-request-next"
        list_[Command.GET_REQUEST << 8 | GetCommandType.WITH_LIST] = "get-request-with-list"
        list_[Command.SET_REQUEST] = "set-request"
        list_[Command.SET_REQUEST << 8 | SetRequestType.NORMAL] = "set-request-normal"
        list_[Command.SET_REQUEST << 8 | SetRequestType.FIRST_DATA_BLOCK] = "set-request-first-data-block"
        list_[Command.SET_REQUEST << 8 | SetRequestType.WITH_DATA_BLOCK] = "set-request-with-datablock"
        list_[Command.SET_REQUEST << 8 | SetRequestType.WITH_LIST] = "set-request-with-list"
        list_[Command.METHOD_REQUEST] = "action-request"
        list_[Command.METHOD_REQUEST << 8 | ActionRequestType.NORMAL] = "action-request-normal"
        list_[Command.METHOD_REQUEST << 8 | ActionRequestType.NEXT_BLOCK] = "ActionRequestForNextDataBlock"
        list_[Command.METHOD_REQUEST << 8 | ActionRequestType.WITH_LIST] = "action-request-with-list"
        list_[Command.METHOD_RESPONSE] = "action-response"
        list_[Command.METHOD_RESPONSE << 8 | ActionResponseType.NORMAL] = "action-response-normal"
        list_[Command.METHOD_RESPONSE << 8 | ActionResponseType.WITH_FIRST_BLOCK] = "action-response-with-first-block"
        list_[Command.METHOD_RESPONSE << 8 | ActionResponseType.WITH_LIST] = "action-response-with-list"
        list_[TranslatorTags.SINGLE_RESPONSE] = "single-response"
        list_[int(Command.DATA_NOTIFICATION)] = "data-notification"
        list_[Command.GET_RESPONSE] = "get-response"
        list_[Command.GET_RESPONSE << 8 | GetCommandType.NORMAL] = "get-response-normal"
        list_[Command.GET_RESPONSE << 8 | GetCommandType.NEXT_DATA_BLOCK] = "get-response-with-data-block"
        list_[Command.GET_RESPONSE << 8 | GetCommandType.WITH_LIST] = "get-response-with-list"
        list_[Command.SET_RESPONSE] = "set-response"
        list_[Command.SET_RESPONSE << 8 | SetResponseType.NORMAL] = "set-response-normal"
        list_[Command.SET_RESPONSE << 8 | SetResponseType.DATA_BLOCK] = "set-response-data-block"
        list_[Command.SET_RESPONSE << 8 | SetResponseType.LAST_DATA_BLOCK] = "set-response-with-last-data-block"
        list_[Command.SET_RESPONSE << 8 | SetResponseType.WITH_LIST] = "set-response-with-list"
        list_[Command.ACCESS_REQUEST] = "access-request"
        list_[(Command.ACCESS_REQUEST) << 8 | AccessServiceCommandType.GET] = "access-request-get"
        list_[(Command.ACCESS_REQUEST) << 8 | AccessServiceCommandType.SET] = "access-request-set"
        list_[(Command.ACCESS_REQUEST) << 8 | AccessServiceCommandType.ACTION] = "access-request-action"
        list_[Command.ACCESS_RESPONSE] = "access-response"
        list_[(Command.ACCESS_RESPONSE) << 8 | AccessServiceCommandType.GET] = "access-response-get"
        list_[(Command.ACCESS_RESPONSE) << 8 | AccessServiceCommandType.SET] = "access-response-set"
        list_[(Command.ACCESS_RESPONSE) << 8 | AccessServiceCommandType.ACTION] = "access-response-action"
        list_[TranslatorTags.ACCESS_REQUEST_BODY] = "access-request-body"
        list_[TranslatorTags.LIST_OF_ACCESS_REQUEST_SPECIFICATION] = "access-request-specification"
        list_[TranslatorTags.ACCESS_REQUEST_SPECIFICATION] = "Access-Request-Specification"
        list_[TranslatorTags.ACCESS_REQUEST_LIST_OF_DATA] = "access-request-list-of-data"
        list_[TranslatorTags.ACCESS_RESPONSE_BODY] = "access-response-body"
        list_[TranslatorTags.LIST_OF_ACCESS_RESPONSE_SPECIFICATION] = "access-response-specification"
        list_[TranslatorTags.ACCESS_RESPONSE_SPECIFICATION] = "Access-Response-Specification"
        list_[TranslatorTags.ACCESS_RESPONSE_LIST_OF_DATA] = "access-response-list-of-data"
        list_[TranslatorTags.SERVICE] = "service"
        list_[TranslatorTags.SERVICE_ERROR] = "service-error"
        list_[Command.GENERAL_BLOCK_TRANSFER] = "general-block-transfer"
        list_[Command.GATEWAY_REQUEST] = "gateway-request"
        list_[Command.GATEWAY_RESPONSE] = "gateway-response"

    #
    # Get glo tags.
    #
    # @param type
    # @param list
    #
    @classmethod
    def getGloTags(cls, list_):
        list_[Command.GLO_INITIATE_REQUEST] = "glo-initiate-request"
        list_[Command.GLO_INITIATE_RESPONSE] = "glo-initiate-response"
        list_[Command.GLO_GET_REQUEST] = "glo-get-request"
        list_[Command.GLO_GET_RESPONSE] = "glo-get-response"
        list_[Command.GLO_SET_REQUEST] = "glo-set-request"
        list_[Command.GLO_SET_RESPONSE] = "glo-set-response"
        list_[Command.GLO_METHOD_REQUEST] = "glo-action-request"
        list_[Command.GLO_METHOD_RESPONSE] = "glo-action-response"
        list_[Command.GLO_READ_REQUEST] = "glo-read-request"
        list_[Command.GLO_READ_RESPONSE] = "glo-read-response"
        list_[Command.GLO_WRITE_REQUEST] = "glo-write-request"
        list_[Command.GLO_WRITE_RESPONSE] = "glo-write-response"
        list_[Command.GENERAL_GLO_CIPHERING] = "general-glo-ciphering"
        list_[Command.GENERAL_CIPHERING] = "general-ciphering"
        list_[Command.GLO_CONFIRMED_SERVICE_ERROR] = "glo-confirmed-service-error"

    #
    # Get ded tags.
    #
    # @param type
    # @param list
    #
    @classmethod
    def getDedTags(cls, list_):
        list_[Command.DED_GET_REQUEST] = "ded-get-request"
        list_[Command.DED_GET_RESPONSE] = "ded-get-response"
        list_[Command.DED_SET_REQUEST] = "ded-set-request"
        list_[Command.DED_SET_RESPONSE] = "ded-set-response"
        list_[Command.DED_METHOD_REQUEST] = "ded-action-request"
        list_[Command.DED_METHOD_RESPONSE] = "ded-action-response"
        list_[Command.GENERAL_DED_CIPHERING] = "general-ded-ciphering"
        list_[Command.DED_CONFIRMED_SERVICE_ERROR] = "ded-confirmed-service-error"

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
        list_[TranslatorTags.PDU_DLMS] = "xDLMS-APDU"
        list_[TranslatorTags.PDU_CSE] = "aCSE-APDU"
        list_[TranslatorTags.TARGET_ADDRESS] = "TargetAddress"
        list_[TranslatorTags.SOURCE_ADDRESS] = "SourceAddress"
        list_[TranslatorTags.FRAME_TYPE] = "FrameType"
        list_[TranslatorTags.LIST_OF_VARIABLE_ACCESS_SPECIFICATION] = "variable-access-specification"
        list_[TranslatorTags.LIST_OF_DATA] = "list-of-data"
        list_[TranslatorTags.SUCCESS] = "Success"
        list_[TranslatorTags.DATA_ACCESS_ERROR] = "data-access-result"
        list_[TranslatorTags.ATTRIBUTE_DESCRIPTOR] = "cosem-attribute-descriptor"
        list_[TranslatorTags.CLASS_ID] = "class-id"
        list_[TranslatorTags.INSTANCE_ID] = "instance-id"
        list_[TranslatorTags.ATTRIBUTE_ID] = "attribute-id"
        list_[TranslatorTags.METHOD_INVOCATION_PARAMETERS] = "method-invocation-parameters"
        list_[TranslatorTags.SELECTOR] = "selector"
        list_[TranslatorTags.PARAMETER] = "parameter"
        list_[TranslatorTags.LAST_BLOCK] = "last-block"
        list_[TranslatorTags.BLOCK_NUMBER] = "block-number"
        list_[TranslatorTags.RAW_DATA] = "raw-data"
        list_[TranslatorTags.METHOD_DESCRIPTOR] = "cosem-method-descriptor"
        list_[TranslatorTags.METHOD_ID] = "method-id"
        list_[TranslatorTags.RESULT] = "result"
        list_[TranslatorTags.RETURN_PARAMETERS] = "return-parameters"
        list_[TranslatorTags.ACCESS_SELECTION] = "access-selection"
        list_[TranslatorTags.VALUE] = "value"
        list_[TranslatorTags.ACCESS_SELECTOR] = "access-selector"
        list_[TranslatorTags.ACCESS_PARAMETERS] = "access-parameters"
        list_[TranslatorTags.ATTRIBUTE_DESCRIPTOR_LIST] = "attribute-descriptor-list"
        list_[TranslatorTags.ATTRIBUTE_DESCRIPTOR_WITH_SELECTION] = "Cosem-Attribute-Descriptor-With-Selection"
        list_[TranslatorTags.READ_DATA_BLOCK_ACCESS] = "ReadDataBlockAccess"
        list_[TranslatorTags.WRITE_DATA_BLOCK_ACCESS] = "WriteDataBlockAccess"
        list_[TranslatorTags.DATA] = "data"
        list_[TranslatorTags.INVOKE_ID] = "invoke-id-and-priority"
        list_[TranslatorTags.LONG_INVOKE_ID] = "long-invoke-id-and-priority"
        list_[TranslatorTags.DATE_TIME] = "date-time"
        list_[TranslatorTags.CURRENT_TIME] = "current-time"
        list_[TranslatorTags.TIME] = "time"
        list_[TranslatorTags.REASON] = "reason"
        list_[TranslatorTags.VARIABLE_ACCESS_SPECIFICATION] = "Variable-Access-Specification"
        list_[TranslatorTags.CHOICE] = "CHOICE"
        list_[TranslatorTags.NOTIFICATION_BODY] = "notification-body"
        list_[TranslatorTags.DATA_VALUE] = "data-value"
        list_[TranslatorTags.INITIATE_ERROR] = "initiateError"
        list_[TranslatorTags.CIPHERED_SERVICE] = "ciphered-content"
        list_[TranslatorTags.SYSTEM_TITLE] = "system-title"
        list_[TranslatorTags.DATA_BLOCK] = "datablock"
        list_[TranslatorTags.TRANSACTION_ID] = "transaction-id"
        list_[TranslatorTags.ORIGINATOR_SYSTEM_TITLE] = "originator-system-title"
        list_[TranslatorTags.RECIPIENT_SYSTEM_TITLE] = "recipient-system-title"
        list_[TranslatorTags.OTHER_INFORMATION] = "other-information"
        list_[TranslatorTags.KEY_INFO] = "key-info"
        list_[TranslatorTags.CIPHERED_CONTENT] = "ciphered-content"
        list_[TranslatorTags.AGREED_KEY] = "agreed-key"
        list_[TranslatorTags.KEY_PARAMETERS] = "key-parameters"
        list_[TranslatorTags.KEY_CIPHERED_DATA] = "key-ciphered-data"
        list_[TranslatorTags.ATTRIBUTE_VALUE] = "attribute-value"
        list_[TranslatorTags.MAX_INFO_RX] = "MaxInfoRX"
        list_[TranslatorTags.MAX_INFO_TX] = "MaxInfoTX"
        list_[TranslatorTags.WINDOW_SIZE_RX] = "WindowSizeRX"
        list_[TranslatorTags.WINDOW_SIZE_TX] = "WindowSizeTX"
        list_[TranslatorTags.VALUE_LIST] = "value-list"
        list_[TranslatorTags.DATA_ACCESS_RESULT] = "data-access-result"
        list_[TranslatorTags.BLOCK_CONTROL] = "block-control"
        list_[TranslatorTags.BLOCK_NUMBER_ACK] = "block-number-ack"
        list_[TranslatorTags.BLOCK_DATA] = "block-data"
        list_[TranslatorTags.CONTENTS_DESCRIPTION] = "contents-description"
        list_[TranslatorTags.ARRAY_CONTENTS] = "array-contents"
        list_[TranslatorTags.NETWORK_ID] = "network-id"
        list_[TranslatorTags.PHYSICAL_DEVICE_ADDRESS] = "physical-device-address"
        list_[TranslatorTags.PROTOCOL_VERSION] = "protocol-version"
        list_[TranslatorTags.CALLED_AP_TITLE] = "called-ap-title"
        list_[TranslatorTags.CALLED_AP_INVOCATION_ID] = "called-ap-invocation-id"
        list_[TranslatorTags.CALLED_AE_INVOCATION_ID] = "called-ae-invocation-id"
        list_[TranslatorTags.CALLING_AP_INVOCATION_ID] = "calling-ap-invocation-id"
        list_[TranslatorTags.CALLED_AE_QUALIFIER] = "called-ae-qualifier"

    @classmethod
    def getDataTypeTags(cls, list_):
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.NONE] = "null-data"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.ARRAY] = "array"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.BCD] = "bcd"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.BITSTRING] = "bit-string"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.BOOLEAN] = "boolean"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.COMPACT_ARRAY] = "compact-array"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.DATE] = "date"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.DATETIME] = "date-time"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.ENUM] = "enum"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.FLOAT32] = "float32"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.FLOAT64] = "float64,"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.INT16] = "long"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.INT32] = "double-long"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.INT64] = "long64"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.INT8] = "integer"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.OCTET_STRING] = "octet-string"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.STRING] = "visible-string"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.STRING_UTF8] = "utf8-string"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.STRUCTURE] = "structure"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.TIME] = "time"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.UINT16] = "long-unsigned"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.UINT32] = "double-long-unsigned"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.UINT64] = "long64-unsigned"
        list_[_GXCommon.DATA_TYPE_OFFSET + DataType.UINT8] = "unsigned"

    @classmethod
    def errorCodeToString(cls, value):
        value = ErrorCode(value)
        str_ = None
        if value == ErrorCode.ACCESS_VIOLATED:
            str_ = "scope-of-access-violated"
        elif value == ErrorCode.DATA_BLOCK_NUMBER_INVALID:
            str_ = "data-block-number-invalid"
        elif value == ErrorCode.DATA_BLOCK_UNAVAILABLE:
            str_ = "data-block-unavailable"
        elif value == ErrorCode.HARDWARE_FAULT:
            str_ = "hardware-fault"
        elif value == ErrorCode.INCONSISTENT_CLASS:
            str_ = "object-class-inconsistent"
        elif value == ErrorCode.LONG_GET_OR_READ_ABORTED:
            str_ = "long-get-aborted"
        elif value == ErrorCode.LONG_SET_OR_WRITE_ABORTED:
            str_ = "long-set-aborted"
        elif value == ErrorCode.NO_LONG_GET_OR_READ_IN_PROGRESS:
            str_ = "no-long-get-in-progress"
        elif value == ErrorCode.NO_LONG_SET_OR_WRITE_IN_PROGRESS:
            str_ = "no-long-set-in-progress"
        elif value == ErrorCode.OK:
            str_ = "success"
        elif value == ErrorCode.OTHER_REASON:
            str_ = "other-reason"
        elif value == ErrorCode.READ_WRITE_DENIED:
            str_ = "read-write-denied"
        elif value == ErrorCode.TEMPORARY_FAILURE:
            str_ = "temporary-failure"
        elif value == ErrorCode.UNAVAILABLE_OBJECT:
            str_ = "object-unavailable"
        elif value == ErrorCode.UNDEFINED_OBJECT:
            str_ = "object-undefined"
        elif value == ErrorCode.UNMATCHED_TYPE:
            str_ = "type-unmatched"
        else:
            raise ValueError("Error code: " + str(value))
        return str_

    @classmethod
    def value_ofErrorCode(cls, value):
        v = None
        if "scope-of-access-violated".lower() == value.lower():
            v = ErrorCode.ACCESS_VIOLATED
        elif "data-block-number-invalid".lower() == value.lower():
            v = ErrorCode.DATA_BLOCK_NUMBER_INVALID
        elif "data-block-unavailable".lower() == value.lower():
            v = ErrorCode.DATA_BLOCK_UNAVAILABLE
        elif "hardware-fault".lower() == value.lower():
            v = ErrorCode.HARDWARE_FAULT
        elif "object-class-inconsistent".lower() == value.lower():
            v = ErrorCode.INCONSISTENT_CLASS
        elif "long-get-aborted".lower() == value.lower():
            v = ErrorCode.LONG_GET_OR_READ_ABORTED
        elif "long-set-aborted".lower() == value.lower():
            v = ErrorCode.LONG_SET_OR_WRITE_ABORTED
        elif "no-long-get-in-progress".lower() == value.lower():
            v = ErrorCode.NO_LONG_GET_OR_READ_IN_PROGRESS
        elif "no-long-set-in-progress".lower() == value.lower():
            v = ErrorCode.NO_LONG_SET_OR_WRITE_IN_PROGRESS
        elif "success".lower() == value.lower():
            v = ErrorCode.OK
        elif "other-reason".lower() == value.lower():
            v = ErrorCode.OTHER_REASON
        elif "read-write-denied".lower() == value.lower():
            v = ErrorCode.READ_WRITE_DENIED
        elif "temporary-failure".lower() == value.lower():
            v = ErrorCode.TEMPORARY_FAILURE
        elif "object-unavailable".lower() == value.lower():
            v = ErrorCode.UNAVAILABLE_OBJECT
        elif "object-undefined".lower() == value.lower():
            v = ErrorCode.UNDEFINED_OBJECT
        elif "type-unmatched".lower() == value.lower():
            v = ErrorCode.UNMATCHED_TYPE
        else:
            raise ValueError("Error code: " + value)
        return v

    @classmethod
    def __getServiceErrors(cls):
        list_ = dict()
        list_[ServiceError.APPLICATION_REFERENCE] = "application-reference"
        list_[ServiceError.HARDWARE_RESOURCE] = "hardware-resource"
        list_[ServiceError.VDE_STATE_ERROR] = "vde-state-error"
        list_[ServiceError.SERVICE] = "service"
        list_[ServiceError.DEFINITION] = "definition"
        list_[ServiceError.ACCESS] = "access"
        list_[ServiceError.INITIATE] = "initiate"
        list_[ServiceError.LOAD_DATASET] = "load-data-set"
        list_[ServiceError.TASK] = "task"
        return list_

    @classmethod

    def __getApplicationReference(cls):
        list_ = dict()
        list_[ApplicationReference.APPLICATION_CONTEXT_UNSUPPORTED] = "application-context-unsupported"
        list_[ApplicationReference.APPLICATION_REFERENCE_INVALID] = "application-reference-invalid"
        list_[ApplicationReference.APPLICATION_UNREACHABLE] = "application-unreachable"
        list_[ApplicationReference.DECIPHERING_ERROR] = "deciphering-error"
        list_[ApplicationReference.OTHER] = "other"
        list_[ApplicationReference.PROVIDER_COMMUNICATION_ERROR] = "provider-communication-error"
        list_[ApplicationReference.TIME_ELAPSED] = "time-elapsed"
        return list_

    @classmethod
    def __getHardwareResource(cls):
        list_ = dict()
        list_[HardwareResource.MASS_STORAGE_UNAVAILABLE] = "mass-storage-unavailable"
        list_[HardwareResource.MEMORY_UNAVAILABLE] = "memory-unavailable"
        list_[HardwareResource.OTHER] = "other"
        list_[HardwareResource.OTHER_RESOURCE_UNAVAILABLE] = "other-resource-unavailable"
        list_[HardwareResource.PROCESSOR_RESOURCE_UNAVAILABLE] = "processor-resource-unavailable"
        return list_

    @classmethod
    def __getVdeStateError(cls):
        list_ = dict()
        list_[VdeStateError.LOADING_DATASET] = "loading-data-set"
        list_[VdeStateError.NO_DLMS_CONTEXT] = "no-dlms-context"
        list_[VdeStateError.OTHER] = "other"
        list_[VdeStateError.STATUS_INOPERABLE] = "status-inoperable"
        list_[VdeStateError.STATUS_NO_CHANGE] = "status-nochange"
        return list_

    @classmethod
    def __getService(cls):
        list_ = dict()
        list_[Service.OTHER] = "other"
        list_[Service.PDU_SIZE] = "pdu-size"
        list_[Service.UNSUPPORTED] = "service-unsupported"
        return list_

    @classmethod
    def __getDefinition(cls):
        list_ = dict()
        list_[Definition.OBJECT_ATTRIBUTE_INCONSISTENT] = "object-attribute-inconsistent"
        list_[Definition.OBJECT_CLASS_INCONSISTENT] = "object-class-inconsistent"
        list_[Definition.OBJECT_UNDEFINED] = "object-undefined"
        list_[Definition.OTHER] = "other"
        return list_

    @classmethod
    def __getAccess(cls):
        list_ = dict()
        list_[Access.HARDWARE_FAULT] = "hardware-fault"
        list_[Access.OBJECT_ACCESS_INVALID] = "object-access-violated"
        list_[Access.OBJECT_UNAVAILABLE] = "object-unavailable"
        list_[Access.OTHER] = "other"
        list_[Access.SCOPE_OF_ACCESS_VIOLATED] = "scope-of-access-violated"
        return list_

    @classmethod
    def __getInitiate(cls):
        list_ = dict()
        list_[Initiate.DLMS_VERSION_TOO_LOW] = "dlms-version-too-low"
        list_[Initiate.INCOMPATIBLE_CONFORMANCE] = "incompatible-conformance"
        list_[Initiate.OTHER] = "other"
        list_[Initiate.PDU_SIZE_TOO_SHORT] = "pdu-size-too-short"
        list_[Initiate.REFUSED_BY_THE_VDE_HANDLER] = "refused-by-the-VDE-Handler"
        return list_

    @classmethod
    def __getLoadDataSet(cls):
        list_ = dict()
        list_[LoadDataSet.DATASET_NOT_READY] = "data-set-not-ready"
        list_[LoadDataSet.DATASET_SIZE_TOO_LARGE] = "dataset-size-too-large"
        list_[LoadDataSet.INTERPRETATION_FAILURE] = "interpretation-failure"
        list_[LoadDataSet.NOT_AWAITED_SEGMENT] = "not-awaited-segment"
        list_[LoadDataSet.NOT_LOADABLE] = "not-loadable"
        list_[LoadDataSet.OTHER] = "other"
        list_[LoadDataSet.PRIMITIVE_OUT_OF_SEQUENCE] = "primitive-out-of-sequence"
        list_[LoadDataSet.STORAGE_FAILURE] = "storage-failure"
        return list_

    @classmethod
    def __getTask(cls):
        list_ = dict()
        list_[Task.NO_REMOTE_CONTROL] = "no-remote-control"
        list_[Task.OTHER] = "other"
        list_[Task.TI_RUNNING] = "ti-running"
        list_[Task.TI_STOPPED] = "ti-stopped"
        list_[Task.TI_UNUSABLE] = "ti-unusable"
        return list_

    @classmethod
    def getServiceErrorValue(cls, error, value):
        ret = ""
        if error == ServiceError.APPLICATION_REFERENCE:
            ret = cls.__getApplicationReference().get(ApplicationReference(value))
        elif error == ServiceError.HARDWARE_RESOURCE:
            ret = cls.__getHardwareResource().get(HardwareResource(value))
        elif error == ServiceError.VDE_STATE_ERROR:
            ret = cls.__getVdeStateError().get(VdeStateError(value))
        elif error == ServiceError.SERVICE:
            ret = cls.__getService().get(Service(value))
        elif error == ServiceError.DEFINITION:
            ret = cls.__getDefinition().get(Definition(value))
        elif error == ServiceError.ACCESS:
            ret = cls.__getAccess().get(Access(value))
        elif error == ServiceError.INITIATE:
            ret = cls.__getInitiate().get(Initiate(value))
        elif error == ServiceError.LOAD_DATASET:
            ret = cls.__getLoadDataSet().get(LoadDataSet(value))
        elif error == ServiceError.TASK:
            ret = cls.__getTask().get(Task(value))
        elif error == ServiceError.OTHER_ERROR:
            ret = str(value)
        return ret

    #
    # @param error
    #            Service error enumeration value.
    # Service error standard XML tag.
    #
    @classmethod
    def serviceErrorToString(cls, error):
        return cls.__getServiceErrors().get(error)

    #
    # @param value
    #            Service error standard XML tag.
    # Service error enumeration value.
    #
    @classmethod
    def getServiceError(cls, value):
        error = None
        for k, v in cls.__getServiceErrors():
            if value.compareTo(v) == 0:
                error = k
                break
        if error is None:
            raise ValueError()
        return error

    @classmethod
    def __getApplicationReferenceByValue(cls, value):
        ret = None
        for k, v in cls.__getApplicationReference():
            if value.compareTo(v) == 0:
                ret = k
                break
        if ret is None:
            raise ValueError()
        return ret

    @classmethod
    def __getHardwareResourceByValue(cls, value):
        ret = None
        for k, v in cls.__getHardwareResource():
            if value.compareTo(v) == 0:
                ret = k
                break
        if ret is None:
            raise ValueError()
        return ret

    @classmethod
    def __getVdeStateErrorByValue(cls, value):
        ret = None
        for k, v in cls.__getVdeStateError():
            if value.compareTo(v) == 0:
                ret = k
                break
        if ret is None:
            raise ValueError()
        return ret

    @classmethod
    def __getServiceByValue(cls, value):
        ret = None
        for k, v in cls.__getService():
            if value.compareTo(v) == 0:
                ret = k
                break
        if ret is None:
            raise ValueError()
        return ret

    @classmethod
    def __getDefinitionByValue(cls, value):
        ret = None
        for k, v in cls.__getDefinition():
            if value.compareTo(v) == 0:
                ret = k
                break
        if ret is None:
            raise ValueError()
        return ret

    @classmethod
    def __getAccessByValue(cls, value):
        ret = None
        for k, v in cls.__getAccess():
            if value.compareTo(v) == 0:
                ret = k
                break
        if ret is None:
            raise ValueError()
        return ret

    @classmethod
    def __getInitiateByValue(cls, value):
        ret = None
        for k, v in cls.__getInitiate():
            if value.compareTo(v) == 0:
                ret = k
                break
        if ret is None:
            raise ValueError()
        return ret

    @classmethod
    def __getLoadDataSetByValue(cls, value):
        ret = None
        for k, v in cls.__getLoadDataSet():
            if value.compareTo(v) == 0:
                ret = k
                break
        if ret is None:
            raise ValueError()
        return ret

    @classmethod
    def __getTaskByValue(cls, value):
        ret = None
        for k, v in cls.__getTask():
            if value.compareTo(v) == 0:
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
            ret = cls.__getInitiateByValue(value)
        elif serviceError == ServiceError.LOAD_DATASET:
            ret = cls.__getLoadDataSetByValue(value)
        elif serviceError == ServiceError.TASK:
            ret = cls.__getTaskByValue(value)
        elif serviceError == ServiceError.OTHER_ERROR:
            ret = int(value)
        return int(ret)

    @classmethod
    def conformancetoString(cls, value):
        str_ = None
        if value == Conformance.ACCESS:
            str_ = "access"
        elif value == Conformance.ACTION:
            str_ = "action"
        elif value == Conformance.ATTRIBUTE_0_SUPPORTED_WITH_GET:
            str_ = "attribute0-supported-with-get"
        elif value == Conformance.ATTRIBUTE_0_SUPPORTED_WITH_SET:
            str_ = "attribute0-supported-with-set"
        elif value == Conformance.BLOCK_TRANSFER_WITH_ACTION:
            str_ = "block-transfer-with-action"
        elif value == Conformance.BLOCK_TRANSFER_WITH_GET_OR_READ:
            str_ = "block-transfer-with-get-or-read"
        elif value == Conformance.BLOCK_TRANSFER_WITH_SET_OR_WRITE:
            str_ = "block-transfer-with-set-or-write"
        elif value == Conformance.DATA_NOTIFICATION:
            str_ = "data-notification"
        elif value == Conformance.EVENT_NOTIFICATION:
            str_ = "event-notification"
        elif value == Conformance.GENERAL_BLOCK_TRANSFER:
            str_ = "general-block-transfer"
        elif value == Conformance.GENERAL_PROTECTION:
            str_ = "general-protection"
        elif value == Conformance.GET:
            str_ = "get"
        elif value == Conformance.INFORMATION_REPORT:
            str_ = "information-report"
        elif value == Conformance.MULTIPLE_REFERENCES:
            str_ = "multiple-references"
        elif value == Conformance.PARAMETERIZED_ACCESS:
            str_ = "parameterized-access"
        elif value == Conformance.PRIORITY_MGMT_SUPPORTED:
            str_ = "priority-mgmt-supported"
        elif value == Conformance.READ:
            str_ = "read"
        elif value == Conformance.RESERVED_SEVEN:
            str_ = "reserved-seven"
        elif value == Conformance.RESERVED_SIX:
            str_ = "reserved-six"
        elif value == Conformance.RESERVED_ZERO:
            str_ = "reserved-zero"
        elif value == Conformance.SELECTIVE_ACCESS:
            str_ = "selective-access"
        elif value == Conformance.SET:
            str_ = "set"
        elif value == Conformance.UN_CONFIRMED_WRITE:
            str_ = "unconfirmed-write"
        elif value == Conformance.WRITE:
            str_ = "write"
        else:
            raise ValueError(str(value))
        return str_

    @classmethod
    def value_ofConformance(cls, value):
        ret = None
        if "access".lower() == value.lower():
            ret = Conformance.ACCESS
        elif "action".lower() == value.lower():
            ret = Conformance.ACTION
        elif "attribute0-supported-with-get".lower() == value.lower():
            ret = Conformance.ATTRIBUTE_0_SUPPORTED_WITH_GET
        elif "attribute0-supported-with-set".lower() == value.lower():
            ret = Conformance.ATTRIBUTE_0_SUPPORTED_WITH_SET
        elif "block-transfer-with-action".lower() == value.lower():
            ret = Conformance.BLOCK_TRANSFER_WITH_ACTION
        elif "block-transfer-with-get-or-read".lower() == value.lower():
            ret = Conformance.BLOCK_TRANSFER_WITH_GET_OR_READ
        elif "block-transfer-with-set-or-write".lower() == value.lower():
            ret = Conformance.BLOCK_TRANSFER_WITH_SET_OR_WRITE
        elif "data-notification".lower() == value.lower():
            ret = Conformance.DATA_NOTIFICATION
        elif "event-notification".lower() == value.lower():
            ret = Conformance.EVENT_NOTIFICATION
        elif "general-block-transfer".lower() == value.lower():
            ret = Conformance.GENERAL_BLOCK_TRANSFER
        elif "general-protection".lower() == value.lower():
            ret = Conformance.GENERAL_PROTECTION
        elif "get".lower() == value.lower():
            ret = Conformance.GET
        elif "information-report".lower() == value.lower():
            ret = Conformance.INFORMATION_REPORT
        elif "multiple-references".lower() == value.lower():
            ret = Conformance.MULTIPLE_REFERENCES
        elif "parameterized-access".lower() == value.lower():
            ret = Conformance.PARAMETERIZED_ACCESS
        elif "priority-mgmt-supported".lower() == value.lower():
            ret = Conformance.PRIORITY_MGMT_SUPPORTED
        elif "read".lower() == value.lower():
            ret = Conformance.READ
        elif "reserved-seven".lower() == value.lower():
            ret = Conformance.RESERVED_SEVEN
        elif "reserved-six".lower() == value.lower():
            ret = Conformance.RESERVED_SIX
        elif "reserved-zero".lower() == value.lower():
            ret = Conformance.RESERVED_ZERO
        elif "selective-access".lower() == value.lower():
            ret = Conformance.SELECTIVE_ACCESS
        elif "set".lower() == value.lower():
            ret = Conformance.SET
        elif "unconfirmed-write".lower() == value.lower():
            ret = Conformance.UN_CONFIRMED_WRITE
        elif "write".lower() == value.lower():
            ret = Conformance.WRITE
        else:
            raise ValueError(value)
        return ret

    @classmethod
    def releaseResponseReasonToString(cls, value):
        str_ = None
        if value == ReleaseResponseReason.NORMAL:
            str_ = "normal"
        elif value == ReleaseResponseReason.NOT_FINISHED:
            str_ = "not-finished"
        elif value == ReleaseResponseReason.USER_DEFINED:
            str_ = "user-defined"
        else:
            raise ValueError(str(value))
        return str_

    @classmethod
    def value_ofReleaseResponseReason(cls, value):
        ret = None
        if "normal".lower() == value.lower():
            ret = ReleaseResponseReason.NORMAL
        elif "not-finished".lower() == value.lower():
            ret = ReleaseResponseReason.NOT_FINISHED
        elif "user-defined".lower() == value.lower():
            ret = ReleaseResponseReason.USER_DEFINED
        else:
            raise ValueError(value)
        return ret

    @classmethod
    def releaseRequestReasonToString(cls, value):
        str_ = None
        if value == ReleaseRequestReason.NORMAL:
            str_ = "normal"
        elif value == ReleaseRequestReason.URGENT:
            str_ = "not-finished"
        elif value == ReleaseRequestReason.USER_DEFINED:
            str_ = "user-defined"
        else:
            raise ValueError(str(value))
        return str_

    @classmethod
    def value_ofReleaseRequestReason(cls, value):
        ret = None
        if "normal".lower() == value.lower():
            ret = ReleaseRequestReason.NORMAL
        elif "not-finished".lower() == value.lower():
            ret = ReleaseRequestReason.URGENT
        elif "user-defined".lower() == value.lower():
            ret = ReleaseRequestReason.USER_DEFINED
        else:
            raise ValueError(value)
        return ret

    @classmethod
    def stateErrorToString(cls, value):
        if value == StateError.SERVICE_NOT_ALLOWED:
            ret = "service-not-allowed"
        elif value == StateError.SERVICE_UNKNOWN:
            ret = "service-unknown"
        else:
            raise ValueError(value)
        return ret

    @classmethod
    def exceptionServiceErrorToString(cls, value):
        if value == ExceptionServiceError.OPERATION_NOT_POSSIBLE:
            ret = "operation-not-possible"
        elif value == ExceptionServiceError.SERVICE_NOT_SUPPORTED:
            ret = "service-not-supported"
        elif value == ExceptionServiceError.OTHER_REASON:
            ret = "other-reason"
        else:
            raise ValueError(value)
        return ret

    @classmethod
    def valueofStateError(cls, value):
        if "service-not-allowed".lower() == value.lower():
            ret = StateError.SERVICE_NOT_ALLOWED
        elif "service-unknown".lower() == value.lower():
            ret = StateError.SERVICE_UNKNOWN
        else:
            raise ValueError(value)
        return ret

    @classmethod
    def valueOfExceptionServiceError(cls, value):
        if "operation-not-possible".lower() == value.lower():
            ret = ExceptionServiceError.OPERATION_NOT_POSSIBLE
        elif "service-not-supported".lower() == value.lower():
            ret = ExceptionServiceError.SERVICE_NOT_SUPPORTED
        elif "other-reason".lower() == value.lower():
            ret = ExceptionServiceError.OTHER_REASON
        else:
            raise ValueError(value)
        return ret

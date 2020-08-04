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
from .enums import AssociationResult, ErrorCode, SourceDiagnostic

class GXDLMSException(Exception):
    """
    DLMS specific exception class that has error description available from
    GetDescription method.
    """
    def __init__(self, errCode, serviceErr=None):
        if isinstance(errCode, AssociationResult):
            Exception.__init__(self, "Connection is " + self.getResult(errCode) + "\r\n" + self.getDiagnostic(serviceErr))
            self.result = errCode
            self.diagnostic = serviceErr
        else:
            Exception.__init__(self, self.getDescription(errCode))
        self.errorCode = errCode

    #
    # Get result as a string.
    #
    # @param result
    #            Enumeration value of AssociationResult.
    # String description of AssociationResult.
    #
    @classmethod
    def getResult(cls, result):
        if result == AssociationResult.PERMANENT_REJECTED:
            ret = "permanently rejected"
        elif result == AssociationResult.TRANSIENT_REJECTED:
            ret = "transient rejected"
        else:
            ret = "Invalid error code."
        return ret

    #
    # Get diagnostic as a string.
    #
    # @param value
    #            Enumeration value of SourceDiagnostic.
    # String description of SourceDiagnostic.
    #
    @classmethod
    def getDiagnostic(cls, value):
        if value == SourceDiagnostic.NO_REASON_GIVEN:
            ret = "No reason is given."
        elif value == SourceDiagnostic.NOT_SUPPORTED:
            ret = "The application context name is not supported."
        elif value == SourceDiagnostic.NOT_RECOGNISED:
            ret = "The authentication mechanism name is not recognized."
        elif value == SourceDiagnostic.MECHANISM_NAME_REGUIRED:
            ret = "Authentication mechanism name is required."
        elif value == SourceDiagnostic.AUTHENTICATION_FAILURE:
            ret = "Authentication failure."
        elif value == SourceDiagnostic.AUTHENTICATION_REQUIRED:
            ret = "Authentication is required."
        else:
            ret = "Invalid error code."
        return ret

    @classmethod
    def getDescription(cls, errCode):
        if errCode == ErrorCode.REJECTED:
            str_ = "Rejected"
        elif errCode == ErrorCode.OK:
            str_ = ""
        elif errCode == ErrorCode.HARDWARE_FAULT:
            str_ = "Access Error : Device reports a hardware fault."
        elif errCode == ErrorCode.TEMPORARY_FAILURE:
            str_ = "Access Error : Device reports a temporary failure."
        elif errCode == ErrorCode.READ_WRITE_DENIED:
            str_ = "Access Error : Device reports Read-Write denied."
        elif errCode == ErrorCode.UNDEFINED_OBJECT:
            str_ = "Access Error : Device reports a undefined object."
        elif errCode == ErrorCode.INCONSISTENT_CLASS:
            str_ = "Access Error : " + "Device reports a inconsistent Class or object."
        elif errCode == ErrorCode.UNAVAILABLE_OBJECT:
            str_ = "Access Error : Device reports a unavailable object."
        elif errCode == ErrorCode.UNMATCHED_TYPE:
            str_ = "Access Error : Device reports a unmatched type."
        elif errCode == ErrorCode.ACCESS_VIOLATED:
            str_ = "Access Error : Device reports scope of access violated."
        elif errCode == ErrorCode.DATA_BLOCK_UNAVAILABLE:
            str_ = "Access Error : Data Block Unavailable."
        elif errCode == ErrorCode.LONG_GET_OR_READ_ABORTED:
            str_ = "Access Error : Long Get Or Read Aborted."
        elif errCode == ErrorCode.NO_LONG_GET_OR_READ_IN_PROGRESS:
            str_ = "Access Error : No Long Get Or Read In Progress."
        elif errCode == ErrorCode.LONG_SET_OR_WRITE_ABORTED:
            str_ = "Access Error : Long Set Or Write Aborted."
        elif errCode == ErrorCode.NO_LONG_SET_OR_WRITE_IN_PROGRESS:
            str_ = "Access Error : No Long Set Or Write In Progress."
        elif errCode == ErrorCode.DATA_BLOCK_NUMBER_INVALID:
            str_ = "Access Error : Data Block Number Invalid."
        elif errCode == ErrorCode.OTHER_REASON:
            str_ = "Access Error : Other Reason."
        else:
            str_ = "Access Error : Unknown error."
        return str_

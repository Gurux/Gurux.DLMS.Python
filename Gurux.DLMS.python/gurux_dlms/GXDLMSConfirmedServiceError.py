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
from .ServiceError import ServiceError
from .ConfirmedServiceError import ConfirmedServiceError
from .enums.ApplicationReference import ApplicationReference
from .enums.VdeStateError import VdeStateError
from .enums.HardwareResource import HardwareResource
from .enums.Definition import Definition
from .enums.Access import Access
from .enums.Service import Service
from .enums.Initiate import Initiate
from .enums.LoadDataSet import LoadDataSet
from .enums.Task import Task

class GXDLMSConfirmedServiceError(Exception):
    """
    DLMS specific exception class that has error description available from getDescription method.
    """

    #
    # Constructor for Confirmed ServiceError.
    #
    # @param service
    # @param type
    # @param value
    #
    def __init__(self, service=None, type_=None, value=0):
        Exception.__init__(self, "ServiceError " + self.__getConfirmedServiceError(service) + " exception. " + self.__getServiceError(type_) + " " + self.__getServiceErrorValue(type_, value))
        self.confirmedServiceError = service
        self.serviceError = type_
        self.serviceErrorValue = value

    @classmethod
    def __getConfirmedServiceError(cls, stateError):
        str_ = ""
        if stateError == ConfirmedServiceError.INITIATE_ERROR:
            str_ = "Initiate Error"
        elif stateError == ConfirmedServiceError.READ:
            str_ = "Read"
        elif stateError == ConfirmedServiceError.WRITE:
            str_ = "Write"
        return str_

    @classmethod
    def __getServiceError(cls, error):
        str_ = ""
        if error == ServiceError.APPLICATION_REFERENCE:
            str_ = "Application reference"
        elif error == ServiceError.HARDWARE_RESOURCE:
            str_ = "Hardware resource"
        elif error == ServiceError.VDE_STATE_ERROR:
            str_ = "Vde state error"
        elif error == ServiceError.SERVICE:
            str_ = "Service"
        elif error == ServiceError.DEFINITION:
            str_ = "Definition"
        elif error == ServiceError.ACCESS:
            str_ = "Access"
        elif error == ServiceError.INITIATE:
            str_ = "Initiate"
        elif error == ServiceError.LOAD_DATASET:
            str_ = "Load dataset"
        elif error == ServiceError.TASK:
            str_ = "Task"
        elif error == ServiceError.OTHER_ERROR:
            str_ = "Other Error"
        return str_

    @classmethod
    def __getServiceErrorValue(cls, error, value):
        str_ = ""
        if error == ServiceError.APPLICATION_REFERENCE:
            str_ = str(ApplicationReference(value))
        elif error == ServiceError.HARDWARE_RESOURCE:
            str_ = str(HardwareResource(value))
        elif error == ServiceError.VDE_STATE_ERROR:
            str_ = str(VdeStateError(value))
        elif error == ServiceError.SERVICE:
            str_ = str(Service(value))
        elif error == ServiceError.DEFINITION:
            str_ = str(Definition(value))
        elif error == ServiceError.ACCESS:
            str_ = str(Access(value))
        elif error == ServiceError.INITIATE:
            str_ = str(Initiate(value))
        elif error == ServiceError.LOAD_DATASET:
            str_ = str(LoadDataSet(value))
        elif error == ServiceError.TASK:
            str_ = str(Task(value))
        elif error == ServiceError.OTHER_ERROR:
            str_ = str(value)
        return str_

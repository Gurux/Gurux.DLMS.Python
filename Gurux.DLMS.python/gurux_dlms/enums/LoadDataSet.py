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

class LoadDataSet(GXIntEnum):
    """LoadDataSet describes load dataset errors."""
    #pylint: disable=too-few-public-methods

    #Other error.
    OTHER = 0

    #Primitive out of sequence.
    PRIMITIVE_OUT_OF_SEQUENCE = 1

    #Not loadable.
    NOT_LOADABLE = 2

    #Dataset size is too large.
    DATASET_SIZE_TOO_LARGE = 3

    #Not awaited segment.
    NOT_AWAITED_SEGMENT = 4

    #Interpretation failure.
    INTERPRETATION_FAILURE = 5

    #Storage failure.
    STORAGE_FAILURE = 6

    #Dataset not ready.
    DATASET_NOT_READY = 7

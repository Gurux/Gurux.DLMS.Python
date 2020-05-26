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
from gurux_dlms.GXIntEnum import GXIntEnum

class ImageTransferStatus(GXIntEnum):
    """
    Holds the status of the Image transfer process.
    """
    #pylint: disable=too-few-public-methods

    IMAGE_TRANSFER_NOT_INITIATED = 0
    IMAGE_TRANSFER_INITIATED = 1
    IMAGE_VERIFICATION_INITIATED = 2
    IMAGE_VERIFICATION_SUCCESSFUL = 3
    IMAGE_VERIFICATION_FAILED = 4
    IMAGE_ACTIVATION_INITIATED = 5
    IMAGE_ACTIVATION_SUCCESSFUL = 6
    IMAGE_ACTIVATION_FAILED = 7

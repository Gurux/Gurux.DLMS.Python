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

###Python 2 requires this
#pylint: disable=bad-option-value,old-style-class,too-few-public-methods
class GXMacPhyCommunication:
    #
    # Constructor.
    #
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        # EUI is the EUI-48 of the other device.
        self.eui = None
        # The tx power of GPDU packets sent to the device.
        self.txPower = 0
        # The Tx coding of GPDU packets sent to the device.
        self.txCoding = 0
        # The Rx coding of GPDU packets received from the device.
        self.rxCoding = 0
        # The Rx power level of GPDU packets received from the device.
        self.rxLvl = 0
        # SNR of GPDU packets received from the device.
        self.snr = 0
        # The number of times the Tx power was modified.
        self.txPowerModified = 0
        # The number of times the Tx coding was modified.
        self.txCodingModified = 0
        # The number of times the Rx coding was modified.
        self.rxCodingModified = 0

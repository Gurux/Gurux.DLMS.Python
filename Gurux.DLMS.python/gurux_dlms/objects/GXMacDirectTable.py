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
class GXMacDirectTable:
    #
    # Constructor.
    #
    def __init__(self):
        # SID of switch through which the source service node is connected.
        self.sourceSId = 0
        # NID allocated to the source service node.
        self.sourceLnId = 0
        # LCID allocated to this connection at the source.
        self.sourceLcId = 0
        # SID of the switch through which the destination service node is
        # connected.
        self.destinationSId = 0
        # NID allocated to the destination service node.
        self.destinationLnId = 0
        # LCID allocated to this connection at the destination.
        self.destinationLcId = 0
        # Entry DID is the EUI-48 of the direct switch.
        self.did = None

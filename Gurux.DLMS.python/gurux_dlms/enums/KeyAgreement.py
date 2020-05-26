#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename:        $HeadURL$
#
#  Version:         $Revision$,
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

class KeyAgreement(GXIntEnum):
    """Key agreement."""
    #pylint: disable=too-few-public-methods

    # The Ephemeral Unified Model C(2e, 0s, ECC CDH) scheme.
    EPHEMERAL_UNIFIED_MODEL = 0

     # The One-Pass Diffie-Hellman C(1e, 1s, ECC CDH) scheme.
    ONE_PASS_DIFFIE_HELLMAN = 1

    # The Static Unified Model C(0e, 2s, ECC CDH) scheme.
    STATIC_UNIFIED_MODEL = 2

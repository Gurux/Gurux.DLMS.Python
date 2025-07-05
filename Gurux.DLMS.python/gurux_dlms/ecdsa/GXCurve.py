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
#  More information of Gurux products: http:#www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http:#www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
from .enums.Ecc import Ecc
from .GXEccPoint import GXEccPoint


class GXCurve:
    """
    ECC x and y points in the curve.
    """

    __a = None
    """
    ECC curve a value.
    """

    __p = None
    """
    ECC curve p value.
    """

    __b = None
    """
    ECC curve b parameter.
    """

    __g = None
    """
    x and y-coordinate of base point G
    """

    __n = None
    """
    Order of point G in ECC curve.
    """

    @property
    def a(self):
        """
        ECC curve a value.
        """
        return self.__a

    @property
    def p(self):
        """
        ECC curve p value.
        """
        return self.__p

    @property
    def b(self):
        """
        ECC curve b parameter.
        """
        return self.__b

    @property
    def g(self):
        """
        x and y-coordinate of base point G
        """
        return self.__g

    @property
    def n(self):
        """
        Order of point G in ECC curve.
        """
        return self.__n

    def __init__(self, scheme):
        """
        Constructor.

            Parameters:
                a: ECC curve a value.
                b: ECC curve b parameter.
                p: ECC curve p value.
                g: x and y-coordinate of base point G
                n: Order of point G in ECC curve.
        """

        if scheme == Ecc.P256:
            self.__a = (
                0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
            )
            self.__g = GXEccPoint(
                0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
                0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5,
            )
            self.__n = (
                0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
            )
            self.__p = (
                0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
            )
            self.__b = (
                0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
            )
        elif scheme == Ecc.P384:
            self.__a = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFF0000000000000000FFFFFFFC
            self.__g = GXEccPoint(
                0xAA87CA22BE8B05378EB1C71EF320AD746E1D3B628BA79B9859F741E082542A385502F25DBF55296C3A545E3872760AB7,
                0x3617DE4A96262C6F5D9E98BF9292DC29F8F41DBD289A147CE9DA3113B5F0B8C00A60B1CE1D7E819D7A431D7C90EA0E5F,
            )
            self.__n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC7634D81F4372DDF581A0DB248B0A77AECEC196ACCC52973
            self.__p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFF0000000000000000FFFFFFFF
            self.__b = 0xB3312FA7E23EE7E4988E056BE3F82D19181D9C6EFE8141120314088F5013875AC656398D8A2ED19D2A85C8EDD3EC2AEF
        else:
            raise ValueError("Invalid scheme.")

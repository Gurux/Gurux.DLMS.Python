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
#  Gurux Device Framework is Open Source software you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http:#www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http:#www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
from .GXEccPoint import GXEccPoint


class _GXShamirs:
    """
    This class implements GXShamir's trick.
    """

    @classmethod
    def __pointAdd(cls, curve, ret, p1, p2):
        """
        Add points.

            Parameters:
                curve: Used curve.
                ret: Result.
                p1: Point 1.
                p2: Point 2.
        """
        # Calculate lambda.
        ydiff = p2.y
        ydiff -= p1.y
        xdiff = p2.x
        xdiff -= p1.x
        xdiff = pow(xdiff, -1, curve.p)
        lambda_ = ydiff
        lambda_ *= xdiff
        lambda_ %= curve.p
        # calculate resulting x coord.
        ret.x = lambda_
        ret.x *= lambda_
        ret.x -= p1.x
        ret.x -= p2.x
        ret.x %= curve.p
        # calculate resulting y coord
        ret.y = p1.x
        ret.y -= ret.x
        ret.y *= lambda_
        ret.y -= p1.y
        ret.y %= curve.p

    @classmethod
    def _pointDouble(cls, curve, ret, p1):
        """
        Double point.

            Parameters:
                curve: Used curve.
                ret: Result value.
                p1: Point to double
        """
        numer = p1.x
        numer *= p1.x
        numer *= 3
        numer += curve.a
        denom = p1.y
        denom *= 2
        denom = pow(denom, -1, curve.p)
        lambda_ = int(numer)
        lambda_ *= denom
        lambda_ %= curve.p
        # calculate resulting x coord
        ret.x = lambda_
        ret.x *= lambda_
        ret.x -= p1.x
        ret.x -= p1.x
        ret.x %= curve.p
        # calculate resulting y coord
        ret.y = p1.x
        ret.y -= ret.x
        ret.y *= lambda_
        ret.y -= p1.y
        ret.y %= curve.p

    @classmethod
    def pointMulti(cls, curve, ret, point, scalar):
        """
        Multiply point with big integer value.

            Parameters:
                curve: Used curve.
                ret: Return value.
                point: Point.
                scalar: Scaler.
        """
        R0 = GXEccPoint(point.x, point.y)
        R1 = GXEccPoint()
        tmp = GXEccPoint()
        cls._pointDouble(curve, R1, point)
        dbits = scalar.bit_length()
        dbits -= 2
        while True:
            if scalar & 1 << dbits != 0:
                # If bit is set.
                tmp.x = R0.x
                tmp.y = R0.y
                cls.__pointAdd(curve, R0, R1, tmp)
                tmp.x = R1.x
                tmp.y = R1.y
                cls._pointDouble(curve, R1, tmp)
            else:
                tmp.x = R1.x
                tmp.y = R1.y
                cls.__pointAdd(curve, R1, R0, tmp)
                tmp.x = R0.x
                tmp.y = R0.y
                cls._pointDouble(curve, R0, tmp)
            if dbits == 0:
                break
            dbits -= 1
        ret.x = R0.x
        ret.y = R0.y

    # pylint: disable=too-many-arguments
    @classmethod
    def trick(cls, curve, pub, ret, u1, u2):
        """
        Count Shamir's trick.

            Parameters:
                curve: Used curve.
                pub: Public key.
                ret: Result.
                u1:
                u2:
        """
        sum_ = GXEccPoint()
        op2 = GXEccPoint(
            int.from_bytes(pub.x, byteorder="big"),
            int.from_bytes(pub.y, byteorder="big"),
        )
        cls.__pointAdd(curve, sum_, curve.g, op2)
        bits1 = u1.bit_length()
        bits2 = u2.bit_length()
        if bits1 > bits2:
            pos = bits1
        else:
            pos = bits2
        pos -= 1
        if u1 & 1 << pos != 0 and u2 & 1 << pos != 0:
            ret.x = sum_.x
            ret.y = sum_.y
        elif u1 & 1 << pos != 0:
            ret.x = curve.g.x
            ret.y = curve.g.y
        elif u2 & 1 << pos != 0:
            ret.x = op2.x
            ret.y = op2.y
        tmp = GXEccPoint()
        pos -= 1
        while True:
            tmp.x = ret.x
            tmp.y = ret.y
            cls._pointDouble(curve, ret, tmp)
            tmp.x = ret.x
            tmp.y = ret.y
            if u1 & 1 << pos != 0 and u2 & 1 << pos != 0:
                cls.__pointAdd(curve, ret, tmp, sum_)
            elif u1 & 1 << pos != 0:
                cls.__pointAdd(curve, ret, tmp, curve.g)
            elif u2 & 1 << pos != 0:
                cls.__pointAdd(curve, ret, tmp, op2)
            if pos == 0:
                break
            pos -= 1

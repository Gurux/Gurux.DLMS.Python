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
class SerialNumberCounter:
    @classmethod
    def __getValues(cls, expressions):
        """
        Get values to count together.
        """
        values = list()
        last = 0
        index = 0
        for ch in expressions:
            if ch in ('%', '+', '-', '*', '/'):
                values.append(expressions[last: index])
                values.append(str(ch))
                last = index + 1
            index += 1
        if index != last:
            values.append(expressions[last:])
        return values

    @classmethod
    def __getValue(cls, value, sn):
        if value == "sn":
            return sn
        return int(value)

    # Count serial number using formula.
    # sn: Serial number
    # formula: Formula to used.
    @classmethod
    def count(cls, sn, formula):
        values = cls.__getValues(cls.__formatString(formula))
        if len(values) % 2 == 0:
            raise ValueError("Invalid serial number formula.")
        str_ = None
        value = cls.__getValue(values[0], sn)
        index = 1
        while index != len(values):
            str_ = values[index]
            if str_ == "%":
                value = value % cls.__getValue(values[index + 1], sn)
            elif str_ == "+":
                value = value + cls.__getValue(values[index + 1], sn)
            elif str_ == "-":
                value = value - cls.__getValue(values[index + 1], sn)
            elif str_ == "*":
                value = value * cls.__getValue(values[index + 1], sn)
            elif str_ == "/":
                value = value / cls.__getValue(values[index + 1], sn)
            else:
                raise ValueError("Invalid serial number formula.")
            index += 2
        return value

    #
    # Produce formatted String by the given math expression.
    #
    # @param expression
    #            Unformatted math expression.
    # Formatted math expression.
    #
    @classmethod
    def __formatString(cls, expression):
        if not expression:
            raise ValueError("Expression is null or empty")
        sb = ""
        for ch in expression.lower():
            if ch in ('(', ')'):
                raise ValueError("Invalid serial number formula.")
            #  Is not white space.
            if ch != ' ':
                sb += ch
        return sb

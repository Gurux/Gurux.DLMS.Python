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
from .GXStandardObisCode import GXStandardObisCode
from .GXByteBuffer import GXByteBuffer

class GXStandardObisCodeCollection(list):
    """
    Standard OBIS code collection is used to save all default OBIS Codes.
    """

    @classmethod
    def getBytes(cls, ln):
        if not ln:
            return None
        tmp = ln.split('.')
        if len(tmp) != 6:
            #  If value is give as hex.
            tmp = GXByteBuffer.hexToBytes(ln)
            if len(tmp) != 6:
                raise ValueError("Invalid OBIS Code.")
        code_ = bytearray(6)
        code_[0] = int(tmp[0])
        code_[1] = int(tmp[1])
        code_[2] = int(tmp[2])
        code_[3] = int(tmp[3])
        code_[4] = int(tmp[4])
        code_[5] = int(tmp[5])
        return code_

    def find(self, ln, objectType):
        return self.find2(self.getBytes(ln), objectType)

    @classmethod
    def equalsInterface(cls, it, ic):
        """Check is interface included to standard."""

        #  If all interfaces are allowed.
        if int(ic) == 0 or it.interfaces == "*":
            return True
        return str(int(ic)) in it.interfaces.split(',')

    @classmethod
    def equalsMask(cls, obis, ic):
        """Check OBIS codes."""
        ret = False
        number = True
        if obis.find(',') != -1:
            tmp = obis.split(',')
            for it in tmp:
                if it.find('-') != -1:
                    if cls.equalsMask(it, ic):
                        return True
                elif int(it) == ic:
                    return True
            ret = False
        elif obis.find('-') != -1:
            number = False
            tmp = obis.split('-')
            ret = int(ic) >= int(tmp[0]) and ic <= int(tmp[1])
        elif number:
            if obis == "&":
                return ic in (0, 1, 7)
            ret = int(obis) == ic
        return ret

    @classmethod
    def equalsMask2(cls, obisMask, ln):
        return cls.equalsObisCode(obisMask.split('.'), cls.getBytes(ln))

    #
    # Check OBIS code.
    #
    @classmethod
    def equalsObisCode(cls, obisMask, ic):
        ret = True
        if not ic:
            ret = True
        elif not cls.equalsMask(obisMask[0], ic[0]):
            ret = False
        elif not cls.equalsMask(obisMask[1], ic[1]):
            ret = False
        elif not cls.equalsMask(obisMask[2], ic[2]):
            ret = False
        elif not cls.equalsMask(obisMask[3], ic[3]):
            ret = False
        elif not cls.equalsMask(obisMask[4], ic[4]):
            ret = False
        elif not cls.equalsMask(obisMask[5], ic[5]):
            ret = False
        return ret

    #
    # Get N1C description.
    #
    @classmethod
    def getN1CDescription(cls, str_):
        if not str_ or str_[0] != '$':
            return ""
        value = int(str_[1:])
        tmp = ""
        if value == 41:
            tmp = "Absolute temperature"
        elif value == 42:
            tmp = "Absolute pressure"
        elif value == 44:
            tmp = "Velocity of sound"
        elif value == 45:
            tmp = "Density(of gas)"
        elif value == 46:
            tmp = "Relative density"
        elif value == 47:
            tmp = "Gauge pressure"
        elif value == 48:
            tmp = "Differential pressure"
        elif value == 49:
            tmp = "Density of air"
        return tmp

    @classmethod
    def getDescription(cls, str_):
        """Get description."""
        if not str_ or str_[0] != '$':
            return ""

        value = int(str_[1:])
        if value == 1:
            ret = "Sum Li Active power+ (QI+QIV)"
        elif value == 2:
            ret = "Sum Li Active power- (QII+QIII)"
        elif value == 3:
            ret = "Sum Li Reactive power+ (QI+QII)"
        elif value == 4:
            ret = "Sum Li Reactive power- (QIII+QIV)"
        elif value == 5:
            ret = "Sum Li Reactive power QI"
        elif value == 6:
            ret = "Sum Li Reactive power QII"
        elif value == 7:
            ret = "Sum Li Reactive power QIII"
        elif value == 8:
            ret = "Sum Li Reactive power QIV"
        elif value == 9:
            ret = "Sum Li Apparent power+ (QI+QIV)"
        elif value == 10:
            ret = "Sum Li Apparent power- (QII+QIII)"
        elif value == 11:
            ret = "Current: any phase"
        elif value == 12:
            ret = "Voltage: any phase"
        elif value == 13:
            ret = "Sum Li Power factor"
        elif value == 14:
            ret = "Supply frequency"
        elif value == 15:
            ret = "Sum Li Active power (abs(QI+QIV)+abs(QII+QIII))"
        elif value == 16:
            ret = "Sum Li Active power (abs(QI+QIV)-abs(QII+QIII))"
        elif value == 17:
            ret = "Sum Li Active power QI"
        elif value == 18:
            ret = "Sum Li Active power QII"
        elif value == 19:
            ret = "Sum Li Active power QIII"
        elif value == 20:
            ret = "Sum Li Active power QIV"
        elif value == 21:
            ret = "L1 Active power+ (QI+QIV)"
        elif value == 22:
            ret = "L1 Active power- (QII+QIII)"
        elif value == 23:
            ret = "L1 Reactive power+ (QI+QII)"
        elif value == 24:
            ret = "L1 Reactive power- (QIII+QIV)"
        elif value == 25:
            ret = "L1 Reactive power QI"
        elif value == 26:
            ret = "L1 Reactive power QII"
        elif value == 27:
            ret = "L1 Reactive power QIII"
        elif value == 28:
            ret = "L1 Reactive power QIV"
        elif value == 29:
            ret = "L1 Apparent power+ (QI+QIV)"
        elif value == 30:
            ret = "L1 Apparent power- (QII+QIII)"
        elif value == 31:
            ret = "L1 Current"
        elif value == 32:
            ret = "L1 Voltage"
        elif value == 33:
            ret = "L1 Power factor"
        elif value == 34:
            ret = "L1 Supply frequency"
        elif value == 35:
            ret = "L1 Active power (abs(QI+QIV)+abs(QII+QIII))"
        elif value == 36:
            ret = "L1 Active power (abs(QI+QIV)-abs(QII+QIII))"
        elif value == 37:
            ret = "L1 Active power QI"
        elif value == 38:
            ret = "L1 Active power QII"
        elif value == 39:
            ret = "L1 Active power QIII"
        elif value == 40:
            ret = "L1 Active power QIV"
        elif value == 41:
            ret = "L2 Active power+ (QI+QIV)"
        elif value == 42:
            ret = "L2 Active power- (QII+QIII)"
        elif value == 43:
            ret = "L2 Reactive power+ (QI+QII)"
        elif value == 44:
            ret = "L2 Reactive power- (QIII+QIV)"
        elif value == 45:
            ret = "L2 Reactive power QI"
        elif value == 46:
            ret = "L2 Reactive power QII"
        elif value == 47:
            ret = "L2 Reactive power QIII"
        elif value == 48:
            ret = "L2 Reactive power QIV"
        elif value == 49:
            ret = "L2 Apparent power+ (QI+QIV)"
        elif value == 50:
            ret = "L2 Apparent power- (QII+QIII)"
        elif value == 51:
            ret = "L2 Current"
        elif value == 52:
            ret = "L2 Voltage"
        elif value == 53:
            ret = "L2 Power factor"
        elif value == 54:
            ret = "L2 Supply frequency"
        elif value == 55:
            ret = "L2 Active power (abs(QI+QIV)+abs(QII+QIII))"
        elif value == 56:
            ret = "L2 Active power (abs(QI+QIV)-abs(QI+QIII))"
        elif value == 57:
            ret = "L2 Active power QI"
        elif value == 58:
            ret = "L2 Active power QII"
        elif value == 59:
            ret = "L2 Active power QIII"
        elif value == 60:
            ret = "L2 Active power QIV"
        elif value == 61:
            ret = "L3 Active power+ (QI+QIV)"
        elif value == 62:
            ret = "L3 Active power- (QII+QIII)"
        elif value == 63:
            ret = "L3 Reactive power+ (QI+QII)"
        elif value == 64:
            ret = "L3 Reactive power- (QIII+QIV)"
        elif value == 65:
            ret = "L3 Reactive power QI"
        elif value == 66:
            ret = "L3 Reactive power QII"
        elif value == 67:
            ret = "L3 Reactive power QIII"
        elif value == 68:
            ret = "L3 Reactive power QIV"
        elif value == 69:
            ret = "L3 Apparent power+ (QI+QIV)"
        elif value == 70:
            ret = "L3 Apparent power- (QII+QIII)"
        elif value == 71:
            ret = "L3 Current"
        elif value == 72:
            ret = "L3 Voltage"
        elif value == 73:
            ret = "L3 Power factor"
        elif value == 74:
            ret = "L3 Supply frequency"
        elif value == 75:
            ret = "L3 Active power (abs(QI+QIV)+abs(QII+QIII))"
        elif value == 76:
            ret = "L3 Active power (abs(QI+QIV)-abs(QI+QIII))"
        elif value == 77:
            ret = "L3 Active power QI"
        elif value == 78:
            ret = "L3 Active power QII"
        elif value == 79:
            ret = "L3 Active power QIII"
        elif value == 80:
            ret = "L3 Active power QIV"
        elif value == 82:
            ret = "Unitless quantities (pulses or pieces)"
        elif value == 84:
            ret = "Sum Li Power factor-"
        elif value == 85:
            ret = "L1 Power factor-"
        elif value == 86:
            ret = "L2 Power factor-"
        elif value == 87:
            ret = "L3 Power factor-"
        elif value == 88:
            ret = "Sum Li A2h QI+QII+QIII+QIV"
        elif value == 89:
            ret = "Sum Li V2h QI+QII+QIII+QIV"
        elif value == 90:
            ret = "SLi current (algebraic sum of the - unsigned - value of the currents in all phases)"
        elif value == 91:
            ret = "Lo Current (neutral)"
        elif value == 92:
            ret = "Lo Voltage (neutral)"
        else:
            ret = ""
        return ret

    #
    # Get OBIS value.
    #
    # @param formula
    # OBIS formula.
    # @param value
    # OBIS value.
    # @return OBIS value as integer.
    #
    @classmethod
    def getObisValue(cls, formula, value):
        if len(formula) == 1:
            return str(value)
        return str(value + int(formula[1:]))

    #
    # Find Standard OBIS Code description.
    # pylint: disable=too-many-nested-blocks
    def find2(self, obisCode, ic):
        if isinstance(obisCode, str):
            obisCode = self.getBytes(obisCode)
        tmp = None
        list_ = list()
        for it in self:
            #  Interface is tested first because it's faster.
            if self.equalsInterface(it, ic) and self.equalsObisCode(it.obis, obisCode):
                tmp = GXStandardObisCode(it.obis[0:], it.description, it, it.dataType)
                tmp.uiDataType = it.uiDataType
                list_.append(tmp)
                tmp2 = it.description.split(';')
                if len(tmp2) > 1:
                    desc = ""
                    if obisCode and tmp2[1].strip() == "$1":
                        if obisCode[0] == 7:
                            desc = self.getN1CDescription("$" + str(obisCode[2]))
                        else:
                            desc = self.getDescription("$" + str(obisCode[2]))
                    if desc:
                        tmp2[1] = desc
                        tmp.description = ""
                        for s in tmp2:
                            if tmp.description:
                                tmp.description += ";"
                            tmp.description += s
                if obisCode:
                    obis = tmp.obis
                    obis[0] = str(obisCode[0])
                    obis[1] = str(obisCode[1])
                    obis[2] = str(obisCode[2])
                    obis[3] = str(obisCode[3])
                    obis[4] = str(obisCode[4])
                    obis[5] = str(obisCode[5])
                    tmp.obis = obis
                    desc = tmp.description
                    desc = desc.replace("$A", str(obisCode[0]))
                    desc = desc.replace("$B", str(obisCode[1]))
                    desc = desc.replace("$C", str(obisCode[2]))
                    desc = desc.replace("$D", str(obisCode[3]))
                    desc = desc.replace("$E", str(obisCode[4]))
                    desc = desc.replace("$F", str(obisCode[5]))
                    #  Increase value
                    begin = desc.find("$(")
                    if begin != -1:
                        arr = desc[begin + 2:].replace('(', '$').replace(')', '$').split('$')
                        desc = desc[0:begin]
                        for v in arr:
                            if not v:
                                pass
                            elif v[0] == 'A':
                                desc += self.getObisValue(v, obisCode[0])
                            elif v[0] == 'B':
                                desc += self.getObisValue(v, obisCode[1])
                            elif v[0] == 'C':
                                desc += self.getObisValue(v, obisCode[2])
                            elif v[0] == 'D':
                                desc += self.getObisValue(v, obisCode[3])
                            elif v[0] == 'E':
                                desc += self.getObisValue(v, obisCode[4])
                            elif v[0] == 'F':
                                desc += self.getObisValue(v, obisCode[5])
                            else:
                                desc += v
                    tmp.description = desc.replace(';', ' ').replace("  ", " ").strip()
        if not list_:
            tmp = GXStandardObisCode(None, "Invalid", str(int(ic)), "")
            obis = tmp.obis
            obis[0] = str(obisCode[0])
            obis[1] = str(obisCode[1])
            obis[2] = str(obisCode[2])
            obis[3] = str(obisCode[3])
            obis[4] = str(obisCode[4])
            obis[5] = str(obisCode[5])
            tmp.obis = obis
            list_.append(tmp)
        return list_

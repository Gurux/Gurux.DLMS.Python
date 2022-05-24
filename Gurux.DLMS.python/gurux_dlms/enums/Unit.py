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

class Unit(GXIntEnum):
    """Enumerated units."""
    #pylint: disable=too-few-public-methods

    #No Unit.
    NONE = 0
    #Year.
    YEAR = 1
    #Month.
    MONTH = 2
    #Week.
    WEEK = 3
    #Day.
    DAY = 4
    #Hour.
    HOUR = 5
    #Minute.
    MINUTE = 6
    #Second.
    SECOND = 7
    #Phase angle degree.
    PHASE_ANGLE_DEGREE = 8
    #Temperature
    TEMPERATURE = 9
    #Local currency.
    LOCAL_CURRENCY = 10
    #Length l meter m.
    LENGTH = 11
    #Speed.
    SPEED = 12
    #Volume V m3.
    VOLUME_CUBIC_METER = 13
    #Corrected volume m3.
    CORRECTED_VOLUME = 14
    VOLUME_FLUX_HOUR = 15
    CORRECTED_VOLUME_FLUX_HOUR = 16
    VOLUME_FLUXDAY = 17
    CORRECTE_VOLUME_FLUX_DAY = 18
    #Volume 10-3 m3.
    VOLUME_LITER = 19
    #Mass m kilogram kg.
    MASS_KG = 20
    #return "Force F newton N.
    FORCE = 21
    #Energy newtonmeter J = Nm = Ws.
    ENERGY = 22
    PRESSURE_PASCAL = 23
    PRESSURE_BAR = 24
    #Energy joule J = Nm = Ws.
    ENERGY_JOULE = 25
    THERMAL_POWER = 26
    #Active power.
    ACTIVE_POWER = 27
    #Apparent power S.
    APPARENT_POWER = 28
    #Reactive power Q.
    REACTIVE_POWER = 29
    #Active energy W6060s.
    ACTIVE_ENERGY = 30
    #Apparent energy VA6060s.
    APPARENT_ENERGY = 31
    #Reactive energy var6060s.
    REACTIVE_ENERGY = 32
    #Current I ampere A.
    CURRENT = 33
    #Electrical charge Q coulomb C = As.
    ELECTRICAL_CHARGE = 34
    #Voltage.
    VOLTAGE = 35
    ELECTRICAL_FIELD_STRENGTH = 36
    CAPACITY = 37
    RESISTANCE = 38
    #Resistivity.
    RESISTIVITY = 39
    #Magnetic flux F weber Wb = Vs.
    MAGNETIC_FLUX = 40
    INDUCTION = 41
    MAGNETIC = 42
    INDUCTIVITY = 43
    #Frequency f.
    FREQUENCY = 44
    ACTIVE = 45
    #Reactive energy meter constant.
    REACTIVE = 46
    #Apparent energy meter constant.
    APPARENT = 47
    #V26060s.
    V260 = 48
    #A26060s.
    A260 = 49
    MASS_KG_PER_SECOND = 50
    CONDUCTANCE = 51
    #Temperature in Kelvin.
    KELVIN = 52
    V2H = 53
    A2H = 54
    CUBIC_METER_RV = 55
    #Percentage.
    PERCENTAGE = 56
    #Ah ampere hours.
    AMPERE_HOURS = 57
    ENERGY_PER_VOLUME = 60
    WOBBE = 61
    #Mol % molar fraction of gas composition mole percent (Basic gas composition unit).
    MOLE_PERCENT = 62
    MASS_DENSITY = 63
    #Dynamic viscosity pascal second =Characteristic of gas stream).
    PASCAL_SECOND = 64
    JOULE_KILOGRAM = 65
    # Pressure, gram per square centimeter.
    PRESSURE_GRAM_PER_SQUARE_CENTIMETER = 66
    # Pressure, atmosphere.
    PRESSURE_ATMOSPHERE = 67
    # dBm Signal strength =e.g.  of GSM radio systems).
    SIGNAL_STRENGTH = 70
    # Signal strength dB microvolt.
    SIGNAL_STRENGTH_MICRO_VOLT = 71
    # Logarithmic unit that expresses the ratio between two values of a physical quantity.
    DB = 72
    # Length in inches.
    INCH = 128
    # Foot (Length).
    FOOT = 129
    # Pound (mass).
    POUND = 130
    # Fahrenheit.
    FAHRENHEIT = 131
    # Rankine.
    RANKINE = 132
    # Square inch.
    SQUARE_INCH = 133
    # Square foot.
    SQUARE_FOOT = 134
    # Acre.
    ACRE = 135
    # Cubic inch.
    CUBIC_INCH = 136
    # Cubic foot.
    CUBIC_FOOT = 137
    # Acre foot.
    ACRE_FOOT = 138
    # Gallon (imperial).
    GALLON_IMPERIAL = 139
    #  Gallon (US).
    GALLON_US = 140
    # Pound force.
    POUND_FORCE = 141
    # Pound force per square inch.
    POUND_FORCE_PER_SQUARE_INCH = 142
    # Pound per cubic foot.
    POUND_PER_CUBIC_FOOT = 143
    # Pound per (foot second).
    POUND_PER_FOOT_SECOND = 144
    # Square foot per second.
    SQUARE_FOOT_PER_SECOND = 145
    # British thermal unit.
    BRITISH_THERMAL_UNIT = 146
    # Therm EU.
    THERM_EU = 147
    # Therm US.
    THERM_US = 148
    # British thermal unit per pound.
    BRITISH_THERMAL_UNIT_PER_POUND = 149
    # British thermal unit per cubic foot.
    BRITISH_THERMAL_UNIT_PER_CUBIC_FOOT = 150
    # Cubic feet.
    CUBIC_FEET = 151
    # Foot per second.
    FOOT_PER_SECOND = 152
    # Cubic foot per second.
    CUBIC_FOOT_PER_SECOND = 153
    # Cubic foot per min.
    CUBIC_FOOT_PER_MIN = 154
    # Cubic foot per hour.
    CUBIC_FOOT_PER_HOUR = 155
    # Cubic foot per day
    CUBIC_FOOT_PER_DAY = 156
    # Acre foot per second.
    ACRE_FOOT_PER_SECOND = 157
    # Acre foot per min.
    ACRE_FOOT_PER_MIN = 158
    #  Acre foot per hour.
    ACRE_FOOT_PER_HOUR = 159
    #  Acre foot per day.
    ACRE_FOOT_PER_DAY = 160
    # Imperial gallon.
    IMPERIAL_GALLON = 161
    # Imperial gallon per second.
    IMPERIAL_GALLON_PER_SECOND = 162
    # Imperial gallon per min.
    IMPERIAL_GALLON_PER_MIN = 163
    # Imperial gallon per hour.
    IMPERIAL_GALLON_PER_HOUR = 164
    # Imperial gallon per day.
    IMPERIAL_GALLON_PER_DAY = 165
    # US gallon.
    US_GALLON = 166
    # US gallon per second.
    US_GALLON_PER_SECOND = 167
    # US gallon per min.
    US_GALLON_PER_MIN = 168
    # US gallon per hour.
    US_GALLON_PER_HOUR = 169
    # US gallon per day.
    US_GALLON_PER_DAY = 170
    # British thermal unit per second.
    BRITISH_THERMAL_UNIT_PER_SECOND = 171
    # British thermal unit per minute.
    BRITISH_THERMAL_UNIT_PER_MIN = 172
    # British thermal unit per hour.
    BRITISH_THERMAL_UNIT_PER_HOUR = 173
    # British thermal unit per day.
    BRITISH_THERMAL_UNIT_PER_DAY = 174
    #Other Unit.
    OTHER_UNIT = 254
    #No Unit.
    NO_UNIT = 255

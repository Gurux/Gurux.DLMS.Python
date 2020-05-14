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
import datetime

#  Reserved for internal use.
#pylint222: disable=bad-option-value,old-style-class,too-few-public-methods
class GXTimeZone(datetime.tzinfo):
    """
    UTC offset from UTC.

    :param offset:
        UTC time zone offset in minutes.
    """
    def __init__(self, offset):
        self._offset = datetime.timedelta(seconds=offset * 60)
        if offset == 0:
            self._name = "Z"
        else:
            if offset > 0:
                self._name = "+"
            else:
                self._name = "-"
            self._name += str(int(offset / 60)).zfill(2)
            self._name += ":"
            self._name += str(offset % 60).zfill(2)

    def utcoffset(self, dt):
        ###UTC offset in seconds.
        return self._offset

    def dst(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return self._name

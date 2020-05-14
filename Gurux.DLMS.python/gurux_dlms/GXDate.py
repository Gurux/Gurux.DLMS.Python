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
import datetime
from .GXDateTime import GXDateTime
from .enums import DateTimeSkips

class GXDate(GXDateTime):
    def __init__(self, value=None, pattern=None):
        """
        Constructor.

        pattern: Date-time pattern that is used when value is a string.
        value: Date value.
        """
        GXDateTime.__init__(self, value, pattern)
        self.skip |= DateTimeSkips.HOUR
        self.skip |= DateTimeSkips.MINUTE
        self.skip |= DateTimeSkips.SECOND
        self.skip |= DateTimeSkips.MILLISECOND

    def _remove(self, format_):
        format_ = GXDateTime._remove_(format_, "%H", True)
        format_ = GXDateTime._remove_(format_, "%-H", True)
        format_ = GXDateTime._remove_(format_, "%I", True)
        format_ = GXDateTime._remove_(format_, "%-I", True)
        format_ = GXDateTime._remove_(format_, "%M", True)
        format_ = GXDateTime._remove_(format_, "%-M", True)
        format_ = GXDateTime._remove_(format_, "%S", True)
        format_ = GXDateTime._remove_(format_, "%-S", True)
        str_ = datetime.datetime.now().strftime('%p')
        format_ = GXDateTime._remove_(format_, str_, True)
        return format_

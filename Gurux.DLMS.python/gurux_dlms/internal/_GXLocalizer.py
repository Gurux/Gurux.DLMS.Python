#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename: $HeadURL$
#
#  Version: $Revision$,
#                $Date$
#                $Author$
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
import gettext
import os
from collections.abc import Iterable

# This class is used to localize the texts.
class _GXLocalizer:
    #Used language.
    __lang = None

    # pylint: disable=bare-except, broad-exception-caught
    # Return localized value.
    @staticmethod
    def gettext(value):
        try:
            if _GXLocalizer.__lang:
                return _GXLocalizer.__lang.gettext(value)
        except Exception:
            pass
        #Return default value if language is not available.
        return value

    # pylint: disable=bare-except
    @staticmethod
    def init(lang_code):
        try:
            if isinstance(lang_code, Iterable) and not isinstance(lang_code, (str, bytes)):
                if "_" in lang_code[0]:
                    lang_code = lang_code[0].split('_')[0]
            locale_path = os.path.join(os.path.dirname(__file__), "locale")
            _GXLocalizer.__lang = gettext.translation(
                "gurux_dlms", localedir=locale_path, languages=[lang_code], fallback=True
            )
            _GXLocalizer.__lang.install()
        except Exception:
            pass

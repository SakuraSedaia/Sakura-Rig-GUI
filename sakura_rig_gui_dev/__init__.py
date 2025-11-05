# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from . import (
    SedaiaOperators_Dev,
    sacrUI_R8_UI1,
    addon_prefs
)

modules = [
    SedaiaOperators_Dev,
    sacrUI_R8_UI1,
    addon_prefs
]


def register():
    for mod in modules:
        mod.register()


def unregister():
    for mod in modules:
        mod.unregister()


if __name__ == "__main__":
    register()

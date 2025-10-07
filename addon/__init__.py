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

bl_info = {
    "name": "Sakura Rig GUI Experimental",
    "author": "Sakura Sedaia",
    "version": (2, 0, 0, 0),
    "blender": (4, 5, 0),
    "location": "3D View > SACR UI",
    "description": "An Addon containing control scripts for Sakura's Rigs",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "User Interface",
}

from . import (sedaia_operators, global_gui, sacr_r7_0_gui, sacr_r8_0_gui)

modules = [sedaia_operators, global_gui, sacr_r7_0_gui, sacr_r8_0_gui]

def register():
    for mod in modules:
        mod.register()
def unregister():
    for mod in modules:
        mod.unregister()
if __name__ == "__main__":
    register()

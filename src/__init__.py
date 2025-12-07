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
    "name": "Rig GUIs and Utilities",
    "category": "Interface",
    "author": "Sakura Sedaia <sakusedaia@outlook.com>",
    "version": (3, 0, 0),
    "blender": (5, 0, 0),
    "location": "",
    "description": "",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "wiki_url": "",
}

import bpy
from importlib import reload

if "modules" in locals():
    reload(modules)
else:
    from . import modules

O = bpy.ops
# Manifest
module_info = {
    "author": "Sakura Sedaia",
    "author_id": "SEDAIA",

    "name": "Player Skin Manager",
    "id": "SKIN_MANAGER",
    "version": (1, 0, 0),
    "description": "A Skin Management utility which allows users to download, load, and apply Skins from Mojang Servers",
    "type": "util",

    "blender": (5, 0, 0),

    "warning": "",
    "doc_url": "",
    "tracker_url": "",
}


def register():
    modules.register()


def unregister():
    modules.unregister()


if __name__ == "__main__":
    register()

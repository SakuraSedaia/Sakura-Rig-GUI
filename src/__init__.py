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

from importlib import reload

bl_info = {
    "name": "Sakuras Rig Interfaces",
    "category": "Interface",
    "author": "Sakura Sedaia <sakusedaia@outlook.com>",
    "version": (3, 1, 0),
    "blender": (5, 0, 0),
    "location": "",
    "description": "",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "wiki_url": "",
}

if "modules" in locals():
    reload(modules)
else:
    from . import modules


def register():
    modules.register()


def unregister():
    modules.unregister()


if __name__ == "__main__":
    register()

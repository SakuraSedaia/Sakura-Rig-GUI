# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# =============
# region Addon Manifest
from typing import Optional
from bpy.ops import wm
from bpy.utils import extension_path_user
from bpy.props import StringProperty, BoolProperty
from bpy.types import AddonPreferences, Context, Preferences, Operator
import bpy

bl_info = {
    "name": __package__,  # UI Name
    "id": "sedaia_prefs",  # UI ID
    "author": "Sakura Sedaia",
    "author_id": "Sedaia",

    "version": (1, 0, 1),
    "blender": (5, 0, 0),
    "location": "",
    "description": "Addon User Preferences",
    "warning": "",
    "doc_url": "",
    "tracker_url": "https://github.com/SakuraSedaia/Sedaia-Rig-Interfaces/issues",
    "category": "Interface",
}
# endregion
# =============
# region Rig Settings
config: dict = {
    'root_default_dir': extension_path_user(bl_info["name"], create=True, path=""),
    'rig_default_dir': extension_path_user(bl_info["name"], create=True, path="rigs"),
    'player_default_dir': extension_path_user(bl_info["name"], create=True, path="playerdata")
}


# endregion
# =============
# region Class Index
ops = {
    'file_open': "sedaia_prefs_ot.file_open"
}


# endregion
# =============
# region Start Preferences
class PREFS_user_preferences(AddonPreferences):
    bl_idname = bl_info['name']

    prompt_to_refresh_player_data: BoolProperty(
        name="Prompt to Regen Player Data",
        default=True
    )

    def draw(self, context):
        pref = self.layout
        pref.operator(ops['file_open'],
                      icon="FILEBROWSER").path = config['root_default_dir']

        row = pref.row()
        col = row.column()
        col.prop(self, 'prompt_to_refresh_player_data', toggle=True)


# endregion
# =============
# region Operator Functions (def)
def get_prefs(context: Optional[Context] = None) -> Optional[Preferences]:
    """
    Intermediate method for grabbing preferences
    """
    if not context:
        context = bpy.context
    prefs = None

    if hasattr(context, "preferences"):
        prefs = context.preferences.addons.get(__package__, None)
    if prefs:
        return prefs.preferences
    return None


# endregion
# =============
# region Operator Classes
class PREFS_file_open(Operator):
    bl_label = "Open"
    bl_idname = ops['file_open']

    path: StringProperty()

    def execute(self, context):
        wm.path_open(filepath=self.path)
        return {'FINISHED'}


# endregion
# =============
# region Registering
classes = [
    PREFS_user_preferences,
    PREFS_file_open,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
# endregion
# =============

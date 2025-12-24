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
from pathlib import Path
import bpy.types as T
import bpy.props as P
import bpy.utils as U
import bpy.ops as O
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
# region Class Index
ops = {
    'file_open': "sedaia_prefs_ot.file_open"
}

# endregion
# region Operator Functions (def)
def get_prefs(context: Optional[T.Context] = None) -> Optional[T.Preferences]:
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
# region Start Preferences
class PREFS_user_preferences(T.AddonPreferences):
    bl_idname = bl_info['name']

    prompt_to_refresh_player_data: P.BoolProperty(
        name="Prompt to Regen Player Data",
        default=True
    )

    root_dir : P.StringProperty(name="Root Directory", subtype='FILE_PATH', default=U.extension_path_user(bl_info['name'], path="", create=True))

    player_dir : P.StringProperty(name="Player Directory", subtype='FILE_PATH', default=U.extension_path_user(bl_info['name'], path="playerdata", create=True))

    rig_dir : P.StringProperty(name="Rig Directory", subtype='FILE_PATH', default=U.extension_path_user(bl_info['name'], path="rig", create=True))

    debug : P.BoolProperty(name="Debug Mode", default=True)

    def draw(self, context):
        pref = self.layout
        row = pref.row()
        box = row.box()
        col = box.column()
        col.prop(self, 'prompt_to_refresh_player_data', toggle=True, text="Ask for Player Regen")
        col.prop(self, 'debug', toggle=True, text="Debug Mode")

        row = pref.row()
        box = row.box()
        row = box.row()
        row.label(text="Player Data")
        row = box.row(align=True)
        row_l = row.row()
        row_l.ui_units_x = 6
        row_l.alignment = 'LEFT'
        row.operator(ops['file_open'], text="Open Directory", icon="FILEBROWSER").path = self.player_dir
        row_r = row.row()
        row_r.prop(self, 'player_dir', text="")


        row = pref.row()
        box = row.box()
        row = box.row()
        row.label(text="Rig Data")
        row = box.row(align=True)
        row.prop(self, 'rig_dir', text="")
        row_l = row.row()
        row_l.ui_units_x = 6
        row_l.alignment = 'LEFT'
        row_l.operator(ops['file_open'], text="Open Directory", icon="FILEBROWSER").path = self.rig_dir


# endregion
# region Operator Classes
class PREFS_file_open(T.Operator):
    bl_label = "Open"
    bl_idname = ops['file_open']

    path: P.StringProperty()

    def execute(self, context):
        try:
            O.wm.path_open(filepath=self.path)

            return {'FINISHED'}
        except FileNotFoundError:
            self.report({'ERROR'}, f"Directory '{self.path}' does not exist.")
            return {'CANCELLED'}



# endregion
# =============
# region Registering
classes = [
    PREFS_user_preferences,
    PREFS_file_open,
]


def register():
    for cls in classes:
        U.register_class(cls)


def unregister():
    for cls in classes:
        U.unregister_class(cls)
# endregion
# =============

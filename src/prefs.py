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

# =============
# region Addon Manifest
module_info = {
    "author": "Sakura Sedaia",
    "author_id": "SEDAIA",

    "name": __package__,
    "id": "sedaia_prefs",
    "version": (1, 0, 0),
    "description": "The Preferences used by the Addon",

    "blender": (5, 0, 0),

    "warning": "",
    "doc_url": "",
    "tracker_url": "",
}
# endregion
# =============
# region Imports and Common Variables
import bpy
from bpy.types import AddonPreferences, Context, Preferences, Operator, PropertyGroup
from bpy.props import StringProperty, IntProperty, EnumProperty, BoolProperty
from bpy.utils import extension_path_user
from bpy_extras.io_utils import ImportHelper
from bpy.ops import wm
from typing import List, Optional, Union, Tuple, Literal

import os
import shutil

from .utils.id import ModuleID


# endregion
# =============
# region Rig Settings
config: dict = {
    'root_default_dir': extension_path_user(module_info["name"], create=True, path=""),
    'rig_default_dir': extension_path_user(module_info["name"], create=True, path="rigs"),
    'player_default_dir': extension_path_user(module_info["name"], create=True, path="playerdata")
}


# endregion
# =============
# region Class Index
ops = {
    'import_ui': str(ModuleID(cls="O", id='ui_import', cat='Preferences')),
    'file_open': str(ModuleID(cls="O", id='file_open', cat='Preferences'))
}


# endregion
# =============
# region Start Preferences
class PREFS_user_preferences(AddonPreferences):
    bl_idname = module_info['name']

    debug: BoolProperty(
        name='Debug',
        default=True
    )  # type: ignore
    skin_downloader: BoolProperty(
        name='Skin Downloader',
        default=True
    )  # type: ignore
    prompt_to_refresh_player_data: BoolProperty(
        name="Prompt to Regen Player Data",
        default=True
    )  # type: ignore
    http_timeout: IntProperty(
        name="HTTP Timeout (Seconds)",
        min=0,
        max=60,
        default=30
    )  # type: ignore
    file_dir: StringProperty(
        name="File Dictory",
        default=config['root_default_dir'],
        subtype="FILE_PATH"
    )  # type: ignore
    player_dir: StringProperty(
        name="Player Data Directory",
        default=config['player_default_dir'],
        subtype="FILE_PATH"
    )  # type: ignore
    rig_dir: StringProperty(
        name="Rig Directory",
        default=config['rig_default_dir'],
        subtype="FILE_PATH"
    )  # type: ignore

    def draw(self, context):
        pref = self.layout
        pref.operator(ops['file_open'], icon="FILEBROWSER").path = config['root_default_dir']

        row = pref.row()
        col = row.column()
        col.prop(self, 'prompt_to_refresh_player_data', toggle=True)
        col.prop(self, 'debug', toggle=True)
        col.operator(ops['import_ui'])

        col = pref.column()
        col.prop(self, 'skin_downloader', toggle=True)
        col.prop(self, 'http_timeout', toggle=True)

        row = pref.row()
        col = row.column()
        col.prop(self, 'file_dir')

        col = row.column()
        col.prop(self, 'player_dir')
        col.prop(self, 'rig_dir')


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
    # To make the addon stable and non-exception prone, return None
    # raise Exception("Could not fetch user preferences")
    return None


# endregion
# =============
# region Operator Classes


class PREFS_import_ui(Operator, ImportHelper):
    bl_idname = ops['import_ui']
    bl_label = ""

    fileparams = 'use_filter_blender'
    files = bpy.props.CollectionProperty(types=PropertyGroup)

    def execute(self, context):
        uiLocation = bpy.path.abspath(self.filepath)
        base = os.path.basename(uiLocation)
        print(base)

        return {'FINISHED'}


class PREFS_file_open(Operator):
    bl_label = "Open"
    bl_idname = ops['file_open']

    path: StringProperty()  # type: ignore

    def execute(self, context):
        wm.path_open(filepath=self.path)
        return {'FINISHED'}


# endregion
# =============
# region Registering
classes = [
    PREFS_user_preferences,
    PREFS_file_open,
    PREFS_import_ui
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
# endregion
# =============

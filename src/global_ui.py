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
    "author_id": "Sedaia",

    "name": "Sedaia Main Interface",
    "id": "sedaia_main",
    "version": (1, 0, 0),
    "description": "",
    "type": "interface",  # Options: util, interface

    "blender": (5, 0, 0),

    "warning": "",
    "doc_url": "",
    "tracker_url": "",
}

# endregion
# =============
# region Imports and Common Variables
import bpy
from bpy.types import (
    Panel,
    Operator,
    Menu
)
from bpy.props import (
    StringProperty,
    IntProperty,
    BoolProperty,
    EnumProperty,
    RemoveProperty,
    PointerProperty
)
from bpy.utils import (
    extension_path_user,
    register_class,
    unregister_class
)

# Import Sedaia Specific Modules
from .utils import sedaia_utils
from . import prefs

# Common BPY calls
T = bpy.types
P = bpy.props
O = bpy.ops
C = bpy.context
D = bpy.data

# endregion
# =============
# region Addon Metadata (DO NOT MODIFY THIS AREA)
bl_info = {
    "name": module_info["name"],
    "author": module_info["author"],
    "version": module_info['version'],
    "blender": module_info["blender"],
    "location": "",
    "description": module_info["description"],
    "warning": "",
    "doc_url": module_info["doc_url"],
    "tracker_url": module_info["tracker_url"],
    "category": "Interface",
}

# endregion
# =============
# region Module Settings
config = {
    "tab": "Sedaia Skin Utility",

    # Skin Settings
    "utility_bone_name": "Sedaia.Skin_Utility_Config",
    "skin_path": prefs.config['player_default_dir'],
}

# endregion
# =============
# region Properties Start

# endregion
# =============
# region Functions (def) Start

# endregion
# =============
# region Class Start


# endregion
# =============
# region Panel Template
class SEDAIA_MAIN_PT_ui_main(Panel):
    # Panel Info
    bl_label = "Sedaia Utilities"
    bl_idname = "SEDAIA_MAIN_PT_main"
    bl_order = 0

    # Tab Info (DO NOT CHANGE)
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = config['tab']

    @classmethod
    def poll(self, context):
        return True

    def draw(self, context):

        # UI Structure
        panel = self.layout

        row = panel.row()
        row.label(text="This is a Row")

        panel.separator(type="LINE")

        row = panel.row()
        box = row.box()
        box.label(text="This is a Box")

        panel.separator(type="LINE")

        row = panel.row()
        col = row.column()
        col.label(text="This is a Column")


# endregion
# =============
# region Skin Utility
class SEDAIA_MAIN_PT_ui_skinUtility(Panel):
    # Panel Info
    bl_label = "Skin Utility"
    bl_idname = "SEDAIA_MAIN_PT_skin_utility_ui"
    bl_category = config['tab']
    bl_order = 0

    # Tab Info (DO NOT CHANGE)
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = config['tab']

    @classmethod
    def poll(self, context):
        try:
            r = context.active_object
            if r and r.type == "ARMATURE" and r.data:
                if context.active_object.pose.bones[config["utility_bone_name"]] is not None:
                    return True
                else:
                    return False
            else:
                return False
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        # Rig Data
        rig = context.active_object
        rig_bones = rig.pose.bones
        try:
            skinProp = rig_bones[config['utility_bone_name']]
        except (KeyError):
            skinProp = None
        if skinProp is not None:
            panel = self.layout
            p_row = panel.row()
            p_row.label(text="Minecraft Username")

            p_row = panel.row()
            b_col = p_row.column(align=True)
            c_row = b_col.row()

            c_row.prop(skinProp, '["Username"]', text="")
            c_row = b_col.row(align=True)
            c_row.operator(sedaia_utils.ops['skin_router'], icon="URL", text="Change Skin")
            c_row.operator(
                sedaia_utils.ops['file_open'],
                icon="FILEBROWSER",
                text="Player Data").path = config["skin_path"]
            panel.separator(type="LINE")

            p_row = panel.row()
            p_row.label(text="Options")

            p_row = panel.row()
            b_col = p_row.column()
            b_col.prop(
                skinProp, '["SyncArms"]', toggle=False, text="Sync Arm Type")

            b_col.prop(
                skinProp, '["SyncCape"]', toggle=False, text="Sync Cape Status")

            b_col.prop(
                skinProp, '["SyncName"]', toggle=False, text="Set Rig Name to Username")


# endregion
# =============
# region Registering Start
classes = [
    SEDAIA_MAIN_PT_ui_skinUtility
]


def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()

# endregion
# =============

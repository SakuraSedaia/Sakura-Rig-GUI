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

# region Imports and Common Variables
from .. import prefs
from ..utils import sedaia_utils
from bpy.utils import register_class, unregister_class
from bpy.types import Panel

# endregion
# region Addon Manifest
bl_info = {
    "name": "Sedaia Main Interface",  # UI Name
    "id": "sedaia_main",  # UI ID
    "author": "Sakura Sedaia",
    "author_id": "Sedaia",

    "version": (1, 0, 1),
    "blender": (5, 0, 0),
    "location": "",
    "description": "The primary interface for all global operators",
    "warning": "",
    "doc_url": "",
    "tracker_url": "https://github.com/SakuraSedaia/Sedaia-Rig-Interfaces/issues",
    "category": "Interface",
}
# endregion
# region Module Settings
class SEDAIA_SKIN_PT:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Download Skins"

# endregion
# region Skin Utility
class SEDAIA_SKIN_PT_ui_skinUtility(SEDAIA_SKIN_PT, Panel):
    # Panel Info
    bl_label = "Skin Utility"
    bl_idname = "SEDAIA_MAIN_PT_skin_utility_ui"
    bl_order = 0

    utility_bone_name = "Sedaia.Skin_Utility_Config"
    skin_path = prefs.config['player_default_dir']
    cape_enable = False

    @classmethod
    def poll(self, context):
        try:
            r = context.active_object
            if r and r.type == "ARMATURE" and r.data:
                if context.active_object.pose.bones[self.utility_bone_name] is not None:
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
            skinProp = rig_bones[self.utility_bone_name]
        except KeyError:
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
            c_row.operator(
                sedaia_utils.ops['skin_router'], icon="URL", text="Change Skin")
            c_row.operator(
                sedaia_utils.ops['file_open'],
                icon="FILEBROWSER",
                text="Player Data").path = self.skin_path
            panel.separator(type="LINE")

            p_row = panel.row()
            p_row.label(text="Options")

            p_row = panel.row()
            b_col = p_row.column()
            b_col.prop(
                skinProp, '["SyncArms"]', toggle=False, text="Sync Arm Type")
            if self.cape_enable:
                b_col.prop(
                    skinProp, '["SyncCape"]', toggle=False, text="Sync Cape Status")

            b_col.prop(
                skinProp, '["SyncName"]', toggle=False, text="Set Rig Name to Username")

# endregion
# region Registering Start
classes = [
    SEDAIA_SKIN_PT_ui_skinUtility
]

def register():
    for cls in classes:
        register_class(cls)

def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

# endregion

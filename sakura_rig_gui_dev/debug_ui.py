import bpy
from bpy.types import Panel, Operator, AddonPreferences
from bpy.props import StringProperty, BoolProperty, IntProperty
from .addon_prefs import get_addon_preferences


rig_dir = bpy.utils.extension_path_user(
    __package__, create=True, path="rig_cache")


rig = "SACR"
rig_ver = 8
ui_ver = 1
category = f"{rig} R{rig_ver}"

mat_obj_name = "Material_Properties"
prop_bones = [
    "Properties.RigMain",  # 0
    "Properties.Head",    # 1
    "Properties.Torso",   # 2
    "Properties.Arms",    # 3
    "Properties.Legs",     # 4
    "Properties.Skin_Grabber"  # 5
]


# Working Directories
addon_dir = bpy.utils.extension_path_user(
    __package__, create=True, path="")

rig_dir = bpy.utils.extension_path_user(
    __package__, create=True, path="rigs")

player_dir = bpy.utils.extension_path_user(
    __package__, create=True, path="playerdata")


class SEDAIA_DEV_PT_ui_debug(Panel):
    bl_label = "Operator Debugging"
    bl_category = "SACR Debug Util"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        try:
            r = context.active_object
            if r and r.type == "ARMATURE" and r.data:
                return get_addon_preferences().debug
            else:
                return False
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):

        rig = context.active_object
        rig_bones = rig.pose.bones
        skinProp = rig_bones[prop_bones[5]]

        layout = self.layout
        box = layout.box()
        row = box.row()
        row.label(text="Skin Downloader Operators")
        row = box.row()
        col = row.column()
        col.prop(skinProp, '["username"]', text="")
        col.operator("sedaia_ot.change_skin", icon="URL", text="Update Skins")


classes = [
    SEDAIA_DEV_PT_ui_debug
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

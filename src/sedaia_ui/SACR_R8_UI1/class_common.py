
from ... utils.util_global import *

import bpy
import bpy.ops as O
import bpy.types as T
import bpy.props as P
import bpy.utils as U

IN_DEVELOPMENT = True

rig_info = {
  "module":  {
    "name": "Sakura Rig UI",
    "id": "SR_GUI",
    "author": "Sakura Sedaia",
    "author_id": "Sedaia",

    "version": "1.0.0_a",
    "category": "SACR R8"
  },
  "rig": {
    "name": "Sakura's Advanced Character Rig",
    "alias": "SACR",
    "version": "8.0.0_a",
    "rig_id": "SACR.Rev_8.UI_1"
  }
}

# region Object IDs
panel_prefix = "SEDAIA_SACR8_UI1_PT"
panels = {
    "info": f"{panel_prefix}_ui_info",
    "config": f"{panel_prefix}_ui_config",

    # Rig Configs
    "rig_config": f"{panel_prefix}_sui_rig_config",

    # Visual Configs
    "visual_config": f"{panel_prefix}_sui_visual_config",

    # Material Configs
    "material_config": f"{panel_prefix}_sui_material_config",

    # Face Panels
    "face_config": f"{panel_prefix}_sui_face_config",
    "eyebrows_config": f"{panel_prefix}_sui_eyebrow_material",
    "eyes_config": f"{panel_prefix}_sui_eye_material",
    "mouth_config": f"{panel_prefix}_sui_mouth_material",

    # Body Panels
    "torso_config": f"{panel_prefix}_sui_torso_config",
    "arm_config": f"{panel_prefix}_sui_arm_config",
    "leg_config": f"{panel_prefix}_sui_leg_config"
}

class SacrPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = rig_info["module"]["category"]

    config_objs = {
        "main": "Properties.Rig",
        "head": "Properties.Head",
        "torso": "Properties.Torso",
        "eyes": "Properties.Arms",
        "arms": "Properties.Arms",
        "legs": "Properties.Legs",
        "face": "Properties.Face",
        "skin": "Skin_Properties",
        "root_bone": "SACR_Root"
    }

    @classmethod
    def poll(self, context):
        rig_id = rig_info["rig"]["rig_id"]
        r = context.active_object
        try:
            if r and r.type == "ARMATURE" and r.data:
                key = find_key(r.data, rig_id)
                return r.data[key] == rig_id
            else:
                return False
        except (AttributeError, KeyError, TypeError):
            return False

class SacrFace:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = rig_info["module"]["category"]

    @classmethod
    def poll(self, context):
        o = context.active_object
        ft = o.pose.bones["Rig_Properties"]["Face Toggle"]
        return ft


# endregion
# region Custom Properties

# Rig Mode
T.Armature.PanelMode = P.EnumProperty(
    name="Rig Mode",
    default="0",
    items=[
        ("0", "Rig", "Configuration of the Rig"),
        ("1", "Visual", "Visual Characteristics of the Rig"),
        ("2", "Materials", "Material Settings")
    ]
)
T.PoseBone.ArmType_R8 = P.EnumProperty(
    name="Arm Type",
    default="0",
    items=[
        ("0", "Standard", "Standard Arm Style, formerly called Steve Arms"),
        ("1", "Slim", "Slim Arm Style, formerly called Steve Arms"),
        ("2", "Super-Slim", "Super Slim Arm style are a 3x3 version not available in Minecraft")
    ]
)

# Rig Name:
def update_name(self, context):
    O.sedaia_utils_ot.rig_rename(name=context.active_object.data.RigName, update_collection=True)

T.Armature.RigName = P.StringProperty(name="Rig Name", update=update_name)

# Eye Section
T.PoseBone.EYES_visual_style = P.EnumProperty(
    name="Visual Style",
    default="0",
    items=[
        ("0", "Flat", "Flat Eye Style"),
        ("1", "3D", "Classic Eye Style"),
    ]
)
T.PoseBone.EYES_section = P.EnumProperty(
    name="Eye Section",
    default="0",
    items=[
        ("0", "Iris", "Collection of Properties for the Iris"),
        ("1", "Sclera", "Collection of properties for the Sclera")
    ]
)
# Eye Section
T.PoseBone.MOUTH_visual_style = P.EnumProperty(
    name="Visual Style",
    default="0",
    items=[
        ("0", "Flat", "Flat Mouth Style"),
        ("1", "3D", "Classic Mouth Style"),
    ]
)


# TODO: Add in the Enumerator for switching Ankle Style
# endregion

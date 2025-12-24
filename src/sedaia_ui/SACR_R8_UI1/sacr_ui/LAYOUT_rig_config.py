# Addon Imports
from ..class_common import *
from ....utils import util_global

# Face Imports
from .LAYOUT_eyebrows.eyebrows_rig import *
from .LAYOUT_eyes.eyes_rig import *
from .LAYOUT_mouth.mouth_rig import *

# Body Imports
from .LAYOUT_arms.arms_rig import *
from .LAYOUT_legs.legs_rig import *


# BPY imports
import bpy
import bpy.types as T
import bpy.props as P
import bpy.utils as U
import bpy.ops as O

# Layout
def LAYOUT_rig_config(self, context):
    obj = context.active_object
    obj_col = obj.users_collection[0]
    obj_data = obj.data
    rig_bones = obj.pose.bones
    rig_pose = obj.pose
    rig_bc = obj_data.collections_all
    obj_child = obj.children_recursive

    lite = obj_data['SACR_lite']

    # Property Bones
    main_prop = rig_bones[self.config_objs['main']]
    head_prop = rig_bones[self.config_objs['head']]
    leg_prop = rig_bones[self.config_objs['legs']]

    # Interface
    ui = self.layout
    row = ui.row()
    row.label(text="Rig Settings:", icon="ARMATURE_DATA")
    ui.separator(type="LINE")

    # Face Settings
    face_panel = ui.panel(idname=panels['face_config'])

    header = face_panel[0]
    header.label(text="Face")
    header.prop(head_prop, '["FaceToggle"]', text="Enable", icon="CHECKBOX_HLT" if head_prop["FaceToggle"] is True else "CHECKBOX_DEHLT")

    sub_panel = face_panel[1]
    if head_prop["FaceToggle"] and sub_panel is not None:
        LAYOUT_eyebrows(self, context, ui=sub_panel)
        sub_panel.separator(type="LINE")
        LAYOUT_eyes(self, context, ui=sub_panel)
        sub_panel.separator(type="LINE")
        LAYOUT_mouth(self, context, ui=sub_panel)

    row = ui.row()
    LAYOUT_arm(self, context, sub_panel)
    LAYOUT_leg(self, context, sub_panel)


# Addon Imports
from ...class_common import *
from .....utils import util_global

# BPY imports
import bpy
import bpy.types as T
import bpy.props as P
import bpy.utils as U
import bpy.ops as O

# Layout
def LAYOUT_arm(self, context, ui):
    obj = context.active_object
    obj_col = obj.users_collection[0]
    obj_data = obj.data
    rig_bones = obj.pose.bones
    rig_pose = obj.pose
    rig_bc = obj_data.collections_all
    obj_child = obj.children_recursive

    lite = obj_data['SACR_lite']

    # Collections
    mesh_col = obj_data['MeshCol']


    # Property Bones
    main_prop = rig_bones[self.config_objs['main']]
    head_prop = rig_bones[self.config_objs['arms']]

    # Interface
    panel_arms = ui.panel(idname=panels['arm_config'])

    header = panel_arms[0]
    header.label(text="Arms")

    panel = panel_arms[1]
    if panel is not None:
        row = panel.row()
        row.label(text="Arm Rig Settings")


        # TODO: Add in the switches for IK to FK toggles



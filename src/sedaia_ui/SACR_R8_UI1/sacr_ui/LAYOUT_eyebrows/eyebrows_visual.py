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
def LAYOUT_eyebrows(self, context, ui):
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
    head_prop = rig_bones[self.config_objs['head']]
    face_prop = rig_bones[self.config_objs['face']]

    # Interface
    panel_eyebrow = ui.panel(idname=panels['eyebrows_config'])

    header = panel_eyebrow[0]
    header.label(text="Eyebrows")

    panel = panel_eyebrow[1]
    if panel is not None:
        row = panel.row()
        row.label(text="Eyebrows Visual")

        row = panel.row()
        col = row.column()
        col.prop(face_prop, '["EYEBROWS_depth"]', text="Extrude")
        col.prop(face_prop, '["EYEBROWS_thickness"]', text="Thickness")
        col.prop(face_prop, '["EYEBROWS_width"]', text='Width')


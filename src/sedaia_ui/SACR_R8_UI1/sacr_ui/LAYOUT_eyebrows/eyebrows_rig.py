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
    panel_eyebrows = ui.panel(idname=panels['eyebrows_config'])

    header = panel_eyebrows[0]
    header.label(text="Eyebrows")

    sub_panel = panel_eyebrows[1]
    if sub_panel is not None:
        row = sub_panel.row()
        row.label(text="Eyebrow Rig")

        row = sub_panel.row(align=True)
        row.prop(rig_bc['Left Eyebrow'], 'is_visible', text="Left", toggle=True)
        row.prop(rig_bc['Left Eyebrow Extended'], 'is_visible', text="Extended", toggle=True)

        row = sub_panel.row(align=True)
        row.prop(rig_bc['Right Eyebrow'], 'is_visible', text="Right", toggle=True)
        row.prop(rig_bc['Right Eyebrow Extended'], 'is_visible', text="Extended", toggle=True)




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
def LAYOUT_mouth(self, context, ui):
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
    panel_eyes = ui.panel(idname=panels['mouth_config'])

    header = panel_eyes[0]
    header.label(text="Mouth")

    panel = panel_eyes[1]
    if panel is not None:
        row = panel.row()
        row.label(text="Rig Settings")

        row = panel.row()
        box = row.box()
        row = box.row()
        row.prop(
            rig_bc['Mouth'],
            'is_visible',
            toggle=True,
            text="Controllers"
        )
        if rig_bc['Mouth'].is_visible:
            row = box.row()
            col = row.column()

            col.prop(
                rig_bc['Mouth Basic'],
                'is_visible',
                toggle=True,
                icon="HIDE_ON" if rig_bc['Mouth Basic'].is_visible is False else "HIDE_OFF",
                text="Basic Controls"
            )

            row_1 = col.row(align=True)
            row_1.prop(
                rig_bc['Mouth More'], 'is_visible',
                toggle=True,
                icon="HIDE_ON" if rig_bc['Mouth More'].is_visible is False else "HIDE_OFF",
                text="Guide Controls"
            )

            row_2 = row_1.row()
            row_2.prop(
                rig_bc['Mouth Advanced'], 'is_visible',
                toggle=True,
                icon="HIDE_ON" if rig_bc['Mouth Advanced'].is_visible is False else "HIDE_OFF",
                text="Individual Pins"
        )

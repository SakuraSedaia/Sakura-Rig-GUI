# Addon Imports
from ..class_common import *
from ....utils import util_global
from .LAYOUT_eyes.eyes_material import *

# BPY imports
import bpy
import bpy.types as T
import bpy.props as P
import bpy.utils as U
import bpy.ops as O

# Layout
def LAYOUT_material_config(self, context):
    obj = context.active_object
    obj_col = obj.users_collection[0]
    obj_data = obj.data
    rig_bones = obj.pose.bones
    rig_bc = obj_data.collections_all
    obj_child = obj.children_recursive


    skin_mat = rig_bones[self.config_objs['skin']]["Skin"]
    skin_tex = skin_mat.node_tree.nodes["Skin Texture"].image


    ui = self.layout
    row = ui.row()
    row.label(text="Material Settings:", icon="MATERIAL_DATA")
    ui.separator(type="LINE")

    row = ui.row()
    box = row.box()
    box.label(text="Skin")

    # Change Skin Texture
    row = box.row(align=True)
    row.operator(util_global.ops['image_pack'],
                       icon="PACKAGE" if util_global.is_packed(skin_tex)
                       else "UGLYPACKAGE", text="").path = skin_tex.name

    row = row.row(align=True)
    row.enabled = not util_global.is_packed(skin_tex)
    row.prop(skin_tex, "filepath", text="")
    row.operator(util_global.ops['image_reload'], icon="FILE_REFRESH", text="").path = skin_tex.name

    # TODO: Literally everything in here need to be added.
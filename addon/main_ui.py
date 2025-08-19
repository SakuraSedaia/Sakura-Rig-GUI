import bpy
from bpy.types import Panel, Operator
D = bpy.data
M = bpy.msgbus
O = bpy.ops
T = bpy.types
U = bpy.utils
Pth = bpy.path
A = bpy.app
P = bpy.props


class SEDAIA_PT_Utilities(Panel):
    bl_idname = "SEDAIA_PT_utils"
    bl_label = "Sakura Utils"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Sakura Utils"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Scene Utilities")

        scene = context.scene

        row = layout.row()
        row.label(text="Notes")

        row = layout.row()
        box = row.box()
        column = box.column()
        column.label(text="For SACR R8 Development,")
        column.label(text="use unit scale 1.7065")

        layout.separator(type="LINE")
        row = layout.row()
        row.prop(scene.unit_settings, 'scale_length')
        
class SEDAIA_PT_rig_manager(Panel):
    bl_parent_id = "SEDAIA_PT_utils"
    bl_label = "Rig Manager"
    bl_category = "Sakura Rigs"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="TO BE MADE")
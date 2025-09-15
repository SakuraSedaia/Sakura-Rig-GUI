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
        layout.label(text="TO BE MADE")


class SEDAIA_PT_rig_manager(Panel):
    bl_parent_id = "SEDAIA_PT_utils"
    bl_label = "Rig Manager"
    bl_category = "Sakura Rigs"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("sedaia_ot.append_sacr", text="Append SACR Test")

class SEDAIA_OT_AppendSACR(Operator):
    bl_idname= "sedaia_ot.append_sacr"
    bl_label = "Append SACR"
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        appendSACR()
        return {'FINISHED'}
    
def appendSACR(context):
    import os
    
    script_file = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_file)
    
    sacr_base_file = f"{script_dir}/rigs/SACR_R7.3.0.blend"
    bl_folder = "/Collection/"
    collection = "SACR R7.3"
    
    col_path = f"{sacr_base_file}{bl_folder}{collection}"
    col_dir = f"{sacr_base_file}{bl_folder}"
    col_name = f"{collection}"
    
    try:
        bpy.ops.wm.append(filepath=col_path, filename=col_name, directory=col_dir)
    except:
        print("Could not Append Rig")
    
    print(col_path)
    print(context.rig_name)
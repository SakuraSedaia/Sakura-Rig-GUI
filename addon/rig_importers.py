import bpy
import os

from bpy.types import Operator
P = bpy.props

class SEDAIA_OT_Append_SACR_7_3_0(Operator):
    bl_idname= "sedaia_ot.append_sacr_7_3_0"
    bl_label = "Append SACR"
    
    lite : P.BoolProperty()
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        script_file = os.path.realpath(__file__)
        script_dir = os.path.dirname(script_file)
        
        if self.lite is True:
            sacr_file = f"{script_dir}/rigs/SACR_R7.3.0_Lite.blend"
            bl_folder = "/Collection/"
            collection = "SACR R7.3 Lite"
        else:
            sacr_file = f"{script_dir}/rigs/SACR_R7.3.0.blend"
            bl_folder = "/Collection/"
            collection = "SACR R7.3"
        
        col_path = f"{sacr_file}{bl_folder}{collection}"
        col_dir = f"{sacr_file}{bl_folder}"
        col_name = f"{collection}"
        
        try:
            bpy.ops.wm.append(filepath=col_path, filename=col_name, directory=col_dir)
        except:
            print("Could not Append Rig")
            
        return {'FINISHED'}
    
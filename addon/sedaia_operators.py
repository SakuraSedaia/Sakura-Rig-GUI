import bpy
from bpy.types import Operator

D = bpy.data
C = bpy.context
T = bpy.types
P = bpy.props
import os

def is_packed(img):
    try:
        return img.packed_files.values() != []
    except:
        return False
    
class SEDAIA_OT_ImgPack(Operator):
    bl_idname = "sedaia_ot.imgpack"
    bl_label = ""
    
    img_name : P.StringProperty() # type: ignore
    
    def execute(self, context):
        img = bpy.data.images[self.img_name]
        if is_packed(img):
            if bpy.data.is_saved:
                img.unpack()
                
            else:
                img.unpack(method="USE_LOCAL")
        else:
            img.pack()
        return{"FINISHED"}
    
class SEDAIA_OT_ImgReload(Operator):
    bl_idname = "sedaia_ot.imgreload"
    bl_label = ""
    
    img_name : P.StringProperty() # type: ignore
    
    def execute(self,context):
        bpy.data.images(self.img_name).reload()
        return{"FINISHED"}

sedaia_ops = [
    SEDAIA_OT_ImgPack,
    SEDAIA_OT_ImgReload
]
def register():
    for cls in sedaia_ops:
        bpy.utils.register_class(cls)
def unregister():
    for cls in sedaia_ops:
        bpy.utils.unregister_class(cls)
    
class SEDAIA_OT_Append_SACR_7_3_0(Operator):
    bl_idname= "sedaia_ot.append_sacr_7_3_0"
    bl_label = "Append SACR"
    
    lite : P.BoolProperty() # type: ignore
    
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
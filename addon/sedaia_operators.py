
import bpy
from bpy.types import Operator

D = bpy.data
C = bpy.context
T = bpy.types
P = bpy.props

def is_packed(img):
    try:
        return img.packed_files.values() != []
    except:
        return False
    
class SEDAIA_OT_ImgPack(Operator):
    bl_idname = "sedaia_ot.imgpack"
    bl_label = ""
    
    img_name : P.StringProperty()
    
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
    
    img_name : P.StringProperty()
    
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
    
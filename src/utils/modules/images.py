import bpy
import bpy.types as T
import bpy.props as P
import bpy.utils as U
from ..util_global import *


# region Functions
def pack_img(name):
    image = get_img(name)
    if is_packed(image):
        if bpy.data.is_saved:
            image.unpack()
        else:
            image.unpack(method="USE_LOCAL")
    else:
        image.pack()

def get_img(path):
    return bpy.data.images[path]


def reload_img(name):
    get_img(name).reload()


# endregion
# region Image Classes
class IMAGE_pack(T.Operator):
    """Packs an image into the blend file"""
    bl_label = "Pack Image"
    bl_idname = ops['image_pack']
    bl_options = {"REGISTER", "UNDO"}

    path: P.StringProperty()

    def execute(self, context):
        pack_img(self.path)
        return {"FINISHED"}


class IMAGE_reload(T.Operator):
    """Reloads an image from the source file"""
    bl_label = "Reload Image"
    bl_idname = ops['image_reload']
    bl_options = {"REGISTER", "UNDO"}

    path: P.StringProperty()

    def execute(self, context):
        reload_img(self.path)
        return {"FINISHED"}

def register():
    U.register_class(IMAGE_pack)
    U.register_class(IMAGE_reload)

def unregister():
    U.unregister_class(IMAGE_pack)
    U.unregister_class(IMAGE_reload)
import bpy
import bpy.utils as U
import bpy.types as T
import bpy.props as P
import bpy.ops as O
from ..util_global import *

class OT_ChangeSkin(T.Operator):
    bl_idname = ops['change_skin']
    bl_label = "Change Skin"

    def execute(self, context):
        self.report({'INFO'}, "Skin Changed")
        return {"FINISHED"}

class OT_DownloadSkin(T.Operator):
    bl_idname = ops['download_skin']
    bl_label = "Download Skin"

    def execute(self, context):
        self.report({'INFO'}, "Skin Downloaded")
        return {"FINISHED"}

class OT_UpdateSkin(T.Operator):
    bl_idname = ops['update_skin']
    bl_label = "Update Skin"

    def execute(self, context):
        self.report({'INFO'}, "Skin Updated")
        return {"FINISHED"}

class OT_DeleteSkin(T.Operator):
    bl_idname = ops['delete_skin']
    bl_label = "Purge Skin"

    def execute(self, context):
        self.report({'INFO'}, "Skin Purged")
        return {"FINISHED"}

classes = [
    OT_ChangeSkin,
    OT_DownloadSkin,
    OT_UpdateSkin,
    OT_DeleteSkin
]

def register():
    for cls in classes:
        U.register_class(cls)

def unregister():
    for cls in reversed(classes):
        U.unregister_class(cls)
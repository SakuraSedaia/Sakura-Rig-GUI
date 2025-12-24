import bpy
import bpy.types as T
import bpy.utils as U
import bpy.ops as O
import bpy.props as P
from ... import prefs
from bpy.ops import wm
from ..util_global import *

class FILE_open(T.Operator):
    bl_label = "Open"
    bl_idname = ops['file_open']

    path: P.StringProperty(default="")

    def execute(self, context):
        wm.path_open(filepath=self.path)
        return {"FINISHED"}

def register():
    U.register_class(FILE_open)

def unregister():
    U.unregister_class(FILE_open)
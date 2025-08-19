import bpy
import zipfile
import importlib
from urllib import request

from bpy.types import Operator, Panel

remote_url = ""

class SEDAIA_OT_import(Operator):
    bl_idname = "sedaia.import_sacr_r7"
    bl_label = "SACR R7.2.1"
    
    def execute(self, context):
        
        
        return {'FINISHED'}
    
def import_r7(self, rig_preset):
    ...
    

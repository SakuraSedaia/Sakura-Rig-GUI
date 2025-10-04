bl_info = {
    "name": "SACR R8 GUI",
    "author": "Sakura Sedaia",
    "version": (0, 2, 0),
    "blender": (4, 5, 0),
    "location": "3D View > SACR UI",
    "description": "An Addon containing control scripts for SACR R8.0",
    "warning": "This Addon is still heavily in development, please expect issues to be present",
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "User Interface",
}

import bpy
from bpy.types import Operator, Panel
from .sedaia_operators import is_packed

T = bpy.types
P = bpy.props
O = bpy.ops
C = bpy.context
D = bpy.data

# Here are a list of properties which will be compared
# to the rig. Should a value not align with the selected
# object,  The UI will not show up.
rig_id = "SACR.ui_id.1"
rig_id_prop = "rigID"

mesh_mat_obj = "Material_Properties"

# Global Rig Variables
rig = "SACR"
rig_ver = 8
category = f"{rig} R{rig_ver} GUI"


class SEDAIA_PT_SACR8_uiGlobal(Panel):
    bl_idname = "SEDAIA_PT_SACR8_uiGlobal"
    bl_label = "SACR Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_order = 0
    
    @classmethod
    def poll(self, context):
        try:
            r = context.active_object
            if r and r.type == "ARMATURE" and r.data:
                rData = r.data
                return rData[rig_id_prop] == rig_id
            else:
                return False
        except (AttributeError, KeyError, TypeError):
            return False
    
    def draw(self, context):
        # Rig Data
        rig_obj = context.active_object
        rig_data = rig_obj.data
        bones = rig_obj.pose.bones
        
        lite = rig_data["lite"]
        
        # set Child Object Indices
        i = 0
        for l in rig_obj.children:
            i = i + 1
            # Find Material Object
            objName = l.name.split(".")[0]
            if objName == mesh_mat_obj:
                mat_obj_index = l
                break
            
        panel = self.layout
        
        p_row = panel.row()
        p_row.label(text="Test")
        
sacr_8_classes = [
    SEDAIA_PT_SACR8_uiGlobal
]

def register():
    for cls in sacr_8_classes:
        bpy.utils.register_class(cls)
def unregister():
    for cls in sacr_8_classes:
        bpy.utils.unregister_class(cls)
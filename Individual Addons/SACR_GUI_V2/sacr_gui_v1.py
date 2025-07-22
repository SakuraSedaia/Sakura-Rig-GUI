import bpy

# ==========
# bpy forms & other Variables
# ==========
T = bpy.types
addon_id = "sacr_r7_ui"
rig_id_prop = "sacr_id"
rig_id = "sacr_1"
script_format = 0

# Fully Compatible:
# - 7.2.1
# 
# Partially Compatible
# - 7.2.0
#   - Molars do not controllable via script
          

class SACRUI_PT_template(T.Panel):
    bl_label = "Panel Temlate"
    bl_category = 'SACR UI'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    # ============== 
    # Rig Detection
    # ==============
    @classmethod
    def poll(self, context):
      try:
        obj = context.active_object
        if obj and obj.type == 'ARMATURE' and obj.data:
          armature = obj.data
          return armature["sacr_id"] == "sacr_1"
        else:
          return False
      except (AttributeError, KeyError, TypeError):
        return False

    # ============== 
    # Draw Panel
    # ==============
    def draw(self, context):
        layout = self.layout
        rig = context.active_object
        
        try:
          py_compat = rig.data["script_format"]
        except (AttributeError, TypeError, KeyError):
          py_compat = -1
          
        if py_compat == script_format:
            
            layout.row()
            
            face_on = False
            if face_on == True:
                ...
            else:
                ...


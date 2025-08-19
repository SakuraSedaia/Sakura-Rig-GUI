# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy

# ==========
# bpy forms & other Variables
# ==========
T = bpy.types
addon_id = "sacr_r7_ui"

ui_format = 0 # Matched to the variable on an SACR Armature, used for ensuring proper compatability
# Fully Compatible:
# - 7.2.1
# 
# Partially Compatible
# - 7.2.0
#   - Molars do not controllable via script

# ==============
# Properties Start
# ==============
class SACRUI_PT_g_props(T.Panel):
    bl_label = "Global Properties"
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
        
        scene = context.scene
        
        try:
          py_compat = rig.data["script_format"]
        except (AttributeError, TypeError, KeyError):
          py_compat = -1
        
        if py_compat != ui_format:
          propRow = layout.row()
          propBox = propRow.box()
          warnRow = propBox.column()
          warnRow.label(text="WARNING", icon="ERROR")
          warnRow.alignment = 'EXPAND'
          warnRow.label(text="SACR Version not Compatible")
            
        
        gProp = rig.pose.bones['Rig_Properties']
        fProp = rig.pose.bones["Face_Properties"]
        layer = rig.data.collections_all
        
        face_on = gProp['Face Toggle']
        lite = rig.data["lite"]
        
        propRow = layout.row()
        propRow.label(text="Rig Properties", icon="PROPERTIES")
        
        propRow = layout.row()
        propRow.prop(layer["Properties"], "is_visible", text="Enable Classic Props", toggle=True)
        layout.separator(type="LINE")
        
        propRow = layout.row()
        propBox = propRow.box()
        propBox.label(text="Head Settings")
        propBox.prop(gProp,'["Face Toggle"]', toggle=True, text="Enable Facerig")
        
        boxRow = propBox.row()
        if lite == False:
          boxCol = boxRow.column()
          boxCol.prop(gProp,'["Long Hair Rig"]', text="Long Hair")
        
        if face_on == True:   
          boxCol = boxRow.column()
          boxCol.prop(fProp,'["Face | UV"]', text="UV Projection", toggle=True)
        
        propRow = layout.row()
        propBox = propRow.box()
        boxRow = propBox.row()
        boxRow.label(text="Limb Settings")
        
        boxRow = propBox.row()
        boxRow.prop(gProp, '["Slim Arms"]', text="Arm Dimensions")
        
        boxRow = propBox.row()
        propBox.label(text="IK Settings")
        
        boxRow = propBox.row()
        boxCol = boxRow.column()
        boxCol.label(text='Left Arm')
        boxCol.prop(gProp, '["Arm IK"]', index=0, text="Enable", slider=True)
        boxCol.prop(gProp, '["Arm Stretch"]', index=0, text="Stretch", slider=True)
        boxCol.prop(gProp, '["Arm Wrist IK"]', index=0, text="Wrist IK", slider=True)
        
        boxCol = boxRow.column()
        boxCol.label(text='Right Arm')
        boxCol.prop(gProp, '["Arm IK"]', index=1, text="Enable", slider=True)
        boxCol.prop(gProp, '["Arm Stretch"]', index=1, text="Stretch", slider=True)
        boxCol.prop(gProp, '["Arm Wrist IK"]', index=1, text="Wrist IK", slider=True)
        
        boxRow = propBox.row()
        boxCol = boxRow.column()
        boxCol.label(text='Left Leg')
        boxCol.prop(gProp, '["Leg FK"]', index=0, text="Disable", slider=True)
        boxCol.prop(gProp, '["Leg Stretch"]', index=0, text="Stretch", slider=True)
        
        boxCol = boxRow.column()
        boxCol.label(text='Right Leg')
        boxCol.prop(gProp, '["Leg FK"]', index=1, text="Disable", slider=True)
        boxCol.prop(gProp, '["Leg Stretch"]', index=1, text="Stretch", slider=True)
        
        
        if lite == False:
          propRow = layout.row()
          propBox = propRow.box()
          boxRow = propBox.row()
          propBox.label(text="Armor")
          boxRow = propBox.row()
          boxCol = boxRow.column()
          boxCol.prop(gProp,'["Armor Toggle"]', index=0, text="Helmet", toggle=True)
          boxCol.prop(gProp,'["Armor Toggle"]', index=2, text="Leggings", toggle=True)
          boxCol = boxRow.column()
          boxCol.prop(gProp,'["Armor Toggle"]', index=1, text="Chestplate", toggle=True)
          boxCol.prop(gProp,'["Armor Toggle"]', index=3, text="Boots", toggle=True)
        
        propRow = layout.row()
        propBox = propRow.box()
        boxRow = propBox.row()
        boxRow.label(text="Misc Settings")
        
        boxRow = propBox.row()
        boxCol = boxRow.column()
        boxCol.prop(gProp, '["Wireframe Bones"]', toggle=True, text='Wire Boneshapes')
        boxCol.prop(gProp, '["Flip Bone"]', toggle=True, text='Enable Flip Bone')
        
        propBox.separator(type="LINE")
        propBox.label(text='Viewport Optimization')
        propRow = propBox.row()
        propRow.prop(scene.render, 'use_simplify', text="Limit Subdiv", toggle=True)
        propRow.prop(scene.render, 'simplify_subdivision', text="Limit")
        
        
        if lite == False:
          propRow = layout.row()
          propBox = propRow.box()
          boxRow = propBox.row()
          propBox.label(text='Deformations')
          propBox.prop(gProp, '["Female Curves"]')
          
          propBox.separator(type="LINE")
          
          propBox.label(text="Lattices")
          boxRow = propBox.row()
          boxCol = boxRow.column()
          boxCol.prop(gProp,'["Show Lattices"]', index=0, toggle=True, text="Display Body")
          boxCol = boxRow.column()
          boxCol.prop(gProp,'["Show Lattices"]', index=1, toggle=True, text="Display Eyelashes")

class SACRUI_PT_f_props(T.Panel):
    bl_label = "Face Properties"
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
          
        if py_compat != ui_format:
          propRow = layout.row()
          propBox = propRow.box()
          warnRow = propBox.column()
          warnRow.label(text="WARNING", icon="ERROR")
          warnRow.alignment = 'EXPAND'
          warnRow.label(text="SACR Version not Compatible")
        
        
        gProp = rig.pose.bones['Rig_Properties']
        mProp = rig.pose.bones["Mouth_Properties"]
        eProp = rig.pose.bones["Eye_Properties"]
        ebProp = rig.pose.bones["Eyebrow_Properties"]
        
        face_on = gProp['Face Toggle']
        lite = rig.data["lite"]
        
        propRow = layout.row()
        propRow.prop(gProp,'["Face Toggle"]', toggle=True, text="Enable Facerig")
        layout.separator(type="LINE")
        
        propRow = layout.row()
        propBox = propRow.box()
        boxRow = propBox.row()
        if face_on == True:
            boxRow.label(text="Eyebrow Settings", icon="PROPERTIES")
            propBox.separator(type="LINE")
            
            boxRow = propBox.row()
            boxRow.prop(ebProp, '["Depth"]', slider=True)
            
            boxRow = propBox.row()
            rowCol = boxRow.column()
            rowCol.prop(ebProp, '["Thickness"]', slider=True)
            
            rowCol = boxRow.column()
            boxRow.prop(ebProp, '["Width"]', slider=True)
            
            boxRow = propBox.row()
            boxRow.label(text="More Controls")
            boxRow = propBox.row()
            boxRow.prop(ebProp, '["Extended Controls"]', index=0, text="Left")
            boxRow.prop(ebProp, '["Extended Controls"]', index=1, text="Right")
            layout.separator(type="LINE")

            propRow = layout.row()
            propBox = propRow.box()
            boxRow = propBox.row()
            boxRow.label(text="Eye Settings", icon="PROPERTIES")
            propBox.separator(type="LINE")
            
            boxRow = propBox.row()
            boxCol = boxRow.column()
            boxCol.label(text="Iris Inset")
            boxCol.prop(eProp,'["Iris Inset"]', slider=True, text="")
            
            boxCol = boxRow.column()
            boxCol.label(text="Sclera Depth")
            boxCol.prop(eProp,'["Sclera Depth"]', slider=True, text="")
            
            if lite == False:
              boxRow = propBox.row()
              boxRow.prop(eProp, '["Eyelashes"]', text="Eyelash Style")
              boxRow.prop(eProp, '["Eyesparkle"]', text="Eyesparkle", toggle=True)
            
            propBox.separator(type="LINE")
              
            boxRow = propBox.row()
            boxRow.label(text="More Controls")
            boxRow = propBox.row()
            boxRow.prop(eProp, '["Extended Controls"]', index=0, text="Left")
            boxRow.prop(eProp, '["Extended Controls"]', index=1, text="Right")
            
            propRow = layout.row()
            propBox = propRow.box()
            boxRow = propBox.row()
            boxRow.label(text="Mouth Settings", icon="PROPERTIES")
            propBox.separator(type="LINE")
            
            boxRow = propBox.row()
            boxCol = boxRow.column()
            boxCol.label(text="Square Mouth")
            boxCol.prop(mProp, '["Square Mouth"]', slider=True, text="")
            
            boxCol = boxRow.column()
            boxCol.label(text="More Controls")
            boxCol.prop(mProp, '["Extended Controls"]', text="")
            propBox.separator(type="LINE")
            
            boxRow = propBox.row()
            boxRow.label(text="Molar Settings", icon="PROPERTIES")
            
            boxRow = propBox.row()
            boxCol = boxRow.column()
            boxCol.label(text="Left Height")
            
            boxCol.prop(mProp, '["Molar Height (R -> L)"]', index=3, slider=True, text="")
            boxCol.prop(mProp, '["Molar Height (R -> L)"]', index=2, slider=True, text="")
            
            boxCol = boxRow.column()
            boxCol.label(text="Right Height")
            boxCol.prop(mProp, '["Molar Height (R -> L)"]', index=0, slider=True, text="")
            boxCol.prop(mProp, '["Molar Height (R -> L)"]', index=1, slider=True, text="")
            
            boxRow = propBox.row()
            boxCol = boxRow.column()
            boxCol.label(text="Left Width")
            boxCol.prop(mProp, '["Molar Width (R -> L)"]', index=3, slider=True, text="")
            boxCol.prop(mProp, '["Molar Width (R -> L)"]', index=2, slider=True, text="")
            
            boxCol = boxRow.column()
            boxCol.label(text="Right Width")
            boxCol.prop(mProp, '["Molar Width (R -> L)"]', index=0, slider=True, text="")
            boxCol.prop(mProp, '["Molar Width (R -> L)"]', index=1, slider=True, text="")
        else:
            boxRow.label(text="Facerig Disabled", icon="ERROR")


# ==============
# Properties End
# Register Classes
# ==============

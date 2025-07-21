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


bl_info = {
    "name"          : "SACR R8 Control Interface",
    "author"        : "Sakura Sedaia",
    "version"       : (0, 0, 1),
    "blender"       : (4, 5, 0),
    "location"      : "3D View > SACR UI",
    "description"   : "An Addon containing control scripts for SACR R7.2 and newer",
    "warning"       : "This Addon is still heavily in development, please expect issues to be present",
    "doc_url"       : "",
    "tracker_url"   : "",
    'support'       : "COMMUNITY",
    "category"      : "User Interface"
}
import bpy

""" This Script is for use with SACR R8 """
# ==========
# bpy forms
# ==========
C = bpy.context
D = bpy.data
M = bpy.msgbus
O = bpy.ops
T = bpy.types
U = bpy.utils
Pth = bpy.path
A = bpy.app
P = bpy.props


# Change this value, it should match the the id given in the Armature Properties
sacr_id = "SACR.Armature"
sacr_id_prop = "rig_id"

# ==============
# Enumerators Start
# ==============
T.Armature.Rig_Sector = P.EnumProperty(
    items = [
        ('0','Global',''),
        ('1','Head',''),
        ('2','Torso',''),
        ('3','Arms',''),
        ('4','Legs','')
    ],
    default=0
)
T.Armature.Face_Tab = P.EnumProperty(
    items = [
        ('0','Eyebrow',''),
        ('1','Eyes',''),
        ('2','Mouth','')
    ],
    default=0
)
arm_dim_array = [
        ('0', '4x4', 'Thicc Arms, commonly known as Steve Arms'),
        ('1', '4x3', 'Thinner Arms, commonly known as Alex Arms'),
        ('2', '3x3', 'very thin, 3 by 3 square arms'),
    ]
T.Armature.Arm_L_Dimension = P.EnumProperty(
    items = arm_dim_array,
    default=0,
    name="Left Arm"
)
T.Armature.Arm_R_Dimension = P.EnumProperty(
    items = arm_dim_array,
    default=0,
    name="Right Arm"
)

ankle_array = [
        ('0', 'None', ''),
        ('1', 'Angle', ''),
        ('2', 'Bendy', ''),
    ]

T.Armature.Leg_L_Ankle_Style = P.EnumProperty(
    items = ankle_array,
    default = 1,
    name = "Left Ankle Style"
)
T.Armature.Leg_R_Ankle_Style = P.EnumProperty(
    items = ankle_array,
    default = 1,
    name = "Right Ankle Style"
)
T.Armature.E_Style = P.EnumProperty(
    items = [
        ('0','None','No Eyes on Rig'),
        ('1','3D','Uses a Modelled Face Mesh which has the eyes extruded into the mesh itself.'),
        ('2','2D (WIP)','Uses a series of planes layered over each other like a 2D Motion Graphic')
    ],
    default=1,
    name="Eye Style"
)
T.Armature.EB_Style = P.EnumProperty(
    items = [
        ('0','None','No Eyebrows'),
        ('1','Standard','One Eyebrow per eye'),
        ('2','Unibrow',"One solid eyebrow accross the entire face, like a Villager")
    ],
    name="Eyebrow Style"
)
T.Armature.M_Style = P.EnumProperty(
    name = "Mouth Style",
    default=1,
    items = [
         ('0','None','No Mouth on Rig, useful for characters with Helmets, Masks, or Muzzles'),
         ('1','3D','Uses a Modelled Face Mesh which has the Mouth extruded into the mesh itself.'),
         ('2','2D (WIP)','Uses a series of Meshes with a Shrinkwrap Modifier to create the facerig')
    ]
)
# ==============
# Enumerators End
#
# ==============

                    
        
        

# ==============
#
# Version Panel
# ==============

class SACRUI_PT_rig_info(T.Panel):
    bl_label = 'Version Info'
    bl_category = 'SACR UI'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    @classmethod
    def poll(self, context):
      try:
        obj = context.active_object
        if obj and obj.type == 'ARMATURE' and obj.data:
          armature = obj.data
          return armature[sacr_id_prop] == sacr_id
        else:
          return False
      except (AttributeError, KeyError, TypeError):
        return False
    
    def draw(self, context):
        layout = self.layout
        
        
        verBox = layout.box()
        verRow = verBox.column(align=True)
        verRow.label(text="SACR_D8_Alpha_01", icon="ARMATURE_DATA")
        verRow.label(text="Control UI R1 A-01", icon="TEXT")
        verRow.label(text="Released __/__/____")

# ==============
# Version End
# Bone Groups Start
# ==============
class SACRUI_PT_bone_groups(T.Panel):
    # ============== 
    # Class Definition
    # ==============
    bl_label = 'Visibility'
    bl_icon = "OPTIONS"
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
          return armature[sacr_id_prop] == sacr_id
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
        armature = rig.data
        sector = armature.Rig_Sector
        
        gProp = rig.pose.bones['Rig_Properties']
        fProp = rig.pose.bones["Face_Properties"]
        mProp = rig.pose.bones["Mouth_Properties"]
        eProp = rig.pose.bones["Eye_Properties"]
        ebProp = rig.pose.bones["Eyebrow_Properties"]
        
        group_icon = "BONE_DATA"
        # ============== 
        # Panel Variables
        # ==============
        face_toggle = gProp["Toggle_Face"]
        
        
        # ============== 
        # Bone Collections Variables
        # ==============
        layer = armature.collections_all
        rigBox = layout.box()
        rigBox.label(text="Bone Collections", icon="OUTLINER_COLLECTION")
        
        # ============== 
        # Head Groups
        # ==============
        headBox = rigBox.box()
        headRow = headBox.row()
        headCol = headRow.column()
        headCol.label(text="Head")
        headCol.prop(layer["Head"], "is_visible", text="Main", icon=group_icon, toggle=True)
        
        headRow = headBox.row()
        headCol = headRow.column()
        headCol.prop(gProp, '["Toggle_Face"]', toggle=True)
        
        headCol = headRow.column()
        headCol.prop(layer["Face_Controls"], "is_visible", text="Face Controls", icon=group_icon, toggle=True)
        headRow = headBox.row()
        headCol = headRow.column()
        if face_toggle == True:
            faceGroup = headCol.box()
            faceRow = faceGroup.row()
            faceRow.label(text="Face Bone Collections")
            
            faceRow = faceGroup.row()
            # ============== 
            # Left Face Groups
            # ==============
            faceCol = faceRow.column()
            faceCol.label(text="Left Eyebrow")
            faceCol.prop(layer["Eyebrow_Left"], "is_visible", text="Show", icon=group_icon, toggle=True)
            faceCol.label(text="Left Eye")
            faceCol.prop(layer["Eye_Left_Simplified"], "is_visible", text="Show Simple", icon=group_icon, toggle=True)
            faceCol.prop(layer["Eye_Left_Advanced"], "is_visible", text="Show Advanced", icon=group_icon, toggle=True)
            
            # ============== 
            # Right Face Groups
            # ==============
            faceCol = faceRow.column()
            faceCol.label(text="Right Eyebrow")
            faceCol.prop(layer["Eyebrow_Right"], "is_visible", text="Toggle",toggle=True)
            faceCol.label(text="Right Eye")
            faceCol.prop(layer["Eye_Right_Simplified"], "is_visible", text="Show Simple", icon=group_icon, toggle=True)
            faceCol.prop(layer["Eye_Right_Advanced"], "is_visible", text="Show Advanced", icon=group_icon, toggle=True)
        
            faceRow = faceGroup.row()
            faceCol = faceRow.column()
            faceCol.label(text="Mouth")
            faceCol.prop(layer["Mouth_Simple"], "is_visible", text="Show Simple", icon=group_icon, toggle=True)
            faceCol.prop(layer["Mouth_Adv"], "is_visible", text="Show Advanced", icon=group_icon, toggle=True)
            
        # ============== 
        # Torso Groups
        # ==============
        groupBox = rigBox.box()
        groupCol = groupBox.column()
        groupCol.label(text="Body")
        groupCol.prop(layer["Torso"], "is_visible", text="Torso", icon=group_icon, toggle=True)
        
        # ============== 
        # Left Limb Groups
        # ==============
        groupRow = groupCol.row()
        groupCol = groupRow.column()
        groupCol.prop(layer["Arm_Left"],"is_visible",text="Left Arm", icon=group_icon, toggle=True)
        groupCol.prop(layer["Leg_Left"],"is_visible",text="Left Leg", icon=group_icon, toggle=True)
            
        # ============== 
        # Right Limb Groups
        # ==============
        groupCol = groupRow.column()
        groupCol.prop(layer["Arm_Right"],"is_visible",text="Right Arm", icon=group_icon, toggle=True)
        groupCol.prop(layer["Leg_Right"],"is_visible",text="Right Leg", icon=group_icon, toggle=True)
        
        # ============== 
        # Hair Groups
        # ==============
        headCol = rigBox.row()
        hair = headCol.box()
        hairRow = hair.row()
        hairRow.label(text="Hair Groups")
        hairRow.prop(gProp, '["Toggle_Hair_Rig"]', toggle=True, text="Toggle Meshes")

        hairRow = hair.row()
        hairCol = hairRow.column()
        hairCol.label(text="Left Hair")
        hairCol.prop(layer["Left_Hair"],"is_visible", text="Basic", icon=group_icon, toggle=True)
        hairCol.prop(layer["Left_Hair_Adv"],"is_visible", text="Advanced", icon=group_icon, toggle=True)

        hairCol = hairRow.column()
        hairCol.label(text="Right Hair")
        hairCol.prop(layer["Right_Hair"],"is_visible", text="Basic", icon=group_icon, toggle=True)
        hairCol.prop(layer["Right_Hair_Adv"],"is_visible", text="Advanced", icon=group_icon, toggle=True)

        hairRow = hair.row()
        hairCol = hairRow.column()
        hairCol.label(text="Back Hair")
        hairCol.prop(layer["Back_Hair"],"is_visible", text="Basic", icon=group_icon, toggle=True)
        hairCol.prop(layer["Back_Hair_Adv"],"is_visible", text="Advanced", icon=group_icon, toggle=True)
        

# ==============
# Bone Group End
# Properties Start
# ==============

class SACRUI_PT_properties(T.Panel):
    bl_label = "Properties"
    bl_icon = "PROPERTIES"
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
          return armature[sacr_id_prop] == sacr_id
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
        armature = rig.data
        sector = armature.Rig_Sector
        
        scene = context.scene
        renConfig = T.RenderSettings
        
        gProp = rig.pose.bones['Rig_Properties']
        dProp = rig.pose.bones['Deform_Controls']
        fProp = rig.pose.bones["Face_Properties"]
        mProp = rig.pose.bones["Mouth_Properties"]
        eProp = rig.pose.bones["Eye_Properties"]
        ebProp = rig.pose.bones["Eyebrow_Properties"]
        
        layout.label(text="Rig Properties", icon="PROPERTIES")
        
        propRow = layout.row()
        propRow.prop(armature,'Rig_Sector',expand=True)
        layout.separator(type="LINE")
        
        
        # ============== 
        # Global SubPanel
        # ==============
        if sector == '0':
            propRow = layout.row()
            propBox = propRow.box()
            propBox.label(text="Rig Options", icon="MODIFIER_ON")
            propBox.separator(type="LINE")
            propBox.label(text='Rig Settings Settings')
            propBox.prop(gProp,'["Wireframe_Bones"]', toggle=True, text="Wire Bones")
            
            propBox.separator(type="LINE")
            propBox.label(text='Viewport Optimization')
            propRow = propBox.row()
            propRow.prop(scene.render, 'use_simplify', text="Limit Subdiv", toggle=True)
            propRow.prop(scene.render, 'simplify_subdivision', text="Limit")
            
            propBox.separator(type="LINE")
            
            propBox.label(text='Armor')
            
            propRow = propBox.row()
            propCol = propRow.column()
            propCol.prop(gProp, '["Toggle_Armor"]', text="Helmet", index=0, toggle=True)
            propCol.prop(gProp, '["Toggle_Armor"]', text="Body", index=1, toggle=True)
            propCol = propRow.column()
            propCol.prop(gProp, '["Toggle_Armor"]', text="Leggings", index=2, toggle=True)
            propCol.prop(gProp, '["Toggle_Armor"]', text="Boots", index=3, toggle=True)
            
            
            # bpy.data.scenes["SACR R8"].render.use_simplify
            
            
            # Deform Options
            propRow = layout.row()
            propBox = propRow.box()
            propBox.label(text="Deform Options", icon="LATTICE_DATA")
            propBox.separator(type="LINE")
            latRow = propBox.row()
            latRow.prop(dProp, '["Show_Lattices"]', toggle=True)
            
            latRow = propBox.row()
            latBox = latRow.box()
            latBox.prop(dProp, '["Female_Preset"]', slider=True, text="Female")
            
        # ============== 
        # Head SubPanel
        # ==============
        face_toggle = gProp["Toggle_Face"]
        if sector == '1':
            # Head Options
            propRow = layout.row()
            propBox = propRow.box()
            propBox.label(text="Head Options", icon="MODIFIER_ON")
            propBox.separator(type="LINE")
            
            headRow = propBox.row()
            headCol = headRow.column()
            headCol.prop(gProp, '["Toggle_Extrude_Head"]', text="Extrude Heads", toggle=True)
            headCol.prop(gProp, '["Toggle_Face"]', text="Face Rig", toggle=True)
            
            headCol = headRow.column()
            headCol.prop(gProp, '["Toggle_Hair_Rig"]', text="Hair Rig", toggle=True)
            
            if face_toggle == True:
                # Face Options
                propRow = layout.row()
                propBox = propRow.box()
                headRow = propBox.row()
                headRow.label(text="Face Options", icon="MODIFIER_ON")
                headRow = propBox.row()
                headRow.prop(armature, 'Face_Tab', expand=True)
                
                
                faceTab = armature.Face_Tab
                
                # Eyebrow Options
                ebStyle = armature['EB_Style']
                if faceTab == '0':
                    headRow = propBox.row()
                    eyebrowBox = headRow.box()
                    eyebrowBox.label(text="Eyebrow Options", icon="MODIFIER_ON")
                    eyebrowBox.separator(factor=1,type="LINE")

                    eyebrowRow = eyebrowBox.row()
                    eyebrowRow.label(text="Style")
                    eyebrowRow = eyebrowBox.row()
                    eyebrowRow.prop(armature, 'EB_Style', expand=True)
                    eyebrowBox.separator(factor=1,type="LINE")
                    
                    eyebrowRow = eyebrowBox.row()
                    eyebrowCol = eyebrowRow.column()
                    eyebrowCol.label(text="Settings")
                    eyebrowCol.prop(ebProp, '["Offset"]', slider=True)
                    eyebrowCol.prop(ebProp, '["Width"]', slider=True)
                    eyebrowCol.prop(ebProp, '["Thickness"]', slider=True)
                    

                # Eye Options
                eStyle = armature['E_Style']
                if faceTab == '1':
                    headRow = propBox.row()
                    eyeBox = headRow.box()
                    eyeBox.label(text="Eye Options", icon="MODIFIER_ON")
                    eyeBox.separator(factor=1,type="LINE")

                    eyeRow = eyeBox.row()
                    eyeRow.label(text="Style")
                    eyeRow = eyeBox.row()
                    eyeRow.prop(armature, 'E_Style', expand=True)
                    
                    if eStyle != 0:
                        eyeBox.separator(factor=1,type="LINE")
                        eyeRow = eyeBox.row()
                        eyeCol = eyeRow.column()
                        eyeCol.label(text="Settings")
                    
                    # 3D Properties
                    if eStyle == 1:
                        eyeBox = eyeCol.box()
                        
                        eyeRow = eyeBox.row()
                        eyeRow.label(text="3D Settings")
                        eyeBox.separator(factor=1,type="LINE")
                        
                        
                        eyeRow = eyeBox.row()
                        eyeRow.label(text="Geometry", icon="MESH_DATA")
                        
                        eyeRow = eyeBox.row()
                        eyeCol = eyeRow.column()
                        eyeCol.prop(eProp, '["Iris_Inset"]', text="Iris Inset", slider=True)
                        
                        eyeCol = eyeRow.column()
                        eyeCol.prop(eProp, '["Sclera_Depth"]', text="Sclera Depth", slider=True)
                        
                        eyeRow = eyeBox.row()
                        eyeCol = eyeRow.column()
                        eyeCol.prop(eProp, '["Sparkle"]', toggle=True)
                        
                        
                        
                        eyeBox.separator(factor=1,type="LINE")
                        
                        eyeRow = eyeBox.row()
                        eyeRow.label(text="Eyelashes")
                        
                        eyeRow = eyeBox.row()
                        eyeCol = eyeRow.column()
                        eyeCol.prop(eProp, '["L_Eyelash"]', text="Left")
                        
                        eyeCol = eyeRow.column()
                        eyeCol.prop(eProp, '["R_Eyelash"]', text="Right")

                    # 2D Properties
                    if eStyle == 2:
                        eyeBox = eyeCol.box()
                        eyeBox.label(text="2D Option coming soon")
                        # eyeBox.separator(factor=1,type="LINE")

                # Eye Options
                mStyle = armature['M_Style']
                if faceTab == '2':
                    headRow = propBox.row()
                    mouthBox = headRow.box()
                    mouthBox.label(text="Mouth Options", icon="MODIFIER_ON")
                    mouthBox.separator(factor=1,type="LINE")

                    mouthRow = mouthBox.row()
                    mouthRow.label(text="Style")
                    mouthRow = mouthBox.row()
                    mouthRow.prop(armature, 'M_Style', expand=True)
                    
                    if mStyle != 0:
                        mouthBox.separator(factor=1,type="LINE")
                        mouthRow = mouthBox.row()
                        mouthCol = mouthRow.column()
                        mouthCol.label(text="Settings")
                    
                    # 3D Properties
                    if mStyle == 1:
                        mouthBox = mouthCol.box()
                        mouthRow = mouthBox.row()
                        mouthRow.label(text="3D Settings")
                        mouthBox.separator(factor=1,type="LINE")
                        
                        mouthRow = mouthBox.row()
                        mouthRow.label(text="Mouth Geometry", icon="MESH_DATA")
                        
                        mouthRow = mouthBox.row()
                        mouthRow.prop(mProp, '["Square_Mouth"]', slider=True, text="Square Ends")
                        
                        mouthRow = mouthBox.row()
                        mouthRow.label(text="Lip Bevel")
                        
                        mouthRow = mouthBox.row()
                        mouthRow.prop(mProp, '["Bevel_Dist"]', slider=True, text="Width")
                        mouthRow.prop(mProp, '["Bevel_Segment"]', slider=True, text="Segment")
                        mouthBox.separator(factor=1,type="LINE")
                        
                        mouthRow = mouthBox.row()
                        mouthRow.prop(mProp,'["Molar_Toggle"]', toggle=True, text="Enable Molars")
                        mouthRow = mouthBox.row()
                        
                        mo_toggle = mProp['Molar_Toggle']
                        if mo_toggle == True:
                            molarBox = mouthRow.box()
                            molarRow = molarBox.row()
                            molarRow.label(text="Molar Settings", icon="MODIFIER_ON")
                            
                            molarRow = molarBox.row()
                            molarCol = molarRow.column()
                            molarCol.label(text="Left")
                            
                            molarCol = molarRow.column()
                            molarCol.label(text="Right")
                            
                            
                            molarBox.separator(factor=1,type="LINE")
                            molarBox.label(text="Height")
                            molarRow = molarBox.row()
                            molarCol = molarRow.column()
                            molarCol.prop(mProp, '["Molar_Left_Height"]', text="")
                            
                            molarCol = molarRow.column()
                            molarCol.prop(mProp, '["Molar_Right_Height"]', text="")
                            
                            molarBox.separator(factor=1,type="LINE")
                            molarBox.label(text="Width")
                            molarRow = molarBox.row()
                            molarCol = molarRow.column()
                            molarCol.prop(mProp, '["Molar_Left_Width"]', text="")

                            molarCol = molarRow.column()
                            molarCol.prop(mProp, '["Molar_Right_Width"]', text="")
                            
                            
                    # 2D Properties
                    if mStyle == 2:
                        mouthBox = mouthCol.box()
                        mouthBox.label(text="2D Option coming soon")
                        # mouthBox.separator(factor=1,type="LINE")
            
        # ============== 
        # Torso SubPanel
        # ==============
        if sector == '2':
            propRow = layout.row()
            propBox = propRow.box()
            torsoRow = propBox.row()
            torsoRow.label(text="Torso Options", icon="MODIFIER_ON")
            propBox.separator(factor=1,type="LINE")
            
            
        # ============== 
        # Arms SubPanel
        # ==============
        split_arm_opt = armature["Split_Arm_Opt"]
        if sector == '3':
            propRow = layout.row()
            propBox = propRow.box()
            armRow = propBox.row()
            armRow.label(text="Arm Options", icon="MODIFIER_ON")
            propBox.separator(factor=1,type="LINE")
            
            armRow = propBox.row()
            armRow.prop(armature, '["Split_Arm_Opt"]', toggle=True, text="Split Arm Dimensions")
            
            if split_arm_opt == False:
                armRow = propBox.row()
                armCol = armRow.column()
                armCol.label(text="Both Arms")
                armCol.prop(armature,'Arm_L_Dimension', expand=False, text="")
                armCol.prop(gProp,'["Arm_Fingers"]', toggle=True, index=0, text="Fingers")
                armCol.separator(factor=1,type="LINE")
            
            armRow = propBox.row()
            armCol = armRow.column()
            if split_arm_opt == True:
                armCol.label(text="Left")
                armCol.prop(armature,'Arm_L_Dimension', expand=False, text="")
                armCol.prop(gProp,'["Arm_Fingers"]', toggle=True, index=0, text="Fingers")
                armCol.separator(factor=1,type="LINE")
                armCol.separator(factor=1,type="SPACE")
                armCol.label(text="IK")
                
            if split_arm_opt == False:
                armCol.label(text="Left IK")
                
            armCol.prop(gProp,'["Arm_IK"]', text="Enable", slider=True, index=0)
            armCol.prop(gProp,'["Arm_Stretch"]', text="Stretch", slider=True, index=0)
            armCol.prop(gProp,'["Arm_Wrist_IK"]', text="Wrist", slider=True, index=0)
            
            armCol = armRow.column()
            if split_arm_opt == True:
                armCol.label(text="Right")
                armCol.prop(armature,'Arm_R_Dimension', expand=False, text="")
                armCol.prop(gProp,'["Arm_Fingers"]', toggle=True, index=1, text="Fingers")
                armCol.separator(factor=1,type="LINE")
                armCol.separator(factor=1,type="SPACE")
                armCol.label(text="IK")
            if split_arm_opt == False:
                armCol.label(text="Right IK")
                
            armCol.prop(gProp,'["Arm_IK"]', text="Enable", slider=True, index=1)
            armCol.prop(gProp,'["Arm_Stretch"]', text="Stretch", slider=True, index=1)
            armCol.prop(gProp,'["Arm_Wrist_IK"]', text="Wrist", slider=True, index=1)
            
        # ============== 
        # Legs SubPanel
        # ==============
        if sector == '4':
            propRow = layout.row()
            propBox = propRow.box()
            legRow = propBox.row()
            legRow.label(text="Leg Options", icon="MODIFIER_ON")            
            propBox.separator(factor=1,type="LINE")
            
            legRow = propBox.row()
            legCol = legRow.column()
            legCol.label(text="Left")
            legCol.prop(armature, 'Leg_L_Ankle_Style', text="", index=0)
            legCol.label(text="IK")
            legCol.prop(gProp,'["Leg_IK"]', text="Enable", slider=True, index=0)
            legCol.prop(gProp,'["Leg_Stretch"]', text="Stretch", slider=True, index=0)
            
            
            legCol = legRow.column()
            legCol.label(text="Right")
            legCol.prop(armature, 'Leg_R_Ankle_Style', text="", index=1)
            legCol.label(text="IK")
            legCol.prop(gProp,'["Leg_IK"]', text="Enable", slider=True, index=1)
            legCol.prop(gProp,'["Leg_Stretch"]', text="Stretch", slider=True, index=1)
            
            
# ==============
# Properties End
# Register Classes
# ==============

classes = [
    SACRUI_PT_rig_info,
    SACRUI_PT_bone_groups,
    SACRUI_PT_properties
]

def register(): 
    for cls in classes:
        bpy.utils.register_class(cls)
    
    
    
def unregister(): 
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
        
    
if __name__ == '__main__':
    register()
    
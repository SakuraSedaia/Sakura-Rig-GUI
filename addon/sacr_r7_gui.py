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
from bpy.types import Panel

rig = "SACR"
rig_ver = 7
rig_name = rig + " R" + str(rig_ver)
category = rig_name
# ==========
# bpy forms & other Variables
# ==========
D = bpy.data
C = bpy.context
T = bpy.types
P = bpy.props
addon_id = "sacr_r7_ui"

py_ver = 0  # Matched to the variable on an SACR Armature, used for ensuring proper compatability
id_prop = "sacr_id"
py_ver_prop = "script_format"

# Fully Compatible:
# - 7.2.1
id_str = ["SACR.Armature", "sacr_1"]
#
# Partially Compatible
# - 7.2.0
#   - Molars and Eyesparkle do not controllable via script


# region Main Panel
class SEDAIA_PT_uiGlobal(Panel):
    bl_idname = "SEDAIA_PT_uiGlobal"
    bl_label = category
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = rig_name
    bl_order = 0

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            if obj and obj.type == "ARMATURE" and obj.data:
                armature = obj.data
                return armature[id_prop] == id_str[0] or id_str[1]
            else:
                return False
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        # Variables and Data
        scene = context.scene
        obj = context.active_object
        armature = obj.data
        bone = obj.pose.bones

        main = bone["Rig_Properties"]
        face = bone["Face_Properties"]
        mouth = bone["Mouth_Properties"]
        eyes = bone["Eye_Properties"]
        eyebrows = bone["Eyebrow_Properties"]
        layers = armature.collections_all

        face_on = main["Face Toggle"]
        lite = armature["lite"]

        try:
            py_compat = armature[py_ver_prop]
        except (AttributeError, TypeError, KeyError):
            py_compat = -1

        # Define UI
        layout = self.layout

        if py_compat != py_ver:
            layout.alert = True
            errorBox = layout.row().box().column()
            errorBox.label(text="WARNING", icon="ERROR")
            errorBox.separator(type="LINE")
            errorBox.label(text="This version of SACR is")
            errorBox.label(text="not supported by this UI")
            errorBox.separator()
            errorBox.label(text="Some Features may be Missing")
            errorBox.label(text="Or Inoperable")
            layout.alert = False

        row = layout.row()
        row.label(icon="PROPERTIES")
        row.prop(layers["Properties"], "is_visible", text="Bone Props", toggle=True)

        layout.separator(type="LINE")

        row = layout.row()
        col = layout.column_flow(columns=2, align=True)
        col.prop(
            main,
            '["Wireframe Bones"]',
            toggle=True,
            invert_checkbox=True,
            text="Solid Bones",
        )
        col.prop(layers["Flip"], "is_visible", toggle=True, text="Flip Bone")
        col.prop(main, '["Face Toggle"]', toggle=True, text="Face Rig")
        if lite == False:
            col.prop(main, '["Long Hair Rig"]', text="Long Hair Rig")

        layout.separator(type="LINE")

        row = layout.row(align=True)
        row.prop(main, '["Show Lattices"]', index=0, toggle=True, text="Body Lattices")
        row.prop(main, '["Female Curves"]', slider=True, text="Female Deform")


# endregion
# region Bone Collections


class SEDAIA_PT_uiBoneGroups(Panel):
    bl_parent_id = "SEDAIA_PT_uiGlobal"
    bl_label = "Bone Collections"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = rig_name
    bl_order = 0

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            if obj and obj.type == "ARMATURE" and obj.data:
                armature = obj.data
                return armature[id_prop] == id_str[0] or id_str[1]
            else:
                return False
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        # Variables and Data
        scene = context.scene
        obj = context.active_object
        armature = obj.data
        bone = obj.pose.bones

        main = bone["Rig_Properties"]
        face = bone["Face_Properties"]
        mouth = bone["Mouth_Properties"]
        eyes = bone["Eye_Properties"]
        eyebrows = bone["Eyebrow_Properties"]
        layers = armature.collections_all

        face_on = main["Face Toggle"]
        lite = armature["lite"]

        try:
            py_compat = armature[py_ver_prop]
        except (AttributeError, TypeError, KeyError):
            py_compat = -1

        # Define UI
        layout = self.layout
        row = layout.row()
        row.template_bone_collection_tree()


# endregion
# region Arms
class SEDAIA_PT_uiArms(Panel):
    bl_parent_id = "SEDAIA_PT_uiGlobal"
    bl_label = "Arm Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = rig_name
    bl_order = 1

    def draw(self, context):
        # Variables and Data
        obj = context.active_object
        armature = obj.data
        bone = obj.pose.bones

        main = bone["Rig_Properties"]
        face = bone["Face_Properties"]
        mouth = bone["Mouth_Properties"]
        eyes = bone["Eye_Properties"]
        eyebrows = bone["Eyebrow_Properties"]
        layers = armature.collections_all

        face_on = main["Face Toggle"]
        lite = armature["lite"]

        # UI
        layout = self.layout
        row = layout.row()
        row.label(text="Properties", icon="PROPERTIES")

        row = layout.row()
        row.prop(main, '["Slim Arms"]', text="Slim Arms")

        layout.separator(type="LINE")

        row = layout.row()
        row.label(text="IK Settings")

        row = layout.row(align=True)
        arm = 0
        col = row.column(heading="Left")
        col.prop(main, '["Arm IK"]', index=arm, text="IK", slider=True)
        col.prop(main, '["Arm Stretch"]', index=arm, text="Stretch", slider=True)
        col.prop(main, '["Arm Wrist IK"]', index=arm, text="Wrist IK", slider=True)

        arm = 1
        col = row.column(heading="Right")
        col.prop(main, '["Arm IK"]', index=arm, text="IK", slider=True)
        col.prop(main, '["Arm Stretch"]', index=arm, text="Stretch", slider=True)
        col.prop(main, '["Arm Wrist IK"]', index=arm, text="Wrist IK", slider=True)


# endregion
# region Legs
class SEDAIA_PT_uiLegs(Panel):
    bl_parent_id = "SEDAIA_PT_uiGlobal"
    bl_label = "Leg Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = rig_name
    bl_order = 2

    def draw(self, context):
        # Variables and Data
        obj = context.active_object
        armature = obj.data
        bone = obj.pose.bones

        main = bone["Rig_Properties"]
        face = bone["Face_Properties"]
        mouth = bone["Mouth_Properties"]
        eyes = bone["Eye_Properties"]
        eyebrows = bone["Eyebrow_Properties"]
        layers = armature.collections_all

        face_on = main["Face Toggle"]
        lite = armature["lite"]

        # UI
        layout = self.layout
        row = layout.row(align=True)
        leg = 0
        col = row.column(heading="Left")
        col.prop(main, '["Leg FK"]', index=leg, text="FK", slider=True)
        col.prop(main, '["Leg Stretch"]', index=leg, text="Stretch", slider=True)

        leg = 1
        col = row.column(heading="Right")
        col.prop(main, '["Leg FK"]', index=leg, text="FK", slider=True)
        col.prop(main, '["Leg Stretch"]', index=leg, text="Stretch", slider=True)


# endregion
# region Face
class SEDAIA_PT_uiFace(T.Panel):
    bl_label = "SACR Facerig"
    bl_category = rig_name
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "SEDAIA_PT_uiFace"
    bl_order = 1

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            bone = obj.pose.bones

            main = bone["Rig_Properties"]
            face_on = main["Face Toggle"]
            if face_on == True:
                if obj and obj.type == "ARMATURE" and obj.data:
                    armature = obj.data
                    return armature[id_prop] == id_str[0] or id_str[1]
                else:
                    return False
            else:
                return False
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        # Variables and Data
        obj = context.active_object
        armature = obj.data
        bone = obj.pose.bones

        main = bone["Rig_Properties"]
        face = bone["Face_Properties"]

        # UI
        layout = self.layout

        row = layout.row()
        row.prop(face, '["Face | UV"]', toggle=True, text="UV projection")
        row.prop(main, '["Show Lattices"]', index=1, toggle=True, text="Eyelash Lattice")
# endregion
# region Eyebrows
class SEDAIA_PT_uiEyebrows(T.Panel):
    bl_label = "Eyebrows Settings"
    bl_category = rig_name
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "SEDAIA_PT_uiFace"
    bl_order = 0

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            face_on = obj.pose.bones["Rig_Properties"]["Face Toggle"]
            return face_on
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        # Variables and Data
        obj = context.active_object
        armature = obj.data
        bone = obj.pose.bones

        main = bone["Rig_Properties"]
        eyebrows = bone["Eyebrow_Properties"]

        face_on = main["Face Toggle"]
        lite = armature["lite"]

        # UI
        layout = self.layout

        row = layout.row()
        box = row.box()
        col = box.column(align=True)
        row = col.row(align=True)
        row.prop(eyebrows, '["Depth"]', slider=True)
        row.prop(eyebrows, '["Width"]', slider=True)

        row = col.row()
        row.prop(eyebrows, '["Thickness"]', slider=True)

        box.separator(type="LINE")

        box.label(text="More Controls")
        row = box.row(align=True)
        row.prop(eyebrows, '["Extended Controls"]', index=0, text="Left", slider=True)
        row.prop(eyebrows, '["Extended Controls"]', index=1, text="Right", slider=True)
# endregion
# region Eyes
class SEDAIA_PT_uiEyes(T.Panel):
    bl_label = "Eyes Settings"
    bl_category = rig_name
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "SEDAIA_PT_uiFace"
    bl_order = 1

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            face_on = obj.pose.bones["Rig_Properties"]["Face Toggle"]
            return face_on
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        # Variables and Data
        obj = context.active_object
        armature = obj.data
        bone = obj.pose.bones

        main = bone["Rig_Properties"]
        face = bone["Face_Properties"]
        mouth = bone["Mouth_Properties"]
        eyes = bone["Eye_Properties"]
        eyebrows = bone["Eyebrow_Properties"]
        layers = armature.collections_all

        face_on = main["Face Toggle"]
        lite = armature["lite"]

        try:
            if eyes["Eyesparkle"] == 0 or 1:
                sparkle = True
        except (AttributeError, TypeError, KeyError):
            sparkle = False

        # UI
        layout = self.layout
        row = layout.row()
        box = row.box()
        col = box.column(align=True)
        row = col.row(align=True)
        row.prop(eyes, '["Iris Inset"]', slider=True)
        row.prop(eyes, '["Sclera Depth"]', slider=True)

        row = col.row(align=True)
        row.prop(eyes, '["Eyelashes"]', text="Lash Style")
        if sparkle == True:
            row.prop(eyes, '["Eyesparkle"]', toggle=True)

        box.separator(type="LINE")

        box.label(text="More Controls")
        row = box.row(align=True)
        row.prop(eyes, '["Extended Controls"]', index=0, text="Left", slider=True)
        row.prop(eyes, '["Extended Controls"]', index=1, text="Right", slider=True)


# endregion
# region Mouth
class SEDAIA_PT_uiMouth(T.Panel):
    bl_label = "Mouth Settings"
    bl_category = rig_name
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "SEDAIA_PT_uiFace"
    bl_order = 2

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            face_on = obj.pose.bones["Rig_Properties"]["Face Toggle"]
            return face_on
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        # Variables and Data
        obj = context.active_object
        armature = obj.data
        bone = obj.pose.bones

        main = bone["Rig_Properties"]
        face = bone["Face_Properties"]
        mouth = bone["Mouth_Properties"]
        eyes = bone["Eye_Properties"]
        eyebrows = bone["Eyebrow_Properties"]
        layers = armature.collections_all

        face_on = main["Face Toggle"]
        lite = armature["lite"]

        # UI
        layout = self.layout
        row = layout.row()
        box = row.box()
        row = box.row()
        col = row.column()
        col.label(text="Square Mouth")
        col.prop(mouth, '["Square Mouth"]', slider=True, text="")

        col = row.column()
        col.label(text="More Controls")
        col.prop(mouth, '["Extended Controls"]', text="")
        box.separator(type="LINE")

        row = box.row()
        row.label(text="Molar Settings", icon="PROPERTIES")

        row = box.row()
        col = row.column()
        col.label(text="Left Height")

        col.prop(mouth, '["Molar Height (R -> L)"]', index=3, slider=True, text="")
        col.prop(mouth, '["Molar Height (R -> L)"]', index=2, slider=True, text="")

        col = row.column()
        col.label(text="Right Height")
        col.prop(mouth, '["Molar Height (R -> L)"]', index=0, slider=True, text="")
        col.prop(mouth, '["Molar Height (R -> L)"]', index=1, slider=True, text="")

        row = box.row()
        col = row.column()
        col.label(text="Left Width")
        col.prop(mouth, '["Molar Width (R -> L)"]', index=3, slider=True, text="")
        col.prop(mouth, '["Molar Width (R -> L)"]', index=2, slider=True, text="")

        col = row.column()
        col.label(text="Right Width")
        col.prop(mouth, '["Molar Width (R -> L)"]', index=0, slider=True, text="")
        col.prop(mouth, '["Molar Width (R -> L)"]', index=1, slider=True, text="")
# endregion

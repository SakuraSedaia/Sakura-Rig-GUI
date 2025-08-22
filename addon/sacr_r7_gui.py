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
    "name": "SACR R7 GUI",
    "author": "Sakura Sedaia",
    "version": (1, 1, 0),
    "blender": (4, 5, 0),
    "location": "3D View > SACR UI",
    "description": "An Addon containing control scripts for SACR R7",
    "warning": "This Addon is still heavily in development, please expect issues to be present",
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "User Interface",
}

import bpy
from bpy.types import Panel

rig = "SACR"
rig_ver = 7
category = f"{rig} GUI"
id_prop = "sacr_id"
id_str = [
    "SACR.Rev_7",  # SACR R7.3 and Newer
    "sacr_1",  # SACR R7.2.1 and older
]
D = bpy.data
C = bpy.context
T = bpy.types
P = bpy.props


# region Main Panel
class SEDAIA_PT_sacr_7_uiGlobal(Panel):
    bl_idname = "SEDAIA_PT_sacr_7_uiGlobal"
    bl_label = "SACR Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
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
        obj = context.active_object
        armature = obj.data
        bone = obj.pose.bones

        main = bone["Rig_Properties"]
        layers = armature.collections_all

        try:
            lite = armature["lite"]
        except (AttributeError, TypeError, KeyError):
            lite = False

        # Define UI
        layout = self.layout

        row = layout.row()
        row.label(icon="PROPERTIES")
        row.prop(layers["Properties"], "is_visible", text="Bone Props", toggle=True)

        layout.separator(type="LINE")

        row = layout.row(align=True)
        row.label(text="Rig Settings")
        row = layout.row()
        col = layout.column_flow(columns=2, align=True)
        col.prop(main, '["Wireframe Bones"]', toggle=True, invert_checkbox=True, text="Solid Bones")
        col.prop(layers["Flip"], "is_visible", toggle=True, text="Flip Bone")
        try:
            col.prop(
                layers["Quick Parents"],
                "is_visible",
                toggle=True,
                text="Easy Parenting",
            )
            col.prop(main, '["Face Toggle"]', toggle=True, text="Face Rig")
        except (AttributeError, KeyError, TypeError):
            col.prop(main, '["Face Toggle"]', toggle=True, text="Face Rig")

        col.prop(obj.pose, "use_mirror_x", toggle=True)

        if lite == False:
            col.prop(main, '["Long Hair Rig"]', text="Long Hair")

            layout.separator(type="LINE")
            row = layout.row()
            col = row.column()
            col.label(text="Lattice Deforms")
            col.prop(
                main, '["Show Lattices"]', index=0, toggle=True, text="Show Lattices"
            )

            row = layout.row()
            col = row.column(heading="Presets", align=True)
            col.prop(main, '["Female Curves"]', slider=True, text="Female Deform")

            layout.separator(type="LINE")

            row = layout.row()
            col = row.column(align=True, heading="Armor Toggles")
            col.prop(main, '["Armor Toggle"]', index=0, toggle=True, text="Helmet")
            col.prop(main, '["Armor Toggle"]', index=1, toggle=True, text="Chestplate")
            col.prop(main, '["Armor Toggle"]', index=2, toggle=True, text="Leggings")
            col.prop(main, '["Armor Toggle"]', index=3, toggle=True, text="Boots")


# endregion
# region Bone Collections


class SEDAIA_PT_sacr_7_suiBoneGroups(Panel):
    bl_parent_id = "SEDAIA_PT_sacr_7_uiGlobal"
    bl_label = "Bone Collections"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
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
        # Define UI
        layout = self.layout
        row = layout.row()
        row.template_bone_collection_tree()


# endregion
# region Arms
class SEDAIA_PT_sacr_7_suiArms(Panel):
    bl_parent_id = "SEDAIA_PT_sacr_7_uiGlobal"
    bl_label = "Arm Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_order = 1

    def draw(self, context):
        # Variables and Data
        obj = context.active_object
        bone = obj.pose.bones
        main = bone["Rig_Properties"]

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
class SEDAIA_PT_sacr_7_suiLegs(Panel):
    bl_parent_id = "SEDAIA_PT_sacr_7_uiGlobal"
    bl_label = "Leg Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_order = 2

    def draw(self, context):
        # Variables and Data
        obj = context.active_object
        bone = obj.pose.bones
        main = bone["Rig_Properties"]

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
class SEDAIA_PT_sacr_7_uiFace(T.Panel):
    bl_label = "SACR Facerig"
    bl_category = category
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "SEDAIA_PT_sacr_7_uiFace"
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
                    return obj.data[id_prop] == id_str[0] or id_str[1]
                else:
                    return False
            else:
                return False
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        # Variables and Data
        obj = context.active_object
        bone = obj.pose.bones

        main = bone["Rig_Properties"]
        face = bone["Face_Properties"]

        # UI
        layout = self.layout

        row = layout.row()
        row.prop(face, '["Face | UV"]', toggle=True, text="UV projection")
        row.prop(
            main, '["Show Lattices"]', index=1, toggle=True, text="Eyelash Lattice"
        )


# endregion
# region Eyebrows
class SEDAIA_PT_sacr_7_suiEyebrows(T.Panel):
    bl_label = "Eyebrows Settings"
    bl_category = category
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "SEDAIA_PT_sacr_7_uiFace"
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
        bone = obj.pose.bones

        eyebrows = bone["Eyebrow_Properties"]

        # UI
        layout = self.layout

        row = layout.row()
        col = row.column(align=True)
        col.prop(eyebrows, '["Depth"]', slider=True)
        col.prop(eyebrows, '["Width"]', slider=True)
        col.prop(eyebrows, '["Thickness"]', slider=True)

        layout.separator(type="LINE")

        row = layout.row()
        row.label(text="More Controls")
        row = layout.row(align=True)
        row.prop(eyebrows, '["Extended Controls"]', index=0, text="Left", slider=False)
        row.prop(eyebrows, '["Extended Controls"]', index=1, text="Right", slider=False)


# endregion
# region Eyes
class SEDAIA_PT_sacr_7_suiEyes(T.Panel):
    bl_label = "Eyes Settings"
    bl_category = category
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "SEDAIA_PT_sacr_7_uiFace"
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

        eyes = bone["Eye_Properties"]

        try:
            lite = armature["lite"]
        except (AttributeError, TypeError, KeyError):
            lite = False

        try:
            if eyes["Eyesparkle"] == 0 or 1:
                sparkle = True
        except (AttributeError, TypeError, KeyError):
            sparkle = False

        # UI
        layout = self.layout
        row = layout.row()
        col = row.column(align=True)
        col.prop(eyes, '["Iris Inset"]', slider=True)
        col.prop(eyes, '["Sclera Depth"]', slider=True)

        if lite == False:
            col.prop(eyes, '["Eyelashes"]', text="Lash Style")
            if sparkle == True:
                col.prop(eyes, '["Eyesparkle"]', toggle=True)

        layout.separator(type="LINE")

        row = layout.row()
        row.label(text="More Controls")
        row = layout.row(align=True)
        row.prop(eyes, '["Extended Controls"]', index=0, text="Left", slider=False)
        row.prop(eyes, '["Extended Controls"]', index=1, text="Right", slider=False)


# endregion
# region Mouth
class SEDAIA_PT_sacr_7_suiMouth(T.Panel):
    bl_label = "Mouth Settings"
    bl_category = category
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "SEDAIA_PT_sacr_7_uiFace"
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
        bone = obj.pose.bones
        mouth = bone["Mouth_Properties"]

        # UI
        layout = self.layout
        row = layout.row()
        col = row.column()
        col.prop(mouth, '["Square Mouth"]', slider=True, text="Square")
        col.prop(mouth, '["Extended Controls"]', text="Extra Controls")
        classic_molar = False
        try:
            mouth["Molar Height (R -> L)"]
        except (AttributeError, KeyError, TypeError):
            classic_molar = True

        if classic_molar is True:
            col.prop(
                mouth, '["Fangs Controller"]', toggle=True, text="Molar/Fang Controls"
            )

        else:
            col.separator()
            row = col.row()
            row.label(text="Molar Settings", icon="PROPERTIES")
            row = col.row()
            col = row.column(align=True)
            col.label(text="Left Height")

            top = "T"
            bottom = "B"

            col.prop(mouth, '["Molar Height (R -> L)"]', index=3, slider=True, text=top)
            col.prop(
                mouth, '["Molar Height (R -> L)"]', index=2, slider=True, text=bottom
            )

            col = row.column(align=True)
            col.label(text="Right Height")
            col.prop(mouth, '["Molar Height (R -> L)"]', index=0, slider=True, text=top)
            col.prop(
                mouth, '["Molar Height (R -> L)"]', index=1, slider=True, text=bottom
            )

            row = layout.row()
            col = row.column(align=True)
            col.label(text="Left Width")
            col.prop(mouth, '["Molar Width (R -> L)"]', index=3, slider=True, text=top)
            col.prop(
                mouth, '["Molar Width (R -> L)"]', index=2, slider=True, text=bottom
            )

            col = row.column(align=True)
            col.label(text="Right Width")
            col.prop(mouth, '["Molar Width (R -> L)"]', index=0, slider=True, text=top)
            col.prop(
                mouth, '["Molar Width (R -> L)"]', index=1, slider=True, text=bottom
            )


# endregion

# Un-comment below for if this script is installed on the rig level
# =========
# classes = [
#     SEDAIA_PT_sacr_7_uiGlobal,
#     SEDAIA_PT_sacr_7_uiFace,
#     SEDAIA_PT_sacr_7_suiArms,
#     SEDAIA_PT_sacr_7_suiLegs,
#     SEDAIA_PT_sacr_7_suiEyebrows,
#     SEDAIA_PT_sacr_7_suiEyes,
#     SEDAIA_PT_sacr_7_suiMouth
# ]
#
# def register():
#     for cls in classes:
#         bpy.utils.register_class(cls)
#
# def unregister():
#     for cls in classes:
#         bpy.utils.unregister_class(cls)
#
# if __name__ == '__main__':
#     register()

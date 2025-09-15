import bpy
from mathutils import *
from bpy.types import Panel, Operator

D = bpy.data
C = bpy.context
T = bpy.types
P = bpy.props

rig = "SAR"
rig_ver = 1
rig_name = f"{rig} R{rig_ver}"
rig_id_prop = "rig_id"
rig_id = "SAR.Armature"
cat_id = f"{rig} GUI"


# region Main Panel
class SEDAIA_PT_sar_1_uiGlobal(Panel):
    bl_idname = "SEDAIA_PT_sar_1_uiGlobal"
    bl_label = "SACR Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = cat_id
    bl_order = 0

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            if obj and obj.type == "ARMATURE" and obj.data:
                return obj.data[rig_id_prop] == rig_id_prop
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


class SEDAIA_PT_sar_1_suiBoneGroups(Panel):
    bl_parent_id = "SEDAIA_PT_sar_1_uiGlobal"
    bl_label = "Bone Collections"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = cat_id
    bl_order = 0

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            if obj and obj.type == "ARMATURE" and obj.data:
                return obj.data[rig_id_prop] == rig_id_prop
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
class SEDAIA_PT_sar_1_suiArms(Panel):
    bl_parent_id = "SEDAIA_PT_sar_1_uiGlobal"
    bl_label = "Arm Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = cat_id
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
class SEDAIA_PT_sar_1_suiLegs(Panel):
    bl_parent_id = "SEDAIA_PT_sar_1_uiGlobal"
    bl_label = "Leg Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = cat_id
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
class SEDAIA_PT_sar_1_uiFace(T.Panel):
    bl_label = "SACR Facerig"
    bl_category = cat_id
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "SEDAIA_PT_sar_1_uiFace"
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
                    return obj.data[rig_id_prop] == rig_id_prop
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
class SEDAIA_PT_sar_1_suiEyebrows(T.Panel):
    bl_label = "Eyebrows Settings"
    bl_category = cat_id
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "SEDAIA_PT_sar_1_uiFace"
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
class SEDAIA_PT_sar_1_suiEyes(T.Panel):
    bl_label = "Eyes Settings"
    bl_category = cat_id
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "SEDAIA_PT_sar_1_uiFace"
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
class SEDAIA_PT_sar_1_suiMouth(T.Panel):
    bl_label = "Mouth Settings"
    bl_category = cat_id
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "SEDAIA_PT_sar_1_uiFace"
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
        # bone_ref = bone["Bone Name"] # To be used when needing a bone referenced

        # UI
        layout = self.layout
        layout.row().label(text="Temp Text")


# endregion

# Un-comment below for if this script is installed on the rig level
# =========
# classes = [
#     SEDAIA_PT_sar_1_uiGlobal,
#     SEDAIA_PT_sar_1_uiFace,
#     SEDAIA_PT_sar_1_suiArms,
#     SEDAIA_PT_sar_1_suiLegs,
#     SEDAIA_PT_sar_1_suiEyebrows,
#     SEDAIA_PT_sar_1_suiEyes,
#     SEDAIA_PT_sar_1_suiMouth
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

# region Script Configuration
# Uncomment  when distributed inside the Addon
from .sedaia_operators import is_packed
import bpy
from bpy.types import Operator, Panel

bl_info = {
    "name": "SACR R8 GUI",
    "author": "Sakura Sedaia",
    "version": (0, 3, 0),
    "blender": (4, 5, 0),
    "location": "3D View > SACR UI",
    "description": "An Addon containing control scripts for SACR R8.0",
    "warning": "This Addon is still heavily in development, please expect issues to be present",
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "User Interface",
}
# Scene Scale is 1.7065 for editing the rig
T = bpy.types
P = bpy.props
O = bpy.ops
C = bpy.context
D = bpy.data

# Global Rig Variables
rig = "SACR"
rig_ver = 8
ui_ver = 1
category = f"{rig} R{rig_ver}"
# Default Rig ID: SACR.Rev_8.UI_1

# Here are a list of properties which will be compared
# to the rig. Should a value not align with the selected
# object,  The UI will not show up.
rig_id = f"{rig}.Rev_{rig_ver}.UI_{ui_ver}"
rig_id_prop = "rigID"

mat_obj_name = "Material_Properties"
prop_bones = [
    "Properties.RigMain",  # 0
    "Properties.Head",    # 1
    "Properties.Torso",   # 2
    "Properties.Arms",    # 3
    "Properties.Legs"     # 4
]
T.PoseBone.ArmType = P.EnumProperty(
    name="Arm Type",
    description="Select your Arm Dimension",
    default="0",
    items=[
        ("0", "Standard", "Standard Arm Style, formerly called Steve Arms"),
        ("1", "Slim", "Slim Arm Style, formerly called Steve Arms"),
        ("2", "Super-Slim",
         "Super Slim Arm style are a 3x3 version not available in Minecraft")
    ]
)
T.PoseBone.AnkleType = P.EnumProperty(
    name="Ankle Type",
    description="Ankle Type for the Left Leg",
    items=[
        ("0", "Sharp", "Angular Style"),
        ("1", "Smooth", "Bendy Style")
    ]
)


class SEDAIA_PT_SACR8_ui_global(Panel):
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
        rig = context.active_object
        rig_data = rig.data
        rig_bones = rig.pose.bones
        scene = context.scene
        lite = rig_data["lite"]

        # set Child Object Indices
        i = 0
        for l in rig.children:
            i = i + 1
            # Find Material Object
            objName = l.name.split(".")[0]
            if objName == mat_obj_name:
                mat_obj = l
                break

        skin = mat_obj.material_slots[0].material.node_tree
        skinTex = skin.nodes["Skin Texture"].image
        mainProp = rig_bones[prop_bones[0]]
        panel = self.layout

        p_row = panel.row()
        p_row.label(text="Utilities")

        p_row = panel.row()
        p_row.label(text="Skin Texture")
        i_row = panel.row(align=True)
        i_row.operator("sedaia_ot.imgpack", icon="PACKAGE" if is_packed(
            skinTex) else "UGLYPACKAGE").img_name = skinTex.name
        i_row = i_row.row(align=True)
        i_row.enabled = not is_packed(skinTex)
        i_row.prop(skinTex, "filepath", text="")
        i_row.operator("sedaia_ot.imgreload", icon="FILE_REFRESH",
                       text="").img_name = skinTex.name

        p_row = panel.row()

        p_col = p_row.column_flow(columns=2, align=True)
        p_col.prop(rig.pose, "use_mirror_x", toggle=True)
        p_col.prop(mainProp, '["Anti-Lag"]', toggle=True)

        panel.separator(type="LINE")


class SEDAIA_PT_SACR8_sui_QuickParentCTRL(Panel):
    bl_parent_id = "SEDAIA_PT_SACR8_ui_global"
    bl_label = "Quick Parent Objects"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_order = 5

    def draw(self, context):
        panel = self.layout

        rig = context.active_object
        rig_data = rig.data

        rig_bc = rig_data.collections_all

        t_row = panel.row()
        t_row.prop(rig_bc["Quick Parenting Objects"],
                   "is_visible", text="QP Show Objects", toggle=False)

        p_row = panel.row()
        p_row.enabled = rig_bc["Quick Parenting Objects"].is_visible
        p_col = p_row.column(align=True)
        c_row = p_col.row()
        c_row.prop(rig_bc["QP.Head"], "is_visible", text="Head", toggle=True)

        panel.separator(type="SPACE")

        p_row = panel.row()
        p_row.enabled = rig_bc["Quick Parenting Objects"].is_visible
        p_col = p_row.column(align=True)
        c_row = p_col.row()
        c_row.prop(rig_bc["QP.Torso"], "is_visible", text="Torso", toggle=True)
        d_row = p_col.row(align=True)
        d_row.enabled = rig_bc["QP.Torso"].is_visible
        d_row.prop(rig_bc["QP.Chest"], "is_visible", text="Chest", toggle=True)
        d_row.prop(rig_bc["QP.Hip"], "is_visible", text="Hips", toggle=True)
        d_row.prop(rig_bc["QP.Pelvis"], "is_visible", text="Root", toggle=True)

        panel.separator(type="SPACE")

        p_row = panel.row(align=True)
        p_row.enabled = rig_bc["Quick Parenting Objects"].is_visible
        p_col = p_row.column(align=False)
        p_col.prop(rig_bc["QP.Arm L"], "is_visible",
                   text="Left Arm", toggle=True)
        d_col = p_col.column(align=True)
        d_col.enabled = rig_bc["QP.Arm L"].is_visible
        d_col.prop(rig_bc["QP.Shoulder L"], "is_visible",
                   text="Shoulder", toggle=True)
        d_col.prop(rig_bc["QP.Forearm L"], "is_visible",
                   text="Forearm", toggle=True)
        d_col.prop(rig_bc["QP.Hand L"], "is_visible", text="Hand", toggle=True)

        p_col = p_row.column(align=False)
        p_col.prop(rig_bc["QP.Arm R"], "is_visible",
                   text="Right Arm", toggle=True)
        d_col = p_col.column(align=True)
        d_col.enabled = rig_bc["QP.Arm R"].is_visible
        d_col.prop(rig_bc["QP.Shoulder R"], "is_visible",
                   text="Shoulder", toggle=True)
        d_col.prop(rig_bc["QP.Forearm R"], "is_visible",
                   text="Forearm", toggle=True)
        d_col.prop(rig_bc["QP.Hand R"], "is_visible", text="Hand", toggle=True)

        panel.separator(type="SPACE")

        p_row = panel.row(align=True)
        p_row.enabled = rig_bc["Quick Parenting Objects"].is_visible
        p_col = p_row.column(align=False)
        p_col.prop(rig_bc["QP.Leg L"], "is_visible",
                   text="Left Leg", toggle=True)
        d_col = p_col.column(align=True)
        d_col.enabled = rig_bc["QP.Leg L"].is_visible
        d_col.prop(rig_bc["QP.Thigh L"], "is_visible",
                   text="Thigh", toggle=True)
        d_col.prop(rig_bc["QP.Knee L"], "is_visible", text="Knee", toggle=True)

        p_col = p_row.column(align=False)
        p_col.prop(rig_bc["QP.Leg R"], "is_visible",
                   text="Right Leg", toggle=True)
        d_col = p_col.column(align=True)
        d_col.enabled = rig_bc["QP.Leg R"].is_visible
        d_col.prop(rig_bc["QP.Thigh R"], "is_visible",
                   text="Thigh", toggle=True)
        d_col.prop(rig_bc["QP.Knee R"], "is_visible", text="Knee", toggle=True)


class SEDAIA_PT_SACR8_sui_headConfig(Panel):
    bl_parent_id = "SEDAIA_PT_SACR8_ui_global"
    bl_label = "Head"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_order = 0

    def draw(self, context):
        # Variables and Data
        rig = context.active_object
        rig_data = rig.data
        rig_bones = rig.pose.bones

        mainProp = rig_bones[prop_bones[0]]
        headProp = rig_bones[prop_bones[1]]

        # UI Layout
        panel = self.layout

        p_row = panel.row()
        p_row.prop(headProp, '["FaceToggle"]', text="Enable Face", toggle=True)

        p_row = panel.row()
        f_box = p_row.box()
        f_box.enabled = headProp['FaceToggle']

        f_row = f_box.row()
        f_row.label(text="Face Settings")


class SEDAIA_PT_SACR8_sui_torsoConfig(Panel):
    bl_parent_id = "SEDAIA_PT_SACR8_ui_global"
    bl_label = "Torso"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_order = 1

    def draw(self, context):
        # Variables and Data
        rig = context.active_object
        rig_data = rig.data
        rig_bones = rig.pose.bones

        mainProp = rig_bones[prop_bones[0]]
        torsoProp = rig_bones[prop_bones[2]]

        # UI Layout
        panel = self.layout

        p_row = panel.row()
        p_row.label(text="Style")
        p_row = panel.row()
        p_row.prop(torsoProp, '["FemaleDeformWeight"]',
                   text="Female Deforms", slider=True)


class SEDAIA_PT_SACR8_sui_armConfig(Panel):
    bl_parent_id = "SEDAIA_PT_SACR8_ui_global"
    bl_label = "Arms"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_order = 2

    def draw(self, context):
        # Variables and Data
        rig = context.active_object
        rig_data = rig.data
        rig_bones = rig.pose.bones

        mainProp = rig_bones[prop_bones[0]]
        armProp = rig_bones[prop_bones[3]]

        # UI Layout
        panel = self.layout

        p_row = panel.row()
        p_row.label(text="Style")
        p_row = panel.row()
        p_row.prop(armProp, '["SmoothBends"]', toggle=True, text="Smooth Bend")

        panel.separator(type="SPACE")
        p_row = panel.row()
        p_row.label(text="Arm Type")
        p_row = panel.row()
        p_row.prop(armProp, 'ArmType', expand=True)

        panel.separator(type="LINE")
        p_row = panel.row()
        p_row.label(text="Controllability")
        p_row = panel.row()
        p_row.label(text="IK Settings")
        p_row = panel.row(align=True)
        p_col = p_row.column(heading="Left", align=True)
        p_col.prop(armProp, '["ArmIK"]', slider=True, index=0, text="IK")
        p_col.prop(armProp, '["ArmStretchIK"]',
                   slider=True, index=0, text="Stretch")
        p_col.prop(armProp, '["WristIK"]', slider=True,
                   index=0, text="Wrist IK")

        p_col = p_row.column(heading="Right", align=True)
        p_col.prop(armProp, '["ArmIK"]', slider=True, index=1, text="IK")
        p_col.prop(armProp, '["ArmStretchIK"]',
                   slider=True, index=1, text="Stretch")
        p_col.prop(armProp, '["WristIK"]', slider=True,
                   index=1, text="Wrist IK")


class SEDAIA_PT_SACR8_sui_legConfig(Panel):
    bl_parent_id = "SEDAIA_PT_SACR8_ui_global"
    bl_label = "Legs"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_order = 3

    def draw(self, context):
        # Variables and Data
        rig = context.active_object
        rig_data = rig.data
        rig_bones = rig.pose.bones

        mainProp = rig_bones[prop_bones[0]]
        legProp = rig_bones[prop_bones[4]]

        # UI Layout
        panel = self.layout

        p_row = panel.row()
        p_row.label(text="Style")
        p_row = panel.row()
        p_row.prop(legProp, '["SmoothBends"]', toggle=True, text="Smooth Bend")
        b_row = panel.row()
        b_row.prop(legProp, '["FemaleDeformWeight"]',
                   text="Female Deforms", slider=True)

        panel.separator(type="SPACE")
        p_row = panel.row()
        p_row.label(text="Ankle Type")
        p_row = panel.row()
        p_row.prop(legProp, 'AnkleType', expand=True)

        panel.separator(type="LINE")
        p_row = panel.row()
        p_row.label(text="Controllability")
        p_row = panel.row()
        p_row.label(text="IK Settings")
        p_row = panel.row(align=True)
        p_col = p_row.column(heading="Left", align=True)
        p_col.prop(legProp, '["LegIK"]', slider=True, index=0, text="IK")
        p_col.prop(legProp, '["LegStretchIK"]',
                   slider=True, index=0, text="Stretch")
        p_col.prop(legProp, '["AnkleIK"]', slider=True,
                   index=0, text="Ankle IK")

        p_col = p_row.column(heading="Right", align=True)
        p_col.prop(legProp, '["LegIK"]', slider=True, index=1, text="IK")
        p_col.prop(legProp, '["LegStretchIK"]',
                   slider=True, index=1, text="Stretch")
        p_col.prop(legProp, '["AnkleIK"]', slider=True,
                   index=1, text="Ankle IK")

# Inclusion is purely for standalone script use,
# to disable, comment the associated classes in
# the "classes" variable at bottom of script,
# otherwise this UI will reference the addon for
# this purpose


def is_packed(img):
    try:
        return img.packed_files.values() != []
    except:
        return False


class SEDAIA_OT_SACR8_ImgPack(Operator):
    bl_idname = "sedaia_ot.imgpack"
    bl_label = ""

    img_name: P.StringProperty()  # type: ignore

    def execute(self, context):
        img = bpy.data.images[self.img_name]
        if is_packed(img):
            if bpy.data.is_saved:
                img.unpack()

            else:
                img.unpack(method="USE_LOCAL")
        else:
            img.pack()
        return {"FINISHED"}


class SEDAIA_OT_SACR8_ImgReload(Operator):
    bl_idname = "sedaia_ot.imgreload"
    bl_label = ""

    img_name: P.StringProperty()  # type: ignore

    def execute(self, context):
        bpy.data.images(self.img_name).reload()
        return {"FINISHED"}


classes = [
    # Main Panels
    SEDAIA_PT_SACR8_ui_global,

    # Sub Panels
    SEDAIA_PT_SACR8_sui_QuickParentCTRL,
    SEDAIA_PT_SACR8_sui_headConfig,
    SEDAIA_PT_SACR8_sui_torsoConfig,
    SEDAIA_PT_SACR8_sui_armConfig,
    SEDAIA_PT_SACR8_sui_legConfig

    # Operators, Uncomment when distributed as a Standalone Script
    # SEDAIA_OT_SACR8_ImgPack,
    # SEDAIA_OT_SACR8_ImgReload
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

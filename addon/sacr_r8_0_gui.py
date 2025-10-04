from .sedaia_operators import is_packed
from bpy.types import Operator, Panel
import bpy
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
# Scene Scale is 1.7065 for editing the rig

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

mat_obj_name = "Material_Properties"
prop_bones = [
    "Properties.RigMain",
    "Properties.Arms",
    "Properties.Legs"
]


# Global Rig Variables
rig = "SACR"
rig_ver = 8
category = f"{rig} R{rig_ver}"

# region Custom Properties

T.PoseBone.ArmType = P.EnumProperty(  # type: ignore
    name="Arm Type",
    description="Select your Arm Dimension",
    default="0",
    items=[
        ("0", "Standard", "Standard Arm Style, formerly called Steve Arms"),
        ("1", "Slim", "Slim Arm Style, formerly called Steve Arms"),
        ("2", "Super-Slim","Super Slim Arm style are a 3x3 version not available in Minecraft")
    ]
)

T.PoseBone.AnkleType = P.EnumProperty( #type: ignore
    name="Ankle Type",
    description="Ankle Type for the Left Leg",
    items=[
        ("0","Sharp","Angular Style"),
        ("1","Smooth","Bendy Style")
    ]
)
# endregion
# region Properties


class SEDAIA_PT_SACR8_ui_global(Panel):
    bl_label = "Properties"
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
        bones = rig.pose.bones
        scene = context.scene
        lite = rig_data["lite"]

        panel = self.layout

        p_row = panel.row()
        p_row.label(text="Utilities")

        p_row = panel.row()

        p_col = p_row.column_flow(columns=2, align=True)
        p_col.prop(rig.pose, "use_mirror_x", toggle=True)
        p_col.prop(scene.render, 'use_simplify', text="Anti-Lag", toggle=True)

        panel.separator(type="LINE")

# endregion
# region Customization


class SEDAIA_PT_SACR8_ui_visual(Panel):
    bl_label = "Visual Style"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_order = 1

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
        # Variables and Data
        rig = context.active_object
        rig_data = rig.data
        rig_bones = rig.pose.bones
        
        armProp = rig_bones[prop_bones[1]]
        legProp = rig_bones[prop_bones[2]]
        
        # UI Begin
        panel = self.layout
        p_row = panel.row()
        p_row.label(text="Arm Type")
        p_row = panel.row()
        p_row.prop(armProp, 'ArmType', expand=True)
        
        p_row = panel.row()
        p_box = p_row.box()
        b_row = p_box.row()
        b_row.label(text="Leg Customization")
        
        b_row = p_box.row(align=True)
        b_row.prop(legProp, '["AnkleToggle"]', toggle=True)
        b_row.prop(legProp, '["SmoothKnee"]', toggle=True, text="Sharp Knee")
        
        b_row = p_box.row()
        b_row.label(text="Ankle Type")
        b_row = p_box.row()
        b_row.prop(legProp, 'AnkleType', expand=True)
        
#endregion
#region Control Options
class SEDAIA_PT_SACR8_ui_controls(Panel):
    bl_label = "Control Styles"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_order = 2
    
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
        
        armProp = rig_bones[prop_bones[1]]
        legProp = rig_bones[prop_bones[2]]
        
        
        panel = self.layout
        panel.label(text="Control Options")
    
        p_row = panel.row()
        p_box = p_row.box()
        b_row = p_box.row()
        b_row.label(text="Arm Kinematics")
        b_row = p_box.row(align=True)
        b_col = b_row.column(align=True,heading="Left")
        b_col.prop(armProp, '["ArmIK"]', index=0, text="IK", slider=True)
        b_col.prop(armProp, '["ArmStretchIK"]', index=0, text="Stretch", slider=True)
        b_col.prop(armProp, '["WristIK"]', index=0, text="Wrist IK", slider=True)
        b_col = b_row.column(align=True,heading="Right")
        b_col.prop(armProp, '["ArmIK"]', index=1, text="IK", slider=True)
        b_col.prop(armProp, '["ArmStretchIK"]', index=1, text="Stretch", slider=True)
        b_col.prop(armProp, '["WristIK"]', index=1, text="Wrist IK", slider=True)
        
        
        p_row = panel.row()
        p_box = p_row.box()
        b_row = p_box.row()
        b_row.label(text="Leg Kinematics")
        b_row = p_box.row(align=True)
        b_col = b_row.column(align=True,heading="Left")
        b_col.prop(legProp, '["LegIK"]', index=0, text="IK", slider=True)
        b_col.prop(legProp, '["LegStretchIK"]', index=0, text="Stretch", slider=True)
        b_col.prop(legProp, '["AnkleIK"]', index=0, text="Ankle IK", slider=True)
        b_col = b_row.column(align=True,heading="Right")
        b_col.prop(legProp, '["LegIK"]', index=1, text="IK", slider=True)
        b_col.prop(legProp, '["LegStretchIK"]', index=1, text="Stretch", slider=True)
        b_col.prop(legProp, '["AnkleIK"]', index=1, text="Ankle IK", slider=True)
# endregion
# region Base Material
class SEDAIA_PT_SACR8_sui_baseMaterial(Panel):
    bl_parent_id = "SEDAIA_PT_SACR8_ui_global"
    bl_label = "Material Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_order = 0

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
            if objName == mat_obj_name:
                mat_obj = l
                break

        skin = mat_obj.material_slots[0].material.node_tree
        skinTex = skin.nodes["Skin Texture"].image

        # UI Begin
        panel = self.layout

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

        panel.separator(type="LINE")
# endregion
# region Registering
classes = [
    # Main Panels
    SEDAIA_PT_SACR8_ui_global,
    SEDAIA_PT_SACR8_ui_visual,
    SEDAIA_PT_SACR8_ui_controls,

    # Sub Panels
    SEDAIA_PT_SACR8_sui_baseMaterial

]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
# endregion

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


# =============
# region Imports
# Util Import
import bpy
from bpy.types import (
    Panel,
    PoseBone
)
from bpy.props import (
    EnumProperty,
)
from ..utils import sedaia_utils as utils


# endregion
# =============
# region Manifest
bl_info = {
    "name": "Sakura Rig UI",  # UI Name
    "id": "SR_GUI",  # UI ID
    "author": "Sakura Sedaia",
    "author_id": "Sedaia",

    "version": (2, 0, 0),
    "blender": (5, 0, 0),
    "location": "",
    "description": "",
    "warning": "",
    "doc_url": "",
    "tracker_url": "https://github.com/SakuraSedaia/Sedaia-Rig-Interfaces/issues",
    "category": "Interface",
}


rig_info = {
    "name": "Sakura's Advanced Character Rig",
    "id": "SACR",
    "version": (7, 4, 0),
}
# endregion
# =============
# region Addon Metadata (DO NOT MODIFY THIS AREA)

# endregion
# =============
# region Rig Settings
config = {
    # UI properties
    "tab": f"{rig_info['id']} R{rig_info['version'][0]}",

    # Rig Properties
    # ==============
    # Should output SACR.Rev_7.UI_2
    "id": f"{rig_info['id']}.Rev_{rig_info['version'][0]}.UI_{bl_info['version'][0]}",
    "idProp": "rigID",
    # Will set the Collection Name to match the rig when the name is changed
    "setGroupNamewithRig": True,
}

config_objs = {
    "main": "Rig_Properties",
    "face": "Face_Properties",
    "mouth": "Mouth_Properties",
    "eyes": "Eye_Properties",
    "eyebrows": "Eyebrow_Properties",
    "materials": "MaterialEditor",
    "root_bone": "SACR_Root"
}
# endregion
# =============
# region Object IDs
panel_prefix = f"SEDAIA_SACR{rig_info['version'][0]}_UI{bl_info['version'][0]}_PT"
panel = {
    "global": f"{panel_prefix}_global",
    "head": f"{panel_prefix}_sui_head",
    "face": f"{panel_prefix}_sui_face",
    "eyebrows": f"{panel_prefix}_sui_eyebrows",
    "iris": f"{panel_prefix}_sui_irises",
    "sclera": f"{panel_prefix}_sui_sclera",
    "mouth": f"{panel_prefix}_sui_mouth",
    "arm": f"{panel_prefix}_sui_arm",
    "torso": f"{panel_prefix}_sui_torso",
    "quick_parent": f"{panel_prefix}_sui_quick_parent",
    "armor": f"{panel_prefix}_sui_armor",
}


# endregion
# =============
# region Custom Properties
PoseBone.ArmType = EnumProperty(
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
PoseBone.Eyelashes = EnumProperty(
    name="Lash Type",
    description="What style Eyelashes you want",
    default="1",
    items=[
        ("0", "None", ""),
        ("1", "Classic", ""),
        ("2", "SACR", ""),
        ("3", "Flat", ""),
        ("4", "Enchanted Mob", ""),
        ("5", "DanoBandi", ""),
    ]
)


# endregion
# =============
# region Global Panel
class SACR7_UI2_ui_global(Panel):
    bl_label = "SACR Properties"
    bl_idname = panel['global']
    bl_category = config["tab"]
    bl_order = 0

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        try:
            r = context.active_object
            if r and r.type == "ARMATURE" and r.data:
                rData = r.data
                return rData[config["idProp"]] == config["id"]
            else:
                return False
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):

        # Rig Data
        rig = context.active_object
        rig_col = rig.users_collection[0]
        rig_data = rig.data
        rig_bones = rig.pose.bones
        rig_bc = rig_data.collections_all
        rig_child = rig.children_recursive

        mat_obj = utils.lookup_name(
            list=rig_child, query=config_objs['materials'])

        meshCol = utils.lookup_name(
            list=rig_col.children, query="Mesh")

        lite = rig_data['lite']
        skin = mat_obj.material_slots[0].material.node_tree
        skinTex = skin.nodes["Skin Texture"].image
        mainProp = rig_bones[config_objs['main']]
        root = rig_bones[config_objs["root_bone"]]

        panel = self.layout

        row = panel.row()
        row.label(text="Utilities")

        row = panel.row(align=True)
        row.prop(rig_data, '["Rig Name"]', text="Rig Name")

        rename = row.operator(
            utils.ops["rig_rename"], icon="FILE_REFRESH", text="")
        rename.name = rig_data['Rig Name']
        rename.update_collection = True

        row = panel.row()
        row.label(text="Skin Texture")
        row = panel.row(align=True)
        row.operator(utils.ops['image_pack'], icon="PACKAGE" if utils.is_packed(
            skinTex) else "UGLYPACKAGE", text="").path = skinTex.name
        row = row.row(align=True)
        row.enabled = not utils.is_packed(skinTex)
        row.prop(skinTex, "filepath", text="")
        row.operator(utils.ops['image_reload'], icon="FILE_REFRESH",
                     text="").path = skinTex.name

        row = panel.row()
        col = row.column_flow(columns=2, align=True)
        col.prop(rig.pose, "use_mirror_x",
                 icon="MOD_MIRROR", text="Mirror X-Axis")
        col.prop(rig_bc['Properties'], 'is_visible',
                 toggle=True, text="Legacy Properties",
                 icon="HIDE_ON" if rig_bc['Properties'].is_visible is False else "HIDE_OFF")
        col.prop(
            root.constraints["NormalizeScale"],
            'enabled',
            text="Reset Rig Scale",
            invert_checkbox=True, icon="CHECKBOX_DEHLT")
        col.prop(meshCol, 'hide_select',
                 text="Restrict Selection")
        if lite is False:
            col.prop(mainProp, '["Show Lattices"]',
                     index=0,
                     text="Body Lattices",
                     icon="HIDE_ON" if mainProp["Show Lattices"][0] is False else "HIDE_OFF")


# endregion
# =============
# region Head Settings
class SACR7_UI2_sui_head(Panel):
    bl_parent_id = panel['global']
    bl_idname = panel['head']
    bl_label = "Head"
    bl_order = 0

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        # Variables and Data
        rig = context.active_object
        rig_data = rig.data
        rig_bones = rig.pose.bones

        mainProp = rig_bones[config_objs['main']]

        # UI Layout
        panel = self.layout

        p_row = panel.row()
        p_col = p_row.column(align=True)
        p_col.prop(mainProp, '["Face Toggle"]',
                   text="Enable Face",
                   toggle=True,
                   icon="HIDE_ON" if mainProp["Face Toggle"] is False else "HIDE_OFF")


# endregion
# =============
# region Face Panel
# Child of the Head Panel
class SACR7_UI2_sui_face(Panel):
    bl_label = "Face"
    bl_idname = panel["face"]
    bl_parent_id = panel["head"]
    bl_order = 0

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

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
        rig = context.active_object
        rig_data = rig.data
        rig_bones = rig.pose.bones
        rig_bc = rig_data.collections_all
        faceProp = rig_bones[config_objs["face"]]

        panel = self.layout

        p_row = panel.row()
        p_row.label(text="Face Controls")

        p_row = panel.row(align=True)
        p_row.prop(faceProp, '["Face | UV"]',
                   text="Face Auto-UV", toggle=True,
                   icon="HIDE_ON" if faceProp["Face | UV"] is False else "HIDE_OFF")

        p_row = panel.row()
        p_row.label(text="On-Face Controls")

        p_row = panel.row()
        f_col = p_row.column()
        fc_row = f_col.row()

        fc_row.prop(rig_bc["Eyebrow_Left_Simplified"], 'is_visible',
                    text="Left Eyebrow",
                    icon="HIDE_ON" if rig_bc["Eyebrow_Left_Simplified"].is_visible is False else "HIDE_OFF"
                    )

        fc_row.prop(rig_bc["Eyebrow_Right_Simplified"],
                    'is_visible',
                    text="Right Eyebrow",
                    icon="HIDE_ON" if rig_bc["Eyebrow_Right_Simplified"].is_visible is False else "HIDE_OFF"
                    )

        fc_row = f_col.row()
        fc_row.prop(rig_bc["Eye_Left_Simplified"], 'is_visible',
                    text="Left Eye",
                    icon="HIDE_ON" if rig_bc["Eye_Left_Simplified"].is_visible is False else "HIDE_OFF"
                    )

        fc_row.prop(rig_bc["Eye_Right_Simplified"],
                    'is_visible',
                    text="Right Eye",
                    icon="HIDE_ON" if rig_bc["Eye_Right_Simplified"].is_visible is False else "HIDE_OFF"
                    )

        fc_row = f_col.row()
        fc_row.prop(rig_bc["Mouth"],
                    'is_visible',
                    text="Mouth",
                    icon="HIDE_ON" if rig_bc["Mouth"].is_visible is False else "HIDE_OFF"
                    )

        p_row = panel.row()
        p_row.label(text="On-Face Controls")
        p_row = panel.row()
        f_col = p_row.column()
        fc_row = f_col.row()

        col = fc_row.column()
        col.enabled = rig_bc['Eyebrow_Left_Simplified'].is_visible
        col.prop(rig_bc["Eyebrow_Left_Advanced"],
                 'is_visible',
                 text="Left Eyebrow",
                 icon="HIDE_ON" if rig_bc["Eyebrow_Left_Advanced"].is_visible is False else "HIDE_OFF"
                 )

        col = fc_row.column()
        col.enabled = rig_bc['Eyebrow_Right_Simplified'].is_visible
        col.prop(rig_bc["Eyebrow_Right_Advanced"],
                 'is_visible',
                 text="Right Eyebrow",
                 icon="HIDE_ON" if rig_bc["Eyebrow_Right_Advanced"].is_visible is False else "HIDE_OFF"
                 )

        fc_row = f_col.row()
        col = fc_row.column()
        col.enabled = rig_bc['Eye_Left_Simplified'].is_visible
        col.prop(rig_bc["Eye_Left_Advanced"],
                 'is_visible',
                 text="Left Eye",
                 icon="HIDE_ON" if rig_bc["Eye_Left_Advanced"].is_visible is False else "HIDE_OFF"
                 )

        col = fc_row.column()
        col.enabled = rig_bc['Eye_Right_Simplified'].is_visible
        col.prop(rig_bc["Eye_Right_Advanced"],
                 'is_visible',
                 text="Right Eye",
                 icon="HIDE_ON" if rig_bc["Eye_Right_Advanced"].is_visible is False else "HIDE_OFF"
                 )

        fc_row = f_col.row()
        col = fc_row.column()
        col.enabled = rig_bc['Mouth'].is_visible
        col.prop(rig_bc["Mouth_Advanced"],
                 'is_visible',
                 text="Mouth",
                 icon="HIDE_ON" if rig_bc["Mouth_Advanced"].is_visible is False else "HIDE_OFF"
                 )


# endregion
# =============
# region Eyebrows Panel
# Child of Face Panel
class SACR7_UI2_sui_eyebrows(Panel):
    bl_label = "Eyebrows"
    bl_idname = panel["eyebrows"]
    bl_parent_id = panel["face"]
    bl_order = 0

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            face_on = obj.pose.bones["Rig_Properties"]["Face Toggle"]
            return face_on
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        # Rig Data
        rig = context.active_object
        rig_bones = rig.pose.bones

        eyebrowProp = rig_bones[config_objs["eyebrows"]]

        rig_child = rig.children_recursive

        mat_obj = utils.lookup_name(
            list=rig_child, query=config_objs['materials'])

        skin = mat_obj.material_slots[0].material.node_tree

        eyebrowMat = mat_obj.material_slots[6].material.node_tree.nodes['Node']
        eyebrowGrad = eyebrowMat.inputs['Gradient'].default_value
        eyebrowSplit = eyebrowMat.inputs['Split Color'].default_value

        panel = self.layout

        row = panel.row()
        row.label(text="Options", icon="PROPERTIES")

        row = panel.row()
        col = row.column(align=True)
        col.prop(eyebrowProp, '["Depth"]', slider=True)
        col.prop(eyebrowProp, '["Width"]', slider=True)
        col.prop(eyebrowProp, '["Thickness"]', slider=True)

        panel.separator(type="LINE")

        row = panel.row()
        row.label(text='Colors', icon="MOD_COLOR_BALANCE")

        row = panel.row(align=True)

        colLeft = row.column(heading="", align=True)
        colLeftRow1 = colLeft.row(align=True)
        colLeftRow2 = colLeft.row(align=True)
        colRight = row.column(heading="", align=True)
        colRightRow1 = colRight.row(align=True)
        colRightRow2 = colRight.row(align=True)
        colLeftRow1.prop(
            eyebrowMat.inputs['L.Color In'], "default_value", text="")
        colLeft.prop(
            eyebrowMat.inputs['Gradient'], "default_value", text='Gradient', toggle=True)
        colRight.prop(
            eyebrowMat.inputs['Split Color'], "default_value", text='Split', toggle=True)

        colLeftRow2.enabled = eyebrowGrad
        colLeftRow2.prop(
            eyebrowMat.inputs['L.Color Out'], "default_value", text="")

        colRightRow1.enabled = eyebrowSplit
        colRightRow1.prop(
            eyebrowMat.inputs['R.Color In'], "default_value", text="")

        colRightRow2.enabled = eyebrowSplit and eyebrowGrad
        colRightRow2.prop(
            eyebrowMat.inputs['R.Color Out'], "default_value", text="")


# endregion
# =============
# region Iris Panel
# Child of Face Panel
class SACR7_UI2_sui_iris(Panel):
    bl_label = "Irises"
    bl_idname = panel["iris"]
    bl_parent_id = panel["face"]
    bl_order = 1

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            face_on = obj.pose.bones["Rig_Properties"]["Face Toggle"]
            return face_on
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        # Rig Data
        rig = context.active_object
        rig_bones = rig.pose.bones

        props = rig_bones[config_objs["eyes"]]
        mainProp = rig_bones[config_objs['main']]

        # set Child Object Indices
        rig_child = rig.children_recursive

        mat_obj = utils.lookup_name(
            list=rig_child, query=config_objs['materials'])

        iris_mat = mat_obj.material_slots[1].material.node_tree
        iris_shad = iris_mat.nodes['Iris_Shader']
        pupil_tex = iris_mat.nodes['Pupil_Tex'].image
        iris_ramp = iris_mat.nodes['Ramp']

        panel = self.layout

        row = panel.row()
        row.label(text="Options", icon="PROPERTIES")

        if rig.data['lite'] is False:
            row = panel.row(align=True)
            split = row.split(factor=.3)
            split.label(text="Lash Style")
            split.prop(props, 'Eyelashes', text="")

            row = panel.row()
            col = row.column(align=True)

            crow = col.row(align=True)
            crow.prop(mainProp, '["Show Lattices"]',
                      index=1,
                      toggle=True,
                      text="Show Lattice",
                      icon="HIDE_ON" if mainProp["Show Lattices"][1] is False else "HIDE_OFF"
                      )
            crow.prop(props, '["Eyesparkle"]',
                      text="Eye Sparkles",
                      icon="HIDE_ON" if props["Eyesparkle"] is False else "HIDE_OFF"
                      )
            col.prop(props, '["Iris Inset"]', text="Inset Irises")
        else:
            row = panel.row()
            col = row.column(align=True)
            col.prop(props, '["Iris Inset"]', text="Inset Irises")

        panel.separator(type="LINE")

        row = panel.row()
        row.label(text="Materials")

        iris_grad = iris_shad.inputs[0].default_value
        iris_het = iris_shad.inputs[3].default_value

        row = panel.row()
        row.label(text="Colors", icon="MOD_COLOR_BALANCE")
        row = panel.row(align=True)
        colLeft = row.column(heading="", align=True)
        colLeftRow1 = colLeft.row(align=True)
        colLeftRow2 = colLeft.row(align=True)
        colRight = row.column(heading="", align=True)
        colRightRow1 = colRight.row(align=True)
        colRightRow2 = colRight.row(align=True)
        colLeftRow1.prop(
            iris_shad.inputs[1], "default_value", text="")
        colLeft.prop(
            iris_shad.inputs[0], "default_value",
            text='Gradient',
            icon="CHECKBOX_HLT" if iris_shad.inputs[0].default_value is True else "CHECKBOX_DEHLT",
        )
        colRight.prop(
            iris_shad.inputs[3], "default_value",
            text='Hetero',
            icon="CHECKBOX_HLT" if iris_shad.inputs[3].default_value is True else "CHECKBOX_DEHLT",
        )

        colLeftRow2.enabled = iris_grad
        colLeftRow2.prop(
            iris_shad.inputs[2], "default_value", text="")

        colRightRow1.enabled = iris_het
        colRightRow1.prop(
            iris_shad.inputs[4], "default_value", text="")

        colRightRow2.enabled = iris_het and iris_grad
        colRightRow2.prop(
            iris_shad.inputs[5], "default_value", text="")

        row = panel.row(align=True)
        row.label(text="Reflections", icon="MATERIAL_DATA")

        row = panel.row(align=True)
        col = row.column(align=True)
        col.prop(iris_shad.inputs[19], 'default_value', text="Metalic")
        col.prop(iris_shad.inputs[20], 'default_value', text="Specular")
        col.prop(iris_shad.inputs[21], 'default_value', text="Roughness")
        row = col.row()
        split = row.split(factor=.3)
        split.label(text="Spec Tint")
        split.prop(iris_shad.inputs[22], 'default_value', text="")

        panel.separator(type="LINE")

        emit_enable = iris_shad.inputs[31].default_value

        row = panel.row()
        split = row.split(factor=.92)
        split.label(text="Emission", icon="OUTLINER_OB_LIGHT")
        split.prop(iris_shad.inputs[31],
                   'default_value',
                   text="",
                   icon="CHECKBOX_HLT" if emit_enable is True else "CHECKBOX_DEHLT",
                   )

        if emit_enable:
            row = panel.row(align=True)

            emit_het = iris_shad.inputs[34].default_value
            emit_grad = iris_shad.inputs[35].default_value

            if iris_shad.inputs[33].default_value is True:
                colLeft = row.column(heading="", align=True)
                colLeftRow1 = colLeft.row(align=True)
                colLeftRow2 = colLeft.row(align=True)
                colRight = row.column(heading="", align=True)
                colRightRow1 = colRight.row(align=True)
                colRightRow2 = colRight.row(align=True)
                colLeftRow1.prop(
                    iris_shad.inputs[36], "default_value", text="")
                colLeft.prop(
                    iris_shad.inputs[35], "default_value",
                    text='Gradient',
                    icon="CHECKBOX_HLT" if iris_shad.inputs[35].default_value is True else "CHECKBOX_DEHLT",
                )
                colRight.prop(
                    iris_shad.inputs[34], "default_value",
                    text='Hetero',
                    icon="CHECKBOX_HLT" if iris_shad.inputs[34].default_value is True else "CHECKBOX_DEHLT",
                )

                colLeftRow2.enabled = emit_grad
                colLeftRow2.prop(
                    iris_shad.inputs[37], "default_value", text="")

                colRightRow1.enabled = emit_het
                colRightRow1.prop(
                    iris_shad.inputs[38], "default_value", text="")

                colRightRow2.enabled = emit_het and emit_grad
                colRightRow2.prop(
                    iris_shad.inputs[39], "default_value", text="")
            else:
                col = row.column()
                col.prop(iris_shad.inputs[36],
                         "default_value", text="Strength")
                col.prop(
                    iris_shad.inputs[33], "default_value", text='Split Channels', toggle=True)

        row = panel.row()
        split = row.split(factor=.92)
        split.label(text="Pupils", icon="SHADING_RENDERED")
        split.prop(iris_shad.inputs[40],
                   'default_value',
                   text="",
                   icon="CHECKBOX_HLT" if iris_shad.inputs[40].default_value is True else "CHECKBOX_DEHLT",
                   )

        pupil_toggle = iris_shad.inputs[40].default_value
        if pupil_toggle is True:
            row = panel.row()
            row.prop(iris_shad.inputs[41], 'default_value', text='')

            row = panel.row(align=True)

            row.prop(iris_shad.inputs[42], 'default_value', text='Opacity')
            row.prop(iris_shad.inputs[43], 'default_value', text='Custom')

            row = panel.row(align=True)
            row.label(text="Pupil Scale")

            row = panel.row(align=True)

            row.enabled = iris_shad.inputs[40].default_value
            row.prop(iris_shad.inputs['Size X'],
                     'default_value', text='X', slider=True)
            row.prop(iris_shad.inputs['Size Y'],
                     'default_value', text='Y', slider=True)

            panel.separator(type="LINE")

            row = panel.row(align=True)

            row = panel.row(align=True)
            if iris_shad.inputs[43].default_value > 0:
                row = row.row()
                row.label(text="Pupil Texture")

                row = panel.row(align=True)
                row.enabled = iris_shad.inputs[43].default_value > 0
                row = row.row(align=True)
                row.operator(utils.ops['image_pack'], icon="PACKAGE" if utils.is_packed(
                    pupil_tex) else "UGLYPACKAGE", text="").path = pupil_tex.name
                row = row.row(align=True)
                row.enabled = not utils.is_packed(pupil_tex)
                row.prop(pupil_tex, "filepath", text="")
                row.operator(utils.ops['image_reload'], icon="FILE_REFRESH",
                             text="").path = pupil_tex.name

                row = panel.row(align=True)
                row.enabled = iris_shad.inputs[43].default_value > 0

                boxe = row.box()
                boxe.label(text="Pupil Ramp")
                boxe.template_color_ramp(iris_ramp, 'color_ramp', expand=True)


# endregion
# =============
# region Sclera Panel
# Child of Face Panel
class SACR7_UI2_sui_sclera(Panel):
    bl_label = "Sclera"
    bl_idname = panel["sclera"]
    bl_parent_id = panel["face"]
    bl_order = 1

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            face_on = obj.pose.bones["Rig_Properties"]["Face Toggle"]
            return face_on
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        # Rig Data
        rig = context.active_object
        rig_data = rig.data
        rig_bones = rig.pose.bones
        rig_bc = rig_data.collections_all

        props = rig_bones[config_objs["eyes"]]

        # set Child Object Indices
        rig_child = rig.children_recursive

        mat_obj = utils.lookup_name(
            list=rig_child, query=config_objs['materials'])

        iris_mat = mat_obj.material_slots[2].material.node_tree
        iris_shad = iris_mat.nodes['Sclera_Shader']

        panel = self.layout

        row = panel.row()
        row.label(text="Options", icon="PROPERTIES")

        row = panel.row()
        col = row.column(align=True)
        col.prop(props, '["Sclera Depth"]', text="Eye Depth")

        panel.separator(type="LINE")

        row = panel.row()
        row.label(text="Materials")

        iris_grad = iris_shad.inputs[0].default_value
        iris_het = iris_shad.inputs[3].default_value

        row = panel.row()
        row.label(text="Colors", icon="MOD_COLOR_BALANCE")
        row = panel.row(align=True)
        colLeft = row.column(heading="", align=True)
        colLeftRow1 = colLeft.row(align=True)
        colLeftRow2 = colLeft.row(align=True)
        colRight = row.column(heading="", align=True)
        colRightRow1 = colRight.row(align=True)
        colRightRow2 = colRight.row(align=True)
        colLeftRow1.prop(
            iris_shad.inputs[1], "default_value", text="")
        colLeft.prop(
            iris_shad.inputs[0], "default_value", text='Gradient',
            icon="CHECKBOX_HLT" if iris_grad is True else "CHECKBOX_DEHLT",
        )
        colRight.prop(
            iris_shad.inputs[3], "default_value", text='Hetero',
            icon="CHECKBOX_HLT" if iris_het is True else "CHECKBOX_DEHLT",
        )

        colLeftRow2.enabled = iris_grad
        colLeftRow2.prop(
            iris_shad.inputs[2], "default_value", text="")

        colRightRow1.enabled = iris_het
        colRightRow1.prop(
            iris_shad.inputs[4], "default_value", text="")

        colRightRow2.enabled = iris_het and iris_grad
        colRightRow2.prop(
            iris_shad.inputs[5], "default_value", text="")

        row = panel.row(align=True)
        row.label(text="Reflections", icon="MATERIAL_DATA")

        row = panel.row(align=True)
        col = row.column(align=True)
        col.prop(iris_shad.inputs[19], 'default_value', text="Metalic")
        col.prop(iris_shad.inputs[20], 'default_value', text="Specular")
        col.prop(iris_shad.inputs[21], 'default_value', text="Roughness")
        row = col.row()
        split = row.split(factor=.3)
        split.label(text="Spec Tint")
        split.prop(iris_shad.inputs[22], 'default_value', text="")

        panel.separator(type="LINE")

        emit_enable = iris_shad.inputs[31].default_value

        row = panel.row()
        split = row.split(factor=.92)
        split.label(text="Emission", icon="OUTLINER_OB_LIGHT")
        split.prop(iris_shad.inputs[31],
                   'default_value',
                   text="",
                   icon="CHECKBOX_HLT" if emit_enable is True else "CHECKBOX_DEHLT",
                   )

        if emit_enable:

            emit_het = iris_shad.inputs[34].default_value
            emit_grad = iris_shad.inputs[35].default_value

            if iris_shad.inputs[33].default_value is True:

                row = panel.row(align=True)
                split = row.split(factor=.5)
                split.prop(
                    iris_shad.inputs[33], "default_value",
                    text='Split Channels',
                    icon="CHECKBOX_HLT" if iris_shad.inputs[33].default_value is True else "CHECKBOX_DEHLT",
                )

                row = panel.row(align=True)
                colLeft = row.column(heading="", align=True)
                colLeftRow1 = colLeft.row(align=True)
                colLeftRow2 = colLeft.row(align=True)
                colRight = row.column(heading="", align=True)
                colRightRow1 = colRight.row(align=True)
                colRightRow2 = colRight.row(align=True)
                colLeftRow1.prop(
                    iris_shad.inputs[36], "default_value", text="")
                colLeft.prop(
                    iris_shad.inputs[35], "default_value", text='Gradient',
                    icon="CHECKBOX_HLT" if emit_grad is True else "CHECKBOX_DEHLT",
                )
                colRight.prop(
                    iris_shad.inputs[34], "default_value", text='Hetero',
                    icon="CHECKBOX_HLT" if emit_het is True else "CHECKBOX_DEHLT",
                )

                colLeftRow2.enabled = emit_grad
                colLeftRow2.prop(
                    iris_shad.inputs[37], "default_value", text="")

                colRightRow1.enabled = emit_het
                colRightRow1.prop(
                    iris_shad.inputs[38], "default_value", text="")

                colRightRow2.enabled = emit_het and emit_grad
                colRightRow2.prop(
                    iris_shad.inputs[39], "default_value", text="")

            else:
                row = panel.row(align=True)
                row.prop(
                    iris_shad.inputs[33], "default_value",
                    text='Split Channels',
                    icon="CHECKBOX_HLT" if iris_shad.inputs[33].default_value is True else "CHECKBOX_DEHLT",
                )

                row.prop(iris_shad.inputs[36],
                         "default_value", text="Strength")


# endregion
# =============
# region Mouth Panel
# Child of Face Panel
class SACR7_UI2_sui_mouth(Panel):
    bl_label = "Mouth"
    bl_idname = panel["mouth"]
    bl_parent_id = panel["face"]
    bl_order = 2

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            face_on = obj.pose.bones["Rig_Properties"]["Face Toggle"]
            return face_on
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        # Rig Data
        rig = context.active_object
        rig_data = rig.data
        rig_bones = rig.pose.bones
        rig_bc = rig_data.collections_all

        props = rig_bones[config_objs["mouth"]]

        # set Child Object Indices
        i = 0
        rig_child = rig.children_recursive

        mat_obj = utils.lookup_name(
            list=rig_child, query=config_objs['materials'])

        mouth_back = mat_obj.material_slots[3].material.node_tree.nodes['Material']
        teeth = mat_obj.material_slots[4].material.node_tree.nodes['Material']

        panel = self.layout

        row = panel.row()
        row.label(text="Options", icon="PROPERTIES")
        row = panel.row()
        col = row.column(align=True)
        col.prop(props, '["Square Mouth"]', slider=True, text="Square")
        crow = col.row(align=True)
        crow.prop(props, '["Classic Mouth"]', text="Shallow Mouth",
                  icon="CHECKBOX_HLT" if props['Classic Mouth'] is True else "CHECKBOX_DEHLT",
                  )
        crow.prop(rig_bc['Molar Controls'], "is_visible",
                  text="Molar Controls",
                  icon="HIDE_OFF" if rig_bc['Molar Controls'].is_visible is True else "HIDE_ON",
                  )

        panel.separator(type="LINE")

        row = panel.row()
        row.label(text="Colors", icon="MOD_COLOR_BALANCE")

        row = panel.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.label(text="Inside")
        row.label(text="Teeth")
        row = col.row(align=True)
        row.prop(mouth_back.inputs['Base Color'],
                 "default_value", text="")
        row.prop(teeth.inputs['Base Color'],
                 "default_value", text="")


# endregion
# =============
# region Torso Panel
# Child of Global
class SACR7_UI2_sui_torso(Panel):
    bl_label = "Torso"
    bl_idname = panel["torso"]
    bl_parent_id = panel["global"]
    bl_order = 1

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        if context.active_object.data['lite'] is True:
            return False
        else:
            return True

    def draw(self, context):
        # Variables and Data
        rig = context.active_object
        rig_bones = rig.pose.bones

        mainProp = rig_bones[config_objs["main"]]

        # UI Layout
        panel = self.layout

        p_row = panel.row()
        p_row.label(text="Style")
        p_row = panel.row()
        p_row.prop(mainProp, '["Female Curves"]',
                   text="Female Deforms", slider=True)

        p_row = panel.row()
        p_row.prop(mainProp, '["Long Hair Rig"]',
                   text="Hair Rig")


# endregion
# =============
# region Arm Panel
# Child of Global
class SACR7_UI2_sui_arm(Panel):
    bl_label = "Arm"
    bl_idname = panel["arm"]
    bl_parent_id = panel["global"]
    bl_order = 2

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        # Variables and Data
        rig = context.active_object
        rig_bones = rig.pose.bones

        mainProp = rig_bones[config_objs['main']]

        # UI Layout
        panel = self.layout

        p_row = panel.row()

        panel.separator(type="SPACE")
        p_row = panel.row()
        p_row.label(text="Arm Type")
        p_row = panel.row()
        p_row.prop(mainProp, 'ArmType', expand=True)

        panel.separator(type="LINE")
        p_row = panel.row()
        p_row.label(text="Controllability")
        p_row = panel.row()
        p_row.label(text="IK Settings")
        p_row = panel.row(align=True)
        p_col = p_row.column(heading="Left", align=True)
        p_col.prop(mainProp, '["Arm IK"]', slider=True, index=0, text="IK")
        p_col.prop(mainProp, '["Arm Stretch"]',
                   slider=True, index=0, text="Stretch")
        p_col.prop(mainProp, '["Arm Wrist IK"]', slider=True,
                   index=0, text="Wrist IK")

        p_col = p_row.column(heading="Right", align=True)
        p_col.prop(mainProp, '["Arm IK"]', slider=True, index=1, text="IK")
        p_col.prop(mainProp, '["Arm Stretch"]',
                   slider=True, index=1, text="Stretch")
        p_col.prop(mainProp, '["Arm Wrist IK"]', slider=True,
                   index=1, text="Wrist IK")


# endregion
# =============
# region Quick Parent Panel
# Child of Global
class SACR7_UI2_sui_quick_parent(Panel):
    bl_label = "Quick Parents"
    bl_idname = panel["quick_parent"]
    bl_parent_id = panel["global"]
    bl_order = 3

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        panel = self.layout

        rig = context.active_object
        rig_data = rig.data

        rig_bc = rig_data.collections_all

        t_row = panel.row()
        t_row.prop(rig_bc["Quick Parents"],
                   "is_visible", text="QP Show Objects",
                   icon="HIDE_ON" if rig_bc["Quick Parents"].is_visible is False else "HIDE_OFF")

        p_row = panel.row()
        p_row.enabled = rig_bc["Quick Parents"].is_visible
        p_col = p_row.column(align=True)
        c_row = p_col.row()
        c_row.prop(rig_bc["QP.Head"], "is_visible", text="Head",
                   icon="HIDE_ON" if rig_bc["QP.Head"].is_visible is False else "HIDE_OFF")

        panel.separator(type="SPACE")

        p_row = panel.row()
        p_row.enabled = rig_bc["Quick Parents"].is_visible
        p_col = p_row.column(align=True)
        c_row = p_col.row()
        c_row.prop(rig_bc["QP.Torso"], "is_visible", text="Torso",
                   icon="HIDE_ON" if rig_bc["QP.Torso"].is_visible is False else "HIDE_OFF")
        d_row = p_col.row(align=True)
        d_row.enabled = rig_bc["QP.Torso"].is_visible
        d_row.prop(rig_bc["QP.Chest"], "is_visible", text="Chest",
                   icon="HIDE_ON" if rig_bc["QP.Chest"].is_visible is False else "HIDE_OFF")
        d_row.prop(rig_bc["QP.Hip"], "is_visible", text="Hips",
                   icon="HIDE_ON" if rig_bc["QP.Hip"].is_visible is False else "HIDE_OFF")
        d_row.prop(rig_bc["QP.Pelvis"], "is_visible", text="Root",
                   icon="HIDE_ON" if rig_bc["QP.Pelvis"].is_visible is False else "HIDE_OFF")

        panel.separator(type="SPACE")

        p_row = panel.row(align=True)
        p_row.enabled = rig_bc["Quick Parents"].is_visible
        p_col = p_row.column(align=False)
        p_col.prop(rig_bc["QP.Arm L"], "is_visible", text="Left Arm",
                   icon="HIDE_ON" if rig_bc["QP.Arm L"].is_visible is False else "HIDE_OFF")
        d_col = p_col.column(align=True)
        d_col.enabled = rig_bc["QP.Arm L"].is_visible
        d_col.prop(rig_bc["QP.Shoulder L"], "is_visible", text="Shoulder",
                   icon="HIDE_ON" if rig_bc["QP.Shoulder L"].is_visible is False else "HIDE_OFF")
        d_col.prop(rig_bc["QP.Forearm L"], "is_visible", text="Forearm",
                   icon="HIDE_ON" if rig_bc["QP.Forearm L"].is_visible is False else "HIDE_OFF")
        d_col.prop(rig_bc["QP.Hand L"], "is_visible", text="Hand",
                   icon="HIDE_ON" if rig_bc["QP.Hand L"].is_visible is False else "HIDE_OFF")

        p_col = p_row.column(align=False)
        p_col.prop(rig_bc["QP.Arm R"], "is_visible", text="Right Arm",
                   icon="HIDE_ON" if rig_bc["QP.Arm R"].is_visible is False else "HIDE_OFF")
        d_col = p_col.column(align=True)
        d_col.enabled = rig_bc["QP.Arm R"].is_visible
        d_col.prop(rig_bc["QP.Shoulder R"], "is_visible", text="Shoulder",
                   icon="HIDE_ON" if rig_bc["QP.Shoulder R"].is_visible is False else "HIDE_OFF")
        d_col.prop(rig_bc["QP.Forearm R"], "is_visible", text="Forearm",
                   icon="HIDE_ON" if rig_bc["QP.Forearm R"].is_visible is False else "HIDE_OFF")
        d_col.prop(rig_bc["QP.Hand R"], "is_visible", text="Hand",
                   icon="HIDE_ON" if rig_bc["QP.Hand R"].is_visible is False else "HIDE_OFF")

        panel.separator(type="SPACE")

        p_row = panel.row(align=True)
        p_row.enabled = rig_bc["Quick Parents"].is_visible
        p_col = p_row.column(align=False)
        p_col.prop(rig_bc["QP.Leg L"], "is_visible", text="Left Leg",
                   icon="HIDE_ON" if rig_bc["QP.Leg L"].is_visible is False else "HIDE_OFF")
        d_col = p_col.column(align=True)
        d_col.enabled = rig_bc["QP.Leg L"].is_visible
        d_col.prop(rig_bc["QP.Thigh L"], "is_visible", text="Thigh",
                   icon="HIDE_ON" if rig_bc["QP.Thigh L"].is_visible is False else "HIDE_OFF")
        d_col.prop(rig_bc["QP.Knee L"], "is_visible", text="Knee",
                   icon="HIDE_ON" if rig_bc["QP.Knee L"].is_visible is False else "HIDE_OFF")

        p_col = p_row.column(align=False)
        p_col.prop(rig_bc["QP.Leg R"], "is_visible", text="Right Leg",
                   icon="HIDE_ON" if rig_bc["QP.Leg R"].is_visible is False else "HIDE_OFF")
        d_col = p_col.column(align=True)
        d_col.enabled = rig_bc["QP.Leg R"].is_visible
        d_col.prop(rig_bc["QP.Thigh R"], "is_visible", text="Thigh",
                   icon="HIDE_ON" if rig_bc["QP.Thigh R"].is_visible is False else "HIDE_OFF")
        d_col.prop(rig_bc["QP.Knee R"], "is_visible", text="Knee",
                   icon="HIDE_ON" if rig_bc["QP.Knee R"].is_visible is False else "HIDE_OFF")


# endregion
# =============
# region Armor Panel
# Child of Global
class SACR7_UI2_sui_armor(Panel):
    bl_label = "Armor"
    bl_idname = panel['armor']
    bl_parent_id = panel['global']
    bl_order = 4

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        if context.active_object.data['lite'] is True:
            return False
        else:
            return True

    def draw(self, context):

        # Rig Data
        rig = context.active_object
        rig_bones = rig.pose.bones

        # set Child Object Indices
        rig_child = rig.children_recursive

        mat_obj = utils.lookup_name(
            list=rig_child, query=config_objs['materials'])

        mainProp = rig_bones[config_objs["main"]]

        panel = self.layout

        row = panel.row()
        column = row.column(align=True)

        row = column.row()
        row.prop(mainProp, '["Armor Toggle"]',
                 index=0, text="Helmet",
                 icon="HIDE_ON" if mainProp["Armor Toggle"][0] is False else "HIDE_OFF"
                 )
        Mat = mat_obj.material_slots[8].material.node_tree.nodes["Armor Texture"].image

        row = column.row(align=True)
        row.operator(utils.ops['image_pack'], icon="PACKAGE" if utils.is_packed(
            Mat) else "UGLYPACKAGE", text="").path = Mat.name
        row = row.row(align=True)
        row.enabled = not utils.is_packed(Mat)
        row.prop(Mat, "filepath", text="")
        row.operator(utils.ops['image_reload'], icon="FILE_REFRESH",
                     text="").path = Mat.name

        column.separator(type='SPACE')
        column.separator(type='LINE')
        column.separator(type='SPACE')

        row = column.row()
        row.prop(mainProp, '["Armor Toggle"]', index=1,
                 text="Chestplate",
                 icon="HIDE_ON" if mainProp["Armor Toggle"][1] is False else "HIDE_OFF"
                 )
        Mat = mat_obj.material_slots[9].material.node_tree.nodes["Armor Texture"].image

        row = column.row(align=True)
        row.operator(utils.ops['image_pack'], icon="PACKAGE" if utils.is_packed(
            Mat) else "UGLYPACKAGE", text="").path = Mat.name
        row = row.row(align=True)
        row.enabled = not utils.is_packed(Mat)
        row.prop(Mat, "filepath", text="")
        row.operator(utils.ops['image_reload'], icon="FILE_REFRESH",
                     text="").path = Mat.name

        column.separator(type='SPACE')
        column.separator(type='LINE')
        column.separator(type='SPACE')

        row = column.row()
        row.prop(mainProp, '["Armor Toggle"]',
                 index=2, text="Leggings",
                 icon="HIDE_ON" if mainProp["Armor Toggle"][2] is False else "HIDE_OFF"
                 )
        Mat = mat_obj.material_slots[10].material.node_tree.nodes["Armor Texture"].image

        row = column.row(align=True)
        row.operator(utils.ops['image_pack'], icon="PACKAGE" if utils.is_packed(
            Mat) else "UGLYPACKAGE", text="").path = Mat.name
        row = row.row(align=True)
        row.enabled = not utils.is_packed(Mat)
        row.prop(Mat, "filepath", text="")
        row.operator(utils.ops['image_reload'], icon="FILE_REFRESH",
                     text="").path = Mat.name

        column.separator(type='SPACE')
        column.separator(type='LINE')
        column.separator(type='SPACE')

        row = column.row()
        row.prop(mainProp, '["Armor Toggle"]',
                 index=3, text="Boots",
                 icon="HIDE_ON" if mainProp["Armor Toggle"][3] is False else "HIDE_OFF"
                 )
        Mat = mat_obj.material_slots[11].material.node_tree.nodes["Armor Texture"].image

        row = column.row(align=True)
        row.operator(utils.ops['image_pack'], icon="PACKAGE" if utils.is_packed(
            Mat) else "UGLYPACKAGE", text="").path = Mat.name
        row = row.row(align=True)
        row.enabled = not utils.is_packed(Mat)
        row.prop(Mat, "filepath", text="")
        row.operator(utils.ops['image_reload'], icon="FILE_REFRESH",
                     text="").path = Mat.name


# endregion
# =============
# region Registering Start
classes = [
    SACR7_UI2_ui_global,
    SACR7_UI2_sui_head,
    SACR7_UI2_sui_face,
    SACR7_UI2_sui_torso,
    SACR7_UI2_sui_arm,
    SACR7_UI2_sui_quick_parent,
    SACR7_UI2_sui_armor,
    SACR7_UI2_sui_eyebrows,
    SACR7_UI2_sui_iris,
    SACR7_UI2_sui_sclera,
    SACR7_UI2_sui_mouth,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

# endregion
# =============

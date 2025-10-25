from .sedaiaOpsDev import is_packed
from bpy.types import Panel, Operator
import bpy
bl_info = {
    "name": "SACR R7 GUI",
    "author": "Sakura Sedaia",
    "version": (1, 3, 0),
    "blender": (4, 5, 0),
    "location": "3D View > SACR UI",
    "description": "An Addon containing control scripts for SACR R7",
    "warning": "This Addon is still heavily in development, please expect issues to be present",
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "User Interface",
}
rig = "SACR"
rig_ver = 7
category = f"{rig} R{rig_ver}"
id_prop = "sacr_id"
id_str = [
    "SACR.Rev_7",  # SACR R7.3 and Newer
    "sacr_1",  # SACR R7.2.1 and older
]
mesh_mat_obj = "MaterialEditor"

dev_mode = True

if dev_mode is True:
    op_id = "sedaia_dev_ot."
else:
    op_id = "sedaia_ot."

D = bpy.data
C = bpy.context
T = bpy.types
P = bpy.props


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

        try:
            latticeProp = armature['Show Lattices']
        except (AttributeError, KeyError, TabError):
            latticeProp = False

        if obj.data[id_prop] == id_str[0]:
            # Object Name: MaterialEditor
            i = 0
            for l in obj.children:
                i = i + 1
                # Find Material Object
                objName = l.name.split(".")[0]
                if objName == mesh_mat_obj:
                    matObj = l
                    break
            skinMat = matObj.material_slots[0].material.node_tree
            skinImgProp = skinMat.nodes["Rig Texture"].image

        # Define UI
        layout = self.layout

        row = layout.row()
        row.label(icon="PROPERTIES")
        row.prop(layers["Properties"], "is_visible",
                 text="Bone Props", toggle=True)

        layout.separator(type="LINE")

        if obj.data[id_prop] == id_str[0]:
            row = layout.row()
            row.label(text="Skin Texture")
            row = layout.row(align=True)
            row.operator(f"{op_id}imgpack", icon="PACKAGE" if is_packed(
                skinImgProp) else "UGLYPACKAGE").img_name = skinImgProp.name
            row = row.row(align=True)
            row.enabled = not is_packed(skinImgProp)
            row.prop(skinImgProp, "filepath", text="")
            row.operator(f"{op_id}imgreload", icon="FILE_REFRESH",
                         text="").img_name = skinImgProp.name

            layout.separator(type="LINE")

        row = layout.row(align=True)
        row.label(text="Rig Settings")
        row = layout.row()
        col = layout.column_flow(columns=2, align=True)
        col.prop(main, '["Wireframe Bones"]', toggle=True,
                 invert_checkbox=True, text="Solid Bones")
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

            if latticeProp is not False:
                row = layout.row()
                col = row.column()
                col.label(text="Lattice Deforms")
                col.prop(
                    main, '["Show Lattices"]', index=0, toggle=True, text="Show Lattices"
                )

            row = layout.row()
            col = row.column(heading="Presets", align=True)
            col.prop(main, '["Female Curves"]',
                     slider=True, text="Female Deform")

            layout.separator(type="LINE")

            row = layout.row()
            col = row.column(align=True, heading="Armor Toggles")
            col.prop(main, '["Armor Toggle"]', index=0,
                     toggle=True, text="Helmet")
            col.prop(main, '["Armor Toggle"]', index=1,
                     toggle=True, text="Chestplate")
            col.prop(main, '["Armor Toggle"]', index=2,
                     toggle=True, text="Leggings")
            col.prop(main, '["Armor Toggle"]', index=3,
                     toggle=True, text="Boots")


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
                return obj.data[id_prop] == id_str[0] or id_str[1]
            else:
                return False
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        # Define UI
        layout = self.layout
        row = layout.row()
        row.template_bone_collection_tree()


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
        col.prop(main, '["Arm Stretch"]', index=arm,
                 text="Stretch", slider=True)
        col.prop(main, '["Arm Wrist IK"]', index=arm,
                 text="Wrist IK", slider=True)

        arm = 1
        col = row.column(heading="Right")
        col.prop(main, '["Arm IK"]', index=arm, text="IK", slider=True)
        col.prop(main, '["Arm Stretch"]', index=arm,
                 text="Stretch", slider=True)
        col.prop(main, '["Arm Wrist IK"]', index=arm,
                 text="Wrist IK", slider=True)


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
        col.prop(main, '["Leg Stretch"]', index=leg,
                 text="Stretch", slider=True)

        leg = 1
        col = row.column(heading="Right")
        col.prop(main, '["Leg FK"]', index=leg, text="FK", slider=True)
        col.prop(main, '["Leg Stretch"]', index=leg,
                 text="Stretch", slider=True)


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

        try:
            latticeProp = obj.data['Show Lattices']
        except (AttributeError, KeyError, TabError):
            latticeProp = False

        # UI
        layout = self.layout

        row = layout.row()
        row.prop(face, '["Face | UV"]', toggle=True, text="UV projection")
        if latticeProp is not False:
            row.prop(
                main, '["Show Lattices"]', index=1, toggle=True, text="Eyelash Lattice"
            )


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

        if obj.data[id_prop] == id_str[0]:
            # Object Name: MaterialEditor
            i = 0
            for l in obj.children:
                i = i + 1
                objName = l.name.split(".")[0]
                if objName == mesh_mat_obj:
                    matObj = l
                    break

            eyebrowMat = matObj.material_slots[6].material.node_tree.nodes['Node']
            eyebrowGrad = eyebrowMat.inputs['Gradient'].default_value
            eyebrowSplit = eyebrowMat.inputs['Split Color'].default_value

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
        row.prop(eyebrows, '["Extended Controls"]',
                 index=0, text="Left", slider=False)
        row.prop(eyebrows, '["Extended Controls"]',
                 index=1, text="Right", slider=False)

        if obj.data[id_prop] == id_str[0]:
            row = layout.row()
            row.label(text='Eyebrow Colors')

            row = layout.row(align=True)

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


class SEDAIA_PT_sacr_7_suiEyes(Panel):
    bl_label = "Eyes Settings"
    bl_category = category
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "SEDAIA_PT_sacr_7_uiFace"
    bl_idname = "SEDAIA_PT_sacr_7_suiEyes"
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

        if eyes['Eyelashes'] > 0:
            lashTog = True
        else:
            lashTog = False

        # Face Material Objs
        if obj.data[id_prop] == id_str[0]:
            i = 0
            for l in obj.children:
                i = i + 1
                objName = l.name.split(".")[0]
                if objName == mesh_mat_obj:
                    matObj = l
                    break
            irisMat = matObj.material_slots[1].material.node_tree.nodes['Group.001']
            scleraMat = matObj.material_slots[2].material.node_tree.nodes['Node']
            lashMat = matObj.material_slots[7].material.node_tree.nodes['Group']
            sparkleMat = matObj.material_slots[5].material.node_tree.nodes['Emission']
            irisImgProp = matObj.material_slots[1].material.node_tree.nodes["Image Texture.001"].image

            scleraGrad = scleraMat.inputs['Gradient'].default_value
            scleraSplit = scleraMat.inputs['Heterochromia'].default_value

        # UI
        layout = self.layout
        row = layout.row()
        col = row.column(align=True)
        col.prop(eyes, '["Iris Inset"]', slider=True)
        col.prop(eyes, '["Sclera Depth"]', slider=True)

        if lite == False:
            row = col.row(align=True)
            row.prop(eyes, '["Eyelashes"]', text="Lash Style")

            if obj.data[id_prop] == id_str[0]:
                rowTog = row.row(align=True)
                rowTog.enabled = lashTog
                rowTog.prop(lashMat.inputs['Base Color'],
                            'default_value', text="")

            if sparkle == True:
                row = col.row(align=True)
                row.prop(eyes, '["Eyesparkle"]', toggle=True, text="Sparkle")

                if obj.data[id_prop] == id_str[0]:
                    rowTog = row.row(align=True)
                    rowTog.enabled = eyes['Eyesparkle']
                    rowTog.prop(sparkleMat.inputs[0], 'default_value', text="")

        layout.separator(type="LINE")

        row = layout.row()
        row.label(text="More Controls")
        row = layout.row(align=True)
        row.prop(eyes, '["Extended Controls"]',
                 index=0, text="Left", slider=False)
        row.prop(eyes, '["Extended Controls"]',
                 index=1, text="Right", slider=False)


class SEDAIA_PT_sacr_7_muiIrises(Panel):
    bl_label = "Iris Material"
    bl_category = category
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "SEDAIA_PT_sacr_7_suiEyes"
    bl_idname = "SEDAIA_PT_sacr_7_muiIris"
    bl_order = 0

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            if obj and obj.type == "ARMATURE" and obj.data:
                armature = obj.data
                return armature[id_prop] == id_str[0]
            else:
                return False
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        obj = context.active_object

        # Object Name: MaterialEditor
        i = 0
        for l in obj.children:
            i = i + 1
            objName = l.name.split(".")[0]
            if objName == mesh_mat_obj:
                matObj = l
                break

        irisMat = matObj.material_slots[1].material.node_tree.nodes['Group.001']

        # Material Settings
        irisGrad = irisMat.inputs['Gradient'].default_value
        irisSplit = irisMat.inputs['Heterochromia'].default_value

        sepaEmitCtrls = irisMat.inputs['Split Emission Controls'].default_value
        emitGrad = irisMat.inputs[16].default_value
        emitSplit = irisMat.inputs[15].default_value

        # UI
        layout = self.layout

        row = layout.row()
        row.label(text="Colors", icon="SHADING_RENDERED")

        row = layout.row(align=True)
        leftCol = row.column(align=True)
        rightCol = row.column(align=True)

        leftCol.prop(irisMat.inputs["Gradient"],
                     'default_value', text="Gradient", toggle=True)
        rightCol.prop(irisMat.inputs["Heterochromia"],
                      'default_value', text="Split", toggle=True)

        leftColRow1 = leftCol.row(align=True)
        leftColRow1.prop(irisMat.inputs["Color1.L"], 'default_value', text="")

        if irisGrad is True:
            leftColRow2 = leftCol.row(align=True)
            leftColRow2.prop(
                irisMat.inputs["Color2.L"], 'default_value', text="")
        if irisSplit is True:
            rightColRow1 = rightCol.row(align=True)
            rightColRow1.prop(
                irisMat.inputs["Color1.R"], 'default_value', text="")

            if irisGrad is True:
                rightColRow2 = rightCol.row(align=True)
                rightColRow2.prop(
                    irisMat.inputs["Color2.R"], 'default_value', text="")

        layout.separator(type="LINE")
        row = layout.row(align=True)
        row.label(text="Reflections", icon="MATERIAL_DATA")

        row = layout.row(align=True)
        irisCol = row.column(align=True)
        irisCol.prop(irisMat.inputs[7], 'default_value', text="Metalic")
        irisCol.prop(irisMat.inputs[6], 'default_value', text="IOR")
        irisCol.prop(irisMat.inputs[8], 'default_value', text="Specular")
        irisCol.prop(irisMat.inputs[9], 'default_value', text="Roughness")

        layout.separator(type="LINE")

        row = layout.row()
        row.label(text="Emission", icon="OUTLINER_OB_LIGHT")
        row = layout.row(align=True)
        col = row.column(align=True)
        col.prop(irisMat.inputs['Emission Mask'],
                 'default_value', text="Toggle")
        col.prop(irisMat.inputs['Split Emission Controls'],
                 'default_value', text="Split Controls", toggle=True)
        if sepaEmitCtrls is True:
            colRow = col.row(align=True)
            colRow.prop(irisMat.inputs[15], 'default_value',
                        text="Heterochromia", toggle=True)
            colRow.prop(
                irisMat.inputs[16], 'default_value', text="Gradient", toggle=True)
        row = layout.row(align=True)
        if sepaEmitCtrls is False:
            col = row.column(align=True)
            col.prop(irisMat.inputs['LT'],
                     'default_value', text="Emission Strength")
        else:
            col = row.column(align=True, heading="Left")
            col.prop(irisMat.inputs['LT'], 'default_value', text="L Top")
            if emitGrad is True:
                col.prop(irisMat.inputs['LB'],
                         'default_value', text="L Bottom")
            if emitSplit is True:
                col = row.column(align=True, heading="Right")
                col.prop(irisMat.inputs['RT'], 'default_value', text="R Top")
                if emitGrad is True:
                    col.prop(irisMat.inputs['RB'],
                             'default_value', text="R Bottom")


class SEDAIA_PT_sacr_7_muiPupil(Panel):
    bl_label = "Pupil Material"
    bl_category = category
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "SEDAIA_PT_sacr_7_suiEyes"
    bl_order = 1

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            if obj and obj.type == "ARMATURE" and obj.data:
                armature = obj.data
                return armature[id_prop] == id_str[0]
            else:
                return False
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        obj = context.active_object
        i = 0
        for l in obj.children:
            i = i + 1
            objName = l.name.split(".")[0]
            if objName == mesh_mat_obj:
                matObj = l
                break

        irisMat = matObj.material_slots[1].material.node_tree.nodes['Group.001']
        irisImgProp = matObj.material_slots[1].material.node_tree.nodes["Image Texture.001"].image

        # UI
        layout = self.layout

        row = layout.row()
        row.label(text="Colors", icon="SHADING_RENDERED")

        row = layout.row(align=True)
        row.prop(irisMat.inputs['Pupil Toggle'],
                 'default_value', text="Opacity", slider=True)
        row.prop(irisMat.inputs['Color'], 'default_value', text='')

        row = layout.row(align=True)
        col = row.column(align=True)
        col.label(text="Pupil Scale")
        row = col.row(align=True)
        row.prop(irisMat.inputs['Scale1'],
                 'default_value', text='X', slider=True)
        row.prop(irisMat.inputs['Scale2'],
                 'default_value', text='Y', slider=True)

        layout.separator(type="LINE")
        row = layout.row(align=True)
        row.label(text="Reflections", icon="MATERIAL_DATA")

        row = layout.row(align=True)
        irisCol = row.column(align=True)
        irisCol.prop(irisMat.inputs[27], 'default_value', text="Metalic")
        irisCol.prop(irisMat.inputs[28], 'default_value', text="Specular")
        irisCol.prop(irisMat.inputs[29], 'default_value', text="Roughness")

        layout.separator(type="LINE")

        row = layout.row()
        row.label(text="Emission", icon="OUTLINER_OB_LIGHT")
        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.prop(irisMat.inputs['Emission Mask'],
                 'default_value', text="Toggle")
        row1 = row.row(align=True)
        row1.enabled = irisMat.inputs['Emission Mask'].default_value > 0
        row1.prop(irisMat.inputs['Strength'], 'default_value', text="Strength")
        row = col.row(align=True)
        row.enabled = irisMat.inputs['Emission Mask'].default_value > 0
        row.prop(irisMat.inputs['Emit_Color'], 'default_value', text="")


class SEDAIA_PT_sacr_7_muiSclera(Panel):
    bl_label = "Sclera Material"
    bl_category = category
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "SEDAIA_PT_sacr_7_suiEyes"
    bl_order = 2

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            if obj and obj.type == "ARMATURE" and obj.data:
                armature = obj.data
                return armature[id_prop] == id_str[0]
            else:
                return False
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        obj = context.active_object

        # Object Name: MaterialEditor
        i = 0
        for l in obj.children:
            i = i + 1
            objName = l.name.split(".")[0]
            if objName == mesh_mat_obj:
                matObj = l
                break

        scleraMat = matObj.material_slots[2].material.node_tree.nodes['Node']

        # Material Settings
        scleraGrad = scleraMat.inputs['Gradient'].default_value
        scleraSplit = scleraMat.inputs['Heterochromia'].default_value

        sepaEmitCtrls = scleraMat.inputs['Split Emission Controls'].default_value
        emitGrad = scleraMat.inputs[16].default_value
        emitSplit = scleraMat.inputs[15].default_value

        # UI
        layout = self.layout

        row = layout.row()
        row.label(text="Colors", icon="SHADING_RENDERED")

        row = layout.row(align=True)
        leftCol = row.column(align=True)
        rightCol = row.column(align=True)

        leftCol.prop(scleraMat.inputs["Gradient"],
                     'default_value', text="Gradient", toggle=True)
        rightCol.prop(scleraMat.inputs["Heterochromia"],
                      'default_value', text="Split", toggle=True)

        leftColRow1 = leftCol.row(align=True)
        leftColRow1.prop(
            scleraMat.inputs["Color1.L"], 'default_value', text="")

        if scleraGrad is True:
            leftColRow2 = leftCol.row(align=True)
            leftColRow2.prop(
                scleraMat.inputs["Color2.L"], 'default_value', text="")
        if scleraSplit is True:
            rightColRow1 = rightCol.row(align=True)
            rightColRow1.prop(
                scleraMat.inputs["Color1.R"], 'default_value', text="")

            if scleraGrad is True:
                rightColRow2 = rightCol.row(align=True)
                rightColRow2.prop(
                    scleraMat.inputs["Color2.R"], 'default_value', text="")

        layout.separator(type="LINE")
        row = layout.row(align=True)
        row.label(text="Reflections", icon="MATERIAL_DATA")

        row = layout.row(align=True)
        irisCol = row.column(align=True)
        irisCol.prop(scleraMat.inputs['Metalic'],
                     'default_value', text="Metalic")
        irisCol.prop(scleraMat.inputs['IOR'], 'default_value', text="IOR")
        irisCol.prop(scleraMat.inputs['Specular'],
                     'default_value', text="Specular")
        irisCol.prop(scleraMat.inputs['Roughness'],
                     'default_value', text="Roughness")

        layout.separator(type="LINE")

        row = layout.row()
        row.label(text="Emission", icon="OUTLINER_OB_LIGHT")
        row = layout.row(align=True)
        col = row.column(align=True)
        col.prop(scleraMat.inputs['Emission Mask'],
                 'default_value', text="Toggle")
        col.prop(scleraMat.inputs['Split Emission Controls'],
                 'default_value', text="Split Controls", toggle=True)
        if sepaEmitCtrls is True:
            colRow = col.row(align=True)
            colRow.prop(
                scleraMat.inputs[15], 'default_value', text="Heterochromia", toggle=True)
            colRow.prop(
                scleraMat.inputs[16], 'default_value', text="Gradient", toggle=True)
        row = layout.row(align=True)
        if sepaEmitCtrls is False:
            col = row.column(align=True)
            col.prop(scleraMat.inputs['LT'],
                     'default_value', text="Emission Strength")
        else:
            col = row.column(align=True, heading="Left")
            col.prop(scleraMat.inputs['LT'], 'default_value', text="L Top")
            if emitGrad is True:
                col.prop(scleraMat.inputs['LB'],
                         'default_value', text="L Bottom")
            if emitSplit is True:
                col = row.column(align=True, heading="Right")
                col.prop(scleraMat.inputs['RT'], 'default_value', text="R Top")
                if emitGrad is True:
                    col.prop(scleraMat.inputs['RB'],
                             'default_value', text="R Bottom")


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

        if obj.data[id_prop] == id_str[0]:
            # Object Name: MaterialEditor
            i = 0
            for l in obj.children:
                i = i + 1
                objName = l.name.split(".")[0]
                if objName == mesh_mat_obj:
                    matObj = l
                    break

            backMat = matObj.material_slots[3].material.node_tree.nodes["Group.001"]
            teethMat = matObj.material_slots[4].material.node_tree.nodes["Group"]

        # UI
        layout = self.layout
        row = layout.row()
        col = row.column(align=True)
        col.prop(mouth, '["Square Mouth"]', slider=True, text="Square")
        col.prop(mouth, '["Extended Controls"]', text="Extra Controls")

        if obj.data[id_prop] == id_str[0]:
            col.prop(backMat.inputs['Base Color'],
                     "default_value", text="Inside Color")
            col.prop(teethMat.inputs['Base Color'],
                     "default_value", text="Teeth Color")

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

            col.prop(mouth, '["Molar Height (R -> L)"]',
                     index=3, slider=True, text=top)
            col.prop(
                mouth, '["Molar Height (R -> L)"]', index=2, slider=True, text=bottom
            )

            col = row.column(align=True)
            col.label(text="Right Height")
            col.prop(mouth, '["Molar Height (R -> L)"]',
                     index=0, slider=True, text=top)
            col.prop(
                mouth, '["Molar Height (R -> L)"]', index=1, slider=True, text=bottom
            )

            row = layout.row()
            col = row.column(align=True)
            col.label(text="Left Width")
            col.prop(mouth, '["Molar Width (R -> L)"]',
                     index=3, slider=True, text=top)
            col.prop(
                mouth, '["Molar Width (R -> L)"]', index=2, slider=True, text=bottom
            )

            col = row.column(align=True)
            col.label(text="Right Width")
            col.prop(mouth, '["Molar Width (R -> L)"]',
                     index=0, slider=True, text=top)
            col.prop(
                mouth, '["Molar Width (R -> L)"]', index=1, slider=True, text=bottom
            )


classes = [
    SEDAIA_PT_sacr_7_uiGlobal,
    SEDAIA_PT_sacr_7_uiFace,
    SEDAIA_PT_sacr_7_suiArms,
    SEDAIA_PT_sacr_7_suiLegs,
    SEDAIA_PT_sacr_7_suiEyebrows,
    SEDAIA_PT_sacr_7_suiEyes,
    SEDAIA_PT_sacr_7_suiMouth
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

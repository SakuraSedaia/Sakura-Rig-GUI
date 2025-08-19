import bpy
from mathutils import *
from bpy.types import Panel
from easybpy import *

D = bpy.data
C = bpy.context
T = bpy.types
P = bpy.props

rig_name = "SAR"
rig_version = 1

rig_id_prop = "rig_id"
rig_id = rig_name + " R" + str(rig_version)


# region Main
class SEDAIA_PT_sar_ui(Panel):
    bl_idname = "SEDAIA_PT_sar_ui"
    bl_label = "Mode Selector"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = rig_id

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            if obj and obj.type == "ARMATURE" and obj.data:
                armature = obj.data
                return armature[rig_id_prop] == rig_id
            else:
                return False
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        obj = context.active_object
        armature = obj.data
        scene = context.scene
        bone = obj.pose.bones

        layout = self.layout

        row = layout.row()
        row.alert = True
        row.box().label(text="UI Currently in development", icon="ERROR")
        row.alert = False
        row = layout.row()
        box = row.box()
        col = box.column()
        col.label(text=rig_id, icon="ARMATURE_DATA")
        col.label(text="Released: TBD")


# endregion
# region Head
class SEDAIA_PT_uihead(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = rig_id
    bl_label = "Head"
    bl_idname = "SEDAIA_PT_uihead"

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            armature = obj.data
            if obj and obj.type == "ARMATURE" and obj.data:
                return armature[rig_id_prop] == rig_id
            else:
                return False
        except:
            return False

    def draw(self, context):
        obj = context.active_object
        armature = obj.data

        bone = obj.pose.bones
        head = bone["DEF_HEAD"]

        layout = self.layout

        row = layout.row()
        row.label(text="Features")
        
        row = layout.row()
        col = row.column_flow(columns=2, align=True)
        col.prop(head, '["face"]', text="Face", toggle=True)
        col.prop(head, '["neck"]', text="Neck", toggle=True)


# endregion
# region Face


class SEDAIA_PT_uiface(Panel):
    bl_label = "Face"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = rig_id
    bl_parent_id = "SEDAIA_PT_uihead"

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            armature = obj.data
            is_on = obj.pose.bones["DEF_HEAD"]["face"]

            if is_on == True:
                if obj and obj.type == "ARMATURE" and obj.data:
                    return armature[rig_id_prop] == rig_id
                else:
                    return False
            else:
                return False
        except:
            return False

    def draw(self, context):
        layout = self.layout
        layout.label(text="Face Properties")


# endregion
# region Body
class SEDAIA_PT_uitorso(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = rig_id
    bl_label = "Body"
    bl_idname = "SEDAIA_PT_uitorso"

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            armature = obj.data
            if obj and obj.type == "ARMATURE" and obj.data:
                return armature[rig_id_prop] == rig_id
            else:
                return False
        except:
            return False

    def draw(self, context):
        obj = context.active_object
        armature = obj.data

        bone = obj.pose.bones

        layout = self.layout

        layout.box().label(text="Limb Settings")


class SEDAIA_PT_uiarms(Panel):
    bl_label = "Arms"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = rig_id
    bl_parent_id = "SEDAIA_PT_uitorso"

    def draw(self, context):
        obj = context.active_object
        armature = obj.data

        bone = obj.pose.bones

        layout = self.layout

        layout.box().label(text="Arm Settings")


class SEDAIA_PT_uilegs(Panel):
    bl_label = "Legs"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = rig_id
    bl_parent_id = "SEDAIA_PT_uitorso"

    def draw(self, context):
        obj = context.active_object
        armature = obj.data

        bone = obj.pose.bones

        layout = self.layout

        layout.box().label(text="Leg Settings")


# endregion

# region Definitions


# endregion

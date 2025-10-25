import bpy
from bpy.types import Panel, Operator


class SEDAIA_DEV_PT_ui_RigImporter(Panel):
    bl_label = "Rig Manager"
    bl_category = "Sakura Rigs"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.label(text="Append SACR R7.3")
        row = box.row()
        row.operator("sedaia_ot.append_sacr_7_3_0", text="Base")
        row.operator("sedaia_ot.append_sacr_7_3_0", text="Lite").lite = True


classes = [
    SEDAIA_DEV_PT_ui_RigImporter
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

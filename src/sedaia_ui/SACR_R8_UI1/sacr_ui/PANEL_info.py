from ..class_common import *
import bpy.types as T
import bpy.props as P
import bpy.utils as U

class R8_UI1_PT_info(SacrPanel, T.Panel):
    bl_idname = panels['info']
    bl_label = "Info"

    def draw_header(self, context):
        self.layout.label(text="", icon="HELP")

    def draw(self, context):
        layout = self.layout
        layout.alert = IN_DEVELOPMENT
        row = layout.row()
        row.alignment = 'CENTER'
        row.label(text=rig_info['rig']['name'])
        row = layout.row()
        row.scale_y = 1.5
        row.ui_units_x = 4
        row.label(text=f"Version: ")

        box = row.box()
        box.scale_y = .75
        box.label(text=f"{rig_info['rig']['alias']} R{rig_info['rig']['version']}")

        if IN_DEVELOPMENT:
            row = layout.row()
            box = row.box()
            box.alert = True
            box.label(text="DEVELOPMENT BUILD", icon="ERROR")

def register():
    U.register_class(R8_UI1_PT_info)
    
def unregister():
    U.unregister_class(R8_UI1_PT_info)
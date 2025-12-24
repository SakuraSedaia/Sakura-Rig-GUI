from ..class_common import *
import bpy.types as T
import bpy.props as P
import bpy.utils as U
import bpy.ops as O
from ....utils import util_global

# Import Layouts
from .LAYOUT_rig_config import *
from .LAYOUT_visual_config import *
from .LAYOUT_material_config import *


class R8_UI1_PT_config(SacrPanel, T.Panel):
    bl_idname = panels['config']
    bl_label = "Rig Config"

    def draw_header(self, context):
        self.layout.label(text="", icon="PREFERENCES")

    def draw(self, context):
        # Variables and Data
        obj = context.active_object
        obj_col = obj.users_collection[0]
        obj_data = obj.data
        rig_bones = obj.pose.bones
        rig_bc = obj_data.collections_all
        rig_pose = obj.pose
        obj_child = obj.children_recursive

        # Properties
        rig_name = obj_data.RigName
        mesh_col = obj_data['MeshCol']
        lite = obj_data['SACR_lite']

        # Property Bones
        main_prop = rig_bones[self.config_objs['main']]
        head_prop = rig_bones[self.config_objs['head']]
        leg_prop = rig_bones[self.config_objs['legs']]

        # UI
        ui = self.layout

        row = ui.row()
        box = row.box()
        box.label(text="Rig Name:")
        box.prop(obj_data, 'RigName', text="")

        # Basic Rig Settings
        row = ui.row()
        box = row.box()
        b_row = box.row()
        b_row.label(text="Basic Settings")
        col = box.column_flow(columns=2, align=True)
        col.prop(rig_pose, "use_mirror_x",
                 icon="MOD_MIRROR", text="Mirror X-Axis")
        col.prop(rig_bc['Properties Legacy'], 'is_visible',
                 toggle=True, text="Debug Props",
                 icon="HIDE_ON" if rig_bc['Properties Legacy'].is_visible is False else "HIDE_OFF")

        col.prop(mesh_col, 'hide_select',
                 text="Restrict Selection")

        if not lite:
            col.prop(main_prop, '["ShowLattices"]',
                     index=0,
                     text="Body Lattices",
                     icon="HIDE_ON" if main_prop["ShowLattices"][0] is False else "HIDE_OFF")

        # Layout Changer
        row = ui.row()
        row.scale_y = 2
        row.prop(obj_data, 'PanelMode' or '["PanelMode"]', expand=True)
        ui.separator(type="SPACE")
        panel_mode = obj_data.PanelMode
        if str(panel_mode) == "0":
            LAYOUT_rig_config(self, context)
        elif str(panel_mode) == "1":
            LAYOUT_visual_config(self, context)
        elif str(panel_mode) == "2":
            LAYOUT_material_config(self, context)





def register():
    U.register_class(R8_UI1_PT_config)

def unregister():
    U.unregister_class(R8_UI1_PT_config)
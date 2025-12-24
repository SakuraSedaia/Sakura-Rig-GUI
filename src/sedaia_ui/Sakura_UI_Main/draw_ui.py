import bpy
from ...utils.util_global import *
from ...prefs import get_prefs
import bpy
import bpy.types as T
import bpy.props as P
import bpy.utils as U

from pathlib import Path
import os

T.Scene.PlayerExists = P.BoolProperty(name="Player Exists", default=False)

def update_user(self, context):
    data = get_prefs().player_dir
    username = self.Username
    player_data = Path(f"{data}/{username}/{username}_Data.json").absolute()
    bpy.context.scene.PlayerExists = Path(player_data).exists()

T.Scene.Username = P.StringProperty(name="Username", default="Steve", update=update_user)
T.Scene.SyncArms = P.BoolProperty(name="Sync Arms", default=False)
T.Scene.SyncCape = P.BoolProperty(name="Sync Cape", default=False)
T.Scene.SyncName = P.BoolProperty(name="Sync Name", default=False)

class PanelSetting:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Sedaia UI"

class SEDAIA_PT_info(T.Panel, PanelSetting):
    bl_label = "Info"
    bl_idname = "SEDAIA_PT_info"

    def draw_header(self, context):
        self.layout.label(icon="HELP", text="")

    def draw(self, context):
        self.layout.label(text="Sakura UI Info")

# Skin Changer

class SEDAIA_PT_skin_changer(T.Panel, PanelSetting):
    bl_label = "Skin Changer"
    bl_idname = "SEDAIA_PT_skin_changer"

    def draw_header(self, context):
        self.layout.label(text="", icon="TEXTURE_DATA")

    def draw(self, context):
        scene = context.scene

        ui = self.layout

        ui.label(text="Sakura UI")

        box = ui.box()
        col = box.column(heading="Username:")

        col.prop(scene, 'Username', text='')

        if scene.PlayerExists:
            row = col.row()
            row.operator(ops['change_skin'], text="Change", icon="AREA_SWAP")
            row.operator(ops['update_skin'], text="Update", icon="FILE_REFRESH")
        else:
            row = col.row()
            row.operator(ops['download_skin'], text="Download", icon="IMPORT")

        col.operator(ops['file_open'], icon="FILEBROWSER").path = get_prefs().player_dir

        if get_prefs().debug:
            row = box.row()
            row.label(text=f"Player Exists: {scene.PlayerExists}")

classes = [
    SEDAIA_PT_info,
    SEDAIA_PT_skin_changer,
]

def register():
    for cls in classes:
        U.register_class(cls)

def unregister():
    for cls in reversed(classes):
        U.unregister_class(cls)
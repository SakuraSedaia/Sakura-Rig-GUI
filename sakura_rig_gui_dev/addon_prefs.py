import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty, IntProperty, EnumProperty, BoolProperty


class SEDAIA_DEV_PF_addon_prefs(AddonPreferences):
    bl_idname = __package__

    debug: BoolProperty(
        name='Debug',
        default=True
    )  # type: ignore
    prompt_to_refresh_player_data: BoolProperty(
        name="Prompt to Regen Player Data",
        default=True
    )  # type: ignore

    def draw(self, context):
        pref = self.layout
        pref.operator("sedaia_ot.open_directory", icon="FILEBROWSER")
        # pref.prop(self, 'debug')
        pref.prop(self, 'prompt_to_refresh_player_data')


def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(__package__)
    return getattr(addon, "preferences", None)


classes = [SEDAIA_DEV_PF_addon_prefs]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

from importlib import reload


from .sacr_ui import PANEL_info

from .sacr_ui import PANEL_rig_config


modules = [PANEL_info, PANEL_rig_config]

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in reversed(modules):
        mod.unregister()
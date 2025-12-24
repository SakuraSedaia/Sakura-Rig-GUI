from .. import prefs
from bpy.utils import extension_path_user
from importlib import reload
import bpy
from . import util_global

C = bpy.context
D = bpy.data
pref_access = prefs.get_prefs

if "files" in locals():
    reload(files)
else:
    from .modules import files

if "images" in locals():
    reload(images)
else:
    from .modules import images

if "rigs" in locals():
    reload(rigs)
else:
    from .modules import rigs

if "skins" in locals():
    reload(skins)
else:
    from .modules import skins


modules = [
    files,
    images,
    rigs,
    skins
]

def register():
    for mod in modules:
        mod.register()



def unregister():
    for mod in reversed(modules):
        mod.unregister()

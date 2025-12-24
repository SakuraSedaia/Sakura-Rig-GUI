from importlib import reload, import_module
import pkgutil
from pathlib import Path

# Core UI
if "prefs" in locals():
    reload(prefs)
else:
    from . import prefs

if "Sakura_UI_Main" in locals():
    reload(Sakura_UI_Main)
else:
    from .sedaia_ui import Sakura_UI_Main

# Utilities
if "utils" in locals():
    reload(utils)
else:
    from . import utils
# endregion


# Import SACR Rigs
if "SACR_R7_UI1" in locals():
    reload(SACR_R7_UI1)
else:
    from .sedaia_ui import SACR_R7_UI1

if "SACR_R7_UI2" in locals():
    reload(SACR_R7_UI2)
else:
    from .sedaia_ui import SACR_R7_UI2

if "SACR_R8_UI1" in locals():
    reload(SACR_R8_UI1)
else:
    from .sedaia_ui import SACR_R8_UI1

# Auto-Import Rig UIs


def get_all_submodules(directory):
    return list(iter_submodules(directory, __package__))


def iter_submodules(path, package_name):
    for name in sorted(iter_submodule_names(path)):
        yield import_module(f".{name}", package_name)


def iter_submodule_names(path, root="rig_ui."):
    for _, module_name, is_package in pkgutil.iter_modules([str(path)]):
        if is_package:
            sub_path = f"{root}/{module_name}."
            sub_root = f"{root}.{module_name}."
            yield from iter_submodule_names(sub_path, sub_root)
        else:
            yield root + module_name


# endregion
# region Registering
modules = (
    # Core UI
    prefs,
    Sakura_UI_Main,

    # Utilities
    utils,

    # SACR GUI's
    SACR_R7_UI1,
    SACR_R7_UI2,
    SACR_R8_UI1
)

rig_modules = get_all_submodules(f"{Path(__file__).parent}/rig_ui/")


def register():
    for mod in modules:
        mod.register()

    for rMod in rig_modules:
        if hasattr(rMod, "register"):
            rMod.register()


def unregister():
    for mod in reversed(modules):
        mod.unregister()

    for rMod in reversed(rig_modules):
        if hasattr(rMod, "unregister"):
            rMod.unregister()


if __name__ == "__main__":
    register()

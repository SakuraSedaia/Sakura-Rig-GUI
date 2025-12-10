from importlib import reload, import_module
import pkgutil
from pathlib import Path

# =============
# Core UI
# =============
if "prefs" in locals():
    reload(prefs)
else:
    from . import prefs

if "ulobal_ui" in locals():
    reload(global_ui)
else:
    from . import global_ui


# =============
# Utilities
# =============
if "sedaia_utils" in locals():
    reload(sedaia_utils)
else:
    from .utils import sedaia_utils

# =============
# Auto-Import Rig UIs
# =============


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


modules = (
    # Core UI
    prefs,
    global_ui,

    # Utilities
    sedaia_utils,
)
rig_modules = get_all_submodules(f"{Path(__file__).parent}/rig_ui/")


def register():
    for mod in modules:
        if hasattr(mod, "register"):
            mod.register()

    for rMod in rig_modules:
        if hasattr(rMod, "register"):
            rMod.register()


def unregister():
    for mod in reversed(modules):
        if hasattr(mod, "unregister"):
            mod.unregister()

    for rMod in reversed(rig_modules):
        if hasattr(rMod, "unregister"):
            rMod.unregister()


if __name__ == "__main__":
    register()

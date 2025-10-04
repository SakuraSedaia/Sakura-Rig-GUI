bl_info = {
    "name": "SACR R7 GUI",
    "author": "Sakura Sedaia",
    "version": (1, 2, 0),
    "blender": (4, 5, 0),
    "location": "3D View > SACR UI",
    "description": "An Addon containing control scripts for SACR R7",
    "warning": "This Addon is still heavily in development, please expect issues to be present",
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "User Interface",
}


from . import (sedaia_operators, sacr_r7_0_gui, sacr_r8_0_gui)

modules = [sedaia_operators, sacr_r7_0_gui, sacr_r8_0_gui]


def register():
    for mod in modules:
        mod.register()


def unregister():
    for mod in modules:
        mod.unregister()


if __name__ == "__main__":
    register()

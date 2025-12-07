# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# =============
# region Manifest
module_info = {  # Just a manifest containing details which can be referenced by other modules
    "author": "Your Name",
    "author_id": "Nickname",

    "name": "Your Rig UI",
    "id": "YR_GUI",
    "version": (1, 0, 0),
    "description": "",
    "type": "interface",  # Options: util, interface

    "blender": (5, 0, 0),

    "warning": "",
    "doc_url": "",
    "tracker_url": "",
}

rig_info = {
    "name": "",  # The full Name of your rig
    "id": "",  # Set to your Rig's Acronym or Nickname, should be a single word, no punctuation or spaces
    "version": (1, 0, 0),
}

# endregion
# =============
# region Imports
import bpy
from bpy.types import (
    Panel,
    Operator,
    Menu,
    PoseBone,
    Armature,
)

from bpy.props import (
    StringProperty,
    IntProperty,
    BoolProperty,
    EnumProperty,
    RemoveProperty,
    PointerProperty
)

from bpy.utils import (
    extension_path_user
)

# Util Import
from ..utils import sedaia_utils
from .. import prefs


# Common BPY calls
T = bpy.types
P = bpy.props
O = bpy.ops
C = bpy.context
D = bpy.data


# endregion
# =============
# region Addon Metadata (DO NOT MODIFY THIS AREA)
bl_info = {
    "name": module_info["name"],
    "author": module_info["author"],
    "version": module_info['version'],
    "blender": module_info["blender"],
    "location": "",
    "description": module_info["description"],
    "warning": "",
    "doc_url": module_info["doc_url"],
    "tracker_url": module_info["tracker_url"],
    "category": "Interface",
}

# endregion
# =============
# region Rig Settings
config = {
    # Required Properties
    # =============
    "tab": f"{rig_info['id']} R{rig_info['version'][0]}",
    "id": "",  # ID the Addon references to know when to draw your interface
    "idProp": "",  # this ID set in the Armature Properties

    # =============
    # Your Properties
    # =============
    "your_setting": "Value",
}

config_objs = {
    "main": "Rig_Properties",
    "face": "Face_Properties",
    "materials": "MaterialEditor"
}


# endregion
# =============
# region Object IDs
panel_prefix = f"YOURNAME_RIG1_UI1_PT"
panel = {
    "global": f"{panel_prefix}_global",
    "head": f"{panel_prefix}_sui_head",
}


# endregion
# =============
# region Custom Properties
PoseBone.enum_property_1 = EnumProperty(
    name="Enumerator on a Bone",
    items={
        ("0", "Item 1", "Description"),
        ("1", "Item 2", "Description"),
    }
)
Armature.string_property_1 = StringProperty(
    default="String Property on the Armature"
)


# endregion
# =============
# region Class Start
class RIG1_UI1_ui_global(Panel):
    bl_label = "Properties"
    bl_idname = panel['global']
    bl_category = config["tab"]
    bl_order = 0

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        try:
            r = context.active_object
            if r and r.type == "ARMATURE" and r.data:
                return r.data[config["idProp"]] == config["id"]
            else:
                return False
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):

        # Rig Data
        rig = context.active_object
        rig_data = rig.data
        rig_bones = rig.pose.bones
        rig_bc = rig_data.collections_all

        # set Child Object Indices
        i = 0
        for l in rig.children_recursive:
            i = i + 1
            # Find Material Object
            objName = l.name.split(".")[0]
            if objName == config_objs['materials']:
                mat_obj = l
                break

        skin = mat_obj.material_slots[0].material.node_tree
        skinTex = skin.nodes["Skin Texture"].image
        root = rig_bones[config_objs["root_bone"]]

        panel = self.layout

        row = panel.row()
        row.label(text="Utilities")

        row = panel.row(align=True)
        row.prop(rig_data, '["Rig Name"]', text="Rig Name")

        rename = row.operator(sedaia_utils.ops["rig_rename"], icon="FILE_REFRESH", text="")
        rename.name = rig_data['Rig Name']
        rename.update_collection = True

        row = panel.row()
        row.label(text="Skin Texture")
        row = panel.row(align=True)
        row.operator(sedaia_utils.ops['image_pack'], icon="PACKAGE" if sedaia_utils.is_packed(
            skinTex) else "UGLYPACKAGE", text="").path = skinTex.name
        row = row.row(align=True)
        row.enabled = not sedaia_utils.is_packed(skinTex)
        row.prop(skinTex, "filepath", text="")
        row.operator(sedaia_utils.ops['image_reload'], icon="FILE_REFRESH",
                     text="").path = skinTex.name

        row = panel.row()
        col = row.column_flow(columns=2, align=True)
        col.prop(rig.pose, "use_mirror_x", toggle=True)

        panel.separator(type="LINE")


# endregion
# =============
# region Head Settings
class RIG1_UI1_sui_head(Panel):
    bl_parent_id = panel['global']
    bl_idname = panel['head']
    bl_label = "Head"
    bl_order = 0

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        # Variables and Data
        rig = context.active_object
        rig_data = rig.data
        rig_bones = rig.pose.bones
        rig_bc = rig_data.collections_all

        mainProp = rig_bones[config_objs['main']]

        # UI Layout
        panel = self.layout

        panel.label("Template Panel")


# endregion
# =============
# region Registering Start
classes = [
    RIG1_UI1_ui_global,
    RIG1_UI1_sui_head,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

# endregion
# =============

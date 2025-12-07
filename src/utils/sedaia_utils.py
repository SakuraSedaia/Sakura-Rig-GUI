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
# region Addon Manifest
module_info = {
    "author": "Sakura Sedaia",
    "author_id": "SEDAIA",

    "name": "Sedaia Utilities",
    'id': "sedaia_utils",
    "version": (1, 0, 0),
    "description": "A collection of Operators",

    "blender": (5, 0, 0),

    "warning": "",
    "doc_url": "",
    "tracker_url": "",
}

# endregion
# =============
# region Imports and Common Variables

# BPY Imports
import bpy
from bpy.types import (
    Menu,
    Operator,
    Panel,
    PoseBone,
    Bone,
    BoneCollection
)
from bpy.props import (BoolProperty, StringProperty, IntProperty)
from bpy.utils import (extension_path_user, register_class, unregister_class)

import bpy.types as T
import bpy.props as P
import bpy.ops as O


from bpy.ops import wm

# Sedaia Modules
from .. import prefs

# Python Modules
from pathlib import Path
from shutil import rmtree
import json
from base64 import b64decode
from urllib import request, error

# Common BPY calls
C = bpy.context
D = bpy.data
pref_access = prefs.get_prefs

# endregion
# =============
# region Module Metadata (DO NOT MODIFY THIS SECTION)
bl_info = {
    "name": module_info["name"],
    "author": module_info["author"],
    "version": module_info["version"],
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
# region Module Settings

# TODO: This needs to reference directly off of Preferences, once I figure
# out how to actually get varables to read from Preferences.
config: dict = {
    "file_path": extension_path_user(prefs.module_info["name"], create=True, path=""),
    "player_path": extension_path_user(prefs.module_info["name"], create=True, path="playerdata"),
    "utility_bone_name": "Sedaia.Skin_Utility_Config",

    # Skin Configs
    # TODO: This needs to reference directly off of Preferences, once I figure
    # out how to actually get varables to read from Preferences.
    "skin_file_path": extension_path_user(prefs.module_info["name"], create=True, path="playerdata"),
    "skin_utility_bone": "Sedaia.Skin_Utility_Config",
    "skin_links": {
        "api": "https://api.mojang.com/users/profiles/minecraft/",
        "profile": "https://sessionserver.mojang.com/session/minecraft/profile/",
        "textures": "http://textures.minecraft.net/texture/",
    }
}
# endregion
# =============
# region Object IDs
op_id: str = "sedaia_util_ot"
ops: dict = {
    # File Operations
    "file_open": f"{op_id}.file_open",
    "file_delete": f"{op_id}.file_delete",

    # Image Operations
    "image_pack": f"{op_id}.image_pack",
    "image_reload": f"{op_id}.image_reload",

    # Rig Operations
    "rig_rename": f"{op_id}.rig_rename",

    # Skin Operations
    "skin_router": f"{op_id}.skin_router",
    "skin_get": f"{op_id}.skin_get",
    "skin_add": f"{op_id}.skin_add",
    "skin_load": f"{op_id}.skin_load",
    "skin_purge": f"{op_id}.skin_purge",

}

menu_id: str = "SEDAIA_UTIL_MT"
menus: dict = {
    "skin_regen": f"{menu_id}_skin_regen",
    "skin_purge": f"{menu_id}_skin_purge",
}
# endregion
# =============
# region Utility Functions (def)


def allow_online():
    return bpy.app.online_access


def file_exists(path):
    return Path(path).exists()


def is_packed(file):
    try:
        return file.packed_files.values() != []
    except:
        return False


# endregion
# =============
# region HTTP Operations (def)
def download(url, path):
    request.urlretrieve(url, path)


def retrieveJSON(url):
    try:
        error.URLError
        return json.loads(request.urlopen(url).read())
    except (request.HTTPError, error.URLError):
        return "http_error"


# endregion
# =============
# region File Ops Classes
class FILE_open(Operator):
    bl_label = "Open"
    bl_idname = ops['file_open']

    path: StringProperty(default=config["file_path"])  # type: ignore

    def execute(self, context):
        wm.path_open(filepath=self.path)
        return {"FINISHED"}


# TODO: This absolutely needs to have a confirmation prompt before full implementation
class FILE_delete(Operator):
    bl_idname = ops['file_delete']

    path: StringProperty()  # type: ignore

    def execute(self, context):
        self.report({"ERROR"}, "Operator not yet finished")
        return {"FINISHED"}


# endregion
# =============
# region Image Functions (def)
def pack_img(name):
    image = get_img(name)
    if is_packed(image):
        if bpy.data.is_saved:
            image.unpack()
        else:
            image.unpack(method="USE_LOCAL")
    else:
        image.pack()


def get_img(path):
    return bpy.data.images[path]


def reload_img(name):
    get_img(name).reload()


# endregion
# =============
# region Image Classes
class IMAGE_pack(Operator):
    bl_label = ""
    bl_idname = ops['image_pack']

    path: StringProperty()  # type: ignore

    def execute(self, context):
        pack_img(self.path)
        return {"FINISHED"}


class IMAGE_reload(Operator):
    bl_label = ""
    bl_idname = ops['image_reload']

    path: StringProperty()  # type: ignore

    def execute(self, context):
        reload_img(self.path)
        return {"FINISHED"}
# endregion
# =============
# region Rig Functions (def)


# endregion
# =============
# region Rig Classes
class RIGS_set_name(Operator):
    bl_idname = ops['rig_rename']
    bl_label = "Set Rig Name"

    name: StringProperty()  # type: ignore
    update_collection: BoolProperty()  # type: ignore

    def execute(self, context):
        context.active_object.name = self.name
        context.active_object.data.name = self.name

        if self.update_collection is True:
            try:
                context.collection.name = self.name
            except (AttributeError, KeyError):
                context.asset.name = self.name

        return {"FINISHED"}


# endregion
# =============
# region Skin Utility Functions (def)
def loadPlayer(Name):
    try:
        with open(f"{config['player_path']}/{Name}/{Name}_Data.json", "r") as file:
            PlayerJSON = json.load(file)
            return PlayerJSON
    except (TypeError, FileNotFoundError):
        return "load_fail"


def decodeMoj(string):
    return json.loads(str(b64decode(string), "utf-8"))


def grabProfile(uuid):
    http = config["skin_links"]
    try:
        RawMojangPr = retrieveJSON(f"{http["profile"]}{uuid}")
        MojangProfile = decodeMoj(RawMojangPr["properties"][0]["value"])
        return MojangProfile
    except (RuntimeError, TypeError):
        return "ty"


# endregion
# =============
# region Skin Utility Classes
# Determines what set of actions must be taken when a Username is entered and submitted
class SKIN_router(Operator):
    """Enter in a Java Edition username that you wish to download/use the skin of."""
    bl_idname = ops['skin_router']
    bl_label = "Skin Utility Router"

    def execute(self, context):
        rig: object = context.active_object
        rig_bones: PoseBone = rig.pose.bones
        skinMeta = rig_bones[config["utility_bone_name"]]
        Username = skinMeta["Username"]

        FilePath = config["player_path"]

        # Operators and Preferences

        if file_exists(f"{FilePath}/{Username}/{Username}_Data.json"):
            if (allow_online() and prefs.get_prefs().prompt_to_refresh_player_data) is True:
                self.report({"ERROR"}, "Error at Online Check and Menu Regen Prompt")
                wm.call_menu(name=menus["skin_regen"])
            else:
                O.skin_utils_ot.skin_load()
        else:
            if allow_online() is True:
                self.report({"INFO"}, "Attempting to Generate new Skin File")
                O.sedaia_utils_ot.skin_get()
            else:
                self.report({"ERROR"}, "Online Access Denied, please enable Online Access in Properties > System")
                return {"CANCELLED"}

        return {"FINISHED"}


# Downloads a new skin
class SKIN_get(Operator):
    bl_label = "Retrieve Player Data"
    bl_idname = ops['skin_get']

    def execute(self, context):
        print("Is this working?")
        http: str = config["skin_links"]
        rig = context.active_object
        rig_bones: object = rig.pose.bones
        skinMeta: PoseBone = rig_bones[config["utility_bone_name"]]
        Username: str = skinMeta["Username"]
        FilePath: str = config["player_path"]
        Remote = retrieveJSON(f"{http["api"]}{Username}")
        if Remote == "http":
            print(Remote)
            self.report(
                {"ERROR_INVALID_INPUT"},
                f"Could not find profile by the name of {Username}, check internet connection and Username spelling")
            return {"FINISHED"}
        Player: dict = grabProfile(Remote['id'])

        PlayerPath: Path = f"{FilePath}/{Username}"

        try:
            if Player["textures"]["SKIN"]["metadata"]["model"] == "slim":
                PlayerModel = "1"
        except (KeyError):
            PlayerModel = "0"

        try:
            SkinPath: Path = f"{PlayerPath}/{Username}_Skin.png"
            SkinHash: str = Player["textures"]["SKIN"]["url"].strip(http["textures"])

            download(Player["textures"]["SKIN"]["url"], SkinPath)
        except (request.HTTPError):
            self.report({"ERROR"}, "Skin Not Found")
            return {"CANCELLED"}

        try:
            CapePath = f"{PlayerPath}/{Username}_Cape.png"
            CapeHash = Player["textures"]["CAPE"]["url"].strip(http["textures"])
            CapeExists = True

            download(Player["textures"]["CAPE"]["url"], CapePath)
        except (KeyError):
            CapePath = ""
            CapeExists = False
            CapeHash = ""

        PlayerData = {
            "UUID": Player["profileId"],
            "NAME": Player["profileName"],
            "SKINS": [
                {
                    "index": 0,
                    "path": SkinPath,
                    "hash": SkinHash,
                    "model": PlayerModel
                },
            ],
            "CAPES": [
                {
                    "index": 0,
                    "path": CapePath,
                    "hash": CapeHash,
                    "exists": CapeExists
                },
            ]
        }

        PlayerFile = f"{FilePath}/{Username}/{Username}_Data.json"
        with open(PlayerFile, "w") as j:
            json.dump(PlayerData, j, ensure_ascii=True, indent=4)

        O.sedaia_utils.skin_load(index=0)

        return {"FINISHED"}


# Adds a new Skin Entry to a Player
class SKIN_add(Operator):
    bl_label = "Add to Index"
    bl_idname = ops['skin_add']

    def execute(self, context):
        http: str = config["skin_links"]
        rig = context.active_object
        rig_data = rig.data
        rig_bones = rig.pose.bones
        skinProp = config["utility_bone_name"]
        skinMeta = rig_bones[skinProp]
        Username = skinMeta["Username"]

        FilePath = config['player_path']

        PlayerFile = f"{FilePath}/{Username}/{Username}_Data.json"
        LocalPlayer = loadPlayer(Username)

        try:
            Player = grabProfile(LocalPlayer["UUID"])
        except (TypeError):
            O.sedaia_utils.skin_add()
            return {"FINISHED"}

        oldHash: str = LocalPlayer["SKINS"][-1]["hash"]
        newHash: str = Player["textures"]["SKIN"]["url"].strip(http["textures"])

        if oldHash == newHash:
            self.report({"WARNING"}, "Skin has not been changed, Skipping Download")
        else:
            print("Does not Match, adding new skin entry")

            PlayerPath: Path = f"{FilePath}/{Username}"

            # Set Metadata and Download Files
            try:
                if Player["textures"]["SKIN"]["metadata"]["model"] == "slim":
                    PlayerModel: str = "1"
            except (KeyError):
                PlayerModel: str = "0"

            try:
                if LocalPlayer["SKINS"][-1]["index"] + 1 > 0:
                    FileIndex: str = f"_{LocalPlayer["SKINS"][-1]["index"] + 1}"
                else:
                    FileIndex = ""
                SkinPath: Path = f"{PlayerPath}/{Username}_Skin{FileIndex}.png"
                SkinHash: str = Player["textures"]["SKIN"]["url"].strip(http["textures"])

                download(Player["textures"]["SKIN"]["url"], SkinPath)
            except (request.HTTPError):
                self.report({"ERROR"}, "Skin Not Found")
                return {"CANCELLED"}

            try:
                if LocalPlayer["SKINS"][-1]["index"] + 1 > 0:
                    FileIndex = f"_{LocalPlayer["CAPES"][-1]["index"] + 1}"
                else:
                    FileIndex = ""
                CapePath: Path = f"{PlayerPath}/{Username}_Cape{FileIndex}.png"
                CapeHash: str = Player["textures"]["CAPE"]["url"].strip(http["textures"])
                CapeExists = True

                download(Player["textures"]["CAPE"]["url"], CapePath)
            except (KeyError):
                CapePath = ""
                CapeExists = False
                CapeHash = ""

            SkinData = {
                "index": LocalPlayer["SKINS"][-1]["index"] + 1,
                "path": SkinPath,
                "hash": SkinHash,
                "model": PlayerModel
            }
            CapeData = {
                "index": LocalPlayer["CAPES"][-1]["index"] + 1,
                "path": CapePath,
                "hash": CapeHash,
                "exists": CapeExists
            }

            LocalPlayer["SKINS"].append(SkinData)
            LocalPlayer["CAPES"].append(CapeData)

            with open(PlayerFile, "w") as j:
                json.dump(LocalPlayer, j, ensure_ascii=True, indent=4)

        O.sedaia_utils_ot.load_skin(index=LocalPlayer["SKINS"][-1]["index"])
        return {"FINISHED"}


# Loads a skin from local storage
class SKIN_load(Operator):
    bl_idname = ops['skin_load']
    bl_label = "Load Player Data"

    index: IntProperty(
        default=0,
        min=0
    )  # type:ignore

    def execute(self, context):
        rig = context.active_object
        rig_data = rig.data
        rig_bones = rig.pose.bones
        skinProp = config["utility_bone_name"]
        skinMeta = rig_bones[skinProp]
        Username = skinMeta["Username"]

        # Metadata
        MatObj = skinMeta["MatObj"]
        SkinMat = skinMeta["SkinMatName"]
        SkinImgNode = skinMeta["SkinImageNodeID"]
        ArmPropName = skinMeta["ArmPropName"]
        ArmPropBone = rig_bones[skinMeta["ArmPropBone"]]
        RigName = skinMeta["RigName"]

        # Config
        Username = skinMeta["Username"]
        SyncName = skinMeta["SyncName"]
        SyncArms = skinMeta["SyncArms"]
        SyncCape = skinMeta["SyncCape"]
        index = self.index
        playerData = loadPlayer(Username)

        # Set Material Handler
        i = 0
        for l in rig.children:
            i = i + 1
            # Find Material Object
            objName = l.name.split(".")[0]
            if objName == MatObj:
                MaterialManager = l
                break
        SkinNodetree = MaterialManager.material_slots[0].material.node_tree
        SkinNode = SkinNodetree.nodes[SkinImgNode].image

        if is_packed(bpy.data.images[SkinNode.name]):
            bpy.data.images[SkinNode.name].unpack(method="USE_LOCAL")
        SkinNode.filepath = playerData["SKINS"][index]["path"]
        print(SkinNode.name)
        # ops["img_pack"](path=SkinNode.name)

        if SyncArms:
            try:
                ArmPropBone.ArmType = playerData["SKINS"][index]["model"]
            except (TypeError):
                ArmPropBone[ArmPropName] = int(playerData["SKINS"][index]["model"])

        if SyncName:
            ops['rig_rename'][1](rig_rename=f"{Username} - {RigName}")
            rig_data["Rig Name"] = f"{Username} - {RigName}"

        return {"FINISHED"}


# Purges the Player file, then calls the SKIN_add operator
class SKIN_purge(Operator):
    """Completely deletes the directory and creates a new entry from a clean download"""
    bl_idname = ops["skin_purge"]
    bl_label = "Purge and Retrieve"
    bl_options = {"REGISTER", "INTERNAL"}

    ask: BoolProperty()  # type: ignore
    confirm: BoolProperty()  # type: ignore

    def execute(self, context):
        rig = context.active_object
        rig_data = rig.data
        rig_bones = rig.pose.bones
        skinProp = config["utility_bone_name"]
        skinMeta = rig_bones[skinProp]
        Username = skinMeta["Username"]

        PlayerPath = f"{config['player_path']}/{Username}"
        rmtree(PlayerPath)

        ops["skin_load"][1]

        return {"FINISHED"}


# Promps to ask if the player is sure they want to purge a skin
class SKIN_menu_purge(Menu):
    bl_idname = menus["skin_purge"]
    bl_label = "Confirm Purging of Player Data"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator(ops["skin_purge"][0], text="Confirm", icon="ERROR").confirm = True


# Asks what the player wants to do with an existing entry
class SKIN_menu_regen(Menu):
    bl_idname = menus['skin_regen']
    bl_label = "Regenerate Player Data?"

    def draw(self, context):
        layout = self.layout
        layout.operator(ops['skin_load'], text="Load Data")
        layout.operator(ops['skin_add'], text="Add Entry")
        layout.menu(menu=menus["skin_purge"], text="Clean Slate", icon="ERROR")


# endregion
# =============
# region Register Classes
classes = [
    FILE_open,

    # Image Classes
    IMAGE_pack,
    IMAGE_reload,

    # Rig Classes
    RIGS_set_name,

    # Skin Util Operators
    SKIN_router,
    SKIN_get,
    SKIN_add,
    SKIN_load,
    SKIN_purge,

    # Skin Util Menu
    SKIN_menu_regen,
    SKIN_menu_purge
]


def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in classes:
        unregister_class(cls)

# endregion
# =============

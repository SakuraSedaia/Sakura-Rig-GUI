import bpy
from bpy.types import Operator, Menu
from bpy.props import StringProperty, BoolProperty
from pathlib import Path
import json
import urllib
from base64 import b64decode
from urllib import request
import os
from .addon_prefs import get_addon_preferences


D = bpy.data
C = bpy.context
T = bpy.types
P = bpy.props
O = bpy.ops


script_version = "2.0.0-Alpha"

prop_bones = [
    "Properties.RigMain",  # 0
    "Properties.Head",    # 1
    "Properties.Torso",   # 2
    "Properties.Arms",    # 3
    "Properties.Legs",     # 4
    "Properties.Skin_Grabber"  # 5
]

# Working Directories
addon_dir = bpy.utils.extension_path_user(
    __package__, create=True, path="")

rig_dir = bpy.utils.extension_path_user(
    __package__, create=True, path="rigs")

player_dir = bpy.utils.extension_path_user(
    __package__, create=True, path="playerdata")


def is_packed(img):
    try:
        return img.packed_files.values() != []
    except:
        return False


def update():
    ...


def img_pack(img_name):
    img = bpy.data.images[img_name]
    if is_packed(img):
        if bpy.data.is_saved:
            img.unpack()

        else:
            img.unpack(method="USE_LOCAL")
    else:
        img.pack()


class SEDAIA_DEV_OT_ImgPack(Operator):
    bl_idname = "sedaia_ot.imgpack"
    bl_label = ""

    img_name: P.StringProperty()  # type: ignore

    def execute(self, context):
        img_pack(self.img_name)
        return {"FINISHED"}


class SEDAIA_DEV_OT_ImgReload(Operator):
    bl_idname = "sedaia_ot.imgreload"
    bl_label = ""

    img_name: StringProperty()  # type: ignore

    def execute(self, context):
        bpy.data.images(self.img_name).reload()
        return {"FINISHED"}


class SEDAIA_DEV_OT_Append_SACR_7_3_0(Operator):
    bl_idname = "sedaia_ot.append_sacr_7_3_0"
    bl_label = "Append SACR"

    lite: BoolProperty()  # type: ignore

    def execute(self, context):
        script_file = os.path.realpath(__file__)
        script_dir = os.path.dirname(script_file)

        if self.lite is True:
            sacr_file = f"{script_dir}/rigs/SACR_R7.3.0_Lite.blend"
            bl_folder = "/Collection/"
            collection = "SACR R7.3 Lite"
        else:
            sacr_file = f"{script_dir}/rigs/SACR_R7.3.0.blend"
            bl_folder = "/Collection/"
            collection = "SACR R7.3"

        col_path = f"{sacr_file}{bl_folder}{collection}"
        col_dir = f"{sacr_file}{bl_folder}"
        col_name = f"{collection}"

        try:
            bpy.ops.wm.append(filepath=col_path,
                              filename=col_name, directory=col_dir)
        except:
            print("Could not Append Rig")

        return {'FINISHED'}


class SEDAIA_DEV_OT_update_rig_name(Operator):
    bl_idname = "sedaia_ot.update_rig_name"
    bl_label = "Set Name"

    rig_name: StringProperty()  # type: ignore

    def execute(self, context):
        context.active_object.name = self.rig_name
        context.collection.name = self.rig_name

        return {'FINISHED'}


class SEDAIA_DEV_OT_open_folder(Operator):
    '''Opens the Local Directory, where Skins, Capes, and Rigs are stored.'''
    bl_idname = "sedaia_ot.open_directory"
    bl_label = "Local Files"

    path: StringProperty(default=addon_dir)  # type: ignore

    def execute(self, context):

        bpy.ops.wm.path_open(
            filepath=self.path)
        return {"FINISHED"}


def generate_player(name):
    if bpy.app.online_access is True:
        moj_api = "https://api.mojang.com/users/profiles/minecraft/"
        moj_profile_api = "https://sessionserver.mojang.com/session/minecraft/profile/"
        mc_ids = json.loads(request.urlopen(
            f"{moj_api}{name}/").read())
        mc_uuid = mc_ids['id']
        mc_profile = json.loads(request.urlopen(
            f"{moj_profile_api}{mc_uuid}").read())

        for item in mc_profile['properties']:
            raw_val = item['value']
            val = str(b64decode(raw_val), 'utf-8')
            tex = json.loads(val)['textures']
            mc_skin = tex['SKIN']['url']

            try:
                mc_cape = tex['CAPE']['url']
                mc_cape_exists = True
            except (KeyError):
                mc_cape = ""
                mc_cape_exists = False

            try:
                if tex['SKIN']['metadata']['model'] == 'slim':
                    mc_model = '1'
                else:
                    mc_model = '0'
            except (KeyError):
                mc_model = '0'

        # Download Texture Files
        bpy.utils.extension_path_user(
            __package__, create=True, path=f"playerdata/{name}")

        request.urlretrieve(mc_skin, f"{player_dir}/{name}/{name}_Skin.png")

        if mc_cape_exists == True:
            request.urlretrieve(
                mc_cape, f"{player_dir}/{name}/{name}_Cape.png")

        # Generate JSON Data Structure
        player_data = [
            {
                "mc_user": f"{mc_uuid}",
                "mc_uuid": f"{name}",
                "SKIN": {
                    "http": mc_skin,
                    "local": f"{player_dir}/{name}/{name}_Skin.png",
                    "model": mc_model
                },
                "CAPE": {
                    "http": mc_cape,
                    "local": f"{player_dir}/{name}/{name}_Cape.png",
                    "exists": mc_cape_exists
                }
            }
        ]
        make_json = f"{player_dir}/{name}/{name}_Data.json"
        with open(make_json, 'w') as f:
            json.dump(player_data, f, indent=4)

        if Path(make_json).exists():
            print(f"Successfully saved {name}_Data.json")
            return player_data
        else:
            return "gen_fail"


def load_player(name):
    player_file = f"{name}_Data.json"
    try:
        with open(f"{player_dir}/{name}/{player_file}", 'r') as file:
            player_data = json.load(file)

            return player_data
    except (TypeError, FileNotFoundError):
        return 'load_fail'


class SEDAIA_OT_change_skin(Operator):
    bl_idname = f"sedaia_ot.change_skin"
    bl_label = "Change Skin"

    def execute(self, context):
        rig = context.active_object
        rig_bones = rig.pose.bones
        skinProp = rig_bones[prop_bones[5]]
        mc_name = skinProp["username"]

        player_file = f"{mc_name}_Data.json"
        playerdata_path = f"{player_dir}/{skinProp['username']}"
        if bpy.app.online_access:
            if get_addon_preferences().prompt_to_refresh_player_data:
                print(f"{playerdata_path}/{player_file}")
                if Path(f"{playerdata_path}/{player_file}").exists():
                    print("Blob")
                    bpy.ops.wm.call_menu(
                        name="SEDAIA_MT_prompt_for_player_reload")
                else:
                    O.sedaia_ot.load_player_data(
                        mc_name=skinProp["username"], path=playerdata_path, generate=True)

            else:
                if Path(f"{playerdata_path}/{skinProp['username']}/{player_file}").exists():
                    O.sedaia_ot.load_player_data(
                        mc_name=skinProp["username"], path=playerdata_path)
                else:
                    O.sedaia_ot.load_player_data(
                        mc_name=skinProp["username"], path=playerdata_path, generate=True)

        else:
            if Path(f"{playerdata_path}/{player_file}").exists():
                O.sedaia_ot.load_player_data(
                    mc_name=skinProp["username"], path=playerdata_path)
            else:
                self.report(
                    {"ERROR"}, 'Local Player Data does not exist, please enable "Allow Online Access" to generate a new Entry')

        return {'FINISHED'}


class SEDAIA_MT_prompt_for_player_reload(Menu):
    bl_label = "Regenerate Player Data?"
    bl_idname = "SEDAIA_MT_prompt_for_player_reload"

    def draw(self, context):
        layout = self.layout

        rig = context.active_object
        rig_bones = rig.pose.bones
        skinProp = rig_bones[prop_bones[5]]

        load_data = layout.operator(
            "sedaia_ot.load_player_data", text="Load Data")
        load_data.mc_name = skinProp["username"]
        load_data.path = player_dir

        gen_data = layout.operator(
            "sedaia_ot.load_player_data", text="Regenerate Data")
        gen_data.mc_name = skinProp["username"]
        gen_data.path = player_dir
        gen_data.generate = True


class SEDAIA_OT_load_player(Operator):
    bl_idname = f"sedaia_ot.load_player_data"
    bl_label = "Load Player Data"

    mc_name: StringProperty()  # type: ignore
    path: StringProperty()  # type: ignore
    generate: BoolProperty(default=False)  # type: ignore

    def execute(self, context):
        rig = context.active_object
        rig_data = rig.data
        rig_bones = rig.pose.bones

        skinProp = rig_bones["Properties.Skin_Grabber"]
        armProp = rig_bones[prop_bones[3]]

        if self.generate == True:
            try:
                data = generate_player(self.mc_name)
                if data == 'gen_fail':
                    self.report(
                        {"ERROR"}, 'Could not Generate File')
                    return {"CANCELLED"}

            except (urllib.error.HTTPError):
                self.report(
                    {"ERROR"}, "Error 404, Username does not exist as a Java Edition Account")
                return {"CANCELLED"}
        else:
            data = load_player(self.mc_name)
            if data == 'load_fail':
                return {"CANCELLED"}

        # Set Material Handler
        rig = context.active_object
        i = 0
        for l in rig.children:
            i = i + 1
            # Find Material Object
            objName = l.name.split(".")[0]
            if objName == "Material_Properties":
                mat_obj = l
                break

        skin_nodetree = mat_obj.material_slots[0].material.node_tree
        skin_node = skin_nodetree.nodes["Skin Texture"].image

        if is_packed(bpy.data.images[skin_node.name]):
            bpy.data.images[skin_node.name].unpack(
                method="USE_LOCAL")

        skin_node.filepath = data[0]['SKIN']['local']
        img_pack(skin_node.name)

        if skinProp['auto_arm_type']:
            armProp.ArmType = data[0]['SKIN']['model']

        if skinProp["rig_username_match"] == True:
            O.sedaia_ot.update_rig_name(rig_name=f"{self.mc_name} - SACR R8")
            rig_data["Rig Name"] = f"{self.mc_name} - SACR R8"

        return {"FINISHED"}


sedaia_ops_dev = [
    SEDAIA_DEV_OT_ImgPack,
    SEDAIA_DEV_OT_ImgReload,
    SEDAIA_DEV_OT_update_rig_name,
    SEDAIA_DEV_OT_open_folder,

    # Skin Downloader
    SEDAIA_OT_change_skin,
    SEDAIA_MT_prompt_for_player_reload,
    SEDAIA_OT_load_player
]


def register():
    for cls in sedaia_ops_dev:
        bpy.utils.register_class(cls)


def unregister():
    for cls in sedaia_ops_dev:
        bpy.utils.unregister_class(cls)

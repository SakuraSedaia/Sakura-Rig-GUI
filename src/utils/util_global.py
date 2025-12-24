from typing import Optional
import bpy
import bpy.types as T
import bpy.utils as U
import bpy.props as P


# Class Index
op_id: str = "sedaia_utils_ot"
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
    "change_skin": f"{op_id}.change_skin",
    "download_skin": f"{op_id}.download_skin",
    "load_skin": f"{op_id}.load_skin",
    "update_skin": f"{op_id}.update_skin",
    "delete_skin": f"{op_id}.delete_skin",
}

menu_id: str = "SEDAIA_UTIL_MT"
menus: dict = {
}


# Functions
def allow_online():
    return bpy.app.online_access

# File Functions
def file_exists(path):
    return Path(path).exists()


def is_packed(file):
    try:
        return file.packed_files.values() != []
    except:
        return False

# Lookup Tables
def lookup_name(bl_list: dict, query: str):
    for i in enumerate(bl_list):
        if query in i[1].name:
            return bl_list[i[0]]
        else:
            continue

    return None

def find_key(obj, value):
    for key, v in obj.items():
        if v == value:
            return key
        else:
            continue
    return None

# HTTP and JSON
def download(url, path):
    request.urlretrieve(url=url, filename=path)


def retrieve_json(url):
    try:
        return json.loads(request.urlopen(url).read())
    except (request.HTTPError, error.URLError):
        return "http_error"


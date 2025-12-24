ZIP_File = False
SaveToBlenderRepo = True
"""
A Simple Build Script to create a usable addon archive for use in Blender
"""
import os
import shutil
import tomllib
from pathlib import Path
import cgitb

blacklist = {  # Dirs to not include
    "templates",
    "__pycache__"
}


FileStructure = []
SourcePath: Path = Path("src").absolute()


BuildPath: Path = Path("_build").absolute()
Blender_Repo: Path = Path("/home/sakura/.config/blender/5.0/extensions/PyCharm/").absolute()

if BuildPath.exists():
    shutil.rmtree(BuildPath)
    shutil.copytree(src=SourcePath, dst=BuildPath)
else:
    shutil.copytree(src=SourcePath, dst=BuildPath)

filedirs = []
rootpath = Path(BuildPath).walk()
for d in rootpath:
    path = d[0]
    if path.name in blacklist:
        shutil.rmtree(path)
    else:
        filedirs.append(d[0])

struct = []
for f in filedirs:
    tree = Path(f).iterdir()
    for t in enumerate(tree):
        if not t[1].is_dir():
            struct.append(str(t[1])[len(str(BuildPath))+1:])

# Get Addon Info
with open(f"{str(BuildPath)}/blender_manifest.toml", "rb") as m:
    Manifest = tomllib.load(m)

AddonName: str = f"{Manifest['id']}_V{Manifest['version']}"

if SaveToBlenderRepo:
    dest = f"{Blender_Repo}/{Manifest['id'].lower()}_dev"
    if BuildPath.exists():
        shutil.rmtree(dest)

    shutil.copytree(src=BuildPath, dst=dest)


if ZIP_File:
    ZipFileName: str = f"{AddonName}.zip"
    ZipPath: Path = Path(f"archives/{AddonName}")

    if ZipPath.exists():
        os.remove(ZipPath)

    shutil.make_archive(base_name=ZipPath, format='zip',
                            root_dir=str(BuildPath))

shutil.rmtree(BuildPath)

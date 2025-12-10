'''
A Simple Build Script to create a usable addon archive for use in Blender
'''
import os
import shutil
import tomllib
from pathlib import Path


blacklist = {  # Dirs to not include
    "templates",
    "__pycache__"
}


FileStructure = []
SourcePath: Path = Path("src")
BuildPath: Path = Path("tmp")

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
        if t[1].is_dir() is not True:
            struct.append(str(t[1])[len(str(BuildPath))+1:])

# Get Addon Info
with open(f"{str(BuildPath)}/blender_manifest.toml", "rb") as m:
    Manifest = tomllib.load(m)

ZipName: str = f"{Manifest['id']}_V{Manifest['version']}"
ZipFileName: str = f"{ZipName}.zip"
ZipPath: Path = Path(f"archives/{ZipName}")

if ZipPath.exists():
    os.remove(ZipPath)

shutil.make_archive(base_name=ZipPath, format='zip',
                    root_dir=str(BuildPath))

shutil.rmtree(BuildPath)

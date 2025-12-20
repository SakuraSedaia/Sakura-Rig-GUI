"""
A Simple Build Script to create a usable addon archive for use in Blender
"""
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
BuildPath: Path = Path("_build")

if BuildPath.exists():
    print("Build Path Exists, Purging Old Data")
    shutil.rmtree(BuildPath)
    shutil.copytree(src=SourcePath, dst=BuildPath)
else:
    print("Creating new Build Path")
    shutil.copytree(src=SourcePath, dst=BuildPath)


file_dirs = []
rootpath = Path(BuildPath).walk()
for d in rootpath:
    path = d[0]
    if path.name in blacklist:
        print(f"Removing {path} from File Structure")
        shutil.rmtree(path)
    else:
        print(f"Adding {path} to Cache")
        file_dirs.append(d[0])

struct = []
for f in file_dirs:
    tree = Path(f).iterdir()
    print(f"Creating File Structure for {f}")
    for t in enumerate(tree):
        if not t[1].is_dir():
            print(f"Adding {str(t[1])[len(str(BuildPath))+1:]} to archive")
            struct.append(str(t[1])[len(str(BuildPath))+1:])

# Get Addon Info
print(f"Getting Addon ID and Version {str(BuildPath)}/blender_manifest.toml")
with open(f"{str(BuildPath)}/blender_manifest.toml", "rb") as m:
    Manifest = tomllib.load(m)

ZipName: str = f"{Manifest['id']}_V{Manifest['version']}"
ZipFileName: str = f"{ZipName}.zip"
ZipPath: Path = Path(f"archives/{ZipName}")

if ZipPath.exists():
    print("Overriding old Archive")
    os.remove(ZipPath)

print(f"Creating New Archive: {ZipPath}")
shutil.make_archive(base_name=ZipPath, format='zip',
                    root_dir=str(BuildPath))

print("Cleaning Up")
shutil.rmtree(BuildPath)



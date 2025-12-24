from importlib import reload

if "R8_modules" in locals():
    reload(R8_modules)
else:
    from . import modules as R8_modules

def register():
    R8_modules.register()

def unregister():
    R8_modules.unregister()
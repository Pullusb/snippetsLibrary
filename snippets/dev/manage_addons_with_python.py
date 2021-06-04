## addon python management
import bpy
import addon_utils

## print all addons pathes
for fp in addon_utils.paths():
    print(fp)


## get list of enabled addon name on disk (stem of the .py file or the folder name for multifile addons)
print(f'{len(bpy.context.preferences.addons.keys())} addons enabled')
print( bpy.context.preferences.addons.keys() )


## print all addon names and version (from bl_info dic)
for mod in addon_utils.modules():
    print(mod.bl_info.get('name', ''), mod.bl_info.get('version', (-1, -1, -1)))


## enable / disable addon through python
addon_name = 'Megaddon'
if not addon_name in [m.bl_info.get('name') for m in addon_utils.modules()]:
    print(f'{addon_name} not found in addons')
else:
    # Raise a silent error if not found and return None
    active = addon_utils.enable(addon_name) # default_set=False, persistent=False
    if active:
        print("enabled", active.bl_info['name'])
    else:
        print(addon_name, "not found !")

## Check loaded state of and addon
saved_in_pref, is_enabled = addon_utils.check('MyKeyMouse') # return (loaded_default, loaded_state)
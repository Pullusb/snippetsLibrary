## import addons as module to use in scripts

## Can do direct import from modules (even if not enabled)
from my_addon_name import some_module

## For legacy addons there will be an error if there are dashes in name, use importlib
import importlib
mod = importlib.import_module("my-addon-name")
func = mod.some_module.specific_func

## Extension use namespaced path: bl_ext.<repo>.<module_name>
## Dashes are automatically resolved as undescore)
from bl_ext.user_default.addon_folder_name import some_module

## Example:
# from bl_ext.blender_org.SB_path_actions.path_func import open_folder

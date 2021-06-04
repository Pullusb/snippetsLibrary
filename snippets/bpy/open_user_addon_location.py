## quick open user addons in OS
import bpy
bpy.ops.wm.path_open(filepath=bpy.utils.user_resource('SCRIPTS', 'addons'))

## open blender system addon in OS
# import os
# bpy.ops.wm.path_open(os.path.join(bpy.utils.resource_path('LOCAL') , 'scripts', 'addons'))
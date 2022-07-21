## update custom prop parameters
# Blender 3.0+

import bpy

# usage : obj.id_properties_ui("property name").update(description='placeholder')

## ex: create float props on a set of bones and set parameters
arm = bpy.context.object
bones_name = ('blendshape-corner-mouth', 'blendshape-eyes', 'blendshape-eye.L', 'blendshape-eye.R',
'eyebrow-ext.L', 'eyebrow-ext.R', 'eyebrow-int.L', 'eyebrow-int.R', 'jaw', 'center-up-mouth',
'center-low-mouth' )
for bone_name in bones_name:
    bone = arm.pose.bones.get(bone_name)
    print(bone)

    for k in bone.keys():
        bone[k] = 0.0
        bone.id_properties_ui(k).update(
            min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, default=0.0)
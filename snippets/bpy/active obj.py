# change active object/bone
# set active bone
objarm = bpy.context.view_layer.objects.active
objarm.data.bones.active = objarm.data.bones['Bone']
objarm.data.bones.active = objarm.pose.bones['Bone'].bone
# set active object
bpy.context.view_layer.objects.active = D.objects['Cube']
# iterate over context mode and object type, do action after mode change.
#
# exemple wih recalculate normals outside :
for ob in bpy.context.selected_objects:
    if bpy.context.mode == 'OBJECT':#'EDIT_MESH','POSE','EDIT_ARMATURE',
        if bpy.context.object.type == 'MESH':#('MESH', 'CURVE', 'SURFACE', 'METABALL', 'TEXT', 'ARMATURE', 'LATTICE', 'EMPTY', 'SPEAKER', 'CAMERA', 'LAMP',)
            bpy.context.view_layer.objects.active = ob
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode='OBJECT')
## Translate object or bone in world space by a given vector

def add_translation_vector(target, translation_vector):
    """Apply world space translation vector to an object or a bone
    Usage:
        Add 1 unit up:
        add_translation_vector(bpy.context.object, Vector((0,0,1)))
    """
    if isinstance(target, bpy.types.PoseBone):
        armature = target.id_data  # Get the armature object
        # Switch to armature space
        current_world_position = (armature.matrix_world @ target.matrix).to_translation()
        new_world_position = current_world_position + translation_vector
        new_local_position = armature.matrix_world.inverted() @ new_world_position
        target.matrix.translation = new_local_position
        # return new_local_position
        return

    ## Add directly to object matrix
    target.matrix_world.translation += translation_vector
    # return target.matrix_world.to_translation()

## Apply quaternion rotation on object or pose bone

from mathutils import Matrix

def apply_quaternion_to_pose_bone(posebone, quaternion):
    """Rotate pose bone in world space by given quaternion"""
    # Create rotation matrix from quaternion
    rot_mat = quaternion.to_matrix().to_4x4()

    # Get bone current world matrix
    armature = posebone.id_data
    world_mat = (armature.matrix_world @ posebone.matrix).copy()

    # Get world pivot point
    world_pivot = armature.matrix_world @ posebone.head

    # Apply the rotation on the copy of world matrix
    # remove pivot vector, apply rotation, re-apply pivot
    new_world_mat = Matrix.Translation(world_pivot) @ \
                rot_mat @ \
                Matrix.Translation(-world_pivot) @ \
                world_mat

    ## Assign matrix to posebone in armature space
    posebone.matrix = armature.matrix_world.inverted() @ new_world_mat

def apply_quaternion_to_object(obj, quaternion):
    """Rotate pose bone in world space by given quaternion"""
    # Create rotation matrix from quaternion
    rotation_matrix = quaternion.to_matrix().to_4x4()

    # Get object's current world matrix
    world_matrix = obj.matrix_world

    # Get object's pivot point (origin) in world space
    pivot = world_matrix.to_translation()

    # Create translation matrices
    to_pivot = mathutils.Matrix.Translation(-pivot)
    from_pivot = mathutils.Matrix.Translation(pivot)

    # Apply rotation around pivot:
    # 1. Move to center, 2. Apply rotation, 3. Move back to initail position
    obj.matrix_world = from_pivot @ rotation_matrix @ to_pivot @ world_matrix

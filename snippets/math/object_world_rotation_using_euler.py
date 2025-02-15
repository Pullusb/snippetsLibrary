## Apply a Euler to rotate an object in worldspace (not much use case)

import bpy
from mathutils import Matrix, Euler
from math import radians

def apply_world_euler_rotation_object(obj, rotation_euler):
    # Get current world matrix
    world_matrix = obj.matrix_world

    # Get pivot point
    pivot = world_matrix.to_translation()

    # Create rotation matrix from Euler
    rotation_matrix = rotation_euler.to_matrix().to_4x4()

    # Create translation matrices
    to_pivot = Matrix.Translation(-pivot)
    from_pivot = Matrix.Translation(pivot)

    # Apply rotation around pivot
    new_matrix = from_pivot @ rotation_matrix @ to_pivot @ world_matrix

    # Extract Euler angles from the new matrix while maintaining rotation mode
    rot_mode = obj.rotation_mode
    new_euler = new_matrix.to_euler(rot_mode)

    # Make compatible with previous rotation to avoid discontinuities
    new_euler.make_compatible(obj.rotation_euler)

    # Update object's rotation
    obj.rotation_euler = new_euler

# Example, rotate active object by 45 degrees on World X axis
apply_world_euler_rotation_object(bpy.context.object, Euler((radians(45),0,0)))

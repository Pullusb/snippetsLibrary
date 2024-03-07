## Rotate object by some angle on defined axis
## if angle value is in degree, use: math.radians(angle)

import bpy
from math import pi, radians
from mathutils import Matrix, Vector

def rotate_on_axis(obj, axis, angle):
    '''Rotate passed object on axis by an angle
    obj: Object to rotate
    axis: an axis as string, ex: "X", or a Vector, ex: Vector((0,0,1))
    angle: An angle value in radians (signed)
    ''' 

    ## Create rotation matrix
    rot_matrix = Matrix.Rotation(angle, 4, axis)
    ## create a working copy of current matrix
    mat = obj.matrix_world.copy()

    ## Reset translation, rotate, re-apply translation
    mat.translation = Vector((0,0,0))
    mat = rot_matrix @ mat
    mat.translation = obj.matrix_world.translation

    # Assign new rotated matrix
    obj.matrix_world = mat


## Rotate active object by 90 degrees (in radians: pi/2)...

## ... on global Z axis
rotate_on_axis(bpy.context.object, "Z", pi/2)

## ... on current view axis (need to be executed in viewport context, using a context override from script editor)
# view_vector = Vector((0,0,-1))
# view_vector.rotate(bpy.context.space_data.region_3d.view_rotation)
# rotate_on_axis(bpy.context.object, view_vector, pi/2)

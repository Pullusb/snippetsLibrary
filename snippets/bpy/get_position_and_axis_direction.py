## Get object or posebone world position + 3 axis direction vectors

def get_position_and_axis_direction(target):
    '''Get world position and local direction axis of object or bone
    return 4 vector: loc, x, y, z (1 position, 3 for axis directions)'''
    if isinstance(target, bpy.types.PoseBone):
        armature = target.id_data
        matrix = armature.matrix_world @ target.matrix
    else:
        matrix = target.matrix_world
    x = Vector((1,0,0))
    y = Vector((0,1,0))
    z = Vector((0,0,1))
    x.rotate(matrix)
    y.rotate(matrix)
    z.rotate(matrix)
    return matrix.to_translation(), (x, y, z)

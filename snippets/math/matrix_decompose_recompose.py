## Decompose - recompose a Matrix
import bpy
from mathutils import Matrix

def scale_matrix_from_vector(scale):
    # recreate a neutral mat scale
    matscale_x = Matrix.Scale(scale[0], 4,(1,0,0))
    matscale_y = Matrix.Scale(scale[1], 4,(0,1,0))
    matscale_z = Matrix.Scale(scale[2], 4,(0,0,1))
    matscale = matscale_x @ matscale_y @ matscale_z
    return matscale

mat = bpy.context.object.matrix_world

# decompose
loc, rot, scale = mat.decompose()

# compose
loc_mat = Matrix.Translation(loc)
rot_mat = rot.to_matrix().to_4x4()
scale_mat = scale_matrix_from_vector(scale)

new_mat = loc_mat @ rot_mat @ scale_mat

bpy.context.object.matrix_world = new_mat

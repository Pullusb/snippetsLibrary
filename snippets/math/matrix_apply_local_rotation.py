## Apply a rotation matrix of -90 degrees on X local axis
import bpy
from mathutils import Matrix
from math import pi

ob = bpy.context.object
mat_90 = Matrix.Rotation(-pi/2, 4, 'X')
ob.matrix_world = ob.matrix_world @ mat_90
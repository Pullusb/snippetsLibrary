## context managers for Bmesh editing
## Author: Salai Vedha Viradhan : from https://salaivv.com/2023/07/07/context-mangers-blender

import bpy
import bmesh
from contextlib import contextmanager

# Bmesh operations on a mesh object
@contextmanager
def BMeshObject(mesh_object):
    # Setup process
    mesh = bmesh.new()
    mesh.from_mesh(mesh_object.data)

    try:
        # Yielding mesh to the outer context to execute
        # the statements inside the 'with' block
        yield mesh
    finally:
        # Teardown process
        mesh.to_mesh(mesh_object.data)
        mesh.free()

## Usage:
# with BMeshObject(mesh_object) as mesh:
#     bmesh.ops.remove_doubles(mesh, verts=mesh.verts, dist=0.0001)

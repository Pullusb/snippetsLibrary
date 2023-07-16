## context managers for edit mode
## Author: Salai Vedha Viradhan : from https://salaivv.com/2023/07/07/context-mangers-blender

import bpy
import contextlib

# Edit mode operations on passed object
@contextlib.contextmanager
def EditMode(active_object):
    # Setup process
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = active_object
    bpy.ops.object.mode_set(mode='EDIT')

    try:
        # Yielding execution to the outer context to execute
        # the statements inside the 'with' block
        yield
    finally:
        # Teardown process
        bpy.ops.object.mode_set(mode='OBJECT')

## usage:
# with EditMode(mesh_object):
#     bpy.ops.mesh.select_all(action='SELECT')
#     bpy.ops.mesh.remove_doubles()
#     bpy.ops.mesh.dissolve_limited()
#     bpy.ops.mesh.tris_convert_to_quads()

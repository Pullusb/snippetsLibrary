## Get viewport's current view vector or camera view vector

import bpy
from mathutils import Vector

# Standalone functions

def get_viewport_view_vector():
    '''return current viewport view vector (normalized direction)'''
    view_vector = Vector((0,0,-1))
    view_vector.rotate(bpy.context.space_data.region_3d.view_rotation)
    return view_vector

def get_camera_view_vector():
    '''return active camera view vector (normalized direction)
    return None if no active camera
    '''
    view_vector = Vector((0,0,-1))
    if not bpy.context.scene.camera:
        return
    view_vector.rotate(bpy.context.scene.camera.matrix_world)
    return view_vector


# Mixed function (with camera as option)

def get_view_vector(camera=False):
    '''return current viewport view vector (normalized direction)
    camera: if True return active camera view vector (None if no active camera)
    '''
    view_vector = Vector((0,0,-1))
    if camera:
        if not bpy.context.scene.camera:
            return
        view_vector.rotate(bpy.context.scene.camera.matrix_world)

    else:
        view_vector.rotate(bpy.context.space_data.region_3d.view_rotation)

    return view_vector

## ----

## For camera
cam_view_vec = get_camera_view_vector()


## For view vector
## In view 3D context
# view_vec = get_view_vector()
# view_vec = get_viewport_view_vector()

## Here with context override for use from text editor
def get_viewport_override():
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                return {'window': window, 'screen': screen, 'area': area}

with bpy.context.temp_override(**get_viewport_override()):
    view_vec = get_view_vector()

print("camera view vector:", cam_view_vec)
print("view vector:", view_vec)

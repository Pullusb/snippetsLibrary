## function to fit camera according to objects

import bpy
from mathutils import Vector

def cam_fitting(objects=None, camera=None, margin_lens=3):
    '''Fit scene camera to objects.
    objects (list): if no objects passed, fit on selection (or all object if nothing selected)
    camera (cam obj): if no camera passed, use active camera
    margin_lens (int): temporarily add lens value before fitting, give more margin
    '''

    scn = bpy.context.scene
    cam=camera or scn.camera

    if objects is None:
        # Smart fitting on selection or all
        if bpy.context.selected_objects:
            objects = bpy.context.selected_objects
        else:
            objects = scn.objects


    ob_list = [o for o in objects if o.type not in ('ARMATURE', 'CAMERA', 'LIGHT', 'SPEAKER', 'EMPTY')]
    armatures = [o for o in objects if o.type == 'ARMATURE']
    arma_coords = [(ob.matrix_world @ b.matrix).to_translation() for ob in armatures for b in ob.pose.bones]

    coords = arma_coords + [ob.matrix_world @ Vector(co) for ob in ob_list for co in ob.bound_box[:]]
    if not coords:
        print('no objects/coordinate to frame')
        return

    flatten_coords = [elem for v in coords for elem in v]

    if margin_lens:
        cam.data.lens += margin_lens

    depsgraph = bpy.context.evaluated_depsgraph_get()
    cam.location, _ = cam.camera_fit_coords(depsgraph, flatten_coords)

    if margin_lens:
        cam.data.lens -= margin_lens


## example of argument
# scope = scn.objects # all objects
# scope = bpy.context.selected_objects # selection
# camera = bpy.context.scene.objects['Camera.001']

cam_fitting() # objects=scope, camera=None

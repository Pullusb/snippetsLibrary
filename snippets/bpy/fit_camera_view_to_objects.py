## function to fit camera according to objects

import bpy
from mathutils import Vector
import numpy as np


def bounding_box_from_coords(coords):
    ## numpy oriented multi-bbox solution here :
    ## https://blender.stackexchange.com/questions/223858/how-do-i-get-the-bounding-box-of-all-objects-in-a-scene

    import itertools
    # bottom front left (all the mins)
    bfl = coords.min(axis=0)
    # top back right
    tbr = coords.max(axis=0)
    G  = np.array((bfl, tbr)).T
    # bbox coords, ie the 8 combinations of bfl tbr.
    return [Vector(i) for i in itertools.product(*G)]


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
    if not objects:
        print('No target objects')
        return

    skip = ('ARMATURE', 'CAMERA', 'LIGHT', 'SPEAKER', 'EMPTY')
    
    ob_list = [o for o in objects if o.type not in skip]

    armatures = [o for o in objects if o.type == 'ARMATURE']
    arma_coords = [(ob.matrix_world @ b.matrix).to_translation() for ob in armatures for b in ob.pose.bones]
    
    ## get instances (! not recursive, won't take nested collection)
    instances = [o for o in objects if o.type == 'EMPTY' and o.instance_type == 'COLLECTION' and o.instance_collection]
    vecs = [empty.matrix_world @ o.matrix_world @ Vector(v) for empty in instances for o in empty.instance_collection.all_objects if o.type not in skip and not o.hide_viewport for v in o.bound_box[:]]


    coords = vecs + arma_coords + [ob.matrix_world @ Vector(co) for ob in ob_list for co in ob.bound_box[:]]

    
    if not coords:
        print('no objects/coordinate to frame')
        return
    ## Optionally reduce to a single overall bounding box corners coords covering all objects, speed untested
    # if coords:
    #     coords = bounding_box_from_coords(np.array(coords)) # (reduce to instance overall bbox)
    #     # ## check center of bbox for debug, or Vector(np.sum(vecs, axis=0)) / len(vecs)
    #     # bpy.context.scene.cursor.location = np.add.reduce(coords) / 8

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

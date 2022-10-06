## Get camera frame 3D corner world coordinates

def get_cam_frame_world(cam, scene=None):
    '''get camera frame center position in 3d space
    Need scene to get resolution ratio (default to active scene)
    ortho camera note: scale must be 1,1,1 (parent too)
    to fit right in cam-frame rectangle
    '''

    scene = scene or bpy.context.scene

    # Without scene passed, base on square
    frame = cam.data.view_frame(scene)
    mat = cam.matrix_world
    frame = [mat @ v for v in frame]
    #-# Get center
    # import numpy as np
    # center = np.add.reduce(frame) / 4
    # center = np.sum(frame, axis=0) / 4
    return frame

scn = bpy.context.scene
get_cam_frame_world(scn.camera, scn)

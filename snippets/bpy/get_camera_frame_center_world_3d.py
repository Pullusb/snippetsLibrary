## Get camera frame center in world position
def get_cam_frame_center_world(cam):
    '''get camera frame center position in 3d space'''
    ## ortho cam note: scale must be 1,1,1 (parent too) to fit right in cam-frame rectangle

    import numpy as np
    frame = cam.data.view_frame()
    mat = cam.matrix_world
    frame = [mat @ v for v in frame]

    # return np.add.reduce(frame) / 4
    return np.sum(frame, axis=0) / 4
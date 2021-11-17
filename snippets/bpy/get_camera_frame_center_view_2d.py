## get camera frame center 2D coordinate in view space 
def get_center_view(context, cam):
    '''
    https://blender.stackexchange.com/questions/6377/coordinates-of-corners-of-camera-view-border
    Thanks to ideasman42
    '''
    from bpy_extras import view3d_utils

    frame = cam.data.view_frame()
    mat = cam.matrix_world
    frame = [mat @ v for v in frame]
    frame_px = [view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d, v) for v in frame]
    center_x = frame_px[2].x + (frame_px[0].x - frame_px[2].x)/2
    center_y = frame_px[1].y + (frame_px[0].y - frame_px[1].y)/2

    return Vector((center_x, center_y))

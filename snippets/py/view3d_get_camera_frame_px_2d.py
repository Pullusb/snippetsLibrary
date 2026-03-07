## Get camera framing in viewport pixel coordinate  
from bpy_extras.view3d_utils import location_3d_to_region_2d

def view3d_get_camera_frame_px_2d(cam=None, context=None) -> list:
    """Get Camera 2d frame in viewport pixel coordinate, starting top-right corner going CW (clockwise)

    Args:
        context (Context): blender context, default to bpy.context
        cam (Object): camera to get view_frame from, default to context's scene camera

    Return:
        Camera frame in pixel 2D coordinate (list of 4 Vector2)
    """

    context = context or bpy.context
    cam = cam or context.scene.camera

    # based on https://blender.stackexchange.com/questions/6377/coordinates-of-corners-of-camera-view-border
    frame = cam.data.view_frame(scene=context.scene)
    # to world-space
    frame = [cam.matrix_world @ v for v in frame]
    # to pixelspace
    region, rv3d = context.region, context.space_data.region_3d
    frame_px = [location_3d_to_region_2d(region, rv3d, v) for v in frame]
    return frame_px

print(view3d_camera_border_2d(C.scene.camera))

## World coordinate to camera pixel coordinate (optional apply resolution percentage)

def world_to_cam_pixel_coord(w_coord, scene=None, camera=None, use_res_percentage=False):
    """Project a 3D world-space coordinate to 2D pixel coordinates in the camera's render frame.

    Wraps bpy_extras.object_utils.world_to_camera_view and scales the resulting
    normalized camera-space coordinates by the render resolution.

    Args:
        w_coord (Vector3): World-space location to project.
        scene (Scene, optional): Scene used for resolution Defaults to active scene.
        camera (Object, optional): Camera object to project from. Defaults scene's active camera.
        use_res_percentage (bool, optional): If True, the output is scaled by resolution_percentage.
            If False (default), the base resolution is used.

    Returns:
        tuple[float, float]: (pixel_x, pixel_y) in the camera's render frame.
            Origin is at the bottom-left (Blender image convention). Values fall in
            `[0, res_x]` / `[0, res_y]` when the point lies inside the frame, and
            outside that range otherwise. Coordinates are float (sub-pixel).

    Notes:
        - Y is bottom-up. For top-down conventions (OpenCV / PIL / most image
          formats), flip with `pixel_y = res_y - pixel_y`.
        - Depth (Z from `world_to_camera_view`) is discarded; points behind the camera 
          still return finite pixel coordinates that do not correspond to a visible screen position.
        - pixel ascpect is not computed, assume square pixel (`render.pixel_aspect_x` / `pixel_aspect_y`)
    """
    from bpy_extras.object_utils import world_to_camera_view

    scene = scene or bpy.context.scene
    camera = camera or scene.camera

    cam_ndc_coord = world_to_camera_view(scene, camera, w_coord)

    rdr = scene.render
    res_x = rdr.resolution_x
    res_y = rdr.resolution_y

    if use_res_percentage:
        fac = rdr.resolution_percentage * 0.01
        res_x = rdr.resolution_x * fac
        res_y = rdr.resolution_y * fac

    pixel_x = res_x * cam_ndc_coord.x
    pixel_y = res_y * cam_ndc_coord.y

    return (pixel_x, pixel_y)

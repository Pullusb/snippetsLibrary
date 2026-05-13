## Convert camera ndc coordinate (vec2) to world coordinate (vec3)

def camera_ndc_to_world(ndc_x, ndc_y, depth=None, scene=None, cam_obj=None):
    """Convert a camera NDC coordinate into a world position
    (0..1, origin bottom-left, matching bpy_extras.object_utils.world_to_camera_view).
    Args:
        ndc_x: X coordinate camera 2d frame
        ndc_y: Y coordinate camera 2d frame
        depth (float, optional): distance along the camera's local -Z axis
            if not passed, coordinate will be on camera frame's plane
        scene (Scane,optional): scene that define frame ratio based on current resolution (default to active scene)
        cam_obj (Obj, optional): camera used for placement and data (default to scene camera)
    """

    scene = scene or bpy.context.scene
    cam_obj = cam_obj or scene.camera

    cam = cam_obj.data
    # view_frame: top-right, bottom-right, bottom-left, top-left
    # - perspective: corners at z = -1 (unit depth)
    # - ortho:       corners at z =  0, sized by ortho_scale
    tr, br, bl, tl = cam.view_frame(scene=scene)

    bottom = bl.lerp(br, ndc_x)
    top    = tl.lerp(tr, ndc_x)
    local  = bottom.lerp(top, ndc_y)

    if depth is not None:
        if cam.type == 'ORTHO':
            # frame size is constant with distance; just push along -Z
            local.z = -depth
        else:  # 'PERSP' (and 'PANO' falls back reasonably for the central case)
            # frame is at z = -1, scale linearly with depth
            local *= depth / abs(local.z)

    return cam_obj.matrix_world @ local

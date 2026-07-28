## function to make a dolly zoom, adjust camera local z translation to compensate the lens change so object keep it's size in frame

import bpy
from mathutils.geometry import intersect_line_plane
from mathutils import Vector


def calculate_dolly_zoom_position(old_position, target_position, old_focal_length, new_focal_length):
    """
    Calculates a new camera position for a dolly zoom effect based on focal length change.
    Designed to be used in a modal operator with a slider.

    Args:
        old_position: The previous/current camera position (mathutils.Vector)
        target_position: The target position (mathutils.Vector)
        old_focal_length: The previous/current focal length in mm
        new_focal_length: The new focal length in mm

    Returns:
        Vector: The new camera position
    """
    # Get direction vector from old camera position to target
    direction = (target_position - old_position).normalized()

    # Calculate current distance
    current_distance = (target_position - old_position).length

    # Calculate new distance to maintain same field of view for subject
    # The ratio of distances should equal the ratio of focal lengths
    new_distance = current_distance * (new_focal_length / old_focal_length)

    # Calculate new position
    return target_position - direction * new_distance


def dolly_zoom_to_lens(new_lens, target=None, camera=None):
    """Get final lens and a target object to apply the lens with compensated translation (dolly/vertigo zoom)

    Args:
        new_lens: the final wanted lens
        target (Vector|Object, optional): a vector3 or an object.
            if not specified, use active object, falling back to 3D cursor
        camera (Object, optional): Camera to use, default to scene's active camera
    """
    cam = camera or bpy.context.scene.camera
    if not cam:
        print('no active camera')
        return

    if target is None:
        # Use active object if nothing specified
        target = bpy.context.object

    ## Define target position
    if isinstance(target, bpy.types.Object):
        focal_target = target.matrix_world.translation.copy()
    elif isinstance(target, Vector):
        focal_target = target
    else:
        # Last, fallback to 3D cursor (or return error ?)
        print('No vector specified or active object, using 3D cursor')
        focal_target = bpy.context.scene.cursor.location.copy()

    init_lens = cam.data.lens
    init_pos = cam.matrix_world.translation.copy()

    ## Reposition the focal_target to stay centered on camera
    cam_forward_vec = Vector((0,0,-1))
    cam_forward_vec.rotate(cam.matrix_world)
    focal_target = intersect_line_plane(init_pos, init_pos + cam_forward_vec * 100000, focal_target, cam_forward_vec)
    if focal_target is None:
        print("Cannot find intersection point with target object on forward camera axis")
        return


    ## Compensated zoom
    cam.matrix_world.translation = calculate_dolly_zoom_position(
                            init_pos,
                            focal_target,
                            init_lens,
                            new_lens
                        )

    ## Assign the new lens
    cam.data.lens = new_lens


final_lens = 70

print(f"Lens {bpy.context.scene.camera.data.lens} -> {final_lens}")
dolly_zoom_to_lens(final_lens, target=bpy.context.scene.cursor.location)

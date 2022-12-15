## Align objects with view or camera. Set object rotation from a matrix

import bpy
from mathutils import Matrix, Vector
from math import pi

def get_scale_matrix(scale):
    '''Recreate a neutral mat scale'''
    matscale_x = Matrix.Scale(scale[0], 4,(1,0,0))
    matscale_y = Matrix.Scale(scale[1], 4,(0,1,0))
    matscale_z = Matrix.Scale(scale[2], 4,(0,0,1))
    matscale = matscale_x @ matscale_y @ matscale_z
    return matscale

def assign_rotation_from_ref_matrix(obj, ref_mat, rot_90=True):
    '''Assin rotation from a reference matrix to an object
    :obj: Object to modify
    :ref_mat: Matrix to get rotation from
    :rot_90: Add and extra 90 degree negative rotation on X axis
    Usefull when aligning with camera view so object keep facing front
    '''

    _ref_loc, ref_rot, _ref_scale = ref_mat.decompose()

    if obj.parent:
        mat = obj.matrix_world
    else:
        mat = obj.matrix_basis

    o_loc, _o_rot, o_scale = mat.decompose()

    loc_mat = Matrix.Translation(o_loc)

    if rot_90:
        mat_90 = Matrix.Rotation(-pi/2, 4, 'X')
        rot_mat = ref_rot.to_matrix().to_4x4() @ mat_90
    else:
        rot_mat = ref_rot.to_matrix().to_4x4()

    scale_mat = get_scale_matrix(o_scale)

    new_mat = loc_mat @ rot_mat @ scale_mat

    if obj.parent:
        obj.matrix_world = new_mat
    else:
        obj.matrix_basis = new_mat

    return new_mat


def align_objects_with_view(keep_z_up=False, find_viewport=False):
    '''Align selected objects with current view
    :keep_z_up: if True, keep object up aligned with world
    '''

    context = bpy.context

    if find_viewport:
        # if not in view 3D context, need to find a viewport in areas
        r3d = next((a.spaces.active.region_3d for a in context.screen.areas if a.type == 'VIEW_3D'), None)
        if not r3d:
            return
    else:
        # Assuming we are in view 3D context
        r3d = context.space_data.region_3d

    for ob in context.selected_objects:
        if keep_z_up:
            # Align to view but keep world Up
            Z_up_vec = Vector((0.0, 0.0, 1.0))
            aim = r3d.view_rotation @ Z_up_vec
            world_aligned_mat = aim.to_track_quat('Z','Y').to_matrix().to_4x4() # Track Up
            assign_rotation_from_ref_matrix(ob, world_aligned_mat)

        else:
            # Align to view
            view_matrix = r3d.view_matrix.inverted()
            assign_rotation_from_ref_matrix(ob, view_matrix)

def align_objects_with_camera(keep_z_up=False, cam=None):
    '''Align selected objects with camera
    :keep_z_up: if True, keep object up aligned with world
    :cam: Camera to use, if nothing passed use scene camera
    '''
    context = bpy.context
    cam = cam or context.scene.camera

    for ob in context.selected_objects:
        if keep_z_up:
            ## Align to camera but keep world Up
            Z_up_vec = Vector((0.0, 0.0, 1.0))
            aim = cam.matrix_world @ Z_up_vec
            world_aligned_mat = aim.to_track_quat('Z','Y').to_matrix().to_4x4() # Track Up
            assign_rotation_from_ref_matrix(ob, world_aligned_mat)
        
        else:
            ## Align to camera
            assign_rotation_from_ref_matrix(ob, cam.matrix_world)


## Align with view (To test from text editor, pass find_viewport to True)
align_objects_with_view(keep_z_up=False, find_viewport=False)

## Align with active camera
# align_objects_with_camera(keep_z_up=True)

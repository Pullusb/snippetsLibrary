## Get view direction string, top, left, etc. from r3d.view_matrix when aligned with world axis

import math

def get_aligned_orientation_string_from_view_matrix(view_matrix=None):
    """Get orientation string from view_matrix (UNDEFINED if not aligned with world axis)"""
    view_matrix = view_matrix or bpy.context.space_data.region_3d.view_matrix
    r = lambda x: round(x, 2)
    view_rot = view_matrix.to_euler()

    orientation_dict = {(0.0, 0.0, 0.0) : 'TOP',
                        (r(math.pi), 0.0, 0.0) : 'BOTTOM',
                        (r(-math.pi/2), 0.0, 0.0) : 'FRONT',
                        (r(math.pi/2), 0.0, r(-math.pi)) : 'BACK',
                        (r(-math.pi/2), r(math.pi/2), 0.0) : 'LEFT',
                        (r(-math.pi/2), r(-math.pi/2), 0.0) : 'RIGHT'}

    return orientation_dict.get(tuple(map(r, view_rot)), 'UNDEFINED')

print(get_view_orientation_from_matrix(bpy.context.space_data.region_3d.view_matrix))

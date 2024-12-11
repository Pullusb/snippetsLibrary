## Get Grease pencil object's canvas matrix

def get_gp_draw_plane_matrix(context):
    '''return matrix representing the drawing plane of the grease pencil object'''

    settings = context.scene.tool_settings
    orient = settings.gpencil_sculpt.lock_axis # 'VIEW', 'AXIS_Y', 'AXIS_X', 'AXIS_Z', 'CURSOR'
    loc = settings.gpencil_stroke_placement_view3d # 'ORIGIN', 'CURSOR', 'SURFACE', 'STROKE'
    mat = context.object.matrix_world if context.object else None

    draw_plane_mat = Matrix().to_3x3()

    # -> placement
    if loc == "CURSOR":
        plane_co = context.scene.cursor.location
    else: # ORIGIN (also on origin if set to 'SURFACE', 'STROKE')
        if not context.object:
            plane_co = None
        else:
            plane_co = context.object.matrix_world.to_translation() # context.object.location

    if not plane_co:
        return

    # -> orientation
    if orient == 'VIEW':
        draw_plane_mat.rotate(context.space_data.region_3d.view_rotation)

    elif orient == 'AXIS_Y': # front (X-Z) - Vector((0,1,0))
        draw_plane_mat = Matrix.Rotation(math.radians(90), 3, 'X')
        draw_plane_mat.rotate(mat)

    elif orient == 'AXIS_X': # side (Y-Z) - Vector((1,0,0))
        draw_plane_mat = Matrix.Rotation(math.radians(-90), 3, 'Y')
        draw_plane_mat.rotate(mat)

    elif orient == 'AXIS_Z': # top (X-Y) - Vector((0,0,1))
        draw_plane_mat.rotate(mat)

    elif orient == 'CURSOR':
        draw_plane_mat.rotate(context.scene.cursor.matrix)

    draw_plane_mat = draw_plane_mat.to_4x4()
    draw_plane_mat.translation = plane_co

    return draw_plane_mat

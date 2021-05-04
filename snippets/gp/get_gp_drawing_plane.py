def get_gp_draw_plane(context):
    ''' return tuple with plane coordinate and normal
    of the curent drawing according to geometry'''

    settings = context.scene.tool_settings
    orient = settings.gpencil_sculpt.lock_axis # 'VIEW', 'AXIS_Y', 'AXIS_X', 'AXIS_Z', 'CURSOR'
    loc = settings.gpencil_stroke_placement_view3d # 'ORIGIN', 'CURSOR', 'SURFACE', 'STROKE'
    mat = context.object.matrix_world if context.object else None

    # -> placement
    if loc == "CURSOR":
        plane_co = context.scene.cursor.location
    else: # ORIGIN (also on origin if set to 'SURFACE', 'STROKE')
        if not context.object:
            plane_co = None
        else:
            plane_co = context.object.matrix_world.to_translation()# context.object.location

    # -> orientation
    if orient == 'VIEW':
        plane_no = context.space_data.region_3d.view_rotation @ Vector((0,0,1))
        ## create vector, then rotate by view quaternion
        # plane_no = Vector((0,0,1))
        # plane_no.rotate(context.space_data.region_3d.view_rotation)

        ## only depth is important, can return None so region to location use same depth
        # plane_no = None

    elif orient == 'AXIS_Y': # front (X-Z)
        plane_no = Vector((0,1,0))
        plane_no.rotate(mat)

    elif orient == 'AXIS_X': # side (Y-Z)
        plane_no = Vector((1,0,0))
        plane_no.rotate(mat)

    elif orient == 'AXIS_Z': # top (X-Y)
        plane_no = Vector((0,0,1))
        plane_no.rotate(mat)

    elif orient == 'CURSOR':
        plane_no = Vector((0,0,1))
        plane_no.rotate(context.scene.cursor.matrix)

    return plane_co, plane_no
def location_to_region(worldcoords):
    from bpy_extras import view3d_utils
    return view3d_utils.location_3d_to_region_2d(bpy.context.region, bpy.context.space_data.region_3d, worldcoords)

def region_to_location(viewcoords, depthcoords):
    from bpy_extras import view3d_utils
    return view3d_utils.region_2d_to_location_3d(bpy.context.region, bpy.context.space_data.region_3d, viewcoords, depthcoords)

def vector_len_from_coord(a, b):
    '''get either two points or world coordinates and return length'''
    from mathutils import Vector    
    if type(a) is Vector:
        return (a - b).length
    else:   
        return (a.co - b.co).length

def get_stroke_length(s):
    '''return 3D total length of given GP stroke'''
    all_len = 0.0
    for i in range(0, len(s.points)-1):
        #print(vector_len_from_coord(s.points[i],s.points[i+1]))
        all_len += vector_len_from_coord(s.points[i],s.points[i+1])   
    return (all_len)

def get_stroke_2D_length(s):
    '''return 2D total length (relative to screen) of given GP stroke'''
    all_len = 0.0
    for i in range(0, len(s.points)-1):
        len_2D = vector_len_from_coord(location_to_region(s.points[i].co), location_to_region(s.points[i+1].co))
        all_len += len_2D
    return (all_len)
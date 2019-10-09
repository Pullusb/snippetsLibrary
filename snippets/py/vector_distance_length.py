def vector_len_from_coord(a, b):
    '''
    Get two points (that has coordinate 'co' attribute) or Vectors (2D or 3D)
    Return length as float
    '''
    from mathutils import Vector    
    if type(a) is Vector:
        return (a - b).length
    else:   
        return (a.co - b.co).length
from numpy import as np

def median_vector(vec_list):
    '''Get median vector from a list of vectors
    e.g: median_vector([ob.matrix_world @ co for co in ob_coordinates])
    '''
    return Vector(np.median(vec_list, axis=0))

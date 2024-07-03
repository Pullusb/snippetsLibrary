from numpy import as np

def mean_vector(vec_list):
    '''Get mean vector from a list of vectors
    e.g: mean_vector([ob.matrix_world @ co for co in ob_coordinates])
    '''
    return Vector(np.mean(vec_list, axis=0))

    ## Without numpy
    # n = Vector()
    # for v in vec_list:
    #     n += v
    # return n / len(vec_list)

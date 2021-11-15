## determine if vector are approximately close with a tolerance  
def is_vector_close(a, b, rel_tol=1e-03):
    '''compare Vector or sequence of value
    by default tolerance is set on 1e-03 (0.001)'''
    return all([math.isclose(i, j, rel_tol=rel_tol) for i, j in zip(a,b)])
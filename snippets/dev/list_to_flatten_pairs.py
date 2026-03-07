## Utils for gpu draw, transform a list of continuous coordinate to a flatten list of segment pair coordinate

def to_flatten_pairs(v_list, closed=True) -> list:
    """Take a sequence of item (vector, vertices), return a lists of flattened pairs.
    ex: for continuous coordinate, return segments pairs, result is usable with gpu_shader 'LINES'

    v_list (list): List of coordinates [a,b,c]
    closed (bool): 
        True return  [a,b,b,c,c,a] (add segment closing last to first coordinate)
        False return [a,b,b,c]
    """
    loop = []
    for i in range(len(v_list) - 1):
        loop += [v_list[i], v_list[i + 1]]
    if closed:
        # Add segment between last and first to close loop
        loop += [v_list[-1], v_list[0]]
    return loop

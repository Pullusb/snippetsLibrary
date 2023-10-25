## Invert a python dictionary

def invert_dict(d):
    '''Invert a dictionary
    values become keys, keys are inserted in a list of values
    This allow to store in list when somes keys initially had the same value (since keys are unique)

    New dict has this shape (here key1 and key2 had same value val2):
    val1 : [key0]
    val2 : [key1, key2]
    '''

    inverted_dict = {}
    for k, v in d.items():
        inverted_dict.setdefault(v, []).append(k)
    return inverted_dict

def invert_dict_strict(d):
    '''Invert a dictionary
    Return None if multiple keys have the same vvalue in initial dict 
    '''

    if len(d) != len(set(d.values())):
        return None

    return {v: k for k, v in d.items()}

def get_collection_childs_recursive(col, cols=[]):
    '''return a list of all the sub-collections in passed col'''
    for sub in col.children:
        if sub not in cols:
            cols.append(sub)
        if len(sub.children):
            cols = get_collection_childs_recursive(sub, cols)
    return cols

def get_parents_cols(col, root=None, cols=[]):
    '''Return a list of parents collections of passed col
    root : Pass a collection to search in (recursive)
    else search in master collection
    '''
    if root == None:
        root=bpy.context.scene.collection

    for sub in root.children:
        if sub == col:
            cols.append(root)

        if len(sub.children):
            cols = get_parents_cols(col, root=sub, cols=cols)
    return cols

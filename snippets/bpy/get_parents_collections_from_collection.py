def get_parents_cols(col, root=None, scene=None, cols=None):
    '''Return a list of parents collections of passed col
    root : Pass a collection to search in (recursive)
        Else search in master collection
    scene: scene to search in (active scene if not passed)
    cols: used internally by the function to collect results
    '''
    if cols is None:
        cols = []
        
    if root == None:
        scn = scene or bpy.context.scene
        root=scn.collection

    for sub in root.children:
        if sub == col:
            cols.append(root)

        if len(sub.children):
            cols = get_parents_cols(col, root=sub, cols=cols)
    return cols

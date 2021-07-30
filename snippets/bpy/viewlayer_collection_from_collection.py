def get_view_layer_col(col, vl_col=None):
    '''return viewlayer collection from collection'''
    if vl_col is None:
        vl_col = bpy.context.view_layer.layer_collection
    for sub in vl_col.children:
        if sub.collection == col:
            return sub
        if len(sub.children):
            return get_view_layer_col(col, sub)

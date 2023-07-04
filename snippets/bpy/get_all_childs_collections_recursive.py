## Get all children collection recursively

def get_collection_children_recursive(col, cols=None) -> list:
    '''return a list of all the child collections
    and their subcollections in the passed collection'''

    cols = cols or [] 
    for sub in col.children:
        if sub not in cols:
            cols.append(sub)
        if len(sub.children):
            cols = get_collection_children_recursive(sub, cols)
    return cols

# get_collection_children_recursive(bpy.context.scene.collection)

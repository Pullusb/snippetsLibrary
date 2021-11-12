## Object included in on layer collection
import bpy

def get_collection_childs_recursive(col, cols=[], include_root=True):
    '''return a list of all the sub-collections in passed col'''
    # force start from fresh list (otherwise same cols list is used at next call)
    cols = cols or []

    for sub in col.children:
        if sub not in cols:
            cols.append(sub)
        if len(sub.children):
            cols = get_collection_childs_recursive(sub, cols)

    if include_root and col not in cols: # add root
        cols.append(col)

    return cols


def is_render_included(o, scn):
    '''return True if object is in at least one non-excluded collection
    in all passed scene viewlayer
    '''

    if o.hide_render:
        return False
    for vl in scn.view_layers:
        all_cols = get_collection_childs_recursive(vl.layer_collection, include_root=True)
        for c in all_cols:
            print(c.name)
            if o in c.collection.objects[:]:
                if not c.exclude:
                    return True
    return False

scn = bpy.context.scene
cube = bpy.data.objects.get('Cube')
if cube:
    print(is_render_included(cube, scn))
## Handler to save window_manager props to scene props when saving and inverse when loading
## This allow to have fast properties that do not trigger a scene refresh when edited, but are still stored in scene.

import bpy
from bpy.app.handlers import persistent

""" TODO: find a clean way to recursively replicate a collection property
def recursive_crawl(d): WIP
    if isinstance(d, dict):
        for k, v in d.items():
            print(k, ':')
            recursive_crawl(v)

    elif isinstance(d, list):
        # print(d, 'is a list')
        for item in d:
            recursive_crawl(item)
    else:
        print(d)
"""

def transfer_properties(a, b):
    for pr in a.bl_rna.properties:
        if pr.is_readonly or pr.identifier == 'name':
            continue
        setattr(b, pr.identifier, getattr(a, pr.identifier))

    for pr in a.bl_rna.properties:
        if pr.type == 'COLLECTION':
            ## Replicate collection items values
            a_col = a.path_resolve(pr.identifier)
            b_col = b.path_resolve(pr.identifier)
            b_col.clear()
            for a_item in a_col:
                b_item = b_col.add()
                for k, v in dict(a_item).items():
                    setattr(b_item, k, v)
            continue

        if pr.is_readonly or pr.name == 'Name':
            ## Skip readonly attributes or the default "Name"
            # print('SKIP:', pr.identifier, pr.type) # Dbg
            continue

        setattr(b, pr.identifier, getattr(a, pr.identifier))

@persistent
def transfer_scn_to_win(dummy):
    scn_props = bpy.context.scene.my_prop_group
    win_props = bpy.context.window_manager.my_prop_group
    transfer_properties(scn_props, win_props)

@persistent
def transfer_win_to_scn(dummy):
    scn_props = bpy.context.scene.my_prop_group
    win_props = bpy.context.window_manager.my_prop_group
    transfer_properties(win_props, scn_props)


def register():
    bpy.app.handlers.load_post.append(transfer_scn_to_win)
    bpy.app.handlers.save_pre.append(transfer_win_to_scn)

def unregister():
    bpy.app.handlers.save_pre.remove(transfer_win_to_scn)
    bpy.app.handlers.load_post.remove(transfer_scn_to_win)

## Dump mesh triangles (tesselated) as flattened text coordinate

import bpy
from mathutils.geometry import tessellate_polygon
# from pprint import pprint as pp


def get_triangles_coords(obj, selected_only=False, apply_transforms=False):
    '''return triangle coordinates as flattened list'''
    dg = bpy.context.evaluated_depsgraph_get()
    eval_ob = obj.evaluated_get(dg)
    tris = []
    for poly in eval_ob.data.polygons:
        if selected_only and not poly.select:
            continue
        vertices = [eval_ob.data.vertices[i] for i in poly.vertices]
        coords = [v.co for v in vertices]
        if apply_transforms:
            coords = [eval_ob.matrix_world @ co for co in coords]
        
        ## Get indices of tesselated coords
        for tri_idx in tessellate_polygon([coords]):
            # Extend with tri coordinates
            tris += [coords[i] for i in tri_idx]

    # pp(tris)
    return tris

def dump_object_xy_tris(obj, coord_2d=True, as_vector=False, multiplier=None) -> str:
    '''Get object tris as text, of 2D coordinates flatenned on XY
    Can be used to get coordinate to trace from
    '''
    tris = get_triangles_coords(obj)
    
    ## Multiply by a factor
    if multiplier is not None:
        tris = [co * mult for co in tris]

    text = []
    for i in range(0, len(tris)-1, 3):
        ## Create text, convert int (equivalent to floor)
        if coord_2d:
            if as_vector:
                text.append(f'Vector(({tris[i].x:.0f}, {tris[i].y:.0f})), Vector(({tris[i+1].x:.0f}, {tris[i+1].y:.0f})), Vector(({tris[i+2].x:.0f}, {tris[i+2].y:.0f})),')
            else:
                ## As Tuple
                text.append(f'({tris[i].x:.0f}, {tris[i].y:.0f}), ({tris[i+1].x:.0f}, {tris[i+1].y:.0f}), ({tris[i+2].x:.0f}, {tris[i+2].y:.0f}),')
        else:
            if as_vector:
                text.append(f'Vector(({tris[i].x:.0f}, {tris[i].y:.0f}, {tris[i].z:.0f})), Vector(({tris[i+1].x:.0f}, {tris[i+1].y:.0f}, {tris[i+1].z:.0f})), Vector(({tris[i+2].x:.0f}, {tris[i+2].y:.0f}, {tris[i+2].z:.0f})),')
            else:
                ## As Tuple
                text.append(f'({tris[i].x:.0f}, {tris[i].y:.0f}, {tris[i].z:.0f}), ({tris[i+1].x:.0f}, {tris[i+1].y:.0f}, {tris[i+1].z:.0f}), ({tris[i+2].x:.0f}, {tris[i+2].y:.0f}, {tris[i+2].z:.0f}),')

    ltext = '\n    '.join(text)
    var_text = f'''{obj.name} = [
    {ltext}
]'''
    return var_text

## Pixel multiplier
## At 10, one blender unit is 10px long
mult = 10

full = []
for o in bpy.context.selected_objects:
    if o.type != 'MESH':
        continue
    full.append(dump_object_xy_tris(o, coord_2d=True, multiplier=mult))

bpy.context.window_manager.clipboard = '\n\n'.join(full)

## Dump mesh edges to lines coordinate list of vector pairs, as string to clipboard

import bpy
from mathutils import Vector

C = bpy.context
D = bpy.data
scn = bpy.context.scene

## Pixel multiplier
## At 10, one blender unit is 10px long
mult = 1


def dump_edges(ob, decimal=7, evaluated=True, as_vector2=False, multiplier=1) -> str:
    """Mesh edges as a flat list of vector pair coordinates
    
    Args:
        ob: Object to get edge from (has to be of mesh type)
        decimal: How many decimals to keep (ex: 2 -> 1.23). Note: with simple print, Blender show 16 decimals 
        evaluated: Wether to evaluate mesh after enabled modifiers are applied
        as_vector2: Keep only xy coordinate (e.g: usefull to trace icons)
        multiplier: Multiplier for the coordinates
            useful in 2D mode(as_vector2). At 10, one blender unit is 10px long
        
    Example:
        For an 2d output like an icon, set as_vector2 to True, a multipllier of 20, with decimal to 0

    Return:
        String representation of the list with name of object as assigned variable
    """
    if evaluated:
        ## Work on evaluated object (after modifiers are applied)
        dg = bpy.context.evaluated_depsgraph_get()
        mesh_eval = ob.evaluated_get(dg)
        me = mesh_eval.to_mesh()
    else:
        ## work on basse object
        me = ob.data

    lines = []
    ## list edge pair vertices.coord 
    for edge in me.edges:
        for idx in edge.vertices:
            if as_vector2:
                lines.append(
                [me.vertices[idx].co[0] * multiplier, me.vertices[idx].co[1] * multiplier] # add as sublist
                    )
            else:
                lines.append(
                [me.vertices[idx].co[0] * multiplier, me.vertices[idx].co[1] * multiplier, me.vertices[idx].co[2] * multiplier] # add as sublist
                    )

    text = []

    if as_vector2:
        ## list on by one
        #for l in lines:
        #    text.append(f'Vector(({l[0]:.{decimal}f}, {l[1]:.{decimal}f})),' )
        ## list two by two
        for i in range(0, len(lines)-1, 2):
            text.append(f'Vector(({lines[i][0]:.{decimal}f}, {lines[i][1]:.{decimal}f})), Vector(({lines[i+1][0]:.{decimal}f}, {lines[i+1][1]:.{decimal}f})),' )
    else:
        ## list on by one
        #for l in lines:
        #    text.append(f'Vector(({l[0]:.{decimal}f}, {l[1]:.{decimal}f}, {l[2]:.{decimal}f})),' )
        ## list two by two
        for i in range(0, len(lines)-1, 2):
            text.append(f'Vector(({lines[i][0]:.{decimal}f}, {lines[i][1]:.{decimal}f}, {lines[i][2]:.{decimal}f})), Vector(({lines[i+1][0]:.{decimal}f}, {lines[i+1][1]:.{decimal}f}, {lines[i+1][2]:.{decimal}f})),')

    ## join text with indent
    ltext = '\n    '.join(text)

    ## add variable
    var_text = f'''{ob.name} = [
    {ltext}
]'''

    return var_text

full = []
for o in C.selected_objects:
    if o.type != 'MESH':
        continue
    full.append( dump_edges(o, decimal=4, evaluated=True, as_vector2=False, multiplier=mult) )

C.window_manager.clipboard = '\n\n'.join(full)

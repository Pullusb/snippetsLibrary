## Dump mesh edges to lines coordinate

import bpy
from mathutils import Vector

C = bpy.context
D = bpy.data
scn = bpy.context.scene

## Pixel multiplier
## At 10, one blender unit is 10px long
mult = 20

def dump_edges(ob):
    me = ob.data
    lines = []
    ## list edge pair vertices.coord 
    for edge in me.edges:
        for idx in edge.vertices:
            lines.append(
            # Vector(me.vertices[idx].co[:2]) # add as Vector2
            [me.vertices[idx].co[0] * mult, me.vertices[idx].co[1] * mult] # add as sublist
                )

    text = []

    ## list on by one
    #for l in lines:
    #    text.append( f'Vector(({l[0]:.0f}, {l[1]:.0f})),' )

    ## list two by two
    for i in range(0, len(lines)-1, 2):
        text.append( f'Vector(({lines[i][0]:.0f}, {lines[i][1]:.0f})), Vector(({lines[i+1][0]:.0f}, {lines[i+1][1]:.0f})),' )

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
    full.append( dump_edges(o) )

C.window_manager.clipboard = '\n\n'.join(full)

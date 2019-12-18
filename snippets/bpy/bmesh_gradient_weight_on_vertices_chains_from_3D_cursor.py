import bpy
from mathutils import Vector, Matrix
import bmesh
C = bpy.context

'''
Assumes we have a mesh object selected

Make a gradient weight assignation (on active vertex_group)
on each vertices "chain"
starting drom the tip closer to 3D cursor
'''

def transfer_value(Value, OldMin, OldMax, NewMin, NewMax):
    '''map a value from a range to another (transfer/translate value)'''
    return (((Value - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

ob = C.object
M = ob.matrix_world

# Get the active mesh
me = ob.data

## get active group
#C.vertex_groups.active_index

if ob.type != 'MESH':
    print('ERROR : not a mesh')

mode = bpy.context.mode

if mode == 'EDIT_MESH':
    #me = bpy.context.edit_object.data
    bm = bmesh.from_edit_mesh(me) #get Bmesh from edit

elif mode == 'OBJECT':
    bm = bmesh.new()   # create an empty BMesh
    bm.from_mesh(me)   # fill it in from a Mesh

bm.verts.ensure_lookup_table()
bm.edges.ensure_lookup_table()
bm.faces.ensure_lookup_table()

#deselect everything first
for f in bm.edges:f.select = False
for e in bm.edges:e.select = False
for v in bm.verts:v.select = False


# Modify the BMesh, can do anything here...
chunks = []
sc = 1
ec = 0
for v in bm.verts:
    v.select_set(False)
    #v.co.x += 1.0
    if len(v.link_edges) == 1:#vertices chain tip
        #sc+=1
        #if sc == 2:
        #    sc = 0
        chunks.append(v.index)

if len(chunks)%2 != 0:
    print("list not pair")

for i in chunks:
    bm.verts[i].select_set(True)

n = 2
pairs = [chunks[i:i + n] for i in range(0, len(chunks), n)]
#print("pairs", pairs)#Dbg
vlists = []
cursorloc = bpy.context.scene.cursor.location
for p in pairs:
    vlen = p[1] - p[0]#number of vertices in chunk
    #get_closest to 3d cursor
    if (cursorloc - M @ bm.verts[p[0]].co).length < (cursorloc - M @ bm.verts[p[1]].co).length:
        print(f'{p[0]} to {p[1]}')
        bm.verts[p[1]].select = False
        vlists.append( [i for i in range(p[0], p[1]+1)] )

    else:# Last point is closer to cursor (so invert direction)
        print(f'{p[1]} to {p[0]}')
        bm.verts[p[0]].select = False
        vlists.append( [i for i in reversed(range(p[0], p[1]+1))] )


if mode == 'EDIT_MESH':
    bmesh.update_edit_mesh(me, True)    

elif mode == 'OBJECT':
    bm.to_mesh(me)
    bm.free()


# tweak vertex group (need to be in object mode)

'''
## classic progressive
for vl in vlists:
    vnum = len(vl)
    for i, vid in enumerate(vl):
        weight = i/vnum# progressive
        weight = abs(weight-1)# reverse
        weight = transfer_value(weight, 0, 1, 0.8, 1)# clamp between two value
        C.object.vertex_groups.active.add([vid], weight, "REPLACE")
'''

## with a divider to limit
## ex with 5 points:
##   divider 2 : 0, 0, 0 , 0.5, 1.0
##   divider 3 : 0, 0, 0.33 , 0.66, 1.0

percentage = 0.2 #(0 for full progressive)
#divider = 3
for vl in vlists:
    vnum = len(vl)
    # limit = int(vnum/divider)
    limit = int(vnum*percentage)
    rest = vnum - limit

    for i, vid in enumerate(vl):
        #weight = i/vnum
        w = weight = (i - limit)/(vnum-limit-1)
        if weight < 0: weight=0

        weight = abs(weight-1)#reverse
        weight = transfer_value(weight, 0, 1, 0.8, 1)# clamp between two last value
        print(i, w, "->", weight)#Dbg
        C.object.vertex_groups.active.add([vid], weight, "REPLACE")

    print("vnum", vnum)#Dbg
    print("limit", limit)#Dbg
    print("rest", rest)#Dbg
    print("full", rest + limit)#Dbg

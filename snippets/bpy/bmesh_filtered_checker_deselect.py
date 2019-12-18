# coding: utf-8
import bpy
import bmesh

ob = bpy.context.object
me = ob.data

bm = bmesh.new()   # create an empty BMesh
bm.from_mesh(me)   # fill it in from a Mesh

bm.verts.ensure_lookup_table()
bm.edges.ensure_lookup_table()
bm.faces.ensure_lookup_table()

#deselect everything first
for f in bm.edges:f.select = False
for e in bm.edges:e.select = False
for v in bm.verts:v.select = False

#Checker deselect on each separate mesh portion
ct = 0
for v in bm.verts:
    ct+=1
    if len(v.link_edges) == 1:#star/end of chain
        # v.select_set(False)#already deselected
        ct = 0#reset ct for next
    else:
        print(v.index, 'select', ct%2)
        v.select_set(ct%2)

bm.to_mesh(me)
bm.free()

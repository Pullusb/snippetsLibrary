# coding: utf-8
import bpy
import bmesh
from math import degrees, radians

ob = bpy.context.object
me = ob.data

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

#keep vertex that mark angle above this degree tolerance
degree_tolerance = 20 
tol = radians(degree_tolerance)

#Checker
ct = 0
for v in bm.verts:
    if len(v.link_edges) == 2:#star/end of chain
        if v.calc_edge_angle() < tol:
            #v.select_set(True)#full select
            v.select_set(ct%2)#checker select
        else:
            ct = 0#reset counter
    ct+=1

if mode == 'EDIT_MESH':
    bmesh.update_edit_mesh(me, True)    

elif mode == 'OBJECT':
    bm.to_mesh(me)
    bm.free()
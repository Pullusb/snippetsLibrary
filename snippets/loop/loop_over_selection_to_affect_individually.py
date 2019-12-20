## Do ops/data actions on individual objects in selection, loop and edit one by one

import bpy

def do_the_thing(ob):
    """Do things in edit mode on each selected object"""
    # eg: Verts border to sphere
    bpy.ops.mesh.select_all(action='SELECT')# MESH
    bpy.ops.mesh.region_to_loop()# select border
    bpy.ops.transform.tosphere(value=1, mirror=True)# to sphere
    #bpy.ops.mesh.select_all(action='INVERT')    
    #bpy.ops.mesh.dissolve_verts()


### --- loop in selection, go in edit and do the thing

pool = bpy.context.selected_objects# get selection

## Deselect everything
bpy.ops.object.select_all(action='DESELECT')# ops way
# for ob in pool:ob.select_set(True)# data way

## iterate
for ob in pool:
    # current_active = bpy.context.view_layer.objects.active
    bpy.context.view_layer.objects.active = ob# change active
    ob.select_set(True)# select_it
    bpy.ops.object.mode_set(mode='EDIT')# go in edit

    do_the_thing(ob)# do things in edit (no need for function but more clear)

    bpy.ops.object.mode_set(mode='OBJECT')# back to object
    ob.select_set(False)# deselect before going to next


for ob in pool:ob.select_set(True)# Reselect
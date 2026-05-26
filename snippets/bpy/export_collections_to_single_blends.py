## Export collections to single blend files using library write method

import bpy
import os

# --- config ---
scene = bpy.context.scene # bpy.data.scenes[scene_name]
output_dir = bpy.path.abspath(r"//collections/")
print("output_dir", output_dir)#Dbg

## Create output direcrories
os.makedirs(output_dir, exist_ok=True)

def has_linked_objects(coll):
    """True if the collection (or any of its sub-collections) holds a linked object."""
    return any(obj.library is not None for obj in coll.all_objects)

## Export all top-level collections of active scene.
target_colls = scene.collection.children

## Exporting all collections in bldn, skipping any nested collections.
# child_collections = set()
# for c in bpy.data.collections:
#     child_collections.update(c.children)
# target_colls = [c for c in bpy.data.collections if c not in child_collections]

## Only export datablock (not linked in any scene)
#for coll in target_colls:
#    filepath = os.path.join(output_dir, f"{coll.name}.blend")

#    bpy.data.libraries.write(
#        filepath,
#        {coll},              # a set; Blender writes the collection + all its dependencies
#        path_remap='RELATIVE',
#        fake_user=True,      # so the collection survives even with no other user in the new file
#        compress=True,
#    )
#    print(f"Wrote {filepath}")

## Export the collections to blends linked into a scene (same name as collection)
for coll in target_colls:
    ## Skip collection containing linked object (do not consider lib override and linked instance)
    # if has_linked_objects(coll):
    #     print(f'Skip {coll.name}: contains linked objects')
    #     continue

    # build a temporary scene that holds just this collection    
    tmp_scene = bpy.data.scenes.new(coll.name)
    tmp_scene.collection.children.link(coll)

    filepath = os.path.join(output_dir, f"{coll.name}.blend")

    # writing the scene pulls in the collection + all its dependencies
    bpy.data.libraries.write(
        filepath,
        {tmp_scene},
        path_remap='RELATIVE',
        fake_user=False,
        compress=True,
    )
    print(f"Wrote {filepath}")

    # clean up so the temp scene doesn't pile up in your working file
    bpy.data.scenes.remove(tmp_scene)

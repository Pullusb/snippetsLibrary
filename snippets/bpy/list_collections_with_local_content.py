## Check if a collection has linked content.
## Detect if there are linked objects in collection.

import bpy

def collection_has_linked_content(coll):
    """True if the collection (or any sub-collection) holds linked data:
    directly linked objects, library overrides, or instanced linked collections.
    Returns the reason string, or None if the collection is fully local.
    """
    # 1. Linked objects + library overrides on objects.
    #    all_objects walks the full hierarchy, so nested cases are caught too.
    for obj in coll.all_objects:
        if obj.library is not None:
            return f"linked object {obj.name!r}"
        if obj.override_library is not None:
            return f"override object {obj.name!r}"
        # 3. Empty (or any object) instancing a linked collection.
        inst = obj.instance_collection
        if inst is not None and (
            inst.library is not None or inst.override_library is not None
        ):
            return f"object {obj.name!r} instances linked collection {inst.name!r}"

    # 2. Linked / overridden sub-collections in the hierarchy.
    #    children_recursive covers the whole nested tree.
    for sub in coll.children_recursive:
        if sub.library is not None:
            return f"linked sub-collection {sub.name!r}"
        if sub.override_library is not None:
            return f"override sub-collection {sub.name!r}"

    return None


## Only top level collections:
# target_colls = scene.collection.children

# All non-nested collection in file:
child_collections = {c.children for c in bpy.data.collections}
for c in bpy.data.collections:
    child_collections.update(c.children)
target_colls = [c for c in bpy.data.collections if c not in child_collections]


print('\n\n-*-')
local_collections = []
for coll in target_colls:
    if (reason := collection_has_linked_content(coll)) is not None:
        print(f"Skipping {coll.name!r} ({reason})")
        continue
    local_collections.append(coll)

print('\n*collections containing local asset only*')
for coll in local_collections:
    print(coll.name)

def link_collection(filepath, coll_name, link=True):
    '''Link a collection by name from a file, if link is False, append instead of linking'''
    # append, set to true to keep the link to the original file

    # link all collections starting with 'MyCollection'
    with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
        data_to.collections = [c for c in data_from.collections if c.startswith(coll_name)]

    # link collection to scene collection
    for coll in data_to.collections:
        if coll is not None:
            bpy.context.scene.collection.children.link(coll)

    return data_to.collections

link_collection(r'path/to/the_file.blend', 'collection_name', link=True)
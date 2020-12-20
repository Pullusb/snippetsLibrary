def link_collection_ops(blend, collec_name):
    # link a collection  an empty with an ops
    import os
    directory, filename = os.path.split(blend)
    collections_path = os.path.join(blend, 'Collection')

    if not os.path.exists(blend):
        print(f'Impossible to find ref source : {blend}')
        return {"CANCELLED"}


    ## make a collection active to link in it
    # bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[col.name]

    #filepath not needed (provide filename as in one example but works without it...)
    ret = bpy.ops.wm.link(filepath=filename, directory=collections_path, filename=collec_name, files=[],
    filemode=1, relative_path=True, link=True, autoselect=False, active_collection=True, instance_collections=True)

    if 'FINISHED' in ret:
        lib_obj = bpy.data.objects.get(collec_name) # empty obj instanciating the collection
        if lib_obj:
            return lib_obj

## better to use data method
link_collection_ops(blend = r'path/to/the_file.blend',
                    collec_name = 'the_collection_name')
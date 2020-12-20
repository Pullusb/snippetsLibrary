def link_by_name(filepath, any_list=[], all_list=[], exclude_list=[], only_one=True):
    '''
    link collections from blend given in filepath with name filters.
    Filter For a colection to be linkable:
    any_list : at least one string in list has to be found in collection's name
    all_list : all strings in list must be found in collection's name
    exclude_list : nothing in list must be found in collection's name
    only_one : if True (default) return after first valid collection encountered
    else link all valid collection
    '''

    existing_instances = [
        o.name for o in bpy.context.scene.objects if o.type == 'EMPTY' and o.instance_collection]

    print('- look for col to link')
    with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
        for name in data_from.collections:
            print('-', name)
            # print('any_list', any_list, any(x.lower() in name.lower() for x in any_list))
            # print('all_list', all_list, all(x.lower() in name.lower() for x in all_list))
            # print('exclude_list', exclude_list, any(x.lower() in name.lower() for x in exclude_list))

            if name in existing_instances:
                print(f'  - {name} already exists in file')
                continue

            if any_list and not any(x.lower() in name.lower() for x in any_list):
                continue

            if all_list and not all(x.lower() in name.lower() for x in all_list):
                continue

            if exclude_list and any(x.lower() in name.lower() for x in exclude_list):
                continue

            data_to.collections.append(name)
            if only_one:
                break

    if not len(data_to.collections):
        print(
            'ERROR', f'No collection found with filters : any:{any_list}, all:{all_list}, exclude:{exclude_list}')
        return

    for new_col in data_to.collections:
        print(f'- linking {new_col.name}')

        ## direct linking (work fine too)
        # parent_col.children.link(new_col)

        ## link and instance
        ob = bpy.data.objects.new(new_col.name, None)  # create an Empty
        bpy.context.scene.collection.objects.link(ob)
        ob.select_set(True)
        bpy.context.view_layer.objects.active = ob
        ob.instance_type = 'COLLECTION'
        ob.instance_collection = new_col
        ob.empty_display_size = 0.05

    ## optionally make all path relative on file (depending on the need)
    # bpy.ops.file.make_paths_relative()


link_by_name('path/to/blend',
             any_list=['chaussure', 'basket'], all_list=[],
             exclude_list=['_test', '_trash'], only_one=True)
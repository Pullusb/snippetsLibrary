## remove end numbering in object name and object data if possible

import bpy, re

def rename_data(ob):
    '''Delete end numbering in object data name if possible
    if single user, rename after object if possible
    '''

    if ob.type == 'EMPTY':
        return

    dt = ob.data
    # get data group - method 1
    cat = repr(dt).split('[')[0].split('.')[-1] # return 'meshes'
    datagroup = bpy.data.path_resolve(cat)

    ## for non Multi-user data,just pick name of the object if possible
    if dt.users == 1 and dt.name != ob.name and ob.name not in datagroup:
        f'{dt.rna_type.identifier} data: {dt.name} >> {ob.name} (same as object)'
        dt.name = ob.name
        return

    if ob.name == dt.name:
        return

    # else just try to rmeove number in name
    new = re.sub(r'\.\d{3}$', '', dt.name)
    if dt.name != new:
        if not new in datagroup:
            print(f'{dt.rna_type.identifier} data: {dt.name} >> {new}')
            dt.name = new
        else:
            print(f'Skip data: {dt.rna_type.identifier} data: {dt.name} ({dt.users} users): {new} already exists ')

def remove_end_numbering(ob, data_rename=True, skip_multi_user_objs=False):
    '''remove 3 digit numbering in object end, if possible'''

    if skip_multi_user_objs and len(ob.users_scene) > 1:
        print('skip obj:', ob.name, len(ob.users_scene))
        # if data_rename:
        #     rename_data(ob)
        return

    new = re.sub(r'\.\d{3}$', '', ob.name)    
    if ob.name != new and not new in bpy.context.scene.objects:
        print(f'{ob.name} >> {new}')
        ob.name = new

    if data_rename:
            rename_data(ob)

for o in bpy.context.scene.objects:
    remove_end_numbering(o)
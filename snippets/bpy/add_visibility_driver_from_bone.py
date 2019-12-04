## create visibility on objects or armature selection from a bone of a rig ##
import bpy

def add_driver(source, target, prop, dataPath, index = -1, negative = False, func = ''):
    ''' Add driver to source prop (at index), driven by target dataPath '''

    source.driver_remove(prop, index)
    if index != -1:
        d = source.driver_add( prop, index ).driver
    else:
        d = source.driver_add( prop ).driver

    v = d.variables.new()
    v.targets[0].id        = target
    v.targets[0].data_path = dataPath

    d.expression = func + "(" + v.name + ")" if func else v.name
    d.expression = d.expression if not negative else "-1 * " + d.expression

def create_hide_custom_prop(src_object, prop_name, prop_bone = ''):
    '''
    add source propertie with boolean option
    place the hide prop on src_object with name prop_name
    '''

    rig = bpy.data.objects.get(src_object)
    if not rig:
        print(f"No objects named {src_object}")
        return 1
    if rig.type != 'ARMATURE':
        print(f"Not an armature : {src_object}")
        return 1

    #add target bone
    if prop_bone:
        holder = rig.pose.bones.get(prop_bone)
    else:
        holder = rig.pose.bones.get('root')

    if not holder:
        print(f'problem finding bone {prop_bone} (or root)')
        return 1

    # create
    if not holder.get('_RNA_UI'):
        holder['_RNA_UI'] = {}

    if not prop_name in holder.keys() :
        holder[prop_name] = 0
        holder['_RNA_UI'][prop_name] = {"default": 0,"min":0,"max":1,"soft_min":0,"soft_max":1}
    else:
        print(f'{prop_name} : already exists on root key')
        return

    return 0

def drive_selection_visibility(rig, prop_name, prop_bone = ''):
    # add driver on selection
    prefixs = ('MCH','DEF','ORG', 'WGT')

    rig = bpy.data.objects.get(src_object)
    if not rig:
        print(f"No objects named {src_object}")
        return 1
    if rig.type != 'ARMATURE':
        print(f"Not an armature : {src_object}")
        return 1

    #add target bone

    if not prop_bone:
        prop_bone = 'root'
    if not rig.pose.bones.get(prop_bone):
        print(f'no bones {prop_bone} on rig {rig.name}')
        return 1

    meshes = [i for i in bpy.context.selected_objects if i.type in ('MESH','CURVE','TEXT') and not i.name.startswith(('WGT', 'WDGT'))]
    armatures = [i for i in bpy.context.selected_objects if i.type == 'ARMATURE']

    if bpy.context.mode == 'POSE':
        obarm = bpy.context.active_object
        for bone in bpy.context.selected_pose_bones_from_active_object:
            prop = 'bones["%s"].hide'%bone.name
            index = -1
            layer = bone.bone.layers
            protect_layer = rig.data.layers_protected
            ### dont check for protected, strictly use selection.
            # if bone.name.startswith(prefixs) or any([i==j==1 for i,j in zip(layer,protect_layer)]) :
            #     print(f'Skipped : Prefixed or protected bone : {bone.name}')
            #     rig.data.driver_remove(prop, index)
            #     continue
            print(f'New : Driver on bone {bone.name}')
            add_driver(obarm.data, rig, prop, f'pose.bones["{prop_bone}"]["{prop_name}"]', index)
        return

    for ob in meshes :
        print('Object : ', obarm.name)

        add_driver(ob, rig, 'hide_viewport', f'pose.bones["{prop_bone}"]["{prop_name}"]', -1)
        add_driver(ob, rig, 'hide_render', f'pose.bones["{prop_bone}"]["{prop_name}"]', -1)

    for obarm in armatures:
        print('Armature : ', obarm.name)
        ## mask armature object
        ## add_driver(obarm, rig, 'hide_viewport', f'pose.bones["{prop_bone}"]["{prop_name}"]', -1)
        ## bette mask pose bones since its a proxy...
        for bone in obarm.pose.bones :
            prop = 'bones["%s"].hide'%bone.name
            index = -1
            layer = bone.bone.layers
            protect_layer = rig.data.layers_protected
            if bone.name.startswith(prefixs) or any([i==j==1 for i,j in zip(layer,protect_layer)]) :
                print(f'Skipped : Prefixed or protected bone : {bone.name}')
                rig.data.driver_remove(prop, index)
            else :
                print(f'New : Driver on bone {bone.name}')
                add_driver(obarm.data, rig, prop, f'pose.bones["{prop_bone}"]["{prop_name}"]', index)

### ---- 

## write the name of the rig source (will put the propertie on the root of this armature)
prop_rig = 'name_of_the_rig'

## write the name of the propertie to attach
prop_name = "hide_something"#'hide_headband'

## prop_bone (bone holding the propertie), 'root' if left string empty.
prop_bone = ''


create_hide_custom_prop(prop_rig, prop_name, prop_bone = prop_bone)
drive_selection_visibility(prop_rig, prop_name, prop_bone = prop_bone)
## Dump matrices of objects relative to a bone space and apply on another one

import bpy
import mathutils
import json

### Convert an object matrix to bone space

def convert_attr(Attr):
    '''Convert given value to a Json serializable format'''
    if isinstance(Attr, (mathutils.Vector,mathutils.Color)):
        return Attr[:]
    elif isinstance(Attr, mathutils.Matrix):
        return [v[:] for v in Attr]
    elif isinstance(Attr,bpy.types.bpy_prop_array):
        return [Attr[i] for i in range(0,len(Attr))]
    else:
        return(Attr)

obj = bpy.data.objects['char_rig']
ref_bone = obj.pose.bones["hips"]

scn = bpy.context.scene

d = {}
for i in range(scn.frame_start, scn.frame_end+1):
    # scn.frame_current = i
    scn.frame_set(i) # actually refresh

    ob_dict = {}
    ## using selection
    for ob in bpy.context.selected_objects:
        ob_dict[ob.name] = convert_attr(ref_bone.matrix.inverted() @ ob.matrix_world)

    ## using a list of names
    # for ob_name in ['obj_name_01', 'obj_name_02']:
    #     ob = scn.objects.get(ob_name)
    #     if not ob:
    #         continue
    #     ob_dict[ob_name] = convert_attr(ref_bone.matrix.inverted() @ ob.matrix_world)
    
    if ob_dict:
        d[i] = ob_dict

## dict ex: d = { 100 : {'ob_name_01' : Matrix} }

## Set to clipboard
bpy.context.window_manager.clipboard = json.dumps(d, indent='\t')


## -------------------------


### Apply dumped value on new bone space

## load from clipboard
d = json.loads(bpy.context.window_manager.clipboard)

obj = bpy.data.objects['char_rig']
ref_bone = obj.pose.bones["hips"]

for k, ob_dic in d.items():
    i = int(k)
    scn.frame_set(i) # set frame and refresh data
    print(scn.frame_current)
        
    ## Set all objects in dict ()
    for ob_name, mat_in_bone_space in ob_dic.items():
        ob = scn.objects.get(ob_name)
        if not ob:
            continue

        ob.matrix_world = ref_bone.matrix @ mathutils.Matrix(mat_in_bone_space)

        ## Add keyframe
        for chan in ('location', 'rotation_euler'):
            # if has_channel_key_at_frame(ob, channel=chan):
            #     # key only when needed...
            #     ob.keyframe_insert(chan,frame=i)
            ob.keyframe_insert(chan, frame=i)

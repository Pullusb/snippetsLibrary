## Test if there is a keyframe on channel (at least on one element of the array) at given frame

import bpy

def has_key_at_frame(item, act=None, frame=None, channel='location', verbose=False):
    '''Return True if pose bone has a key at passed frame'''

    if frame is None:
        frame = bpy.context.scene.frame_current
    
    if isinstance(item, bpy.types.Object):
        ## Object
        if act is None:
            act = item.animation_data.action
        data_path = channel
    else:
        ## Consider it's a Pose bone
        if act is None:
            act = item.id_data.animation_data.action
        data_path = f'pose.bones["{item.name}"].{channel}'

    for i in range(0,3):
        f = act.fcurves.find(data_path, index=i)
        if not f:
            if verbose:
                print(f'{item.name} has not {data_path}')
            continue
        
        if f.is_empty:
            if verbose:
                print(f'fcurve has not keyframes: {f.data_path} {i}')
            continue
        
        if not f.is_valid:
            if verbose:
                print(f'fcurve is invalid {f.data_path} {i}')
            continue
        
        ## ? int frame ?
        if next((k for k in f.keyframe_points if k.co.x == frame), None) is not None:
            if verbose: print(f'{item.name} {channel} is keyframed')
            return True
    return False


item = bpy.context.object
# item = bpy.context.active_pose_bone

## Test per channel
has_key_at_frame(item, channel='location', verbose=True)
has_key_at_frame(item, channel='rotation_euler', verbose=True)
has_key_at_frame(item, channel='scale', verbose=True)

## multiple channels loop
# for chan in ('location', 'rotation_euler', 'scale'):
#     if has_key_at_frame(item, channel=chan):
#         ## ex: insert a key only if there is a keyframe already
#         item.keyframe_insert(chan)
## Insert keyframe on object or posebone, automatically determine rotation data_path with axis choice

# Mapping of rotation modes to data_path
ROTATION_MODE_MAP = {
    'ZYX': 'rotation_euler',
    'ZXY': 'rotation_euler',
    'YZX': 'rotation_euler',
    'YXZ': 'rotation_euler',
    'XZY': 'rotation_euler',
    'XYZ': 'rotation_euler',
    'QUATERNION': 'rotation_quaternion',
    'AXIS_ANGLE': 'rotation_axis_angle'
}

def set_keyframe_on_axis(target, transform, frame, use_x=True, use_y=True, use_z=True):
    '''simple keyframe insertion, pass object or bone, a transform channel name and a frame number
    transform (str): 'location', 'rotation' or 'scale'
    frame: frame number where to add the keyframes
    use_x, use_y, use_z (bool): enable keyframe insertion per axis (always takes all for quaternion and axis-angle rotation)
    '''

    ## Define axis to key (always all 4 in quaternion and axis_angle mode)
    use_axes = [use_x, use_y, use_z] 
    if all(use_axes) or (transform == 'rotation' and target.rotation_mode in ('QUATERNION', 'AXIS_ANGLE')):
        axis_indices = [-1]
    else:
        # Get the indices of enabled axes
        axis_indices = [i for i, use_axis in enumerate(use_axes) if use_axis]

    ## define data_path to keyframe (adjust data_path for rotation)
    data_path = ROTATION_MODE_MAP[target.rotation_mode] if transform == 'rotation' else transform

    # if isinstance(target, bpy.types.PoseBone):
    for axis_index in axis_indices:
        ## set group and options ? (probably not needed)
        target.keyframe_insert(data_path, index=axis_index, frame=frame) # , keytype='KEYFRAME'

    ## Find and return newly created keyframes
    ## (/!\ Using other Ops within operator sometimes void reference to keyframes)
    # path_prefix = ''
    # if isinstance(target, bpy.types.PoseBone):
    #     path_prefix = f'pose.bones["{target.name}"].'
    # return [k for fc in target.id_data.animation_data.action.fcurves 
    #         if fc.data_path == f'{path_prefix}{data_path}' and (axis_indices[0] == -1 or fc.array_index in axis_indices) 
    #         for k in fc.keyframe_points if k.co.x == frame]


## usage: key rotation on  active object at frame 10
set_keyframe_on_axis(bpy.context.object, 'rotation', 10)

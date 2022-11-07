## Jump to previous or next grease pencil keyframe with filters

def gp_key_jump(next=True, obj=None, layer_target='SELECTED', kf_type='ALL'):
    """Jump on next or previous keyframe of Grease pencil object
    :next: if True jump to next, False jump to previous
    :obj: Grease pencil object ot use, active object if not specified
    :layer_target: if not passed, consider every layer without exception
        Available filters:
        ACTIVE: Only active layer
        SELECTED: Active and selected layers
        VISIBLE: Visibles layers
        ACCESSIBLE: Visible and unlocked layers

    :kf_type: Keyframe jump filter, default "ALL".
        Available type:  ALL, KEYFRAME, BREAKDOWN, MOVING_HOLD, EXTREME, JITTER
    """
    scn = bpy.context.scene
    obj = obj or bpy.context.object
    if not obj or obj.type != 'GPENCIL':
        return

    current = scn.frame_current
    p = n = None
    mins = []
    maxs = []


    if layer_target == 'ACTIVE':
        gpl = [obj.data.layers.active]
    elif layer_target == 'SELECTED':
        gpl = [l for l in obj.data.layers if l.select and not l.hide]
        if not obj.data.layers.active in gpl:
            gpl.append(obj.data.layers.active)   
    elif layer_target == 'VISIBLE':
        gpl = [l for l in obj.data.layers if not l.hide]
    elif layer_target == 'ACCESSIBLE':
        gpl = [l for l in obj.data.layers if not l.hide and not l.lock]
    else:
        gpl = obj.data.layers

    for l in gpl:
        for f in l.frames:
            # keyframe type filter
            if kf_type != 'ALL' and f.keyframe_type != kf_type:
               continue

            if f.frame_number < current:
                p = f.frame_number
            if f.frame_number > current:
                n = f.frame_number
                break

        mins.append(p)
        maxs.append(n)
        p = n = None

    mins = [i for i in mins if i is not None]
    maxs = [i for i in maxs if i is not None]

    if mins:
        p = max(mins)
    if maxs:
        n = min(maxs)

    if next and n is not None:
        scn.frame_current = n
    elif not next and p is not None:
        scn.frame_current = p

### Use case examples:

## Jump to previous keyframe (all type, only on active)
# gp_key_jump(next=False, layer_target='ACTIVE')

## Jump to next keyframe (only "KEYFRAME" type, on all visible and unlocked layer)
# gp_key_jump(next=True, layer_target='ACCESSIBLE', kf_type='KEYFRAME')

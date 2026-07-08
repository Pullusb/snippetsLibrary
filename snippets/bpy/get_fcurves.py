## Get fcurves whatever the blender version, either as datablock object or as list

import bpy

def ensure_channelbag(data_block):
    """Utility to returns the channelbag of f-curves for a given ID.
    Or `None` if the ID doesn't have an animation data, an action, or a slot.
    """

    if data_block.animation_data is None:
        return None

    anim_data = data_block.animation_data
    if anim_data.action is None:
        return None

    action = anim_data.action
    if action.is_empty:
        return None

    if anim_data.action_slot is None:
        return None

    from bpy_extras.anim_utils import action_ensure_channelbag_for_slot
    channelbag = action_ensure_channelbag_for_slot(action, anim_data.action_slot)

    return channelbag

def get_fcurves_from_object(obj, path='') -> list:
    """Return a list all f-curves of the object
    if a path is given, filter by data_path
    return empty list if nothing is found
    """

    if not obj.animation_data or not obj.animation_data.action:
        return []

    if bpy.app.version < (5, 0, 0):
        if not path:
            return [fc for fc in obj.animation_data.action.fcurves]
        return [fc for fc in obj.animation_data.action.fcurves if fc.data_path == path]

    channelbag = ensure_channelbag(obj)
    if channelbag is None:
        return []

    if not path:
        return [fc for fc in channelbag.fcurves]

    return [fc for fc in channelbag.fcurves if fc.data_path == path]

def get_fcurves(src, path='', slot=None) -> list:
    """Return a list all f-curves from the passed object/anim_data/action
    path (str, optional): if given, filter returned f-curves by data_path
    slot (action_slot, optional): if an action slot is passed, directly use this action + slot.
        if not passed: get the active slot (first slot if a single action is passed)
    return empty list if nothing is found
    """
    
    obj = None
    anim_data = None
    if isinstance(src, bpy.types.AnimData):
        # case of anim_data, passed
        anim_data = src
        action = anim_data.action
        if not action:
            return []

    elif isinstance(src, bpy.types.Action):
       action = src
    
    else:
        # object of data containing an anim_data
        obj = src
        anim_data = obj.animation_data
        if not anim_data or not anim_data.action:
            return []
        action = obj.animation_data.action

    if bpy.app.version < (5, 0, 0):
        if not path:
            return [fc for fc in action.fcurves]
        return [fc for fc in action.fcurves if fc.data_path == path]

    from bpy_extras.anim_utils import action_ensure_channelbag_for_slot
    # ensure or get ? : animdata_get_channelbag_for_assigned_slot 

    if action.is_empty:
        return []

    if slot is None:
        if anim_data:
            if not anim_data.action_slot:
                ## TODO: add a "return first slot when nothing active" ?
                ## -> could return animation_data.action.layers[0].strips[0].channelbags[0].fcurves
                return []
            slot = anim_data.action_slot
            # print('active_slot from anim_data:', slot)

        elif action:
            # directly check on action
            if not action.slots:
                print(f'{action.name}: no slots on action')
                return []
            ## TODO: add a method to filter by name or by object
            # use first slot
            print(f'{action.name}: using first slot')
            # (should probably do it by name instead of first)
            slot = action.slots[0]

    channelbag = action_ensure_channelbag_for_slot(action, slot)

    if channelbag is None:
        return []
    
    if not path:
        return [fc for fc in channelbag.fcurves]

    return [fc for fc in channelbag.fcurves if fc.data_path == path]

def get_fcurves_datablock(data_block):
    """Return fcurves data for active action/slot
    ex: Allow to list fcurves and call fcurves.remove on it
    None if there is no animation data, action, slots
    """
    if not data_block.animation_data or not data_block.animation_data.action:
        return
    if bpy.app.version < (5, 0, 0):
        return data_block.animation_data.action.fcurves
    channelbag = ensure_channelbag(data_block)
    if channelbag:
        return channelbag.fcurves

# example use:
# location_frames_num = {k.co.x for fc in get_fcurves(bpy.context.object, path='location') for k in fc.keyframe_points}
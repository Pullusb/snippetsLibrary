## Get fcurves whatever the blender version, either as datablock object or as list
## note: can also access without anim_utils wrappers: animation_data.action.layers[0].strips[0].channelbags[0].fcurves

import bpy

def _get_first_channelbag(action):
    """Return the first channelbag found on the action's first layer/strip, or `None`.
    Used as a fallback when an action has no slot assigned (read-only, creates nothing).
    """
    if not action or not action.layers:
        return None
    strips = action.layers[0].strips
    if not strips:
        return None
    channelbags = strips[0].channelbags
    return channelbags[0] if channelbags else None

def get_channelbag(data_block):
    """Utility to return the channelbag of f-curves for a given ID (read-only, creates nothing).
    Falls back to the action's first channelbag if no slot is assigned.
    Or `None` if the ID doesn't have animation data or an action.
    """

    anim_data = data_block.animation_data
    if not anim_data or not anim_data.action:
        return None

    action = anim_data.action
    if anim_data.action_slot:
        from bpy_extras.anim_utils import action_get_channelbag_for_slot
        return action_get_channelbag_for_slot(action, anim_data.action_slot)

    return _get_first_channelbag(action)

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

    channelbag = get_channelbag(obj)
    if channelbag is None:
        return []

    if not path:
        return [fc for fc in channelbag.fcurves]

    return [fc for fc in channelbag.fcurves if fc.data_path == path]

def get_fcurves(src, path='', slot=None) -> list:
    """Return a list all f-curves from the passed object/anim_data/action
    path (str, optional): if given, filter returned f-curves by data_path
    slot (action_slot, optional): if an action slot is passed, directly use this action + slot.
        if not passed: use the assigned slot (or the action's first channelbag as fallback)
    return empty list if nothing is found
    """

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
        anim_data = src.animation_data
        if not anim_data or not anim_data.action:
            return []
        action = anim_data.action

    if bpy.app.version < (5, 0, 0):
        # Code for blender before 5.0
        if not path:
            return [fc for fc in action.fcurves]
        return [fc for fc in action.fcurves if fc.data_path == path]

    if slot is not None:
        from bpy_extras.anim_utils import action_get_channelbag_for_slot
        channelbag = action_get_channelbag_for_slot(action, slot)
    elif anim_data and anim_data.action_slot:
        from bpy_extras.anim_utils import action_get_channelbag_for_slot
        channelbag = action_get_channelbag_for_slot(action, anim_data.action_slot)
    else:
        # no slot given/assigned: fall back to the action's first channelbag
        channelbag = _get_first_channelbag(action)

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
    channelbag = get_channelbag(data_block)
    if channelbag:
        return channelbag.fcurves

# example use:
# location_frames_num = {k.co.x for fc in get_fcurves(bpy.context.object, path='location') for k in fc.keyframe_points}

## Get fcurves whatever the blender version, either as datablock object or as list

import bpy

def ensure_channelbag(data_block):
    """wrapper function, returns the channelbag of f-curves for a given ID.
    Return None if the ID doesn't have an animation data > action > slot.
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

def get_fcurves(obj, path='', slot=None) -> list:
    """Return a list all f-curves of the object
    path: if given, filter by this data_path
    slot: if an action slot is passed, directly use this action + slot.
    return empty list if nothing is found
    """

    anim_data = obj.animation_data
    if not anim_data or not anim_data.action:
        return []

    if bpy.app.version < (5, 0, 0):
        if not path:
            return [fc for fc in anim_data.action.fcurves]
        return [fc for fc in anim_data.action.fcurves if fc.data_path == path]

    if slot is None:
        channelbag = ensure_channelbag(obj)
    else:
        # Directly get channelBag from the action/slot
        import anim_utils
        # slot = anim_data.action_slot # <- also exists on anim_data
        channelbag = anim_utils.action_get_channelbag_for_slot(anim_data.action, slot)

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
# loc_frames = {k.co.x for fc in get_fcurves(bpy.context.object, path='location') for k in fc.keyframe_points}
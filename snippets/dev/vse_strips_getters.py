## functions to get vse strips wahever the blender version with filters.

import bpy

def vse_strips(vse=None):
    """return vse strips, version agnostic"""
    vse = vse or bpy.context.scene.sequence_editor
    if bpy.app.version >= (5,0,0):
        return vse.strips
    else:
        return vse.sequences

def vse_strips_all(vse=None):
    """return vse strips (recursive in meta strips), version agnostic"""
    vse = vse or bpy.context.scene.sequence_editor
    if bpy.app.version >= (5,0,0):
        return vse.strips_all
    else:
        return vse.sequences_all

def get_vse_strips_by_type(vse=None, recursive=False, strip_type=None):
    """Return vse strips matching a given type, version agnostic.

    vse: sequence_editor instance, defaults to bpy.context.scene.sequence_editor
    recursive: if True, include strips inside meta strips (uses strips_all)
    strip_type: str or list of str (e.g. 'SOUND' or ['SOUND', 'MOVIE'])
    possible types: ['SCENE', 'MOVIE', 'IMAGE', 'SOUND', 'COLOR', 'TEXT',
        'EFFECT', 'META', 'TRANSFORM', 'ADJUSTMENT', 'MOVIECLIP', 'MASK']
    """
    vse = vse or bpy.context.scene.sequence_editor
    types = (strip_type,) if isinstance(strip_type, str) else strip_type
    src = vse_strips_all(vse) if recursive else vse_strips(vse)
    return [s for s in src if s.type in types]


def get_enabled_vse_strips_in_scene_range(vse=None, strip_type=None):
    """Return non-muted strips overlapping the scene frame range.

    vse: sequence_editor instance, defaults to bpy.context.scene.sequence_editor
    strip_type: str or list of str to filter by type, or None for all types
    possible types: ['SCENE', 'MOVIE', 'IMAGE', 'SOUND', 'COLOR', 'TEXT',
        'EFFECT', 'META', 'TRANSFORM', 'ADJUSTMENT', 'MOVIECLIP', 'MASK']
    """
    vse = vse or bpy.context.scene.sequence_editor
    scn = bpy.context.scene
    if strip_type is not None:
        types = (strip_type,) if isinstance(strip_type, str) else strip_type
    return [
        s for s in vse_strips(vse)
        if (strip_type is None or s.type in types)
        and not s.mute
        and not (s.frame_final_end <= scn.frame_start or s.frame_final_start >= scn.frame_end)
    ]

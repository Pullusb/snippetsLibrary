import bpy
#keyframe this attribute on selection (can get name with 'copy datapath')
attribute = '${1:rotation_euler}'
for o in bpy.context.selected_objects:
    if hasattr(o,attribute):
        o.keyframe_insert(attribute)
        ${0}
        '''
        ref : keyframe_insert(data_path, index=-1, frame=bpy.context.scene.frame_current, group="", options=set()
            :arg options: Optional set of flags:
       - INSERTKEY_NEEDED Only insert keyframes where they're needed in the relevant F-Curves.
       - INSERTKEY_VISUAL Insert keyframes based on 'visual transforms'.
       - INSERTKEY_XYZ_TO_RGB Color for newly added transformation F-Curves (Location, Rotation, Scale) is based on the transform axis.
       - INSERTKEY_REPLACE Only replace already existing keyframes.
       - INSERTKEY_AVAILABLE Only insert into already existing F-Curves.
       - INSERTKEY_CYCLE_AWARE Take cyclic extrapolation into account (Cycle-Aware Keying option).
       '''
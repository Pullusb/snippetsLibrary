import bpy

def add_frame_padding(name):
    '''
    Return string padded with current blender frame
    if # in string, use this padding for the frame number (rightmost only)
    if path is alread correctly padded return unchanged
    '''

    def pad_with_current_frame(match):
        return str(bpy.context.scene.frame_current).zfill(len(match.group(0)))

    if not '#' in name:
        frame_pad = str(bpy.context.scene.frame_current).zfill(4)
        if name.endswith(frame_pad):
            return name
        return name + str(bpy.context.scene.frame_current).zfill(4)
    # return re.sub(r'\#{1,10}', pad_with_current_frame, name)# all '#...' in string
    import re
    return re.sub(r'\#{1,10}(?!.*\#)', pad_with_current_frame, name)# only last '#...'

bpy.context.scene.render.filepath = add_frame_padding(bpy.context.scene.render.filepath)
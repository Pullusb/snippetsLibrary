import os
import bpy

original_frame = bpy.context.scene.frame_current
output_path = bpy.context.scene.render.filepath
start = bpy.context.scene.frame_start
end = bpy.context.scene.frame_end

def get_all_keyframe(use_only = True):
    sum = set()
    for action in bpy.data.actions:
        if use_only and action.use_fake_user and action.users == 1:
            #avoid saved (fake user) but unused actions
            pass
        elif use_only and action.users == 0:
            #avoid 0 user actions
            pass

        else:
            for fcurve in action.fcurves:
                for key in fcurve.keyframe_points:
                    sum.add(key.co[0])
    return sum


def dopesheet_summary():
    frames = []

    for obj in bpy.context.selected_objects:
        for fcurve in obj.animation_data.action.fcurves:
            for keyframe_point in fcurve.keyframe_points:
                x, y = keyframe_point.co
                if x >= start and x <= end and x not in frames:
                    frames.append(x)
    return frames

#frames = dopesheet_summary()
frames = sorted(get_all_keyframe())
print(len(frames))
print(sorted([int(i) for i in frames]))


for frame in frames:
    #bpy.context.scene.frame_current = frame
    bpy.context.scene.frame_set(frame)
    ##bpy.context.scene.update()
    bpy.context.scene.render.filepath = output_path + "%05d" % frame
#    bpy.ops.render.render(write_still=True)
    bpy.ops.render.opengl(write_still=True, view_context=False)
    ## open GL Not updating frame

bpy.context.scene.frame_current = original_frame
bpy.context.scene.render.filepath = output_path

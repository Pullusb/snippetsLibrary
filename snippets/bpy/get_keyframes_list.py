import bpy
from bpy import context as C
from bpy import data as D
import math
import os

## HALP : http://blender.stackexchange.com/questions/1718/is-it-possible-to-render-only-keyframes-from-dope-sheet

# get all selected objects
selection = bpy.context.selected_objects


def dopesheet_summary():
    original_frame = bpy.context.scene.frame_current
    output_path = bpy.context.scene.render.filepath
    start = bpy.context.scene.frame_start
    end = bpy.context.scene.frame_end
    frames = []

    for obj in bpy.context.selected_objects:
        for fcurve in obj.animation_data.action.fcurves:
            for keyframe_point in fcurve.keyframe_points:
                x, y = keyframe_point.co
                if x >= start and x <= end and x not in frames:
                    frames.append(x)
                    ## for returning an int (import math)
                    #frames.append((math.ceil(x)))
    return frames



def get_all_keyframe(use_only = True):
    sum = set()
    for action in D.actions:
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


def get_keyframes(obj_list):
    keyframes = []
    for obj in obj_list:
        anim = obj.animation_data
        if anim is not None and anim.action is not None:
            for fcu in anim.action.fcurves:
                for keyframe in fcu.keyframe_points:
                    x, y = keyframe.co
                    if x not in keyframes:
                        keyframes.append((math.ceil(x)))
    return keyframes

print ('Keyframes-')

frames = dopesheet_summary()
KF = get_keyframes(selection)
allKF = get_all_keyframe()

'''
print('dopesheet_summary', len(frames))
print(sorted(frames))

print('getKF',len(KF))
print (sorted(KF))
'''

print('getAllKF',len(allKF))
print (sorted(allKF))

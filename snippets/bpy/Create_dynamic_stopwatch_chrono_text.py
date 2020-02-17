## Create a chrono text object that update on fram change with a handler

import bpy
from math import radians

def transfer_value(Value, OldMin, OldMax, NewMin, NewMax):
    '''map a value from a range to another (transfer/translate value)'''
    return (((Value - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

def chrono_trigger(scene):
    fps = scene.render.fps
    i = scene.frame_current #here add an offset by frame amount (ex: +240)
    stop_at = 340#define a stop for the chrono

    if scene.frame_current < 100000: #Stop the watch at this frame
        minutes = str(i//(fps*60))
        secs = str(i//fps%60).zfill(2)

        ## miliseconds
        # milisec = int(transfer_value(i%fps, 0, fps, 0, 100))#to a 0 to 100 value
        # milisec = str(milisec).zfill(2)#padding of 2
        # text = f'{minutes}:{secs}:{milisec}'

        ## frame instead of milisec
        frame = str(i%fps).zfill(2) # 
        text = f'{minutes}:{secs}:{frame}'# frame


        # print("text", text)#Debug print
        bpy.data.objects['chrono'].data.body = text


chrono = bpy.context.scene.objects.get('chrono')
if not chrono:
    ob_data = bpy.data.curves.new("chrono_data", "FONT")
    ob_name = 'chrono'
    ob = bpy.data.objects.new(ob_name, ob_data)
    bpy.context.collection.objects.link(ob)
    ob.location = bpy.context.scene.cursor.location
    ob.rotation_euler.x = radians(90)

if chrono and chrono.type == 'FONT':
    # To update at each frame change (both viewport and render)
    bpy.app.handlers.frame_change_pre.append(chrono_trigger)

    # to activate it when the blend is opened tick the register checkbox of text editor

else:
    print('no font object named chrono found')
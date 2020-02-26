import bpy
import random
C = bpy.context
D = bpy.data

selected_names = [b.name for b in C.selected_pose_bones]

def remove_modifier():
    for fc in C.object.animation_data.action.fcurves:
        if fc.data_path.split('"')[1] in selected_names:
            for m in fc.modifiers:
                fc.modifiers.remove(m)

def create_noise():
    for fc in C.object.animation_data.action.fcurves :
        if fc.data_path.split('"')[1] in selected_names:
            m = fc.modifiers.new(type='NOISE')
            m.scale = 1
            m.strength = 1
            m.depth = 0
            m.phase = 1
            m.offset = 0

def change_noise(channel, axe, scale = 100, strength = 1):
    for fc in C.object.animation_data.action.fcurves:
        if fc.data_path.split('"')[1] in selected_names:
            if fc.data_path.split('.')[-1] in channel and fc.array_index in axe:
                for m in fc.modifiers:
                    if m.type == 'NOISE':
                        m.scale = scale
                        m.strength = strength
                        m.depth = 0
                        m.phase = random.uniform(0,1000)
                        m.offset = random.uniform(0,1000)

#create_noise()

### exemple: change noise(('location', 'rotation_euler', 'scale'), (0,1,2), scale= 100, strength = 1) 0=X 1=Y, 2=Z
#change_noise(('rotation_euler', 'location', 'scale'),(0,1,2))

# change_noise(('location'),(0),100,1)# only on location.x of selected pose bone

# change_noise(('rotation_euler'),(0,1,2),80,3)# rotation.xyz of selected pose bone
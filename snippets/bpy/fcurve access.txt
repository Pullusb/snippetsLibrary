# access fcurves keyframes data modifiers and more
"""
#old 2.79 stuff to get name
reg = re.compile(r'(?<=\[\").*(?=\"\])') #get group(0)
def fname(fcu):
    global reg
    return reg.search(fcu.data_path).group(0), fcu.data_path.rsplit('.',1)[1]
"""

act = C.object.animation_data.action
for i, fcu in enumerate(act.fcurves):

    ##access modifiers
    if fcu.modifiers:
        #print(i, fname(fcu))
        print(i, fcu.data_path, fcu.array_index)
        for j, mod in enumerate(fcu.modifiers):
            print(mod.type)
            if mod.mute:
                print('|-> is disabled')
            #if mod.type == 'STEPPED':
                ## mute (will not be evalueted)
                # mod.mute = not mod.mute

                ## remove modifier
                # fcu.modifiers.remove(mod)

    ##access keyframes of the curve:
    for k in fcu.keyframe_points:
        ##[0] or x is time/frame, [1] or y is space/value
        print('time', k.co[0], '- value', k.co[1]))
        #k.handle_left
        #k.handle_right

        ##change handler type ([‘FREE’, ‘VECTOR’, ‘ALIGNED’, ‘AUTO’, ‘AUTO_CLAMPED’], default ‘FREE’)
        #k.handle_left_type = 'AUTO_CLAMPED'
        #k.handle_right_type = 'AUTO_CLAMPED'
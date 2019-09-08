# create / delete armatures armature for the selected objects (and reset stretch to constraint)
def CreateArmatureModifier(ob, targetRig):
    '''
    TargetRig = name of armature data (str)
    Create armature modifier if necessary and place it on top of stack
    or just after the first miror modifier
    return a list of bypassed objects
    '''

    #get object from armature data with a loop (only way to get armature's owner)
    for obArm in bpy.data.objects:
        if obArm.type == 'ARMATURE' and obArm.data.name == targetRig:
            ArmatureObject = obArm

    #add armature modifier that points to designated rig:
    if not 'ARMATURE' in [m.type for m in ob.modifiers]:
        mod = ob.modifiers.new('Armature', 'ARMATURE')
        mod.object = ArmatureObject#bpy.data.objects[targetRig]

        #bring Armature modifier to the top of the stack
        pos = 1
        if 'MIRROR' in [m.type for m in ob.modifiers]:
            #if mirror, determine it's position
            for mod in ob.modifiers:
                if mod.type == 'MIRROR':
                    pos += 1
                    break
                else:
                    pos += 1

        if len(ob.modifiers) > 1:
            for i in range(len(ob.modifiers) - pos):
                bpy.ops.object.modifier_move_up(modifier="Armature")

    else: #armature already exist
        for m in ob.modifiers:
            if m.type == 'ARMATURE':
                m.object = ArmatureObject#bpy.data.objects[targetRig]

                ## maybe check if it targets the same object ?
                # if m.object == None:
                #     m.object = bpy.data.objects[targetRig]
                # elif m.object != bpy.data.objects[targetRig]:
                #     return (m.object)



def armature_selected(arm_data_name):
    for ob in bpy.context.selected_objects:
        if not 'ARMATURE' in [i.type for i in ob.modifiers]:
            CreateArmatureModifier(ob, arm_data_name)


def remove_armature(apply=0):
    '''apply=1 will apply modifier instead of removing, default = 0'''
    for ob in bpy.context.selected_objects:
        if ob.type in ('MESH', 'CURVE', 'TEXT') and len(ob.modifiers) > 0:
            print (ob.name)
            for mod in ob.modifiers:
                if mod.type == 'ARMATURE':
                    #if mod.object:
                        #print (mod.object.name)#print armatrue target
                        #mod.object = D.objects['caneton-classique_rig']
                    if apply:
                        C.scene.objects.active = ob
                        bpy.ops.object.modifier_apply(modifier=mod.name)
                    else:
                        ob.modifiers.remove(mod) #remove modifier


def reset_stretch():
    for b in C.object.pose.bones:
        for cs in b.constraints:
            #print(cs.type)
            if cs.type == 'STRETCH_TO':
                print ('reseting', b.name)
                cs.rest_length = 0
                ##select one by one
                #C.object.data.bones.active = C.object.data.bones[b.name]
                #return


## remove (or apply) armature modifier for selected objects
#remove_armature(apply=1)

## create an armature modifier for all selected objects with passed armature name as target
#armature_selected('perso_rig')

## reset "stretch to" constraint 
#reset_stretch()
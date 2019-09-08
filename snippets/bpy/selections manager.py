# specific functions to handle selection from multiple context

def select_posebone(pb, select=1):
    '''Select / Deselect given poseBone'''
    pb.bone.select=select
    pb.bone.select_tail=select
    pb.bone.select_head=select

def select_bone(bone, select=1):
    '''Select / Deselect given Bone'''
    bone.select=select
    bone.select_tail=select
    bone.select_head=select

def set_select(ob,select=1):
    '''select passed object, bone or posebone'''
    m = bpy.context.mode
    if m == 'POSE':
        select_posebone(ob,select)
    elif m == 'EDIT_ARMATURE':
        select_bone(ob,select)
    else:
        ob.select = select

def set_active(ob, force_select=1):
    '''make active passed object, bone or posebone'''
    m = bpy.context.mode
    if m == 'POSE':
        if force_select:
            select_posebone(ob,select)
        #id_data is the object, .data access armature
        ob.id_data.data.bones.active = ob.bone
    elif m == 'EDIT_ARMATURE':
        if force_select:
            select_bone(ob,select)
        ob.id_data.bones.active = ob
    else:
        if force_select:
            ob.select = select
        bpy.context.scene.objects.active = ob


def get_selection():
    '''return selection of current context'''
    m = bpy.context.mode
    if m == 'POSE':
        return bpy.context.selected_pose_bones
    elif m == 'EDIT_ARMATURE':
        return bpy.context.selected_bones
    else:
        return bpy.context.selected_objects

def get_active():
    '''return active object of current context'''
    m = bpy.context.mode
    if m == 'POSE':
        return bpy.context.active_pose_bone
    elif m == 'EDIT_ARMATURE':
        return bpy.context.active_bone
    else:
        return bpy.context.active_object

def get_selectable():
    '''return all selectable object (of current context ?)'''
    return bpy.context.selectable_objects

#---
act = get_active()
selection = get_selection()
other = [ob for ob in get_selection() if ob != act]
all = get_selectable()
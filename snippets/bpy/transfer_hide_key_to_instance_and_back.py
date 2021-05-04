import bpy

def transfer_hide_to_instance_type():
    print('-- Hide viewport to instance type --')
    # for o in bpy.context.selected_objects:
    for o in bpy.context.scene.objects:
        if o.type == 'EMPTY' and o.instance_collection:
            anim_data = o.animation_data
            if not anim_data or not anim_data.action:
                continue
            fcurve = anim_data.action.fcurves.find('hide_viewport') 

            if not fcurve:
                continue

            if anim_data.action.fcurves.find('instance_type'):
                continue  # pass existing keyframed instance_type

            print('-', o.name, 'keyframes number', len(fcurve.keyframe_points))
            for pt in fcurve.keyframe_points:
                if pt.co[1] == 1.0:  # 0
                    o.instance_type = 'NONE'
                else:  # 256
                    o.instance_type = 'COLLECTION'

                o.keyframe_insert('instance_type', frame=pt.co[0])  # group ?

            # delete curve for viewport visibility
            anim_data.action.fcurves.remove(fcurve)
            ## delete render anim :
            render_fcurve = anim_data.action.fcurves.find('hide_render')
            if render_fcurve:
                anim_data.action.fcurves.remove(render_fcurve)

            o.hide_viewport = False  # show it !
            o.empty_display_size = 0.25

def transfer_instance_type_to_hide():
    print('-- Instance type >> Hide viewport--')
    # for o in bpy.context.selected_objects:
    for o in bpy.context.scene.objects:
        if o.type == 'EMPTY' and o.instance_collection:

            anim_data = o.animation_data
            if not anim_data or not anim_data.action:
                continue
            fcurve = anim_data.action.fcurves.find('instance_type') 

            if not fcurve:
                continue

            if anim_data.action.fcurves.find('hide_viewport'):
                continue  # pass existing keyframed instance_type

            print('-', o.name, 'keyframes number', len(fcurve.keyframe_points))
            for pt in fcurve.keyframe_points:
                if pt.co[1] == 0:  # 0
                    o.hide_viewport = o.hide_render = True
                else: # 256
                    o.hide_viewport = o.hide_render = False

                o.keyframe_insert('hide_viewport', frame=pt.co[0])
                o.keyframe_insert('hide_render', frame=pt.co[0])

            # delete instance type animation and set collection
            anim_data.action.fcurves.remove(fcurve)
            o.instance_type = 'COLLECTION'


## VISIBILITY TO INSTANCE
transfer_hide_to_instance_type()

## INSTANCE BACK TO VISIBILITY
#transfer_instance_type_to_hide()
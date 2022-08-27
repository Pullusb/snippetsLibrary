# remove all hide render fcurves on scene objects 
import bpy

# fcurve data_path to remove
fcurve_path = ('hide_render', 'hide_viewport')

## remove on all actions
for ac in bpy.data.actions:
    for fc in reversed(ac.fcurves):
        if fc.data_path in fcurve_path:
            print(f'removing hide_render from action: {ac.name}')
            ac.fcurves.remove(fc)

## remove on scene objects only (restore visibility)
for ob in bpy.context.scene.objects:
    if not ob.animation_data or not ob.animation_data.action:
        continue
    ac = ob.animation_data.action
    for fc in reversed(ac.fcurves):
        if fc.data_path in fcurve_path:
            print(f'removing hide_render, object: {ob.name} (action: {ac.name})')
            ac.fcurves.remove(fc)

            # turn visible
            ob.hide_viewport = ob.hide_render = False

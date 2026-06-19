## Swap current active object and mode with a target object.
## When target is already selected, back to previous active/mode
## Useful to make quick specific adjustment, on a pose bone or camera, before resuming activities

def swap_active_to_object_and_back(target_obj, mode='OBJECT') -> bool:
    """Swap an object as active and a mode, keeping memory of previous state.

    Args:
        target_obj (object): the object to swap to
            If target already active, back to previous (none active if no previous stored)
        mode (str): mode string for mode_set operator ('EDIT', 'POSE', ... default  "OBJECT")
    
    Returns:
        True if swapped to object, False if swapped back to previous/None
    """
    context = bpy.context
    wm = context.window_manager        
    active = context.object
    if active:
        if active == target_obj:
            ### Case you're on already with target object active

            target_obj.select_set(False)
            if context.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')

            ## Back to previous object as active if applicable (else None as Active)
            # Restore object    
            if wm.get('swap_back_to_object'):
                context.view_layer.objects.active = wm['swap_back_to_object']
                wm['swap_back_to_object'].select_set(True)
                del wm['swap_back_to_object']

                # Restore mode
                if wm.get('swap_back_to_mode'):
                    bpy.ops.object.mode_set(mode=wm['swap_back_to_mode'])
            else:
                context.view_layer.objects.active = None

            ## ensure mode save is removed as well
            if wm.get('swap_back_to_mode'):
                del wm['swap_back_to_mode']

            return False

        ## Case you're NOT on camera rig
        wm['swap_back_to_object'] = context.object
        ## context mode string is sometimes 'EDIT_...', but always plain 'EDIT' for mode_set
        wm['swap_back_to_mode'] = 'EDIT' if 'EDIT' in context.mode else context.mode

        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        active.select_set(False)

    context.view_layer.objects.active = target_obj
    target_obj.select_set(True)
    if context.mode != mode:
        bpy.ops.object.mode_set(mode=mode)
    return True

# swap_active_to_object_and_back(bpy.context.scene.camera) # for quickly cam setting check
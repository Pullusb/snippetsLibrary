# Simple template of keypress event handling in modal ops with detection of ctrl/alt/shift modifiers
import bpy

class TEMPLATE_OT_keypress_handle(bpy.types.Operator):
    """Handle keypress with modifier"""
    bl_idname = "view3d.template_keypress_handle"
    bl_label = "Modal keyboard and mouse template"
    bl_description = "Use left click to do stuff with modifiers key, right click or Esc to abort"
    bl_options = {"REGISTER", "UNDO"}

    pressed_key = 'NOTHING'
    pressed_alt = False
    pressed_ctrl = False
    pressed_shift = False

    def modal(self, context, event):

        ### /TESTER - keycode printer (flood console but usefull to know a keycode name)
        # if event.type not in {'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE'}:#avoid flood of mouse move.
            # print('key:', event.type, 'value:', event.value)
        ###  TESTER/
       
        ## Handle modifier keys state
        if event.type in {'LEFT_SHIFT', 'RIGHT_SHIFT'}: self.pressed_shift = event.value == 'PRESS'
        if event.type in {'LEFT_CTRL', 'RIGHT_CTRL'}: self.pressed_ctrl = event.value == 'PRESS'
        if event.type in {'LEFT_ALT', 'RIGHT_ALT'}: self.pressed_alt = event.value == 'PRESS'

        ## Get mouse move
        # if event.type in {'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE'}:
        #     # INBETWEEN : Mouse sub-moves when too fast and need precision to get higher resolution sample in coordinate.
        #     ## Store mouse position in a local variable
        #     mouse = (event.mouse_region_x, event.mouse_region_y)

        '''
        ### /CONTINUOUS PRESS
        if event.type == 'LEFTMOUSE' :
            self.pressed_key = 'LEFTMOUSE'
            ## While pushed, variable pressed stay on
            
            if event.value == 'RELEASE':
                # print('Action on release')#Dbg

                #if release, stop continuous press and do the thing !
                # Reset the key
                self.pressed_key = 'NOTHING'
                
                ## if needed, add UNDO STEP push before doing the clicked action (usefull for drawing strokes)
                # bpy.ops.ed.undo_push()

                # if skip_condition :
                #     self.pressed_key = 'NOTHING'# reset pressed_key state
                #     return {'RUNNING_MODAL'}

                # if stop_condition:
                #     # self.report({'ERROR'}, 'Error message for you, dear user')
                #     return {'CANCELLED'}

                ## Do things according to modifier detected (on release here) Put combo longest key combo first
                
                if self.pressed_alt and self.pressed_shift:# shift+alt combo operations (add what necessary)
                    print('Click released with alt + shift')
                elif self.pressed_shift:
                    print('Click released with shift')
                else:
                    print('Click released')
        

        if self.pressed_key == 'LEFTMOUSE':# using pressed_key variable
            ## Code here is continuously triggered during press
            pass
        ### CONTINUOUS PRESS/
        '''


        ## /SINGLE PRESS
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            if self.pressed_ctrl and self.pressed_shift:#combo
                print('Ctrl + Shift + Click')
            elif self.pressed_ctrl:
                print('Ctrl + Click')
            elif self.pressed_shift:
                print('Shift + Click')
            else:
                print('Click')#basic click

            ## Can also finish on click (better do a dedicated exit func if duplicated with abort code)
            # bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            # return {'FINISHED'}
        ## SINGLE PRESS/


        ## TIMER
        # if event.type == 'TIMER':
        #     print('tick')

        ### KEYBOARD SINGLE PRESS

        if event.type in {'NUMPAD_MINUS', 'LEFT_BRACKET', 'WHEELDOWNMOUSE'}:
            if event.value == 'PRESS':
                print('Triggered "less" action')

        if event.type in {'NUMPAD_PLUS', 'RIGHT_BRACKET', 'WHEELUPMOUSE'}:
            if event.value == 'PRESS':
                print('Triggered "more" action')

        # Single keys
        if event.type in {'S'}:
            if event.value == 'PRESS':
                print('S was pressed')

        if event.type in {'D'}:
            if event.value == 'PRESS':
                print('D was pressed')

        # Valid
        if event.type in {'RET', 'SPACE'}:
            print('DONE')#Dbg
            return {'FINISHED'}
        
        # Abort
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            ## Remove timer (if there was any)
            # context.window_manager.event_timer_remove(self.draw_event)
            
            print('STOPPED')#Dbg
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}


    def invoke(self, context, event):
        print('\nSTARTED')#Dbg
        
        ## Potential start checks (ex: stop if not in object mode)
        # if context.mode != 'OBJECT':
        #     self.report({'ERROR'}, "You muse be in object mode, abort")
        #     return {'CANCELLED'}
        
        ## Restrict to 3D view
        # if context.area.type != 'VIEW_3D':
        #     self.report({'WARNING'}, "View3D not found, cannot run operator")
        #     return {'CANCELLED'}
        
        ## If a timer is needed during modal - Time Step, Interval in seconds between timer events (float in [0, inf])
        # self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)

        ## Starts the modal
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

### --- REGISTER ---

def register():
    from bpy.utils import register_class
    register_class(TEMPLATE_OT_keypress_handle)
    # for cls in classes:
    #     register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    unregister_class(TEMPLATE_OT_keypress_handle)
    # for cls in reversed(classes):
    #     unregister_class(cls)


if __name__ == "__main__":
    register()
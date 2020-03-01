## Key pressed tester (also print current area infos on left-click)
## directly called at register (see last line)
import bpy

class TEMPLATE_OT_key_printer(bpy.types.Operator):
    bl_idname = "anyview.keypress_tester"
    bl_label = "key event tester"
    bl_description = "Any key event name will be printed in console (also print infos of clicked area)"
    bl_options = {"REGISTER", "UNDO"}

    def modal(self, context, event):

        ### /TESTER - keycode printer (flood console but usefull to know a keycode name)
        if event.type not in {'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE', 'LEFTMOUSE'}:#avoid flood of mouse move.
            print('key:', event.type, 'value:', event.value)
        ###  TESTER/

        ### /AREA INFOS
        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                print('-=-')
                screen = context.window.screen       
                for i,a in enumerate(screen.areas):
                    if (a.x < event.mouse_x < a.x + a.width
                    and a.y < event.mouse_y < a.y + a.height):
                        print("Clicked in %s area of screen %s" % (a.type, screen.name))
                        access = 'bpy.context.screen.areas[%s]'%i
                        print(access)
                        print(f'Area size {a.width}x{a.height} (corner {a.x},{a.y})')
                        print(f'mouse click {event.mouse_x}x{event.mouse_y}')
                        context.window_manager.clipboard = access
        ### AREA INFOS/

        # QUIT
        if event.type in {'ESC'}:#'RIGHTMOUSE',            
            print('STOPPED')#Dbg
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ## Starts the modal
        print('\nSTARTED')#Dbg
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

### --- REGISTER ---

def register():
    from bpy.utils import register_class
    register_class(TEMPLATE_OT_key_printer)

def unregister():
    from bpy.utils import unregister_class
    unregister_class(TEMPLATE_OT_key_printer)

if __name__ == "__main__":
    register()

    ## Direct call
    bpy.ops.anyview.keypress_tester('INVOKE_DEFAULT')
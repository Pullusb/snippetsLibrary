# Simple exemple of event keypress handling and basic draw in modal ops with detection of ctrl/alt/shift modifiers
import bpy
import gpu
import bgl
import blf
from gpu_extras.batch import batch_for_shader
# from gpu_extras.presets import draw_circle_2d

def draw_callback_px(self, context):
    '''Draw callback use by modal to draw in viewport'''
    ## lines and shaders
    # 50% alpha, 2 pixel width line
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')#initiate shader
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glLineWidth(2)

    # Draw line showing mouse path
    batch = batch_for_shader(shader, 'LINE_STRIP', {"pos": self.mouse_path})
    shader.bind()
    shader.uniform_float("color", (0.5, 0.5, 0.5, 0.5))#grey-light
    batch.draw(shader)

    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)

    ## text
    font_id = 0

    ## Show active modifier key (not necessary if you need performance)
    if self.pressed_alt or self.pressed_shift or self.pressed_ctrl:
        # print(f'mods: alt {self.pressed_alt} - shift {self.pressed_shift} - ctrl {self.pressed_ctrl}')
        blf.position(font_id, self.mouse[0]+10, self.mouse[1]+10, 0)
        blf.size(font_id, 30, 72)#Id, Point size of the font, dots per inch value to use for drawing.
        if self.pressed_alt and self.pressed_shift:
            blf.draw(font_id, 'x')
        elif self.pressed_alt:
            blf.draw(font_id, '-')
        elif self.pressed_shift:
            blf.draw(font_id, '+')
        elif self.pressed_ctrl:
            blf.draw(font_id, 'o')

    ## Draw text debug infos
    blf.position(font_id, 15, 30, 0)
    blf.size(font_id, 20, 72)
    blf.draw(font_id, f'Infos - mouse coord: {self.mouse} - mouse_steps: {len(self.mouse_path)}')


class TEMPLATE_OT_keypress_draw_handle(bpy.types.Operator):
    """Handle keypress with modifier"""
    bl_idname = "view3d.template_keypress_draw"
    bl_label = "Modal draw with keyboard and mouse event template"
    bl_description = "Use left click to draw stuff and combine with mofdifiers key, right click or Esc to abort"
    bl_options = {"REGISTER", "UNDO"}

    pressed_key = 'NOTHING'
    pressed_alt = False
    pressed_ctrl = False
    pressed_shift = False

    def modal(self, context, event):
        context.area.tag_redraw()

        ### /TESTER - keycode printer (flood console but usefull to know a keycode name)
        # if event.type not in {'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE'}:#avoid flood of mouse move.
            # print('key:', event.type, 'value:', event.value)
        ###  TESTER/
       
        ## Handle modifier keys state
        if event.type in {'LEFT_SHIFT', 'RIGHT_SHIFT'}: self.pressed_shift = event.value == 'PRESS'
        if event.type in {'LEFT_CTRL', 'RIGHT_CTRL'}: self.pressed_ctrl = event.value == 'PRESS'
        if event.type in {'LEFT_ALT', 'RIGHT_ALT'}: self.pressed_alt = event.value == 'PRESS'

        ## Get mouse move
        if event.type in {'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE'}:
            # INBETWEEN : Mouse sub-moves when too fast and need precision to get higher resolution sample in coordinate.

            ## Store mouse position in a variable
            self.mouse = (event.mouse_region_x, event.mouse_region_y)
            
            ## Store mouse path in a list (only if left click is pressed)
            if self.pressed_key == 'LEFTMOUSE':# This is evaluated as a continuous press
                self.mouse_path.append((event.mouse_region_x, event.mouse_region_y))

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
                
                if self.pressed_ctrl and self.pressed_alt and self.pressed_shift:# 3 mods combo operations
                    print('Click released with alt + ctrl + shift')

                if self.pressed_alt and self.pressed_shift:# shift+alt combo operations (add what necessary)
                    print('Click released with alt + shift')

                elif self.pressed_shift:
                    print('Click released with shift')    

                elif self.pressed_alt:
                    print('Click released with alt')
                
                elif self.pressed_ctrl:
                    print('Click released with ctrl')

                else:
                    print('Click released')
        

        if self.pressed_key == 'LEFTMOUSE':# using pressed_key variable
            ## Code here is continuously triggered during press
            pass
        ### CONTINUOUS PRESS/


        '''
        ## /SINGLE PRESS
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            if self.pressed_ctrl:
                print('Ctrl + click')
            else:
                print('Click')
            ## Can also finish on click (better do a dedicated exit func if duplicated with abort code)
            # bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            # return {'FINISHED'}
        ## SINGLE PRESS/
        '''

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
            
            ## Remove draw handler (if there was any)
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            
            print('STOPPED')#Dbg
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}


    def invoke(self, context, event):
        print('\nSTARTED')#Dbg
        
        ## Potential start checks (ex: stop if not in perspective view)
        # if not context.area.spaces[0].region_3d.is_perspective:
        #     self.report({'ERROR'}, "You are in Orthographic view (press 5 on your numpad to toggle perspective)")
        #     return {'CANCELLED'}
        
        ## Restrict to 3D view
        # if context.area.type != 'VIEW_3D':
        #     self.report({'WARNING'}, "View3D not found, cannot run operator")
        #     return {'CANCELLED'}

        ## Add the region OpenGL drawing callback (only if drawing is needed)
        ## draw in view space with 'POST_VIEW' and 'PRE_VIEW'
        args = (self, context)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
        
        ## If a timer is needed during modal
        # self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)#Interval in seconds
        
        ## initiate variable to use (ex: mouse coords)
        self.mouse_path = [] # coordinate list of the mouse path
        self.mouse = (0, 0) # updated tuple of mouse coordinate
        
        ## Starts the modal
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

### --- REGISTER ---

def register():
    from bpy.utils import register_class
    register_class(TEMPLATE_OT_keypress_draw_handle)
    # for cls in classes:
    #     register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    unregister_class(TEMPLATE_OT_keypress_draw_handle)
    # for cls in reversed(classes):
    #     unregister_class(cls)


if __name__ == "__main__":
    register()
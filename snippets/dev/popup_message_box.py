## Pop-up a message panel with infos [labels / label + icon / operator + label + icon]

import bpy

def show_message_box(_message = "", _title = "Message Box", _icon = 'INFO'):
    '''Show message box with element passed as string or list
    if _message if a list of lists:
        if sublist have 2 element:
            considered a label [text,icon]
        if sublist have 3 element:
            considered as an operator [ops_id_name, text, icon]
    '''

    def draw(self, context):
        for l in _message:
            if isinstance(l, str):
                self.layout.label(text=l)
            else:
                if len(l) == 2: # label with icon
                    self.layout.label(text=l[0], icon=l[1])
                elif len(l) == 3: # ops
                    self.layout.operator_context = "INVOKE_DEFAULT"
                    self.layout.operator(l[0], text=l[1], icon=l[2], emboss=False) # <- highligh the entry

    if isinstance(_message, str):
        _message = [_message]
    bpy.context.window_manager.popup_menu(draw, title = _title, icon = _icon)


## call with multiline text
#show_message_box(['my line 1', 'my line 2', 'my line 3'], 'Info Popup Title', 'QUESTION')

## call with text and icon
#show_message_box([ ['Crossed element', 'CANCEL'], ['Warning line', 'ERROR']], 'Pop up with icons')

## call with clickable operator call
show_message_box([ ['Blender is awesome', 'INFO'], ['wm.splash', 'Show splash', 'BLENDER']], 'Pop up with operator')

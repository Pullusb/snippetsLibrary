addon_keymaps = []
def register_keymaps():
    addon = bpy.context.window_manager.keyconfigs.addon

    key_prev = "BUTTON4MOUSE"#prev
    key_next = "BUTTON5MOUSE"#next

    ## Set origin to cursor/geometry with ctrl+shift+alt+ extra mousebutton
    km = addon.keymaps.new(name = "3D View", space_type = "VIEW_3D")# valid only in 3d view
    kmi = km.keymap_items.new("object.origin_set", type = key_prev, value = "PRESS", ctrl = True, shift = True, alt = True)
    kmi.properties.type = 'ORIGIN_GEOMETRY'
    kmi = km.keymap_items.new("object.origin_set", type = key_next, value = "PRESS", ctrl = True, shift = True, alt = True)
    kmi.properties.type = 'ORIGIN_CURSOR'

    addon_keymaps.append(km)

    ## Jump to keyframe with alt + extra mousebutton
    km = addon.keymaps.new(name = "Window", space_type = "EMPTY")# valid in all editor
    #kmi = km.keymap_items.new("screen.keyframe_jump", type = "BUTTON6MOUSE", value = "PRESS")#mouse button above 5 aren't recognize on logitech mouse on windaube
    kmi = km.keymap_items.new("screen.keyframe_jump", type = key_prev, value = "PRESS", alt = True)
    kmi.properties.next = False
    #kmi = km.keymap_items.new("screen.keyframe_jump", type = "BUTTON7MOUSE", value = "PRESS")#mouse button above 5 aren't recognize on logitech mouse on windaube
    kmi = km.keymap_items.new("screen.keyframe_jump", type = key_next, value = "PRESS", alt = True)
    kmi.properties.next = True

    addon_keymaps.append(km)

def unregister_keymaps():
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        for kmi in km.keymap_items:
            km.keymap_items.remove(kmi)
        ## Can't (and supposedly shouldn't ) suppress original category name...
        # wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()

def register():
    if not bpy.app.background:
        register_keymaps() 

def unregister():
    if not bpy.app.background:
        unregister_keymaps()

if __name__ == "__main__":
    register()
import bpy

addon_keymaps = []

def register_keymaps():
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc is None:
        return

    key_prev = "BUTTON4MOUSE" # Prev
    key_next = "BUTTON5MOUSE" # Next

    ## Set origin to cursor/geometry with ctrl+shift+alt+ extra mousebutton
    km = kc.keymaps.new(name = "3D View", space_type = "VIEW_3D") # valid only in 3d view
    
    kmi = km.keymap_items.new("object.origin_set", type = key_prev, value = "PRESS", ctrl = True, shift = True, alt = True)
    kmi.properties.type = 'ORIGIN_GEOMETRY'
    addon_keymaps.append((km, kmi))
    
    kmi = km.keymap_items.new("object.origin_set", type = key_next, value = "PRESS", ctrl = True, shift = True, alt = True)
    kmi.properties.type = 'ORIGIN_CURSOR'
    addon_keymaps.append((km, kmi))


    ## Jump to keyframe with alt + extra mousebutton
    km = kc.keymaps.new(name = "Window", space_type = "EMPTY") # valid in all editor

    ## note: BUTTON6MOUSE and BUTTON7MOUSE dont seem to be detected on windows
    kmi = km.keymap_items.new("screen.keyframe_jump", type = key_prev, value = "PRESS", alt = True)
    kmi.properties.next = False
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new("screen.keyframe_jump", type = key_next, value = "PRESS", alt = True)
    kmi.properties.next = True
    addon_keymaps.append((km, kmi))


def unregister_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


def register():
    if not bpy.app.background:
        register_keymaps() 

def unregister():
    if not bpy.app.background:
        unregister_keymaps()

if __name__ == "__main__":
    register()
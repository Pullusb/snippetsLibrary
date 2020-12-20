import bpy

## collapse all
#for km in bpy.context.window_manager.keyconfigs.user.keymaps:
#    for kmi in km.keymap_items:
#        kmi.show_expanded = False

## print info on expanded keymap
#for kmi in bpy.context.window_manager.keyconfigs.user.keymaps['3D View'].keymap_items:
for km in bpy.context.window_manager.keyconfigs.user.keymaps:
    for kmi in km.keymap_items:
        if kmi.show_expanded:
            print(f'\n--{km.name}--')
            for attr in dir(kmi):
                if attr.startswith('__'):
                    continue
                print(attr, getattr(kmi, attr))


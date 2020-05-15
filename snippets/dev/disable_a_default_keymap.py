## disabling a default keymap at startup
# https://blenderartists.org/t/removing-a-specific-default-hotkey-shortcut-via-a-script/1163540

def disable_default_kmi(km=None, idname=None, retries=10):
    wm = bpy.context.window_manager

    if not (km and idname) or retries < 1:
        return

    # the default keyconfig
    kc = wm.keyconfigs.user# ...user (or default) works (['blender'] in the original post )
    for kmi in kc.keymaps[km].keymap_items:
        if kmi.idname == idname:
            kmi.active = False
            print("Disabled", kmi.name)
            return

    print("Retrying..")
    # add some delay
    bpy.app.timers.register(
        lambda: disable_default_kmi(km, idname, retries - 1),
        first_interval=0.1)

# and use it like this:
def register():
    ...
    disable_default_kmi('Screen Editing', 'screen.area_options')
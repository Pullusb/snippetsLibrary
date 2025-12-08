## Custom function and operator to open addon preferences
## Old code! There is a native operator for this:
## bpy.ops.preferences.addon_show(module=__package__)

def open_addon_prefs():
    '''Open addon prefs windows with focus on current addon'''
    from .__init__ import bl_info
    wm = bpy.context.window_manager
    wm.addon_filter = 'All'
    if not 'COMMUNITY' in  wm.addon_support: # reactivate community
        wm.addon_support = set([i for i in wm.addon_support] + ['COMMUNITY'])
    wm.addon_search = bl_info['name']
    bpy.context.preferences.active_section = 'ADDONS'
    ## here if already expanded it will collapse (so drawback is calling alternate the state)
    bpy.ops.preferences.addon_expand(module=__package__)
    bpy.ops.screen.userpref_show('INVOKE_DEFAULT')

class WM_OT_open_addon_prefs(bpy.types.Operator):
    bl_idname = "wm.open_addon_prefs"
    bl_label = "Open Addon Prefs"
    bl_description = "Open user preferences window in addon tab and prefill the search with addon name"
    bl_options = {"REGISTER"}

    def execute(self, context):
        open_addon_prefs()
        return {'FINISHED'}

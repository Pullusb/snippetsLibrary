class myaddonPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__
    #some_bool_prop to display in the addon pref

    super_special_option : bpy.props.BoolProperty(
        name='Use super special option',
        description="This checkbox toggle the use of the super special options",
        default=False)

    def draw(self, context):
            layout = self.layout

            ## some 2.80 UI options
            # layout.use_property_split = True
            # flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
            # layout = flow.column()

            layout.label(text='Some text')

            # display the bool prop
            layout.prop(self, "super_special_option")

            # draw something only if a prop evaluate True
            if self.super_special_option:
                layout.label(text="/!\ Carefull, the super special option is especially powerfull")
                layout.label(text="    and with great power... well you know !")


def get_addon_prefs():
    '''
    function to read current addon preferences properties

    access a prop like this :
    prefs = get_addon_prefs()
    option_state = prefs.super_special_option

    oneliner : get_addon_prefs().super_special_option
    '''
    import os 
    addon_name = os.path.splitext(__name__)[0]
    preferences = bpy.context.preferences
    addon_prefs = preferences.addons[addon_name].preferences
    return (addon_prefs)
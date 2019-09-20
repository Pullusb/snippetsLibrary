##  base panel
class ADDONID_PT_panel_name(bpy.types.Panel):
    # bl_idname = "ADDONID_PT_panel_name"# identifier, if ommited, takes the name of the class.
    bl_label = "panel name"# title
    # bl_parent_id # If set, the panel becomes a sub-panel

    ## bl_options = {'DEFAULT_CLOSED', 'HIDE_HEADER' }# closed by default, collapse the panel and the label
    ## is_popover = False # if ommited
    ## bl_space_type = ['EMPTY', 'VIEW_3D', 'IMAGE_EDITOR', 'NODE_EDITOR', 'SEQUENCE_EDITOR', 'CLIP_EDITOR', 'DOPESHEET_EDITOR', 'GRAPH_EDITOR', 'NLA_EDITOR', 'TEXT_EDITOR', 'CONSOLE', 'INFO', 'TOPBAR', 'STATUSBAR', 'OUTLINER', 'PROPERTIES', 'FILE_BROWSER', 'PREFERENCES'], default 'EMPTY'

    ## bl_region_type types : ['WINDOW', 'HEADER', 'CHANNELS', 'TEMPORARY', 'UI', 'TOOLS', 'TOOL_PROPS', 'PREVIEW', 'HUD', 'NAVIGATION_BAR', 'EXECUTE', 'FOOTER', 'TOOL_HEADER'], default 'WINDOW'

    ## in 3D viewport 'N' menu
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"#name of the tab

    ## in properties
    # bl_space_type = 'PROPERTIES'
    # bl_region_type = 'WINDOW'

    # activating on some context only
    ## bl_context : object, objectmode, mesh_edit, curve_edit, surface_edit, text_edit, armature_edit, mball_edit, lattice_edit, pose_mode, imagepaint, weightpaint, vertexpaint, particlemode
    #bl_context = "objectmode"#render

    #need to be in object mode
    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    ## draw stuff inside the header (place before main label)
    # def draw_header(self, context):
    #     layout = self.layout
    #     layout.label(text="More text in header")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        # flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        # layout = flow.column()

        obj = bpy.context.object

        #default label and operator
        row = layout.row()
        row.label(text="Hello world!", icon='WORLD_DATA')

        row = layout.row()
        row.operator("mesh.primitive_cube_add")

        layout.use_property_split = False
        row = layout.row(align=True)
        row.prop(obj, 'hide_viewport')
        row.prop(obj, 'hide_render')
        row = layout.row(align=True)
        row.prop(obj.cycles, 'use_motion_blur')

        layout.separator()#Get some space

        box = layout.box()#put something in a box
        box.label(text="Selection Tools")
        box.operator("object.select_all").action = 'TOGGLE'#call default operators with options
        row = box.row()
        row.operator("object.select_all", text='Invert select').action = 'INVERT'
        row.operator("object.select_random")

        row = layout.row()
        row.operator("mesh.primitive_cube_add")

# Sub panel
class ADDONID_PT_subpanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    # bl_idname = "ADDONID_PT_panel_name"# identifier, if ommited, takes the name of the class.
    bl_label = "some scenes options"# title
    bl_parent_id = "ADDONID_PT_panel_name"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(context.scene.render, "film_transparent", text="transparent")
        layout.prop(context.scene.cycles, "samples")
        layout.prop(bpy.context.scene.tool_settings, "use_snap")
## UI list exemple with local folder blend listing with reload

import bpy, os

## Manual reloading

def reload_blends(self, context):
    scn = context.scene
    pl_prop = scn.bl_uilist_props
    uilist = scn.bl_uilist_props.blends
    uilist.clear()
    pl_prop['bl_idx'] = 0 # reset idx to zero

    # scan blend alongside current opened
    parent = os.path.dirname(bpy.data.filepath)
    blends = [os.path.join(parent, f)\
        for f in os.listdir(parent)\
        if f.endswith('.blend')\
        # and f != bpy.data.filepath\
        ]

    for bl in blends: # populate list
        item = uilist.add()
        scn.bl_uilist_props['bl_idx'] = len(uilist) - 1 # don't trigger updates
        item.blend_path = bl
        item.blend_name = os.path.basename(bl)

    #scn.bl_uilist_props.bl_idx = len(uilist) - 1 # trigger update

    # return len(blends) # return value must be None if function used in update

class OPS_OT_reload_blends(bpy.types.Operator):
    bl_idname = "op.reload_blends"
    bl_label = "Reload Palette Blends"
    bl_description = "Reload the blends in UI list of palettes linker"
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):
        reload_blends(self, context)
        return {"FINISHED"}

class OPS_OT_use_blend(bpy.types.Operator):
    bl_idname = "op.use_blend"
    bl_label = "Use Blend"
    bl_description = ""
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):
        pl_prop = context.scene.bl_uilist_props
        uilist = pl_prop.blends
        path = uilist[pl_prop.bl_idx].blend_path
        self.report({'INFO'}, f'selected path is {path}')
        return {"FINISHED"}

#--- UI List

class OPS_UL_blend_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        # self.use_filter_show = True # force open the search feature
        layout.label(text=item.blend_name)

    def draw_filter(self, context, layout):
        row = layout.row()
        subrow = row.row(align=True)
        subrow.prop(self, "filter_name", text="") # Only show items matching this name (use ‘*’ as wildcard)

        # reverse order
        icon = 'SORT_DESC' if self.use_filter_sort_reverse else 'SORT_ASC'
        subrow.prop(self, "use_filter_sort_reverse", text="", icon=icon) # built-in reverse

    def filter_items(self, context, data, propname):
        collec = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        flt_flags = []
        flt_neworder = []
        if self.filter_name:
            flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item, collec, "name",
                                                          reverse=self.use_filter_sort_reverse)#self.use_filter_name_reverse)
        return flt_flags, flt_neworder

#--- PROPERTIES

class OPS_PG_blend_prop(bpy.types.PropertyGroup):
    blend_name : bpy.props.StringProperty() # stem of the path
    blend_path : bpy.props.StringProperty() # full path

def do_something(self, context):
    pl_prop = context.scene.bl_uilist_props
    blend_uil = pl_prop.blends
    print(f"index is now {pl_prop['bl_idx']} on {len(blend_uil)} elements")

class OPS_PG_uilist_settings(bpy.types.PropertyGroup):
    bl_idx : bpy.props.IntProperty(update=do_something) # update_on_index_change to reload object
    blends : bpy.props.CollectionProperty(type=OPS_PG_blend_prop)


#--- PANEL

class OPS_PT_palettes_list_ui(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "View"
    bl_label = "Local Blends"
    # bl_options = {'DEFAULT_CLOSED'}
    # bl_parent_id = ""

    def draw(self, context):
        layout = self.layout
        pl_prop = context.scene.bl_uilist_props
        col= layout.column()
        row=col.row()

        # refresh button above
        # row.label(text='Blends in folder')
        # row.operator("op.reload_blends", icon="FILE_REFRESH", text="")

        col= layout.column()
        row = col.row()

        minimum_row = 5 # default number of line showes
        row.template_list("OPS_UL_blend_list", "", pl_prop, "blends", pl_prop, "bl_idx", 
            rows=minimum_row)

        # refresh button above in UIlist right side
        subcol = row.column(align=True)
        subcol.operator("op.reload_blends", icon="FILE_REFRESH", text="")
        
        col.operator("op.use_blend", icon="BLENDER", text="Show Blend Path")

classes = (
# ops
OPS_OT_use_blend,
OPS_OT_reload_blends,

# blend list
OPS_PG_blend_prop,
OPS_UL_blend_list,

# prop containing the one above
OPS_PG_uilist_settings,
OPS_PT_palettes_list_ui,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.bl_uilist_props = bpy.props.PointerProperty(type=OPS_PG_uilist_settings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.bl_uilist_props

if __name__ == "__main__":
    register()

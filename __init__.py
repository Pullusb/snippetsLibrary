# SPDX-License-Identifier: GPL-3.0-or-later
'''
Copyright (C) 2017 Samuel Bernou
Bernou.samuel@gmail.com

Created by Samuel Bernou
'''

bl_info = {
    "name": "Snippets Library",
    "description": "Add a library list to quickly load/save personnal texts snippets from text editor",
    "author": "Samuel Bernou",
    "version": (0, 6, 1),
    "blender": (3, 0, 0),
    "location": "Text editor > toolbar (ctrl+T) > Snippets tab",
    "warning": "",
    "doc_url": "https://github.com/Pullusb/snippetsLibrary",
    "tracker_url": "https://github.com/Pullusb/snippetsLibrary/issues",
    "category": "Text Editor" }


import bpy

# load and reload submodules
##################################

import importlib
from . import developer_utils
#from . import func
#from . import operators
from .operators import *
from .converter import *
from .func import *

# importlib.reload(developer_utils)
# modules = developer_utils.setup_addon_modules(__path__, __package__, "bpy" in locals())


### addon preferences panel

class SNIPPETSLIB_OT_libPathactions(Operator):
    bl_idname = "sniptool.multi_path_action"
    bl_label = "Action on additional paths"

    action: bpy.props.EnumProperty(
        items=(
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", "")
        )
    )

    def invoke(self, context, event):
        pref = get_addon_prefs()
        # scn = context.scene
        idx = pref.multipath_index

        try:
            item = pref.multipath[idx]
        except IndexError:
            pass
        
        else:
            if self.action == 'REMOVE':
                info = 'Item %s removed from list' % (pref.multipath[pref.multipath_index].name)
                pref.multipath_index -= 1
                if pref.multipath_index < 0: pref.multipath_index = 0
                self.report({'INFO'}, info)
                pref.multipath.remove(idx)
                
        if self.action == 'ADD':
            pref.multipath.add()       
            pref.multipath_index = (len(pref.multipath))

        return {"FINISHED"}

class SNIPPETSLIB_pathProp(bpy.types.PropertyGroup):
    """Prop group for multipath UIlist"""
    name : StringProperty( name="",
    description="Additional filepaths",
    subtype='FILE_PATH',
    default="")

class SNIPPETSLIB_UL_libpath(UIList):
    """list of multiple library path to scan"""

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index, flt_flag):
        split=layout.split(factor=0.05)
        split.label(text=str(index+1))
        split.prop(item, "name", emboss=False, translate=False)#, icon='WORDWRAP_ON'
        # layout.prop(item, "name", emboss=False, translate=False)#, icon='WORDWRAP_ON'


class snippetsPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    snippets_use_custom_path : bpy.props.BoolProperty(
        name='Use custom path',
        description="Set a cutom directory for snippets library",
        default=False)

    snippets_filepath : bpy.props.StringProperty(
        name="Snippets folder",
        subtype='FILE_PATH',
        )

    snippets_preview_line_number : bpy.props.IntProperty(
        name='Max preview lines',
        description="Choose number of lines to display on a snippet preview (default=25)",
        min=1,
        soft_max=500,
        max=2000,
        default=25)

    snippets_show_line_numbers : bpy.props.BoolProperty(
        name='Show line numbers',
        description="activate line numbers by defaut",
        default=True)

    snippets_show_word_wrap : bpy.props.BoolProperty(
        name='Show word wrap',
        description="activate word wrap by defaut",
        default=False)

    snippets_show_syntax_highlight : bpy.props.BoolProperty(
        name='Show syntax highlight',
        description="activate syntax highlight by defaut",
        default=True)

    snippets_show_line_highlight : bpy.props.BoolProperty(
        name='Show line highlight',
        description="activate line highlight by defaut",
        default=False)

    snippets_use_standard_template : bpy.props.BoolProperty(
        name='List blender default template',
        description="Include blender build-in template in library. Located in install folder (accessible in text editor footer menu)",
        default=True)

    snippets_convertpath_sublime : bpy.props.StringProperty(
        name="sublime-text snippets path",
        description="Path to save snippets at library conversion (/!\ overwrite files with same name)",
        subtype='DIR_PATH',
        )

    snippets_convertpath_vscode : bpy.props.StringProperty(
        name="vscode snippets path",
        description="Path to save snippets at library conversion (/!\ overwrite python.json)",
        subtype='DIR_PATH',
        )
    
    snippets_convertpath_atom : bpy.props.StringProperty(
        name="atom snippets path",
        description="Path to save snippets at library conversion (/!\ overwrite snippets.cson)",
        subtype='DIR_PATH',
        )

    snippets_convert_open : bpy.props.BoolProperty(
        name='Open containing folders after conversion',
        description="After conversion is finished, open target directory of new converted snippets",
        default=True)

    # snippets_save_as_py : bpy.props.BoolProperty(# format choice
        # name='Save as py',# format choice
        # description="The snippet file will have '.py' extension instead of '.txt' by default.\nThis change nothing for the library use. But a good rule is to use '.py' when the code can run as a standalone script.",# format choice
        # default=False)# format choice

    ### list of additional pathes
    multipath : bpy.props.CollectionProperty(type=SNIPPETSLIB_pathProp)#liloo multipath :)
    multipath_index : bpy.props.IntProperty()

    def draw(self, context):
        layout = self.layout
        # layout.use_property_split = True
        # flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        # layout = flow.column()

        ### layout.label(text="infos:")
        # layout.label(text="Snippets will be saved as invidual files")
        # layout.label(text="in a folder named 'snippets' (created at first use)")
        # layout.label(text="located aside the addon file (unless you enter a custom path)")
        # layout.separator()

        ### main path (default or custom)
        layout.label(text='Library path')
        col = layout.column(align=False)
        col.label(text='Main library:')
        col.prop(self, "snippets_use_custom_path")
        if self.snippets_use_custom_path:
            #layout.label(text="Leave the field empty to get default location")#"Custom path to you text load/save folder\n"
            col.prop(self, "snippets_filepath")
            col.label(text="May not work if space are in path.")

        ### secondary sources
        col = layout.column(align=False)
        col.label(text='Additional sources:')
        # col.label(text='use default template')
        col.prop(self, "snippets_use_standard_template")

        col.label(text='Enter secondary folder filepath to scan:')
        ### multi paths UIlist
        row = col.row()
        row.template_list("SNIPPETSLIB_UL_libpath", "", self, "multipath", self, "multipath_index", rows=2)
        sidecol = row.column(align=True)
        sidecol.operator("sniptool.multi_path_action", icon='ADD', text="").action = 'ADD'#NEWFOLDER
        sidecol.operator("sniptool.multi_path_action", icon='REMOVE', text="").action = 'REMOVE'

        layout = self.layout
        ### Saving format
        # layout.separator()# format choice
        # layout.label(text='Saving preferences:')# format choice
        # layout.prop(self, "snippets_save_as_py")# format choice

        ### UI preferences
        col = layout.column(align=False)
        col.separator()
        col.label(text='Preview preferences:')
        col.prop(self, "snippets_preview_line_number")

        col.separator()
        col.label(text="When creating new text block, what properties to activate :")
        col.prop(self, "snippets_show_line_numbers")
        col.prop(self, "snippets_show_word_wrap")
        col.prop(self, "snippets_show_syntax_highlight")
        col.prop(self, "snippets_show_line_highlight")     

        col.separator()
        col.label(text="Convert the library to external editor format:")
        col.label(text="Sublime Text, VScode, Atom")

        col.prop(self, "snippets_convertpath_sublime")
        col.prop(self, "snippets_convertpath_vscode")
        col.prop(self, "snippets_convertpath_atom")
        col.prop(self, "snippets_convert_open")
        col.label(text="If paths above are not set, destination will be a folder 'converted_snippets' in the addon folder")

        row=col.row(align=True)
        row.operator('sniptool.convert', text='All').convertid = 0
        row.operator('sniptool.convert', text='Sublime').convertid = 1
        row.operator('sniptool.convert', text='VScode').convertid = 2
        row.operator('sniptool.convert', text='Atom').convertid = 3

# register
##################################

classes = (
SNIPPETSLIB_pathProp,
SNIPPETSLIB_sniptoolProp,
snippetsPreferences,
SNIPPETSLIB_OT_actions,
SNIPPETSLIB_OT_saveSnippet,
SNIPPETSLIB_OT_insertTemplate,
SNIPPETSLIB_OT_reloadItems,
SNIPPETSLIB_OT_OpenSnippetsFolder,
SNIPPETSLIB_UL_items,
SNIPPETSLIB_PT_uiList,
SNIPPETSLIB_OT_deleteSnippet,
# SNIPPETSLIB_OT_searchItems,
SNIPPETSLIB_OT_convert,
SNIPPETSLIB_OT_libPathactions,
SNIPPETSLIB_UL_libpath,
)

import traceback

def register():
    try:
        for cls in classes:
            bpy.utils.register_class(cls)
    except:
        traceback.print_exc()

    # print("Registered {} with {} modules".format(bl_info["name"], len(modules)))
    bpy.types.Scene.sniptool = bpy.props.CollectionProperty(type=SNIPPETSLIB_sniptoolProp)
    bpy.types.Scene.sniptool_index = bpy.props.IntProperty(update=update_func)
    bpy.types.Scene.sniptool_preview = bpy.props.StringProperty()
    bpy.types.Scene.sniptool_preview_use = bpy.props.BoolProperty(default=True, description='If enabled show a preview of the snippets and list its methods')
    bpy.types.Scene.sniptool_preview_defs = bpy.props.StringProperty()
    # bpy.types.Scene.sniptool_search = bpy.props.StringProperty(description='Note: The search is case sensitive')

    #launch first reload automatically
    # reload_snippets()#still bad context... cant access scene from pref.
    # bpy.ops.sniptool.reload_list()#not the right context

def unregister():
    try:
        for cls in classes:
            bpy.utils.unregister_class(cls)
    except:
        traceback.print_exc()

    print("Unregistered {}".format(bl_info["name"]))
    del bpy.types.Scene.sniptool
    del bpy.types.Scene.sniptool_index
    del bpy.types.Scene.sniptool_preview
    del bpy.types.Scene.sniptool_preview_use
    del bpy.types.Scene.sniptool_preview_defs
    # del bpy.types.Scene.sniptool_search

if __name__ == "__main__":
    register()

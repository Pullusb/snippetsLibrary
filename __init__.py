'''
Copyright (C) 2017 Samuel Bernou
Bernou.samuel@gmail.com

Created by Samuel Bernou

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "snippets library",
    "description": "Add a library list to quickly load/save personnal texts snippets from text editor",
    "author": "Samuel Bernou",
    "version": (0, 2, 3),
    "blender": (2, 80, 0),
    "location": "Text editor > toolbar (ctrl+T) > Dev tab",
    "warning": "",
    "wiki_url": "https://github.com/Pullusb/snippetsLibrary",
    "category": "Text Editor" }


import bpy
from bpy.props import IntProperty, CollectionProperty #, StringProperty

# load and reload submodules
##################################

import importlib
from . import developer_utils
#from . import func
#from . import operators
from .operators import *
from .converter import *
from .func import *

importlib.reload(developer_utils)
modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())


### addon preferences panel

class snippetsPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    snippets_custom_path : bpy.props.BoolProperty(
        name='Use custom path',
        description="Set a cutom directory for snippets library",
        default=False)

    snippets_filepath : bpy.props.StringProperty(
        name="Snippets folder",
        subtype='FILE_PATH',
        )

    snippets_preview_line_number : bpy.props.IntProperty(
        name='Max preview lines',
        description="Choose number of lines to display on a snippet preview (default=10)",
        min=1,
        soft_max=500,
        max=2000,
        default=10)

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

        layout.prop(self, "snippets_custom_path")
        if self.snippets_custom_path:
            #layout.label(text="Leave the field empty to get default location")#"Custom path to you text load/save folder\n"
            layout.prop(self, "snippets_filepath")
            layout.label(text="May not work if space are in path.")

        layout.separator()
        layout.label(text='Preview preferences:')
        layout.prop(self, "snippets_preview_line_number")

        layout.separator()
        layout.label(text="When creating new text block, what properties to activate :")
        layout.prop(self, "snippets_show_line_numbers")
        layout.prop(self, "snippets_show_word_wrap")
        layout.prop(self, "snippets_show_syntax_highlight")
        layout.prop(self, "snippets_show_line_highlight")     

        layout.separator()
        layout.label(text="Convert the library to external editor format:")
        layout.label(text="Sublime Text, VScode, Atom")

        row=layout.row(align=True)
        row.operator('sniptool.convert', text='All').convertid = 0
        row.operator('sniptool.convert', text='Sublime').convertid = 1
        row.operator('sniptool.convert', text='VScode').convertid = 2
        row.operator('sniptool.convert', text='Atom').convertid = 3
        row=layout.row()
        row.label

# register
##################################

classes = (
SNIPPETSLIB_OT_actions,
SNIPPETSLIB_OT_saveSnippet,
SNIPPETSLIB_OT_insertTemplate,
SNIPPETSLIB_OT_reloadItems,
SNIPPETSLIB_OT_OpenSnippetsFolder,
SNIPPETSLIB_sniptoolProp,
SNIPPETSLIB_UL_items,
SNIPPETSLIB_PT_uiList,
SNIPPETSLIB_OT_deleteSnippet,
SNIPPETSLIB_OT_searchItems,
SNIPPETSLIB_OT_convert,
snippetsPreferences,
)

import traceback

def register():
    try:
        for cls in classes:
            bpy.utils.register_class(cls)
    except:
        traceback.print_exc()

    print("Registered {} with {} modules".format(bl_info["name"], len(modules)))
    bpy.types.Scene.sniptool = CollectionProperty(type=SNIPPETSLIB_sniptoolProp)
    # bpy.types.Scene.sniptool_index = bpy.props.IntProperty(update=update_func, set=set_update_func)
    bpy.types.Scene.sniptool_index = bpy.props.IntProperty(update=update_func)
    bpy.types.Scene.sniptool_preview = bpy.props.StringProperty()
    bpy.types.Scene.sniptool_preview_use = bpy.props.BoolProperty(default=True, description='If enabled show a preview of the snippets and list its methods')
    bpy.types.Scene.sniptool_preview_defs = bpy.props.StringProperty()
    bpy.types.Scene.sniptool_search = bpy.props.StringProperty(description='Note: The search is case sensitive')

    
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
    del bpy.types.Scene.sniptool_search

if __name__ == "__main__":
    register()

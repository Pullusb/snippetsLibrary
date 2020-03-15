import bpy
import os
import re
from os.path import splitext, dirname, basename, join
import time
from bpy.types import Panel, UIList, Operator, PropertyGroup
from bpy.props import StringProperty, EnumProperty, BoolProperty, IntProperty, CollectionProperty

from .func import *
###--- UI List items


# ui list item actions
class SNIPPETSLIB_OT_actions(Operator):
    bl_idname = "sniptool.list_action"
    bl_label = "List Action"

    action : EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
        )
    )

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.sniptool_index

        try:
            item = scn.sniptool[idx]
        except IndexError:
            pass

        else:
            if self.action == 'DOWN' and idx < len(scn.sniptool) - 1:
                item_next = scn.sniptool[idx+1].name
                scn.sniptool_index += 1
                # info = 'Item %d selected' % (scn.sniptool_index + 1)

            elif self.action == 'UP' and idx >= 1:
                item_prev = scn.sniptool[idx-1].name
                scn.sniptool_index -= 1
                # info = 'Item %d selected' % (scn.sniptool_index + 1)
            
            # self.report({'INFO'}, info)

        return {"FINISHED"}


# -------------------------------------------------------------------
# UI draw
# -------------------------------------------------------------------

# sniptool list
class SNIPPETSLIB_UL_items(UIList):
    
    show_category : BoolProperty(name="Show_category", default=False,
    description="display category (containing folder name) in a column")

    # use_filter_name_reverse : BoolProperty(name="Reverse Name", default=False, options=set(),
    #                                                 description="Reverse name filtering")

    filter_content : BoolProperty(name="Filter content", default=True, options=set(),
                                                    description="Search in all snippets contents instead of titles")

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index, flt_flag):        
        self.use_filter_show = True#force open the search feature

        if self.show_category:
            ## splitted with prefix
            split = layout.split(factor=0.2)
            # split.label(text=str(index))
            # split.label(text=item.prefix)#without icon
            split.label(text=item.prefix, icon='WORDWRAP_ON')#with icon
            split.label(text=item.name)
        else :
            ## basic
            layout.label(text=item.name, icon='WORDWRAP_ON')#label instead of prop disable renamimg feature (good)

        ## use basic property
        # layout.prop(item, "name", text="", emboss=False, translate=False, icon='WORDWRAP_ON')
        
        # use operator (problem, text is centered in operator)
        # layout.operator("sniptool.template_insert", text=item.name, emboss=True, translate=False, icon='WORDWRAP_ON')
        """ layout.label(text='', icon='WORDWRAP_ON')
        layout.separator()
        layout.operator("sniptool.template_insert", text=item.name, emboss=False) """

    def draw_filter(self, context, layout):
        # Nothing much to say here, it's usual UI code...
        row = layout.row()

        subrow = row.row(align=True)
        subrow.prop(self, "filter_name", text="")#Only show items matching this name (use ‘*’ as wildcard)
    
        subrow.prop(self, "filter_content", text="", icon='ZOOM_ALL')#search in content


        subrow = row.row(align=True)
        subrow.prop(self, "show_category", text="", icon='LONGDISPLAY')#show category (folder)

        # invert result
        icon = 'ZOOM_OUT' if self.use_filter_invert else 'ZOOM_IN'
        subrow.prop(self, "use_filter_invert", text="", icon=icon)

        # sort by name : ALPHA SORTING NOT WORKING, MUST CHANGE IN filter_items
        # subrow.prop(self, "use_filter_sort_alpha", text="", icon='SORTALPHA')#buit-in sort

        # reverse order
        icon = 'SORT_DESC' if self.use_filter_sort_reverse else 'SORT_ASC'
        subrow.prop(self, "use_filter_sort_reverse", text="", icon=icon)#built-in reverse

        
        '''
        row = layout.row(align=True)
        row.label("Order by:")
        row.prop(self, "use_order_name", toggle=True)
        row.prop(self, "use_order_importance", toggle=True)
        icon = 'TRIA_UP' if self.use_filter_orderby_invert else 'TRIA_DOWN'
        row.prop(self, "use_filter_orderby_invert", text="", icon=icon)
        '''


    def filter_items(self, context, data, propname):
        # example : https://docs.blender.org/api/blender_python_api_current/bpy.types.UIList.html
        # This function gets the collection property (as the usual tuple (data, propname)), and must return two lists:
        # * The first one is for filtering, it must contain 32bit integers were self.bitflag_filter_item marks the
        #   matching item as filtered (i.e. to be shown), and 31 other bits are free for custom needs. Here we use the
        # * The second one is for reordering, it must return a list containing the new indices of the items (which
        #   gives us a mapping org_idx -> new_idx).
        # Please note that the default UI_UL_list defines helper functions for common tasks (see its doc for more info).
        # If you do not make filtering and/or ordering, return empty list(s) (this will be more efficient than
        # returning full lists doing nothing!).
        
        collec = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        # Default return values.
        flt_flags = []
        flt_neworder = []


        # Filtering by name #not working damn !
        if self.filter_name:
            if self.filter_content:
                #search in file content
                # https://docs.blender.org/api/blender_python_api_2_77_0/bpy.types.UI_UL_list.html
                flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item, collec, "content",
                                                          reverse=self.use_filter_sort_reverse)#self.use_filter_name_reverse)
            else:
                #search in name
                flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item, collec, "name",
                                                          reverse=self.use_filter_sort_reverse)#self.use_filter_name_reverse)

        return flt_flags, flt_neworder


# Pannel
class SNIPPETSLIB_PT_uiList(Panel):
    """Creates a Panel in the Object properties window"""
    bl_idname = 'SNIPPETSLIB_PT_ui_panel'
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_category = "Snippets"#Dev
    bl_label = "Snippets List"
    
    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene

        row = layout.row()

        minimum_rows = 8
        row.template_list("SNIPPETSLIB_UL_items", "", scn, "sniptool", scn, "sniptool_index", rows=minimum_rows)
        #https://docs.blender.org/api/blender2.8/bpy.types.UILayout.html#bpy.types.UILayout.template_list

        col = row.column(align=True)
        ## possible icon for insert : #LIBRARY_DATA_DIRECT RIGHTARROW LIBRARY_DATA_DIRECT NODE_INSERT_OFF
        col.operator("sniptool.template_insert", icon="PASTEDOWN", text="").standalone = False
        col.operator("sniptool.template_insert", icon="FILE_NEW", text="").standalone = True#TEXT DUPLICATE
        col.separator()
        col.operator("sniptool.reload_list", icon="FILE_REFRESH", text="")
        # col.operator("sniptool.search_select", icon="ZOOM_ALL", text="")#search_content
        col.separator()
        col.operator("sniptool.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("sniptool.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'
        col.separator()
        col.operator("sniptool.save_snippet", icon="ADD", text="")
        col.operator("sniptool.delete_confirm_dialog", icon="REMOVE", text="")
        col.operator("sniptool.open_snippet_folder", icon="FILE_FOLDER",  text="")

        prev_icon = 'HIDE_OFF' if bpy.context.scene.sniptool_preview_use else 'HIDE_ON'
        col.prop(scn, 'sniptool_preview_use', text="", icon=prev_icon)
        # Preview zone
        # row.prop(scn, 'sniptool_preview_use', text='Preview', icon=prev_icon)#fat button with preview
        if bpy.context.scene.sniptool_preview_use:
            if bpy.context.scene.sniptool_preview:
                box = layout.box()
                col = box.column(align=True)
                for l in bpy.context.scene.sniptool_preview.split('\n'):
                    col.label(text=l)
            
            # def scan box 
            if bpy.context.scene.sniptool_preview_defs:
                box = layout.box()
                col = box.column(align=True)
                for l in bpy.context.scene.sniptool_preview_defs.split('\n'):
                    col.label(text=l)


# -------------------------------------------------------------------
# OPS
# -------------------------------------------------------------------

class SNIPPETSLIB_OT_deleteSnippet(Operator):
    """Delete selected snippet (show a confirmation popup)"""
    bl_idname = "sniptool.delete_confirm_dialog"
    bl_label = "Delete snippet"
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scn = bpy.context.scene
        snip = scn.sniptool[scn.sniptool_index]
        snipname = snip.name
        idx = scn.sniptool_index
        fp = snip.filepath#get_snippet(snipname)
        try:
            os.remove(fp)
        except Exception as e:
            message = 'Error trying to delete {}\n'.format(fp, e)
            return {'CANCELLED'}

        info = 'Item %s removed from list' % (snipname)
        if scn.sniptool_index > 0: scn.sniptool_index -= 1
        self.report({'INFO'}, info)
        scn.sniptool.remove(idx)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.snip = bpy.context.scene.sniptool[bpy.context.scene.sniptool_index].name
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text='Do you really want to delete "{}"'.format(self.snip))
        layout.label(text='This operation delete the snippet file (cant be undone)')
        

class SNIPPETSLIB_OT_saveSnippet(Operator):
    bl_idname = "sniptool.save_snippet"
    bl_label = "Save snippet"
    bl_description = "Save text selection to a new snippet\nPopup a field to name the new snippet"
    bl_options = {'REGISTER', 'INTERNAL'}
    
    # subtype (string) – Enumerator in [‘FILE_PATH’, ‘DIR_PATH’, ‘FILE_NAME’, ‘BYTE_STRING’, ‘PASSWORD’, ‘NONE’].
    # options (set) – Enumerator in [‘HIDDEN’, ‘SKIP_SAVE’, ‘ANIMATABLE’, ‘LIBRARY_EDITABLE’, ‘PROPORTIONAL’,’TEXTEDIT_UPDATE’].
    newsnip      : StringProperty(update=update_save_func, options={'TEXTEDIT_UPDATE'}, subtype='FILE_NAME')
    save_name    : StringProperty()
    # display_name : StringProperty()

    """ @classmethod
    def poll(cls, context):
        return True """

    def execute(self, context):
        # pref = get_addon_prefs()
        scn = context.scene
        # check name
        snipname = formatted_name(self.newsnip)#equivalent of self.save_name
            
        if not snipname:
            #return error or use a placeholder (can be usefull for fast saving when hasty)
            snipname = generate_unique_snippet_name()
            print('no name specified, using generated placeholder:', snipname)
            # self.report({'ERROR'}, 'No Name.\nYou need to specify a naame for your snippet')
            # return{'CANCELLED'}

        # check here if snippets already exists
        if snipname in self.filelist:
            error = f'Snippet "{name}" already exists in library'
            self.report({'ERROR'}, error)
            return{'CANCELLED'}


        ## if arriverd here, all good
        # save the file on disk
        save_template(self.library, snipname, self.selection)
        # add it to UI list
        item = scn.sniptool.add()
        item.id = len(scn.sniptool)

        item.name = path_to_display_name(snipname)#Same format as when reloading
        item.prefix = 'snip'#since it's not 'classed yet, use snip'
        item.content = self.selection
        item.filepath = join(self.library, snipname)


        scn.sniptool_index = (len(scn.sniptool)-1)
        info = '%s added' % (item.name)
        self.report({'INFO'}, info)

        return{'FINISHED'}
    
    def invoke(self, context, event):
        scn = context.scene
        self.pref = get_addon_prefs()
        # sanity/error checks
        lib = locateLibrary(single=True)
        if lib:
            self.library = lib[0]#maybe choose lib in the future...
        else:
            pathErrorMsg = get_main_lib_path() + ' not found or inaccessible'
            self.report({'ERROR'}, pathErrorMsg)
            return{'CANCELLED'}

        self.filelist = []
        for root, dirs, files in os.walk(self.library, topdown=True):
            for f in files:
                if f.endswith('.txt') or f.endswith('.py'):
                    self.filelist.append(os.path.splitext(f)[0])

        text = getattr(bpy.context.space_data, "text", None)
        if not text:
            self.report({'ERROR'}, 'No text file.\nYou need to have a text in the editor with something selected')
            return{'CANCELLED'}
        
        self.selection = selection_to_snippet(self, text)#dedented get_selected_text
        if not self.selection:
            self.report({'ERROR'}, 'Nothing selected.\nYou need to select the text to be saved as snippet')
            return{'CANCELLED'}

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text='Chose a name for this snippet')
        layout.prop(self, "newsnip", text="Name")
        # layout.prop(self.pref, "snippets_save_as_py", text="Save as .py")# format choice
        
        # live helper
        if self.save_name in self.filelist:#self.newsnip:
            layout.label(icon='CANCEL', text='This filename already exists')
        
        if re.search(r'[^A-Za-z0-9\._ -]', self.newsnip):
            layout.label(icon='INFO', text='Invalid character were replaced')#ERROR
        
        if self.save_name:# self.newsnip:
            layout.label(text=f"Filename: {self.save_name}", icon='FILE')
        
        # if self.display_name:#self.newsnip:
        #     layout.label(text=f"Display: {self.display_name}", icon='WORDWRAP_ON')
        


# insert button
class SNIPPETSLIB_OT_insertTemplate(Operator):
    bl_idname = "sniptool.template_insert"
    bl_label = "Insert snippet"
    bl_description = "Insert selected snippet at cursor location or in a new text block"
    bl_options = {'REGISTER', 'INTERNAL'}

    standalone : BoolProperty(default=False)

    def execute(self, context):
        scn = context.scene
        pref = get_addon_prefs()
        if not len(scn.sniptool):
            error = 'No snippets to insert in list\nClick the reload button to scan library.\nIf your library folder is empty, add new snippets with the "+" button'
            self.report({'ERROR'}, error)
            return{'CANCELLED'}

        # snip = scn.sniptool[scn.sniptool_index].name
        snip = scn.sniptool[scn.sniptool_index]
        text = getattr(bpy.context.space_data, "text", None)
        if not text or self.standalone:
            #create new text-block if not any
            text = bpy.data.texts.new(snip.name)# name or filename ? (if no text datablock)
            context.space_data.text = text
            ### Since it's code Toggling ON some coding space data basic feature #maybe add in pref to choose basic behavior (in devtool todo too)
            context.space_data.show_line_numbers = pref.snippets_show_line_numbers
            context.space_data.show_word_wrap = pref.snippets_show_word_wrap
            context.space_data.show_syntax_highlight = pref.snippets_show_syntax_highlight
            context.space_data.show_line_highlight = pref.snippets_show_line_highlight

        #context override for the ops.text.insert() function
        override = {'window': context.window,
                    'area'  : context.area,
                    'region': context.region,
                    'space': context.space_data,
                    'edit_text' : text
                    }

        Loaded_text = snip.content#load_text(get_snippet(snip))
        #get character position in text
        charPos = text.current_character
        #print ('charPos', charPos)

        #indentedText = Loaded_text
        if Loaded_text:
            FormattedText = Loaded_text
            #indent text lines exept first (already at cursor position)
            if charPos > 0:
                textLines = Loaded_text.split('\n')
                if not len(textLines) == 1:
                    #print("indent subsequent lines")
                    indentedLines = []
                    indentedLines.append(textLines[0])
                    for line in textLines[1:]:
                        indentedLines.append(' '*charPos + line)

                    FormattedText = '\n'.join(indentedLines)

            # if future tabstop implementation : put re.search here to get index position of stops

            if '$' in FormattedText:#extra precautions...not really needed.
                # replace tabstop with placeholder (or delete if no placeholder)
                FormattedText = re.sub(r'\${\d{1,2}:?(.*?)}', r'\1', FormattedText)
            # print(FormattedText)
            insert_template(override, FormattedText)

        else:
            error = 'Fail to load snippet content'
            self.report({'ERROR'}, error)
            return{'CANCELLED'}

        return{'FINISHED'}

    """ 
    def invoke(self, context, event):
        print('event.value: ', event.value)
        print('event.type: ', event.type)
        print('event.shift: ', event.shift)
        return self.execute(context)
    """

def reload_snippets():
    preview_enabled = False
    if bpy.context.scene.sniptool_preview_use:
        preview_enabled = True
        bpy.context.scene.sniptool_preview_use = False

    scn = bpy.context.scene
    lst = scn.sniptool
    current_index = scn.sniptool_index

    start = time.time()
    library = locateLibrary()
    # print('--> library: >>', library)

    if library:
        allsnip = scan_multi_folders(library)
        if len(lst) > 0:#remove all item in list
            # reverse range to remove last item first
            for i in range(len(lst)-1,-1,-1):
                scn.sniptool.remove(i)
            #self.report({'INFO'}, "All items removed")

        for snipfp in allsnip:#populate list
            item = scn.sniptool.add()
            item.id = len(scn.sniptool)#id (len of list in the ad loop)
            item.name = path_to_display_name(snipfp)
            item.filepath = snipfp#fullfilepath

            tag = basename(dirname(snipfp))#prefix (folder name) snippets -> snip
            tag = 'snip' if tag.lower() == 'snippets' else tag
            tag = tag.replace('templates', '').strip('_ ') if tag.startswith('templates') else tag
            item.prefix = tag
            item.content = load_text(snipfp)#text

        
        scn.sniptool_index = (len(scn.sniptool)-1)
            #info = '%s added to list' % (item.name)

        print(f"{len(allsnip)} loaded in {time.time()-start:.2f}")
        if preview_enabled:
            bpy.context.scene.sniptool_preview_use = True
    else:
        return (1)

# reload button
class SNIPPETSLIB_OT_reloadItems(Operator):
    bl_idname = "sniptool.reload_list"
    bl_label = "Reload List"
    bl_description = "Load/reload snippets list from disk\nshift+click to clear list (save space in blend file)"
    # bl_options = {'REGISTER', 'INTERNAL'}

    clear : BoolProperty(default=False)

    def execute(self, context):
        if self.clear:
            bpy.context.scene.sniptool.clear()
            bpy.context.scene.sniptool_preview = ''       
            bpy.context.scene.sniptool_preview_defs = ''
            return {'FINISHED'}
        
        error = reload_snippets()
        if error:
            pathErrorMsg = get_main_lib_path() + ' not found or inaccessible'
            self.report({'ERROR'}, pathErrorMsg)
            return{'CANCELLED'}

        return {'FINISHED'}

    def invoke(self, context, event):
        self.clear = event.shift#if shift is pressed, clear instead of reloading
        return self.execute(context)

# search inside the content, "reload" the list with only compatible snippets
class SNIPPETSLIB_OT_searchItems(Operator):
    bl_idname = "sniptool.search_select"
    bl_label = "Search from selection"
    bl_description = "Fill the search field with selection."
    # bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        selection = ''

        text = getattr(bpy.context.space_data, "text", None)
        if text:
            selection = get_selected_text(self, text, one_line=True)
        
        if not selection:
            self.report({'ERROR'}, 'You need to select a text to use this (not multi-line)')
            return{'CANCELLED'}

        # print('SNIPPETSLIB_UL_items: ', SNIPPETSLIB_UL_items)
        attr = getattr(SNIPPETSLIB_UL_items, 'filter_name', '')
        # context.space_data.filter_name
        print('context.space_data: ', dir(context.space_data))
        # print('context.space_data.filter_name: ', context.space_data.filter_name)
        print('SNIPPETSLIB_UL_items.filter_name >>', attr)

        res = setattr(SNIPPETSLIB_UL_items, 'filter_name', selection)
        print('res: ', res)
        # SNIPPETSLIB_UL_items.filter_name = selection
        return{'FINISHED'}

class SNIPPETSLIB_OT_OpenSnippetsFolder(Operator):
    bl_idname = "sniptool.open_snippet_folder"
    bl_label = "Open library folder"
    bl_description = "Open main library folder location\nShift+clic = open folder of selected snippets"
    # bl_options = {'REGISTER', 'INTERNAL'}#internal means it will be hided from the search.

    selected_location : BoolProperty(default=False)

    def execute(self, context):
        scn = context.scene
        library = locateLibrary(single=True)
        print('library: ', library)
        if library:
            if self.selected_location:
                if len(scn.sniptool):
                    #open file of selected
                    fp = scn.sniptool[scn.sniptool_index].filepath
                    if exists(fp):
                        openFolder(fp)
                    else:#try with containing folder
                        pathErrorMsg = f'file {basename(fp)} not found at given adress\n'
                        fp = dirname(fp)
                        if exists(fp):
                            pathErrorMsg += 'Opening previous containing folder'
                            openFolder(fp)
                        else:
                            pathErrorMsg += f'Containing folder not found too: {fp}' 
                        self.report({'ERROR'}, pathErrorMsg)
            else:
                #just open lib folder
                openFolder(library[0])
        else:
            pathErrorMsg = get_main_lib_path() + ' not found or inaccessible'
            self.report({'ERROR'}, pathErrorMsg)
        return{'FINISHED'}

    def invoke(self, context, event):
        self.selected_location = event.shift
        return self.execute(context)

# Create sniptool property group
class SNIPPETSLIB_sniptoolProp(PropertyGroup):
    '''name = StringProperty() '''
    id : IntProperty(update=update_func)
    filepath : StringProperty()
    prefix : StringProperty()
    content : StringProperty()


### TRY implement TABSTOP with Insertion Modal, difficult... (moving the cursor around is hard...)

"""
class SNIPPETSLIB_OT_insertTemplate(Operator):
    bl_idname = "sniptool.template_insert"
    bl_label = "Insert snippet"
    bl_description = "Insert selected snippet at cursor location or in a new text block"
    bl_options = {'REGISTER', 'INTERNAL'}

    standalone : BoolProperty(default=False)

    def modal(self, context, event):
        if event.type in {'ESC', 'ENTER' 'LEFT_ARROW', 'DOWN_ARROW', 'RIGHT_ARROW', 'UP_ARROW', 'RIGHTMOUSE', 'LEFTMOUSE'}:
            # the moment there is a 'move' the modal ends
            return {'FINISHED'}
        
        elif event.type == 'TAB':
            if event.value == 'RELEASE':
                # go to next tabstop
                self.tabcount += 1

        # return {'CANCELLED'}


        # print('event', event.type)
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        scn = context.scene
        if locateLibrary():
            snip = scn.sniptool[scn.sniptool_index].name
            text = getattr(bpy.context.space_data, "text", None)
            if not text or self.standalone:
                pref = get_addon_prefs()
                #create new text-block if not any
                text = bpy.data.texts.new(snip)# get the name of the snippets if no text datablock
                context.space_data.text = text
                ### Since it's code Toggling ON some coding space data basic feature #maybe add in pref to choose basic behavior (in devtool todo too)
                context.space_data.show_line_numbers = pref.snippets_show_line_numbers
                context.space_data.show_word_wrap = pref.snippets_show_word_wrap
                context.space_data.show_syntax_highlight = pref.snippets_show_syntax_highlight
                context.space_data.show_line_highlight = pref.snippets_show_line_highlight

            #context override for the ops.text.insert() function
            override = {'window': context.window,
                        'area'  : context.area,
                        'region': context.region,
                        'space': context.space_data,
                        'edit_text' : text
                        }

            Loaded_text = load_text(get_snippet(snip))
            #get character position in text
            charPos = text.current_character
            #print ('charPos', charPos)

            #indentedText = Loaded_text
            if Loaded_text:
                FormattedText = Loaded_text
                #indent text lines exept first (already at cursor position)
                if charPos > 0:
                    textLines = Loaded_text.split('\n')
                    if not len(textLines) == 1:
                        #print("indent subsequent lines")
                        indentedLines = []
                        indentedLines.append(textLines[0])
                        for line in textLines[1:]:
                            indentedLines.append(' '*charPos + line)

                        FormattedText = '\n'.join(indentedLines)

                # if future tabstop implementation : put re.search here to get index position of stops
                tabstops = False
                if '${' in FormattedText:# TABSTOPS, avoid regexing if no $ found
                    tabstops = True
                    # self.stoptext = FormattedText
                    matches = re.finditer(r'\${(\d{1,2}):?(.*?)}', FormattedText)

                    if matches:
                        FormattedText = re.sub(r'\${\d{1,2}:?(.*?)}', r'\1', FormattedText)
                    else:
                        print('TABSTOPS !')
                        tabstops = False
                        
                    # replace tabstop with placeholder (or delete if not)
                # print(FormattedText)
                insert_template(override, FormattedText)
                #lauch modal with text infos
            else:
                print('Fail to load snippet !')
        else:
            pathErrorMsg = locateLibrary(True) + ' not found or inaccessible'
            self.report({'ERROR'}, pathErrorMsg)
            return {'CANCELLED'}

        ## ----
        if tabstops:
            #Once the snippets is inserted, Gather info in self-variables and go tabstopping
            self.lentotal = len(FormattedText)
            self.tabnum = FormattedText.count('    ')
            print('self.tabnum: ', self.tabnum)
            self.stops = []
            self.tabcount = 0
            self.select = True
            
            total_extra = 0
            for m in matches:
                print('start of group 0:',m.start(0))
                #m.group(1) = number (id), m.group(2) = placeholder
                extra =  m.end(0) - m.start(0) - len( m.group(2) )
                self.stops.append(
                    {'pos' : m.start(0) - total_extra,#position less all tag cahracter
                    'id' : int(m.group(1)),
                    'chars' : len( m.group(2) ),
                    'extra' : extra,
                    })

                total_extra += extra #add after append.

                #eventually sort by id but will be difficult to go reverse...

            #roll back to beggining
            print('self.lentotal: ', self.lentotal)

            self.totalmove = self.lentotal - self.tabnum * 3
            for i in range(self.totalmove):
                bpy.ops.text.move(type='PREVIOUS_CHARACTER')
            
            print('line:', text.current_character,', char:', text.current_line_index)
            #go to first tabstop

            move_to_stop = self.stops[0]['pos']
            print('move_to_stop: ', move_to_stop)
            for i in range(move_to_stop):
                bpy.ops.text.move(type='NEXT_CHARACTER')

            print('line:', text.current_character,', char:', text.current_line_index)

            print('Done !')
            return {'FINISHED'}
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
            
            ''' # standalone filter
            #may be if its use as standalone bypass the tabstopping... why not ??! 
            if self.standalone:

            else:
                self.report({'INFO'}, "New text file created")
                return {'FINISHED'}
            '''

        return {'FINISHED'}




# search inside the content, "reload" the list with only compatible snippets
class SNIPPETSLIB_OT_searchItems(Operator):
    bl_idname = "sniptool.search_content"
    bl_label = "Search inside snippets"
    bl_description = "Like reload but listing only matching snippets.\n\
        Search in content and title.\n\
        (can be slow if a there is a lot of snippets or slow time access to disk/server)\n\
        You can select text (one line only) before launching to use it as search term"
    # bl_options = {'REGISTER', 'INTERNAL'}

    case_sensitive : BoolProperty(
        name='Case sensitive',
        description="Use a case sensitive search",
        default=False)

    use_regex : BoolProperty(
        name='Use regex',
        default=False,
        description='If enabled you can enter a Regular expressions pattern in the searchfield\n(Case sensitive option is take into account)')#text='use regex'


    def execute(self, context):
        # TODO : redo all the search, need to filter only, not rescan...
        scn = bpy.context.scene
        search_term = scn.sniptool_search.strip()
        if not search_term:
            self.report({'ERROR'}, 'Search field is empty')
            return{'CANCELLED'}

        preview_enabled = False
        if bpy.context.scene.sniptool_preview_use:
            preview_enabled = True
            bpy.context.scene.sniptool_preview_use = False

        reg = None
        if self.use_regex:
            try:
                if self.case_sensitive:
                    reg = re.compile(search_term)
                else:
                    reg = re.compile(search_term, flags=re.I)# for case insensitive search

            except Exception as e:
                message = "Error with entered regex:\n%s" % str(e)
                self.report({'ERROR'}, message)
                return{'CANCELLED'}

        lst = scn.sniptool
        current_index = scn.sniptool_index

        library = locateLibrary()
        if library:
            start = time.time()
            allsnip = snippetsList = []

            for lib in library:
                for root, dirs, files in os.walk(lib, topdown=True):
                    for f in files:
                        if f.endswith('.txt') or f.endswith('.py'):
                            fp = join(root, f)
                            with open(fp, 'r') as fd:
                                #search in content and title.
                                if self.use_regex:#regex search
                                    if reg.search(fd.read()) or reg.search(f):
                                        snippetsList.append(splitext(basename(f))[0])
                                
                                else:#classic search
                                    if self.case_sensitive:
                                        if search_term in fd.read() or search_term in f: #search_term.lower() in fd.read().lower()
                                            snippetsList.append(splitext(basename(f))[0])
                                    else:
                                        if search_term.lower() in fd.read().lower() or search_term.lower() in f.lower(): #
                                            snippetsList.append(splitext(basename(f))[0])

            print('searching time: {:.4f}s'.format(time.time() - start) )

            if not allsnip:
                self.report({'ERROR'}, 'Nothing matched')
                return{'CANCELLED'}

            ## populate the list with result of the search
            if len(lst) > 0:#remove all item in list
                # reverse range to remove last item first
                for i in range(len(lst)-1,-1,-1):
                    scn.sniptool.remove(i)
                #self.report({'INFO'}, "All items removed")

            for snipfp in allsnip:#populate list
                item = scn.sniptool.add()
                item.id = len(scn.sniptool)
                item.name = path_to_display_name(snipfp)
                item.filepath = snipfp#fullfilepath
                item.prefix = basename(dirname(snipfp))#prefix (folder name)
                item.content = load_text(snipfp)#text
            
            scn.sniptool_index = (len(scn.sniptool)-1)

            if preview_enabled:
                bpy.context.scene.sniptool_preview_use = True

        else:
            pathErrorMsg = get_main_lib_path() + ' not found or inaccessible'
            self.report({'ERROR'}, pathErrorMsg)
            return{'CANCELLED'}
   
        return{'FINISHED'}

    def invoke(self, context, event):
        text = getattr(bpy.context.space_data, "text", None)
        if text:
            selection = get_selected_text(self, text, one_line=True)
            if selection:
                bpy.context.scene.sniptool_search = selection
            
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        row=layout.row(align=True)
        # layout.label(text='search')
        row.prop(self, "case_sensitive")
        row.prop(self, "use_regex")
        layout = self.layout
        layout.prop(bpy.context.scene, "sniptool_search", text="Find")
"""
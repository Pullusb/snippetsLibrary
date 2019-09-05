import bpy
import os
from os.path import splitext, basename, join
import time
from bpy.types import Panel, UIList, Operator
from bpy.props import IntProperty, CollectionProperty #, StringProperty

from .func import *
###--- UI List items

# ui list item actions
class SNIPPETSLIB_OT_actions(Operator):
    bl_idname = "sniptool.list_action"
    bl_label = "List Action"

    action : bpy.props.EnumProperty(
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
# draw
# -------------------------------------------------------------------

# sniptool list
class SNIPPETSLIB_UL_items(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        self.use_filter_show = True#force open the search feature
        layout.label(text=item.name, icon='WORDWRAP_ON')#label instead of prop disable renamimg feature (good)
        # layout.prop(item, "name", text="", emboss=False, translate=False, icon='WORDWRAP_ON')

        #Other tests
        #split = layout.split(0.3)
        ##add to draw index (useless)
        #split.label("%d" % (index))
        #split.prop(item, "name", text="", emboss=False, translate=False, icon='WORDWRAP_ON')
        ##delete icon to remove sheets icons (also useless)

    def invoke(self, context, event):
        pass

# draw the panel
class SNIPPETSLIB_PT_uiList(Panel):
    """Creates a Panel in the Object properties window"""
    bl_idname = 'SNIPPETSLIB_PT_ui_panel'
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_category = "Dev"
    bl_label = "Snippets List"

    # bpy.types.Scene.new_snippets_name = bpy.props.StringProperty(description='name that snippets will take, name will be generated')
    
    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene

        row = layout.row()

        minimum_rows = 9
        row.template_list("SNIPPETSLIB_UL_items", "", scn, "sniptool", scn, "sniptool_index", rows=minimum_rows)
        #https://docs.blender.org/api/blender2.8/bpy.types.UILayout.html#bpy.types.UILayout.template_list

        col = row.column(align=True)
        ## possible icon for insert : #LIBRARY_DATA_DIRECT RIGHTARROW LIBRARY_DATA_DIRECT NODE_INSERT_OFF
        col.operator("sniptool.template_insert", icon="PASTEDOWN", text="").standalone = False
        col.operator("sniptool.template_insert", icon="FILE_NEW", text="").standalone = True#TEXT DUPLICATE
        col.separator()
        col.operator("sniptool.reload_list", icon="FILE_REFRESH", text="")
        col.operator("sniptool.search_content", icon="ZOOM_ALL", text="")
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
                row = box.column()
                for l in bpy.context.scene.sniptool_preview.split('\n'):
                    row.label(text=l)
            
            # def scan box 
            if bpy.context.scene.sniptool_preview_defs:
                box = layout.box()
                row = box.column()
                for l in bpy.context.scene.sniptool_preview_defs.split('\n'):
                    row.label(text=l)


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
        snip = scn.sniptool[scn.sniptool_index].name
        idx = scn.sniptool_index

        fp = get_snippet(snip)
        try:
            os.remove(fp)
        except Exception as e:
            message = 'Error trying to delete {}\n'.format(fp, e)
            return {'CANCELLED'}

        info = 'Item %s removed from list' % (snip)
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
    
    newsnip: bpy.props.StringProperty()


    def execute(self, context):
        scn = context.scene
        library = locateLibrary()
        if library:
            snipname = clipit(context, self.newsnip)
            if snipname:
                item = scn.sniptool.add()
                item.id = len(scn.sniptool)

                item.name = splitext(snipname)[0]

                scn.sniptool_index = (len(scn.sniptool)-1)
                info = '%s added to list' % (item.name)
                self.report({'INFO'}, info)
            else:
                self.report({'warning'}, 'nothing selected')

            ###print all snipsauce :
            #for i in scn.sniptool:
            #    print (i.name, i.id)

        else:
            pathErrorMsg = locateLibrary(True) + ' not found or inaccessible'
            self.report({'ERROR'}, pathErrorMsg)
        return{'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text='Chose a name for this snippet')
        layout.prop(self, "newsnip", text="Name")


# insert button
class SNIPPETSLIB_OT_insertTemplate(Operator):
    bl_idname = "sniptool.template_insert"
    bl_label = "Insert snippet"
    bl_description = "Insert selected snippet at cursor location or in a new text block"
    bl_options = {'REGISTER', 'INTERNAL'}

    standalone : bpy.props.BoolProperty(default=False)

    def execute(self, context):
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

                if '$' in FormattedText:#extra precautions...not really needed.
                    # replace tabstop with placeholder (or delete if not)
                    FormattedText = re.sub(r'\${\d{1,2}:?(.*?)}', r'\1', FormattedText)
                # print(FormattedText)
                insert_template(override, FormattedText)

            else:
                print('Fail to load snippet !')
        else:
            pathErrorMsg = locateLibrary(True) + ' not found or inaccessible'
            self.report({'ERROR'}, pathErrorMsg)
        return{'FINISHED'}


def reload_snippets():
    preview_enabled = False
    if bpy.context.scene.sniptool_preview_use:
        preview_enabled = True
        bpy.context.scene.sniptool_preview_use = False

    scn = bpy.context.scene
    lst = scn.sniptool
    current_index = scn.sniptool_index
    library = locateLibrary()
    if library:
        allsnip = reload_folder(library)

        if len(lst) > 0:#remove all item in list
            # reverse range to remove last item first
            for i in range(len(lst)-1,-1,-1):
                scn.sniptool.remove(i)
            #self.report({'INFO'}, "All items removed")

        for snipname in allsnip:#populate list
            item = scn.sniptool.add()
            item.id = len(scn.sniptool)
            item.name = snipname
        
        scn.sniptool_index = (len(scn.sniptool)-1)
            #info = '%s added to list' % (item.name)

        # else:
        #     self.report({'INFO'}, "Nothing to add")
        if preview_enabled:
            bpy.context.scene.sniptool_preview_use = True
    else:
        return (1)


# relaod button
class SNIPPETSLIB_OT_reloadItems(Operator):
    bl_idname = "sniptool.reload_list"
    bl_label = "Reload List"
    bl_description = "Reload snippets list from disk"
    # bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        error = reload_snippets()
        if error:
            pathErrorMsg = locateLibrary(True) + ' not found or inaccessible'
            self.report({'ERROR'}, pathErrorMsg)
            return{'CANCELLED'}

        return{'FINISHED'}


# search inside the content, "reload" the list with only compatible snippets
class SNIPPETSLIB_OT_searchItems(Operator):
    bl_idname = "sniptool.search_content"
    bl_label = "Search inside snippets"
    bl_description = "Like reload but listing only matching snippets.\n\
        Search in content and title.\n\
        (can be slow if a there is a lot of snippets or slow time access to disk/server)\n\
        You can select text (one line only) before launching to use it as search term"
    # bl_options = {'REGISTER', 'INTERNAL'}

    case_sensitive : bpy.props.BoolProperty(
        name='Case sensitive',
        description="Use a case sensitive search",
        default=False)

    use_regex : bpy.props.BoolProperty(
        name='Use regex',
        default=False,
        description='If enabled you can enter a Regular expressions pattern in the searchfield\n(Case sensitive option is take into account)')#text='use regex'


    def execute(self, context):
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
            for root, dirs, files in os.walk(library, topdown=True):
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

            for snipname in allsnip:#populate list
                item = scn.sniptool.add()
                item.id = len(scn.sniptool)
                item.name = snipname
            
            scn.sniptool_index = (len(scn.sniptool)-1)
                #info = '%s added to list' % (item.name)

            # else:
            #     self.report({'INFO'}, "Nothing to add")
            if preview_enabled:
                bpy.context.scene.sniptool_preview_use = True

        else:
            pathErrorMsg = locateLibrary(True) + ' not found or inaccessible'
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


class SNIPPETSLIB_OT_OpenSnippetsFolder(Operator):
    bl_idname = "sniptool.open_snippet_folder"
    bl_label = "Open library folder"
    bl_description = "Open snippets folder location"
    # bl_options = {'REGISTER', 'INTERNAL'}#internal means it will be hided from the search.

    def execute(self, context):
        scn = context.scene
        library = locateLibrary()
        if library:
            #open folder
            openFolder(library)
        else:
            pathErrorMsg = locateLibrary(True) + ' not found or inaccessible'
            self.report({'ERROR'}, pathErrorMsg)
        return{'FINISHED'}

# Create sniptool property group
class SNIPPETSLIB_sniptoolProp(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    id : IntProperty(update=update_func)


### Insertion is going Modal ! Yaay !
### TRY implement TABSTOP, difficult... not there yet (moving the cursor around is such a pain...)

"""
class SNIPPETSLIB_OT_insertTemplate(Operator):
    bl_idname = "sniptool.template_insert"
    bl_label = "Insert snippet"
    bl_description = "Insert selected snippet at cursor location or in a new text block"
    bl_options = {'REGISTER', 'INTERNAL'}

    standalone : bpy.props.BoolProperty(default=False)

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
"""
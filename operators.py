import bpy
import os
from bpy.types import Panel, UIList
from bpy.props import IntProperty, CollectionProperty #, StringProperty

from .func import *
###--- UI List items

# ui list item actions
class SNIPPETSLIB_OT_actions(bpy.types.Operator):
    bl_idname = "sniptool.list_action"
    bl_label = "List Action"

    action : bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            # ('REMOVE', "Remove", ""),
            # ('ADD', "Add", ""),
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
        self.use_filter_show = True
        #split = layout.split(0.3)
        ##add to draw index (useless)
        #split.label("%d" % (index))
        #split.prop(item, "name", text="", emboss=False, translate=False, icon='WORDWRAP_ON')
        ##delete icon to remove sheets icons (alsouseless)
        layout.prop(item, "name", text="", emboss=False, translate=False, icon='WORDWRAP_ON')

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

        rows = 2
        row = layout.row()

        """ # refresh and insert above list
        row.operator("sniptool.reload_list", icon="FILE_REFRESH")
        row = layout.row()
        row.operator("sniptool.template_insert", icon="FORWARD")
        row = layout.row() """

        row.template_list("SNIPPETSLIB_UL_items", "", scn, "sniptool", scn, "sniptool_index", rows=rows)

        col = row.column(align=True)
        col.operator("sniptool.reload_list", icon="FILE_REFRESH", text="")
        col.operator("sniptool.template_insert", icon="FORWARD", text="")#LIBRARY_DATA_DIRECT RIGHTARROW PASTEDOWN LIBRARY_DATA_DIRECT NODE_INSERT_OFF
        col.separator()
        col.operator("sniptool.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("sniptool.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'
        col.separator()
        col.operator("sniptool.save_snippet", icon="ADD", text="")
        col.operator("sniptool.delete_confirm_dialog", icon="REMOVE", text="")
        col.operator("sniptool.open_snippet_folder", icon="FILE_FOLDER",  text="")

        """ # add menu under ui list
        row = layout.row()
        col = row.column(align=True)
        col.separator()
        col.prop(context.scene, 'new_snippets_name', text='snippets name')
        col.operator("sniptool.save_snippet", icon="PLUS")#SAVE_COPY COPYDOWN
        col.operator("sniptool.open_snippet_folder", icon="FILE_FOLDER") """

        # Preview zone
        row = layout.row()
        prev_icon = 'HIDE_OFF' if bpy.context.scene.sniptool_preview_use else 'HIDE_ON'
        row.prop(scn, 'sniptool_preview_use', text='Preview', icon=prev_icon)#FILE_TEXT
        if bpy.context.scene.sniptool_preview_use:
            if bpy.context.scene.sniptool_preview:
                # box.prop(scn, 'sniptool_preview', text='')# '\n' not recognised, split in multiple labels
                box = layout.box()
                for l in bpy.context.scene.sniptool_preview.split('\n'):
                    box.label(text=l)
            else:
                pass


# -------------------------------------------------------------------
# OPS
# -------------------------------------------------------------------

class SNIPPETSLIB_OT_deleteSnippet(bpy.types.Operator):
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
        

class SNIPPETSLIB_OT_saveSnippet(bpy.types.Operator):
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

                item.name = os.path.splitext(snipname)[0]

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
class SNIPPETSLIB_OT_insertTemplate(bpy.types.Operator):
    bl_idname = "sniptool.template_insert"
    bl_label = "Insert snippet"
    bl_description = "Insert selected snippet at cursor location"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        scn = context.scene
        if locateLibrary():
            snip = scn.sniptool[scn.sniptool_index].name
            text = getattr(bpy.context.space_data, "text", None)
            if text:
                pass
                #print(text.name)
            else:
                #create new text-block if not any
                text = bpy.data.texts.new(snip)# get the name of the snippets if no text datablock
                context.space_data.text = text

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
class SNIPPETSLIB_OT_reloadItems(bpy.types.Operator):
    bl_idname = "sniptool.reload_list"
    bl_label = "Reload List"
    bl_description = "Reload snippets list from disk"
    # bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        error = reload_snippets()
        if error:
            pathErrorMsg = locateLibrary(True) + ' not found or inaccessible'
            self.report({'ERROR'}, pathErrorMsg)

        return{'FINISHED'}


class SNIPPETSLIB_OT_OpenSnippetsFolder(bpy.types.Operator):
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

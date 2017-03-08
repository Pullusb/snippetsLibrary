bl_info = {
    "name": "snippets library",
    "description": "Add a library list to quickly load/save personnal texts snippets from text editor",
    "author": "Samuel Bernou",
    "version": (0, 0, 1),
    "blender": (2, 78, 0),
    "location": "Text editor > toolbar",
    "warning": "",
    "wiki_url": "",
    "category": "Text Editor" }
 
import bpy, os
import textwrap
from bpy.props import IntProperty, CollectionProperty #, StringProperty 
from bpy.types import Panel, UIList
 

def get_addon_prefs():
    #addon_name = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
    # -> same as __name__
    user_preferences = bpy.context.user_preferences
    addon_prefs = user_preferences.addons[__name__].preferences
    return (addon_prefs)

def openFolder(folderpath):
    """
    open the folder at the path given
    with cmd relative to user's OS
    """
    from sys import platform
    myOS = platform
    if myOS.startswith('linux') or myOS.startswith('freebsd'):
        # linux
        cmd = 'xdg-open '
        #print("operating system : Linux")
    elif myOS.startswith('win'):
        # Windows
        #cmd = 'start '
        cmd = 'explorer '
        #print("operating system : Windows")
        if not folderpath:
            return('/')
        
    else:#elif myOS == "darwin":
        # OS X
        #print("operating system : MACos")
        cmd = 'open '

    if not folderpath:
        print ('in openFolder : no folderpath !', folderpath)
        return('//')

    #double quote the path to avoid problem with special character
    folderpath = '"' + folderpath + '"'
    fullcmd = cmd + folderpath

    #print & launch open command
    print(fullcmd)
    os.system(fullcmd)


def locateLibrary(justGet=False):
    #addon = bpy.context.user_preferences.addons.get('snippetsLibrary')
    # print (addon)
    # prefs = addon.preferences
    prefs = get_addon_prefs()
    cust_path = prefs.snippets_custom_path
    cust_fp = prefs.snippets_filepath 
    if cust_path:#specified user location
        if cust_fp:
            snipDir = bpy.path.abspath(cust_fp)
        else:
            print ('!!! error with Custom file path (or empty), reading blend_directory')
            snipDir = (bpy.data.filepath)
 
    else:#default location (addon folders "snippets" subdir)
        script_file = os.path.realpath(__file__)
        directory = os.path.dirname(script_file)
        snipDir = os.path.join(directory, 'snippets/')
        if not os.path.exists(snipDir):
            try:
                os.mkdir(snipDir)
                print('snippets directory created at:', snipDir)
            except:
                print('!!! could not create snippets directory created at:', snipDir)

    if justGet:
        return(snipdir)
    else:
        if os.path.exists(snipDir):
            if os.path.isdir(snipDir):
                return(snipDir)
            else:
                return (os.path.split(snipDir)[0])
        else:
            print('error with location:', snipDir)
            return (0)



def insert_template(override, src_text):
    bpy.ops.text.insert(override, text=src_text)

def reload_folder(fp):
    '''take a filepath (location of the files) and return a list of filenames'''
    #recursive in folder
    snippetsList = []
    for root, dirs, files in os.walk(fp, topdown=True):
        for f in files:
            if f.endswith('.txt') or f.endswith('.py'):
                snippetsList.append(os.path.splitext(os.path.basename(f))[0])
    return (snippetsList)

                
def load_text(fp):
    if fp:
        with open(fp, 'r') as fd:
            text=fd.read()
        return text
    else:
        print('in load_text: no fp to read !')
        return(0)

def save_template(fp, name, text):
    if not name.endswith(('.txt', '.py')):
        name = name + '.txt'
    fd = open(os.path.join(fp, name),'w')
    fd.write(text)
    fd.close()
    return 0
 
def get_snippet(name):
    '''take a name
    and return a filepath if found in library
    '''
    library = locateLibrary()
    if library:
        for root, dirs, files in os.walk(library, topdown=True):#"."
            for f in files:
                if name.lower() == os.path.splitext(f)[0].lower():
                    return(os.path.join(root, f))
        print('in get_snippet: not found >', name)
        return (0)
    else:
        return(1)

def clipit(context):
    library = locateLibrary()
    bpy.ops.text.copy()
    clip = bpy.context.window_manager.clipboard
    if clip:
        #print (clip)
        ###kill preceding spaces before saving (allow to copy at indentation 0)
        clip = textwrap.dedent(clip)
        if context.scene.new_snippets_name:
            snipname = context.scene.new_snippets_name + '.txt'
        else:#generate Unique snipName
            from random import randrange
            import time
            snipname = 'snip'+ str(randrange(999)) + time.strftime("_%Y-%m-%d_%H-%M-%S") +'.txt'

        save_template(library, snipname, clip)
        return (snipname)
    else:
        return (0)

###--- UI List items

# ui list item actions
class Uilist_actions(bpy.types.Operator):
    bl_idname = "sniptool.list_action"
    bl_label = "List Action"
 
    action = bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", ""),
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
                info = 'Item %d selected' % (scn.sniptool_index + 1)
                self.report({'INFO'}, info)
 
            elif self.action == 'UP' and idx >= 1:
                item_prev = scn.sniptool[idx-1].name
                scn.sniptool_index -= 1
                info = 'Item %d selected' % (scn.sniptool_index + 1)
                self.report({'INFO'}, info)
 
            elif self.action == 'REMOVE':
                info = 'Item %s removed from list' % (scn.sniptool[scn.sniptool_index].name)
                scn.sniptool_index -= 1
                self.report({'INFO'}, info)
                scn.sniptool.remove(idx)
 
        if self.action == 'ADD':
            ###---mypart
            snipname = clipit(context)
            if snipname:
                item = scn.sniptool.add()
                item.id = len(scn.sniptool)

                item.name = os.path.splitext(snipname)[0]

                scn.sniptool_index = (len(scn.sniptool)-1)
                info = '%s added to list' % (item.name)
                self.report({'INFO'}, info)
            else:
                self.report({'warning'}, 'nothing selected')
 
        return {"FINISHED"}
 



# -------------------------------------------------------------------
# draw
# -------------------------------------------------------------------
### addon preferences panel

class snippetsPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    snippets_custom_path = bpy.props.BoolProperty(
        name='Use custom path',
        description="Set a cutom directory for snippets library",
        default=False)

    snippets_filepath = bpy.props.StringProperty(
        name="Snippets folder",
        subtype='FILE_PATH',
        )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "snippets_custom_path")
        layout.label(text="Snippets will be saved as invidual files")
        layout.label(text="in a folder named 'snippets' (created at first use)")
        layout.label(text="located aside the addon file (unless you enter a custom path)")
        if self.snippets_custom_path:
            #layout.label(text="Leave the field empty to get default location")#"Custom path to you text load/save folder\n"
            layout.prop(self, "snippets_filepath")
            layout.label(text="May not work if space are in path.")
 
# sniptool list
class UL_items(UIList):
 
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        #split = layout.split(0.3)
        ##add to draw index (useless)
        #split.label("%d" % (index))
        #split.prop(item, "name", text="", emboss=False, translate=False, icon='WORDWRAP_ON')
        ##delete icon to remove sheets icons (alsouseless)
        layout.prop(item, "name", text="", emboss=False, translate=False, icon='WORDWRAP_ON')

    def invoke(self, context, event):
        pass   
 
# draw the panel
class UIListPanelExample(Panel):
    """Creates a Panel in the Object properties window"""
    bl_idname = 'OBJECT_PT_my_panel'
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_label = "Snippets List"
 
    bpy.types.Scene.new_snippets_name = bpy.props.StringProperty(description='name that snippets will take, name will be generated')

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
 
        rows = 2
        row = layout.row()
        row.operator("sniptool.reload_list", icon="FILE_REFRESH")
        row = layout.row()
        row.template_list("UL_items", "", scn, "sniptool", scn, "sniptool_index", rows=rows)
 
        col = row.column(align=True)
        # col.operator("sniptool.list_action", icon='ZOOMIN', text="").action = 'ADD'
        # col.operator("sniptool.list_action", icon='ZOOMOUT', text="").action = 'REMOVE'
        col.separator()
        col.operator("sniptool.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("sniptool.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'
 
        row = layout.row()
        col = row.column(align=True)
        col.operator("sniptool.template_insert", icon="LIBRARY_DATA_DIRECT")#LIBRARY_DATA_DIRECT RIGHTARROW FORWARD
        col.separator()
        col.prop(context.scene, 'new_snippets_name', text='snippets name')
        col.operator("sniptool.save_snippet", icon="SAVE_COPY")
        col.operator("sniptool.open_snippet_folder", icon="FILE_FOLDER")
        # col.separator()

 
 
class Uilist_saveSnippet(bpy.types.Operator):
    bl_idname = "sniptool.save_snippet"
    bl_label = "save snippet"
    bl_description = "save selection to a file named after this"
 
    def execute(self, context):
        scn = context.scene
        library = locateLibrary()
        if library:
            snipname = clipit(context)
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


# insert button
class Uilist_insertTemplate(bpy.types.Operator):
    bl_idname = "sniptool.template_insert"
    bl_label = "insert List Item"
    bl_description = "insert Item in textBlock"
 
    def execute(self, context):
        scn = context.scene
        if locateLibrary():
            text = getattr(bpy.context.space_data, "text", None)
            if text:
                pass
                #print(text.name)
            else:
                pass
                #print('no text data')
            
            #context override for the ops.text.insert() function
            override = {'window': context.window,
                        'area'  : context.area,
                        'region': context.region,
                        'space': context.space_data,
                        'edit_text' : text
                        }
            snip = scn.sniptool[scn.sniptool_index].name
            
            Loaded_text = load_text(get_snippet(snip))#load_text(r'G:\WORKS\Prog\blender\SB Blender addons\DEV_SamTool\generic name.txt')
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


# relaod button
class Uilist_reloadItems(bpy.types.Operator):
    bl_idname = "sniptool.reload_list"
    bl_label = "Reload List"
    bl_description = "Reload all items in the list"
 
    def execute(self, context):
        scn = context.scene
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
        else:
            pathErrorMsg = locateLibrary(True) + ' not found or inaccessible'
            self.report({'ERROR'}, pathErrorMsg)
 
        return{'FINISHED'}
 

class OpenSnippetsFolder(bpy.types.Operator):
    bl_idname = "sniptool.open_snippet_folder"
    bl_label = "open library folder"
    bl_description = "open snippets folder location"
 
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
class sniptoolProp(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    id = IntProperty()
 
# -------------------------------------------------------------------
# register
# -------------------------------------------------------------------
 
def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.sniptool = CollectionProperty(type=sniptoolProp)
    bpy.types.Scene.sniptool_index = IntProperty()
 
def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.sniptool
    del bpy.types.Scene.sniptool_index
 
if __name__ == "__main__":
    register()
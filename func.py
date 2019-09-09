import bpy
import os, re
import textwrap
import time
from os.path import dirname, basename


def scan_definitions(text):
    'return a list of all def and class'
    # print(text)
    # print('------------')
    # return capture group (avoid the : of the end)
    return re.findall(r'^((?:def|class) [-\w]+\([-\w,\. =]*\)):', text, re.MULTILINE)

def containing_folder(fp):
    '''get a filepath, return only parent folder name (or empty string)'''
    return basename(dirname(fp))


def update_func(self, context):
    '''called when a new snippets is selected'''

    """ if bpy.context.scene.sniptool_insert_on_clic:
        bpy.ops.sniptool.template_insert() """

    if bpy.context.scene.sniptool_preview_use:
        # print('update call', time.strftime('%H:%M:%S'))#debug to find when update is called
        prefs = get_addon_prefs()
        preview_linum = prefs.snippets_preview_line_number
        
        # Change preview content
        select_snip = bpy.context.scene.sniptool[bpy.context.scene.sniptool_index].name
        fp = get_snippet(select_snip)
        if not fp:
            print('impossible to find', select_snip)
            return
        content = load_text(fp)
        if not content:
            print('problem while getting content of:', fp)
        
        # get rid of tabstops and show only placeholder:
        content = re.sub(r'\${\d{1,2}:?(.*?)}', r'\1', content)

        # get first lines of the text to feed preview
        lines = []
        truncated = False

        defs = None
        # with open(fp, 'r') as fd:
            # for i, l in enumerate(fd.readlines()):
        splitcontent = content.splitlines(True)
        for i, l in enumerate(splitcontent):
            if i > preview_linum:#limit of line to preview
                truncated = True
                break
            lines.append(l)
    
        preview = ''.join(lines)
        if truncated: preview += '. . . +{} lines . . .'.format(len(splitcontent)-preview_linum)

        defs = scan_definitions(content)
        deflist = ''
        if defs:
            #before preview -> # deflist = '{0} Functions/classes:\n- {1}\n{2}\n\n'.format(str(len(defs)), '\n- '.join(defs), '*-*-*-*-*-*-*-*-*-*-*-*-*')#**------**\n
            #after preview -> deflist = '\n\n{2}\n{0} Functions/classes:\n- {1}'.format(str(len(defs)), '\n- '.join(defs), '*-*-*-*-*-*-*-*-*-*-*-*-*')
            deflist = '{0} Functions/classes:\n- {1}'.format(str(len(defs)), '\n- '.join(defs))

        # feed preview
        bpy.context.scene.sniptool_preview = preview
        bpy.context.scene.sniptool_preview_defs = deflist
    return


def get_addon_prefs():
    #addon_name = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
    #print ('abspath', os.path.abspath(__file__))
    #print ('file', __file__)
    # -> same as __name__
    #print ('addon_name', addon_name)
    #print('--name--', __name__)
    addon_name = os.path.splitext(__name__)[0]
    preferences = bpy.context.preferences
    addon_prefs = preferences.addons[addon_name].preferences
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
    folderpath = '"' + os.path.normpath(folderpath) + '"'
    fullcmd = cmd + folderpath

    #print & launch open command
    print(fullcmd)
    os.system(fullcmd)

def get_selected_text(self, text, one_line=False):
    """
    get selected text (whitout using copy buffer)
    if no selection return None
    If one_line == True, if selection goes over one line return None.
    Customised function from Dalai Felinto (dfelinto)
    """
    current_line = text.current_line
    select_end_line = text.select_end_line

    current_character = text.current_character
    select_end_character = text.select_end_character

    # if there is no selected text return None
    if current_line == select_end_line:
        if current_character == select_end_character:
            return None
        else:
            return current_line.body[min(current_character,select_end_character):max(current_character,select_end_character)]

    if one_line:
        return

    text_return = None
    writing = False
    normal_order = True # selection from top to bottom

    for line in text.lines:
        if not writing:
            if line == current_line:
                text_return = current_line.body[current_character:] + "\n"
                writing = True
                continue
            elif line == select_end_line:
                text_return =  select_end_line.body[select_end_character:] + "\n"
                writing = True
                normal_order = False
                continue
        else:
            if normal_order:
                if line == select_end_line:
                    text_return += select_end_line.body[:select_end_character]
                    break
                else:
                    text_return += line.body + "\n"
                    continue
            else:
                if line == current_line:
                    text_return += current_line.body[:current_character]
                    break
                else:
                    text_return += line.body + "\n"
                    continue

    return text_return

def locateLibrary(justGet=False):
    #addon = bpy.context.preferences.addons.get('snippetsLibrary')
    # print (addon)
    # prefs = addon.preferences
    prefs = get_addon_prefs()
    cust_path = prefs.snippets_use_custom_path
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

def generate_unique_snippet_name():
    from random import randrange
    import time
    return 'snip_'+ str(randrange(999)) + time.strftime("_%Y-%m-%d_%H-%M-%S") +'.txt'

def selection_to_snippet(self, text):
    """Get selection, dedent it"""
    clip = get_selected_text(self, text)
    if clip:
        clip = textwrap.dedent(clip)
        return clip
    

"""
def clipit(context, name):
    library = locateLibrary()
    bpy.ops.text.copy()
    clip = bpy.context.window_manager.clipboard
    if clip:
        #print (clip)
        ###kill preceding spaces before saving (allow to copy at indentation 0)
        clip = textwrap.dedent(clip)
        # name = context.scene.new_snippets_name.strip()
        name = name.strip()
        if name:
            if not re.search(r'\..{2-4}$', name):#check for an existing extension
                snipname = name + '.txt'
        else:#generate Unique snipName
            print('no name specified, generating a placeholder')
            snipname = generate_unique_snippet_name()

        save_template(library, snipname, clip)
        return (snipname)
    else:
        return (0)
"""
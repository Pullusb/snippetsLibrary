import bpy
import os
import re
import textwrap
import time
import unicodedata
from os.path import dirname, basename, splitext, exists, join, realpath, abspath, isfile, isdir


def get_addon_prefs():
    addon_name = splitext(__name__)[0]
    preferences = bpy.context.preferences
    addon_prefs = preferences.addons[addon_name].preferences
    return (addon_prefs)

def scan_definitions(text):
    '''
    return a list of all def and class
    use capture group (avoid the : of the end)
    '''
    return re.findall(r'^((?:def|class) [-\w]+\([-\w,\. =]*\)):', text, re.MULTILINE)

def containing_folder(fp):
    '''get a filepath, return only parent folder name (or empty string)'''
    return basename(dirname(fp))

def path_to_display_name(fp):
    '''get a path to file, return formatted name for display in list'''
    return splitext(basename(fp))[0].replace('_', ' ')#display name

def insert_template(override, src_text):
    bpy.ops.text.insert(override, text=src_text)

def scan_folder(fp):
    '''take a filepath (location of the files) and return a list of filenames'''
    #recursive in folder
    snippetsList = []
    for root, dirs, files in os.walk(fp, topdown=True):
        for f in files:
            if f.endswith(('.txt', '.py', '.osl')):
                snippetsList.append( join(root, f) )#append full path
    return snippetsList

def scan_multi_folders(fplist):
    all_files = []
    for fp in fplist:
        if exists(fp):
            all_files.extend(scan_folder(fp))
    return all_files

def load_text(fp):
    if fp:
        with open(fp, 'r') as fd:
            text=fd.read()
        return text
    else:
        print('in load_text: no fp to read !')
        return(0)

def save_template(fp, name, text):
    fd = open(join(fp, name),'w')
    fd.write(text)
    fd.close()
    return 0
 
def get_snippet(name):
    '''Take a name
    and return a filepath if found in library
    '''
    library = locateLibrary()
    if library:
        for lib in library:
            for root, dirs, files in os.walk(lib, topdown=True):#"."
                for f in files:
                    if name.lower() == splitext(f)[0].lower():
                        return(join(root, f))
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


def update_func(self, context):
    '''called when a new snippets is selected'''

    """ if bpy.context.scene.sniptool_insert_on_clic:
        bpy.ops.sniptool.template_insert() """

    if bpy.context.scene.sniptool_preview_use:
        # print('update call', time.strftime('%H:%M:%S'))#debug to find when update is called
        prefs = get_addon_prefs()
        preview_linum = prefs.snippets_preview_line_number
        
        # Change preview content
        select_snip = bpy.context.scene.sniptool[bpy.context.scene.sniptool_index]
        
        content = select_snip.content
        if not content:
            print(f'problem while getting content of: {select_snip.name}')
        
        # get rid of tabstops and show only placeholder:
        content = re.sub(r'\${\d{1,2}:?(.*?)}', r'\1', content)
        
        #fix unrecognize tab character in label.
        content = content.replace('\t', '    ')

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


def formatted_name(name):
    '''
    Return passed name as a correct ASCII filename
    add .py extension if not any
    '''
    if name:
        name = name.strip()
        name = name.replace(' ', '_')#clean off whitespace to get clean name
        try:
            #converting to ascii character
            name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
        except:
            #if failing for somme reason just convert non basic chars to underscore
            pass

        # name = bpy.path.clean_name(name)#All characters besides A-Z/a-z, 0-9 are replaced with "_"
        name = re.sub(r'[^A-Za-z0-9\._ -]', '_', name) 

        if not re.search(r'\..{1,4}$', name):#check for an existing extension
            #if no extension provided by the user use default
            name = name.rstrip('.') + '.py'# define format
            # snipname = name + '.py' if self.pref.snippets_save_as_py else name + '.txt'# format choice

        return name

def update_save_func(self, context):
    '''called when typing in field of new snippets creation'''
    self.save_name = formatted_name(self.newsnip)
    # self.display_name = splitext(self.save_name)[0].replace('_', ' ')
    # context.area.tag_redraw()#dont work, draw only when finished typing...


def openFolder(folderpath):
    """
    open the folder at the path given
    with cmd relative to user's OS
    """
    from sys import platform
    import subprocess

    myOS = platform
    if myOS.startswith(('linux','freebsd')):
        cmd = 'xdg-open'
    elif myOS.startswith('win'):
        cmd = 'explorer'
        if not folderpath:
            return('/')
    else:
        cmd = 'open'

    if not folderpath:
        return('//')

    if isfile(folderpath):#case where path point to a file
        if myOS.startswith('win'):
            # keep path the same but add select (/select,) windows option command 
            cmd = 'explorer /select,'
        else:
            # use directory of the file
            folderpath = dirname(folderpath)

    folderpath = os.path.normpath(folderpath)
    fullcmd = cmd.split() + [folderpath]
    print(fullcmd)
    subprocess.Popen(fullcmd)
    return ' '.join(fullcmd)#back to string to print

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

def clean_lib_path(fp):
    '''Check if path exists
    Check if its a folder, return parent folder if not.
    '''

    if exists(fp):
        if os.path.isdir(fp):
            return(fp)
        else:
            return (dirname(fp)[0])
    else:
        print('error with location:', fp)

def get_main_lib_path():
    prefs = get_addon_prefs()
    cust_path = prefs.snippets_use_custom_path
    cust_fp = prefs.snippets_filepath

    if cust_path and cust_fp:#specified user location
        mainDir = bpy.path.abspath(cust_fp)
 
    else:#default location (addon folders "snippets" subdir)
        script_file = os.path.realpath(__file__)
        directory = dirname(script_file)
        mainDir = join(directory, 'snippets/')
        if not exists(mainDir):
            try:
                os.mkdir(mainDir)
                print('snippets directory created at:', mainDir)
            except:
                print('!!! Could not create snippets directory created at:', mainDir)
    return mainDir
 
def locateLibrary(single=False):
    '''return list of lib path'''
    prefs = get_addon_prefs()
    cust_path = prefs.snippets_use_custom_path
    cust_fp = prefs.snippets_filepath

    #handle main Lib file custom user path or addon location
    if cust_path and cust_fp:#specified user location
        mainDir = bpy.path.abspath(cust_fp)
 
    else:#default location (addon folders "snippets" subdir)
        script_file = os.path.realpath(__file__)
        directory = dirname(script_file)
        mainDir = join(directory, 'snippets/')
        if not exists(mainDir):
            try:
                os.mkdir(mainDir)
                print('snippets directory created at:', mainDir)
            except:
                print('!!! Could not create snippets directory created at:', mainDir)

    mainDir = clean_lib_path(mainDir)
    if mainDir:
        maindirlist = [mainDir]

    if single:
        return maindirlist


    all_libs = []
    #here add the list of added secondary dirs in addon prefs (with UIlist or pathstrings)
    altDir = []
    #add path from
    if len(prefs.multipath):
        for loc in prefs.multipath:
            locpath = os.path.normpath(loc.name)
            if exists(locpath):
                altDir.append(locpath)
            else:
                print(f'Path not valid {loc.name} ({locpath})')

    if prefs.snippets_use_standard_template:
        altDir.extend(bpy.utils.script_paths("templates_py"))
        altDir.extend(bpy.utils.script_paths("templates_osl"))
    
    for l in maindirlist + altDir:
        print('checking: ', l)
        clean_path = clean_lib_path(l)
        if clean_path:
            all_libs.append(clean_path)
        else:
            print('invalid library path', l)

    return all_libs

    

### --- temporary store old method for ref
""" 
def reload_folder(fp):
    '''take a filepath (location of the files) and return a list of filenames'''
    #recursive in folder
    snippetsList = []
    for root, dirs, files in os.walk(fp, topdown=True):
        for f in files:
            if f.endswith(('.txt', '.py', '.osl')):
                snippetsList.append(splitext(basename(f))[0])
    return (snippetsList)
"""

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
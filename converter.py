# coding : utf-8
import os,re
from os.path import join, basename, dirname, splitext, exists, split
import time
from .func import *

def get_snippet_infos(fp):
    f = basename(fp)

    with open(fp, 'r') as fd:
        text = fd.read()

    if not text:
        print('no text to read in:', fp)
        return
    
    #name for the file ()
    snipname = f if not '.' in f else splitext(f)[0]
    snipname = snipname.replace('-', ' ').replace('_', ' ').strip()#no need if file is already formated but can't be too carefull

    # description
    #use name without prefix for the description (not meant to be used as filename)
    description = snipname.split('_', 1)[1] if '_' in snipname else snipname
    description = description.replace('-', " ")

    # Use first line of the snippet as description (if not separator/encoding info/licence line)
    header = text.split('\n')[0]
    if header.startswith('#'):
        if not '#####' in header:#consider five hash as separator
            header = header.strip('# ').strip()#slice off useless surrounding '#' and ' ' and '\n'
            if header:#avoid empty string.
                #avoid encoding declaration and need to have some text letters (still avoid separator cases)
                if not re.search(r'coding.*utf-?8', header) and re.search(r'[a-zA-Z]', header):#re.match(r'(?: -*- )?coding\s?:\s?utf'):
                    description = header

    # Trigger
    # Use prefix or containing folder name to use as trigger
    # Alternatively use 'snip' for non categorized snippets.

    if '_' in f:
        #if there is an underscore use prefix
        prefix = f.split('_')[0]
    else:
        #no undescore, use containing folder
        prefix = basename(dirname(fp))
        if prefix.lower() == 'snippets':
            prefix = 'snip'

    if not prefix:
        print('Error,')
        return
    
    trigger = 's'+prefix
    #for exemple  sbpy sregex srig sops spy ssnip etc.
    """ if prefix:
        trigger = 's'+prefix
    else:
        #fallback to containing folder name intead of bsnip
        trigger = 's'+basename(dirname(fp)) """

    return snipname, text, description, trigger

# SUBLIME TEXT ---
def convert_to_sublime_snip(snippet_list, dest):
    """
    Convert a list of filepath (plain text file)
    to sublime text snippets format
    """
    simple_dollar = re.compile(r'\$(?!{\d{1,2}:?.*?})')

    sublimedir = join(dest, 'sublime')
    if not exists(sublimedir): os.mkdir(sublimedir)

    for s in snippet_list:
        snipname, text, description, trigger = get_snippet_infos(s)
        #just for sublime that us one file per snippet with calling name : dash instead of space in filename
        snipname = snipname.replace(' ', '-')
        # escape $ character in text
        sublimetext = text.rstrip('\n')#.replace(r'$', r'\$')
        sublimetext = simple_dollar.sub('\\$', sublimetext)

        sublimefile = f'{snipname}.sublime-snippet'
        sublimesnip = '''<snippet>
    <content><![CDATA[
{0}]]></content>
    <tabTrigger>{1}</tabTrigger>
    <description>{2}</description>
    <scope>source.python</scope>
</snippet>'''.format(sublimetext, trigger, description)

        sublimefile = join(sublimedir, sublimefile)
        with open(sublimefile, 'w') as fd: fd.write(sublimesnip)

### VSCODE ----
def convert_to_vscode_snip(snippet_list, dest):
    """
    Convert a list of filepath (plain text file)
    to vscode snippets format
    """

    simple_dollar = re.compile(r'\$(?!{\d{1,2}:?.*?})')

    vscodefile = 'python.json'#'python.snippets.json'
    vscodedir = join(dest, 'vscode')
    if not exists(vscodedir): os.mkdir(vscodedir)
    vscodefile = join(vscodedir, vscodefile)

    #plug all into one file...

    with open(vscodefile, 'w') as fd:
        fd.write('{\n')

    #start of loop
    for s in snippet_list:
        snipname, text, description, trigger = get_snippet_infos(s)

        fd = open(vscodefile, 'a')
        # # vscode need a lot of formating with escapes for chars and all...(kind of super lame)

        vscodetext = text.replace(r'"', r'\"').replace('\\', r'\\\\')#.replace(r'$', r'\$')
        vscodetext = simple_dollar.sub('\\$', vscodetext)
        vscodetext = '\n'.join(['    "{}",'.format(l) for l in vscodetext.splitlines()]).rstrip('\n,')
        # print(type(vscodetext), 'vscodetext: ', vscodetext)

        vscodesnip = '''
"{3}": {{
"prefix": "{1}",
"body": [
{0}
],
"description": "{2}"
}}
'''.format(vscodetext, trigger, description, snipname)

        fd.write(vscodesnip)

    #end of loop close scope and file
    fd.write('\n}')
    fd.close()


### ATOM ----
def convert_to_atom_snip(snippet_list, dest):
    """
    Convert a list of filepath (plain text file)
    to atom snippets format
    """
    # ! heavy limitation ! cant have multiple snip with same prefix
    # community workaround : add a different amount of space on each one...
    
    simple_dollar = re.compile(r'\$(?!{\d{1,2}:?.*?})')

    atomfile = 'snippets.cson'

    atomdir = join(dest, 'atom')
    if not exists(atomdir): os.mkdir(atomdir)
    atomfile = join(atomdir, atomfile)
    #atom may need tabulation (+ 2 more space for the source type definition above)

    #plug all into one file...

    with open(atomfile, 'w') as fd:
        fd.write("'.source.python':\n")
        # fd.write('{\n')

    #start of loop
    ct_dic = {}
    for s in snippet_list:
        snipname, text, description, trigger = get_snippet_infos(s)
        spacenum = ct_dic.get(trigger, 0)
        ct_dic[trigger] = spacenum + 1

        fd = open(atomfile, 'a')

        #escape dollars and double quote
        atomtext = text.replace('\\', r'\\\\').replace(r'"', r'\"').replace('\n', '\n'+2*' ').rstrip(' ')#.replace(r'$', r'\$')
        atomtext = simple_dollar.sub('\\$', atomtext)

        atomsnip = ''''{2}':
  'prefix': '{1}'
  'body': """
  {0}
  """

'''.format(atomtext, trigger+spacenum*' ', snipname)#use the space hack..., no description

        #get one more indent on the whole snip to be under source.python above. but removing last 
        atomsnip = '  ' +  atomsnip.replace('\n', '\n  ').rstrip(' ') 

        fd.write(atomsnip)

    #end of loop close scope and file
    fd.close()

    print('Conversion Done')


class SNIPPETSLIB_OT_convert(bpy.types.Operator):
    bl_idname = "sniptool.convert"
    bl_label = "Convert snippets library to IDE format"
    bl_description = "Convert all snippets library to chosen external editor snippets format"
    bl_options = {'REGISTER', 'INTERNAL'}#internal means it will be hided from the search.

    convertid : bpy.props.IntProperty(default=0)

    def execute(self, context):
        scn = context.scene
        library = locateLibrary()
        if library:
            start = time.time()
            
            snippet_list = []
            for root, dirs, files in os.walk(library, topdown=True):
                for f in files:
                    if f.endswith('.txt') or f.endswith('.py'):
                        snippet_list.append(join(root, f))
            
            dest = join(dirname(dirname(library)), 'converted_snippets')#up one folder from lib then convert folder...
            if not exists(dest):
                os.mkdir(dest)

            if self.convertid == 0 or self.convertid == 1:
                convert_to_sublime_snip(snippet_list, dest)
            if self.convertid == 0 or self.convertid == 2:
                convert_to_vscode_snip(snippet_list, dest)
            if self.convertid == 0 or self.convertid == 3:
                convert_to_atom_snip(snippet_list, dest)

            openFolder(dest)
            info = f'Finished conversion of {len(snippet_list)} snippets'
            self.report({'INFO'}, info)
        else:
            pathErrorMsg = locateLibrary(True) + ' not found or inaccessible'
            self.report({'ERROR'}, pathErrorMsg)
        return{'FINISHED'}
import os, re
from os.path import join, dirname, basename, splitext, isfile, isdir

### quick explore filesystem, search in a folder for files matching a pattern rename/strip it.

## Where to act
# Use place of the script : dirname(__file__)
# Current working directory : os.getcwd() or '.'
# String path : /path/to/somewhere

loc = dirname(__file__)
print('location: ', loc)

reg = re.compile(r'regex_pattern')# or simple replace()


def scan_rename(loc):
    for f in os.scandir(loc):
        if f.path == __file__: continue#exclude current script

        name, ext = splitext(f.name)

        if f.is_file() and ext.lower() == '.mp3' and reg.search(name):
            new_name = reg.sub('', name)# simple replace : name.replace('stuff', '')
            # new_name = new_name.strip()# Strip heading/trailing whitespace
            new_name = new_name + ext# place extension

            print(f'{f.name} >> {new_name}')
            new_path = join( dirname(f.path), new_name)      

            ## RENAME (comment for test mode)
            os.rename(f.path, new_path)


## single directory
# scan_rename(loc)

## recursive - sending all subdir ! Keep scan_rename(loc) line above to include base dir location !
for root, dirs, files in os.walk(loc):
    for d in dirs:
        scan_rename(join(root, d))


## Recursive old school - without scandir Path Objects
"""
for root, dirs, files in os.walk(loc):
    for f in files:
        fp = join(root, f)
        if fp == __file__: continue#exclude script
        if isfile(fp) and splitext(f)[1].lower() == '.mp3' and reg.search(f):
            new_name = reg.sub('', f)
            print(f'{f} >> {new_name}')
            new_path = join(root, new_name)
            ## RENAME (comment to test mode)
            os.rename(fp, new_path)
"""


## Exemple of regex sub with capture group passed to a function
'''
# replace an element based on a capture group passed to a afunction with re.sub
def increment(match):
    """increment passed match object : numbers(str) return with same padding"""
    return str(int(match.group(1))+1).zfill(len(match.group(1)))

#pass match object to function "increment"
incremented = re.sub(r'(\d+)', increment, 'projet_01')
print(incremented)#>>> projet_02
'''
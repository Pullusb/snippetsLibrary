## ------
#  Script to add/delete prefix on all snippet names in libraty (change the filenames on disk).
#  A filename is considered prefixed if there is an undescore '_' in it.
#  This can be handy if you want to merge all your library in one folder instead of use folder hierarchy.
## ------

import os
from os import listdir
from os.path import join, dirname, basename, exists, isfile, isdir, splitext
import re, fnmatch, glob


### OPTIONS
## ------

## Place this script at the root of your lib folder and uncomment "path_to_your_lib = dirname(__file__)"" below
## or enter the path to your lib here
path_to_your_lib = "" # <--write your filepath to lib folder here
# path_to_your_lib = dirname(__file__)

## test at True  --> will only print in consoledoes not affect the files.
## test at False --> Do the changes
test = True

## delete_prefix at True  -> Delete prefix (snippet parent folder name will be used as a prefix)
## delete_prefix at False -> Create prefix in filename from parent folder name
delete_prefix = True 
## ------

curfile = basename(__file__)
filelist = []
for root, dirs, files in os.walk(path_to_your_lib, topdown=True):
    for f in files:
        if f == curfile:
            print(f'Skip current executed file : {curfile}')
            continue#skip this original file
        if f.endswith('.txt') or f.endswith('.py'):
            fp = join(root, f)
            if delete_prefix:
                #delete_prefix
                if '_' in f:
                    new = f.split('_',1)[1]#extract part after the first '_'
                    new = new.replace('-', ' ').replace('_', ' ')#delete underscore '_' and dash '-'
                    print('rename: {} >> {}'.format(f,new))
                    nfp = join(root, new)
                    # print('nfp: ', nfp)
                    if not test:
                        os.rename(fp, nfp)

                else:
                    print('SKIP:', f)

            else:
                #add prefix
                if not '_' in f:
                    prefix = basename(dirname(fp))
                    if prefix == 'snippets':#root case, general unclassed snippets
                        # make it shorter and more general
                        prefix = 'snip'#or bpy ??

                    print('prefix: ', prefix)
                    ## uncomment line below replace space ' ' by ti'-'
                    # prefix.replace(' ', '-')
                    new = prefix + '_' + f
                    print('rename: {} >> {}'.format(f,new))
                    nfp = join(root, new)
                    # print('nfp: ', nfp)
                    if not test:
                        os.rename(fp, nfp)

                else:
                    print('SKIP:', f)
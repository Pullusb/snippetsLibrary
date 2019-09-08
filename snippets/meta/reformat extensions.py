## ------
#  Script to batch change extension on all files
#  A filename is considered prefixed if there is an undescore '_' in it.
#  This can be handy if you want to merge all your library in one folder instead of use folder hierarchy.
## ------

import os
from os import listdir
from os.path import join, dirname, basename, exists, isfile, isdir, splitext
import re, fnmatch, glob


### OPTIONS
## ------

## Place this script at the root of your lib folder and uncomment "dirname(__file__)"" below
## or enter the path to your lib here
# path_to_lib = "" # <--write your filepath to lib folder here
path_to_lib = dirname(dirname(__file__))

## test at True  --> will only print in console without changing anything.
## test at False --> Do the changes
test = False

extension = 'py'# txt
## ------

if not extension.startswith('.'):
    #ensure extension dot
    extension = '.'+extension

curfile = basename(__file__)
filelist = []
for root, dirs, files in os.walk(path_to_lib, topdown=True):
    for f in files:
        if f == curfile:
            print(f'Skip current executed file : {curfile}')
            continue#skip this original file
        if not f.endswith(extension):
            fp = join(root, f)
            new = splitext(f)[0] + extension
            print('rename: {} >> {}'.format(f,new))
            nfp = join(root, new)
            # print('nfp: ', nfp)
            if not test:
                os.rename(fp, nfp)

        else:
            print('SKIP:', f)
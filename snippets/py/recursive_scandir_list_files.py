## get file recursively
import os
from pathlib import Path

def recursive_scandir(fp, depth=-1, files=None):
    '''depth: 0=no recusion, 1=one sublevel, -1=unlimited
    retrun file list as path objects
    '''
    files = [] if files is None else files

    for f in os.scandir(fp):
        if f.is_dir():
            if depth != 0:
                recursive_scandir(f.path, depth=depth-1, files=files)
        elif f.is_file():
            files.append(Path(f)) # add as Path object

    return files

''' # without depth control
def recursive_scandir(fp, files=None):
    files = [] if files is None else files

    for f in os.scandir(fp):
        if f.is_dir():
            recursive_scandir(f.path, files=files)
        elif f.is_file():
            files.append(Path(f)) # add as Path object

    return files
'''

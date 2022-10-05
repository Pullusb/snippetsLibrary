## Get human readable size of file or folder

import os
from pathlib import Path

def sizeof_fmt(num, suffix='B'):
    '''
    return human readable size from bytes amount
    ex: sizeof_fmt(os.stat(filename).st_size)
    '''
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def get_size(fp):
    fp = Path(fp)
    if fp.is_file():
        return fp.stat().st_size
    size = 0
    for subfp in os.scandir(fp):
        size += get_size(subfp.path)
    return size

def get_human_readable_size(fp):
    return sizeof_fmt(get_size(fp))

filepath = 'path/to/file/or/folder'
size_str = get_human_readable_size(filepath)
print(f'{size_str} : {filepath})

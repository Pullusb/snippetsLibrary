## Explore with filtered os.walk with include/exclude patterns

import os
from pathlib import Path
import re, fnmatch

def filtered_walk(fp, excludes=[], includes=[], exclude_git_files=True):
    '''explore given filepath
    exclude (file and folder) and/or include (file only). # ex: ['*.txt',]
    return file_list matching exclusion and inclusion lists
    '''

    file_list = []

    fp = Path(fp)

    excludes += ['__pycache__'] # always exclude cache files
    if exclude_git_files:
        excludes += ['.git', '*.pyc', '.gitignore']

    # replace names by regex translation
    if includes:
        includes = r'|'.join([fnmatch.translate(x) for x in includes])
    if excludes:
        excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

    for root, dirs, files in os.walk(str(fp)):
        ## exclude dirs
        if excludes:
            # dirs[:] = [os.path.join(root, d) for d in dirs] # as full path
            dirs[:] = [d for d in dirs if not re.match(excludes, d)]

        ## exclude/include files
        # files = [os.path.join(root, f) for f in files]
        if excludes:
            files = [f for f in files if not re.match(excludes, f)]

        if includes:
            files = [f for f in files if re.match(includes, f)]

        for fname in files:
            full_path = Path(root) / fname
            #print(full_path)
            file_list.append(str(full_path))

    return file_list


fp = r'path/to/some/folder'
files = filtered_walk(fp, excludes=[], includes=[], exclude_git_files = True)

for f in files:
    print(f)
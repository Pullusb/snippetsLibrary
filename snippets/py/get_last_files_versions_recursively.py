## Get all last files with filters
import os, re
import itertools

def is_exclude(name, patterns) :
    from fnmatch import fnmatch

    if not isinstance(patterns, (list,tuple)) :
        patterns = [patterns]

    return any([fnmatch(name, p) for p in patterns])

def get_last_files(root, pattern=r'_v\d{3}\.\w+', only_matching=False, ex_file=None, ex_dir=None, keep=1, verbose=False) -> list:
    '''Recursively get last(s) file(s) (when there is multiple versions) in passed directory

    root -> str: Filepath of the folder to scan.
    pattern -> str: Regex pattern to group files.
    only_matching -> bool: Discard files that aren't matched by regex pattern.
    ex_file -> list : List of fn_match pattern to exclude files.
    ex_dir -> list : List of fn_match pattern of directory name to skip.
    keep -> int: Number of lasts versions to keep when there are mutliple versionned files (e.g: 1 keep only last).
    verbose -> bool: Print infos in console.
    '''

    files = []
    if ex_file is None:
        all_items = [f for f in os.scandir(root)]
    else:
        all_items = [f for f in os.scandir(root) if not is_exclude(f.name, ex_file)]

    allfiles = [f for f in all_items if f.is_file()]
    # groupby can fail to group if list is not sorted
    allfiles.sort(key=lambda x: x.name)

    dirs = [f for f in all_items if f.is_dir()]

    for i in range(len(allfiles)-1,-1,-1):# fastest way to iterate on index in reverse
        if not re.search(pattern, allfiles[i].name):
            if only_matching:
                allfiles.pop(i)
            else:
                files.append(allfiles.pop(i).path)

    # separate remaining files in prefix grouped lists
    lilist = [list(v) for k, v in itertools.groupby(allfiles, key=lambda x: re.split(pattern, x.name)[0])]

    # get only item last of each sorted grouplist
    for l in lilist:
        versions = sorted(l, key=lambda x: x.name)[-keep:]  # exclude older
        for f in versions:
            files.append(f.path)

        if verbose and len(l) > 1:
            print(f'{root}: keep {str([x.name for x in versions])} out of {len(l)} elements')

    for d in dirs: # recursively treat all detected directory
        if ex_dir and is_exclude(d.name, ex_dir):
            # skip folder with excluded name 
            continue
        files += get_last_files(
            d.path, pattern=pattern, only_matching=only_matching, ex_file=ex_file, ex_dir=ex_dir, keep=keep)

    return sorted(files)

## Exemple of fnmatch patterns for exclusions (note: '.' dot is literral)

## Everything that: start with a '.', ends with a ~, all 'blend[1@]', that have 'sync-conflict' in name
EXCLUDE_FILE = ['.*', '*.db', '*.blend?', '*~', '*sync-conflict*', '*.DS_Store']
## Prevent entering subfolder that: start with a '.' or named '_old' (literral).
EXCLUDE_DIR = ['.*', '_old']


## --- Set path to directory
fp = r''
files = get_last_files(fp, only_matching=True, keep=1, verbose=True) # ex_file=EXCLUSIONS, ex_dir=EXCLUDE_DIR
for f in files:
    print(f)
print('\n', len(files))
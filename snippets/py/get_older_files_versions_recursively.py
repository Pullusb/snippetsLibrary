## Get all older versions (usefull for cleaning)
import os, re
import itertools

def is_exclude(name, patterns) :
    from fnmatch import fnmatch
    if not isinstance(patterns, (list,tuple)) :
        patterns = [patterns]
    return any([fnmatch(name, p) for p in patterns])

def get_old_version(root, pattern=r'_v\d{3}\.\w+', exclude=None, keep=1, verbose=False):
    '''Recursively get only old version (when a files are versionned) in passed directory

    root -> str: Filepath of the folder to scan.
    pattern -> str: Regex pattern to group files.
    exclude -> list : List of fn_match pattern to exclude files.
    only_matching -> bool: Discard files that aren't matched by regex pattern.
    keep -> int: Number of lasts versions to keep out of list mutliple versionned files.
    verbose -> bool: Print infos in console.
    '''

    files = []
    if exclude is None:
        all_items = [f for f in os.scandir(root)]
    else:
        all_items = [f for f in os.scandir(root) if not is_exclude(f.path, exclude)]

    allfiles = [f for f in all_items if f.is_file()]
    dirs = [f for f in all_items if f.is_dir()]

    for i in range(len(allfiles)-1,-1,-1):# fastest way to iterate on index in reverse
        if not re.search(pattern, allfiles[i].name):
            continue

    # separate remaining files in prefix grouped lists
    lilist = [list(v) for k, v in itertools.groupby(allfiles, key=lambda x: re.split(pattern, x.name)[0])]

    # get only item last of each sorted grouplist
    for l in lilist:
        if len(l) == 1:
            # if verbose:
            #     print('Skip Single version :', l[0].path)
            continue

        versions = sorted(l, key=lambda x: x.name)[:-keep] # exclude most recent
        for f in versions:
            files.append(f.path)

        if verbose:
            print(f'{root}: {len(versions)} old -> {str([x.name for x in versions])}')

    for d in dirs:#recursively treat all detected directory
        files += get_old_version(d.path, pattern=pattern, exclude=exclude, keep=keep, verbose=verbose)

    return sorted(files)

## exemple of exclusion fnmatch pattern
#EXCLUSIONS = ['.*', '*.pdf', '*.blend?'] # exclude what start by a point or is a pdf or is a .blend[1@]

fp = r''
files = get_old_version(fp, verbose=True) # exclude=EXCLUSIONS

# for f in files:
#     print(f)
print('\n', len(files))
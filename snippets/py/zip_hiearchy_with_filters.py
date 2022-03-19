## zip files and directories with filters while keeping structure

def expand_list(entry_list, recursive=True):
    '''Get a list of Path objects, mixed files and dirs
    return a list with directory expanded as files
    '''

    pattern = '**/*' if recursive else '*'
    only_files = []
    for fp in entry_list:
        if fp.is_file():
            only_files.append(fp)
        else:
            only_files += [f for f in fp.glob(pattern) if f.is_file()]
            ## note: glob is the slowest to explore (os.scandir the fastest)

    return list(set(only_files))

def zip_with_structure(filelist, zip, root=None, compressed=True, recursive=True, include_filter=None, exclude_filter=None, no_git=False, no_caches=True, verbose=1):
    '''
    Zip passed filelist into a zip with root path as toplevel tree
    If root is not passed, the shortest path in filelist becomes the root

    :filelist: list list of filepaht as string or Path object (converted anyway)
    :zip: string output fullpath of the created zip
    :root: string top level of the created hierarchy, file that are not inside root are discarded
    :compressed: bool Decide if zip is compressed or not
    :recursive: bool When a directory is contained in filelist, recursive mode take all sub-directorys files as well
    :include_filter: string (coma separated values) Get only files that match this list filter ex: '*.py, *.png'
    :exclude_filter: string (coma separated values) Get only files that match this list filter ex: '*.pdf, _old'
    :no_git: bool add git files exclusions to exclude_filter ['.git', '.gitignore']
    :no_caches:  bool add python caches exclusions to exclude_filter ['*.pyc', '__pycache__']
    :verbose: int  prints additions in console (faster without verbose at 0)

    '''

    import zipfile as zp
    import fnmatch
    import re
    import time

    if not zip:
        print('Need zip destination')
        return
    if not Path(zip).parent.exists():
        print('Zip destination parent folder must exists')
        return

    filelist = [Path(f) for f in filelist] # ensure pathlib
    if not filelist:
        print('No file in list')
        return

    if not root:
        # autodetect the path thats is closest to root
        root = sorted(filelist, key=lambda f: f.as_posix().count('/'))[0].parent
        print('Auto determined root:', root)
    else:
        root = Path(root)

    # Expand encountered folders in list to individual file path (recursively or not)
    # create a list oof files instead of files and folders (allow to do a set to remove double)

    filelist = expand_list(filelist, recursive=recursive)       

    includes = []
    excludes = []
    if include_filter:
        includes = [i.strip() for i in include_filter.split(',')] # ['*.doc', '*.odt'] # for files only
    if exclude_filter:
        excludes = [i.strip() for i in exclude_filter.split(',')] # for dirs and files

    # Add presets
    if no_git:
        excludes += ['.git', '.gitignore']
    if no_caches:
        excludes += ['*.pyc', '__pycache__']
    excludes = set(excludes)

    # replace by regex translation
    if includes:
        includes = r'|'.join([fnmatch.translate(x) for x in includes])
    if excludes:
        excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

    print(f'Zipping to: {zip}\nWith root {root}')

    t0 = time.time()
    compress_type = zp.ZIP_DEFLATED if compressed else zp.ZIP_STORED
    with zp.ZipFile(zip, 'w',compress_type) as zipObj:        
        for fp in filelist:
            if not fp.exists():
                print(f'Not exists: {fp.name}')
                continue

            if str(root) not in str(fp):
                print(f'{fp} is out of root {root}')
                continue

            ## Case of file
            if fp.is_file():
                if excludes and re.match(excludes, fp.name):
                    if verbose > 1:
                        print(f'is excluded: {fp}')
                    continue
                if includes and not re.match(includes, fp.name):
                    if verbose > 1:
                        print(f'not included: {fp}')
                    continue

                arcname = fp.as_posix().replace(root.parent.as_posix(), '').lstrip('/')
                if verbose:
                    print(f'adding: {arcname}')
                zipObj.write(str(fp), arcname)
                continue

    print(f'zipped {len(filelist)} files in {time.time() - t0:.2f}s')
    return zip


#zip_with_structure(
#    filelist, # list of filepaths and folderpaths
#    zip, # zip path destination
#    root=None, 
#    compressed=True, 
#    recursive=True, 
#    include_filter=None,
#    exclude_filter=None, 
#    no_git=False, 
#    no_caches=True, 
#    verbose=1)

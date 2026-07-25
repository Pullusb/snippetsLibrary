## Get file recursively, additional function to filter by extension.
import os
from pathlib import Path

def recursive_scandir(fp, depth=-1, files=None) -> list:
    """Recursive scandir with error handling and explicit handle release.

    Does not follow directory symlinks, survives unreadable directories,
    closes each scandir iterator before descending.
    Note: scandir is faster than `os.walk(fp)` and way faster than `Path(fp).rglob('*')`

    Args:
        fp (str | Path): Directory to scan.
        depth (int): 0=no recursion, 1=one sublevel, -1=unlimited.
        files (list | None): Accumulator, created if None.

    Returns:
        list[Path]: Files found as Path objects.
    """
    files = [] if files is None else files
    subdirs = []

    try:
        with os.scandir(fp) as it:
            for f in it:
                try:
                    if f.is_dir(follow_symlinks=False):
                        subdirs.append(f.path)
                    elif f.is_file():
                        files.append(Path(f)) # Conversion to Path object cost ~11% scan speed
                except OSError:
                    continue  # entry vanished or stat failed
    except OSError:
        return files  # unreadable dir, keep what we have

    if depth != 0:
        for d in subdirs:
            recursive_scandir(d, depth=depth - 1, files=files)

    return files

# Scan with extension filter (In this case, using str based version barely gain ~2,5% speed, not worth ergonomic cost)
def recursive_scan_ext(fp, ext=('.blend',), depth=-1, files=None) -> list:
    """Recursively collect files matching an extension.

    Args:
        fp (str | Path): Directory to scan.
        ext (str | tuple[str]): Lowercase extension(s), dot included.
        depth (int): 0=no recursion, 1=one sublevel, -1=unlimited.
        files (list | None): Accumulator, created if None.

    Returns:
        list[Path]: Matching files.
    """
    files = [] if files is None else files
    append = files.append
    subdirs = []

    try:
        with os.scandir(fp) as it:
            for f in it:
                try:
                    if f.is_dir(follow_symlinks=False):
                        subdirs.append(f.path)
                    elif f.name.lower().endswith(ext):
                        append(Path(f))
                except OSError:
                    continue
    except OSError:
        return files

    if depth != 0:
        for d in subdirs:
            recursive_scan_ext(d, ext=ext, depth=depth - 1, files=files)

    return files

# string version, Same as recursive_scandir but accumulates strings instead of Path objects.
# Isolates the cost of Path instantiation from the cost of the traversal, gain ~11% speed
def recursive_scandir_str(fp, depth=-1, files=None):
    """Recursive scandir return list of strings with error handling and explicit handle release.
    
    Does not follow directory symlinks, survives unreadable directories,
    closes each scandir iterator before descending.
    Note: scandir is faster than `os.walk(fp)` and way faster than `Path(fp).rglob('*')`

    Args:
        fp (str | Path): Directory to scan.
        depth (int): 0=no recursion, 1=one sublevel, -1=unlimited.
        files (list | None): Accumulator, created if None.

    Returns:
        list[str]: File paths found.
    """
    files = [] if files is None else files
    append = files.append
    subdirs = []

    try:
        with os.scandir(fp) as it:
            for f in it:
                try:
                    if f.is_dir(follow_symlinks=False):
                        subdirs.append(f.path)
                    elif f.is_file():
                        append(f.path) # keeping stre instead or Path gain ~11% scan speed
                except OSError:
                    continue
    except OSError:
        return files

    if depth != 0:
        for d in subdirs:
            recursive_scandir_str(d, depth=depth - 1, files=files)

    return files


'''
# Simple version with depth control (same speed, no error handling)
def recursive_scandir(fp, depth=-1, files=None) -> list:
    """depth: 0=no recusion, 1=one sublevel, -1=unlimited
    return file list as path objects
    """
    files = [] if files is None else files

    for f in os.scandir(fp):
        if f.is_dir():
            if depth != 0:
                recursive_scandir(f.path, depth=depth-1, files=files)
        elif f.is_file():
            files.append(Path(f)) # add as Path object

    return files

# Simplest (same speed, no error handling)
def recursive_scandir(fp, files=None) -> list:
    """return recursive file list as path objects"""
    files = [] if files is None else files

    for f in os.scandir(fp):
        if f.is_dir():
            recursive_scandir(f.path, files=files)
        elif f.is_file():
            files.append(Path(f)) # add as Path object

    return files
'''

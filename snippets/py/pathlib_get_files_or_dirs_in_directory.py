## get files or dirs in directory recursively or not

from pathlib import Path

fp = 'path/to/dir'
fp = Path(fp)

## one level
# all files directly in directory
all_files = [f for f in fp.iterdir() if f.is_file()]

# all dirs directly in directory
all_files = [f for f in fp.iterdir() if f.is_dir()]

## recursive
# all files in directory and subdirectories recursively
all_files = [f for f in fp.glob('**/*') if f.is_file()]

# directory recursively
all_files = [f for f in fp.glob('**/*') if f.is_dir()]

# old recursive method using os.walk
import os
all_files = []
for R, _D, F in os.walk(fp):
    for f in F:
        sub.append(Path(R) / f)
    all_files += sub

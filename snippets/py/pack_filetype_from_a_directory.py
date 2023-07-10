## Pack (Copy or move) all filetype contained in subdirectory

from pathlib import Path
import time

source_path = Path('/folder/containing/videos')
assert source_path.exists(), f'Not found: {source_path}'

print(f'-- Copy Prores from: {source_path}')
date = time.strftime('%Y_%m_%d')

print('Using date: ', date)


file_list = source_path.rglob('*.mov')

dest_folder = Path(f'/path/to/exports/{date}_video_pack/')
dest_folder.parent.mkdir(exist_ok=True, parents=True)

# Root to create subpath by curring root from
root = source_path 

for f in file_list: 
    ## subpath
    subpath = f.as_posix().replace(root.as_posix(), '').lstrip('/')
    # print('subpath: ', subpath)
    dest_file = dest_folder / str(subpath)
    print('\nsrc:', f)
    print('dst:', dest_file)
    dest_file.parent.mkdir(exist_ok=True, parents=True)

    ## Move file to destination
    f.rename(dest_file)

    ## Copy to destination
    # import shutil
    # shutil.copy(f, dest_file) # need str for python <= 3.7

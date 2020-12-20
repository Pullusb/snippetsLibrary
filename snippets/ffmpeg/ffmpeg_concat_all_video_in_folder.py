## Concat/join all videos in given folder in a new video using ffmpeg
import os
from os.path import join, dirname, basename
from pathlib import Path
import subprocess

pack = Path(__file__).parent #'path/to/folder/containing/all/videos'

## create a list of path object to video files and sort by name
file_list = sorted([Path(f) for f in os.scandir(pack) if f.name.endswith('.mp4')], key=lambda x : x.name)

## Sort by modification 'st_mtime' time (or creation time 'st_ctime')
file_list.sort(key=lambda x : x.stat().st_mtime)

assert file_list

listfile = pack / 'list.txt'

with open(listfile, 'w') as fd:
    for f in file_list:
        fd.write(f"file 'file:{f.as_posix()}'\n")


# -- absolute (weirly enough, give an errolast tested on windows...)
# output = pack / 'concat.mp4'
# cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', f'"{listfile.as_posix()}"', '-c', 'copy',  f'"{output.as_posix()}"' ]

# -- relative
# - direct concat (no re-encode) - not always reliable but instant
# cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy',  'concat.mp4' ]

#-  reencode
cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-crf', '20', '-pix_fmt', 'yuv420p', 'PACK.mp4' ]

print('cmd: ', ' '.join(cmd))
subprocess.call(cmd)

print('Done')

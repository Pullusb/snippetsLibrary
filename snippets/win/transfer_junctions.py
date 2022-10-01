## List every junction in a folder and recreate in another
## ugly method, will probably fail on path with special character (accentuated and such)

import os
import re
import subprocess
from pathlib import Path


loc = ''
dest_folder = r'%APPDATA%\Blender Foundation\Blender\3.4\scripts\addons'

loc = Path(loc) if loc else Path(__file__).parent

print('loc: ', loc)

res = subprocess.check_output(['dir'], cwd=loc, shell=True)

res = res.decode("utf-8", errors='ignore')
# print(res)
for l in res.split('\n'):

    if not '<JUNCTION>' in l:
        # print(f'not a junction {l}')
        continue

    parse = re.search('<JUNCTION>\s+(.*?) \[(.*)\]', l)
    if not parse:
        print(f'error parsing : {l}')
        continue
    name = parse.group(1)
    folder_path = Path(parse.group(2))

    if not folder_path.exists():
        print(f'{name} path not found: {folder_path}')
        continue


    dest = Path(dest_folder, name)
    if dest.exists():
        print(f'SKIP: "{name}" already exists in destination')
        continue
    print(f'Creating: {name} --> {folder_path}')
    cmd = ['MKLINK', '/J', str(dest), str(folder_path)]
    subprocess.call(cmd, shell=True)

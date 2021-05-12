## list dependancies with BAT
import bpy
from blender_asset_tracer.trace import deps
from pathlib import Path
from time import time

print('-'*10, '\n'*3)

# Set filepath here
fp = bpy.data.filepath

fp = Path(fp)

assert fp.exists

start = time()

absol = []
not_exists = []
errors = []

for lib in deps(fp):
    try:
        if not lib.abspath.exists():
            print('!! not found:', lib)
            not_exists.append(lib)
            continue

        if lib.asset_path.is_absolute():
            ## print abs lib only
            absol.append(lib)
            print('absolute', lib)

    except error as e:
        print('Error accessing:', lib)
        print(e)
        errors.append(lib)


print(f'''
===
Lib Scan Results for {fp}:
===''')

if absol:
    print('All absolute libs:')
    for l in absol:
        print('-', l)

if not_exists:
    print('All non existing libs:')
    for l in not_exists:
        print('-', l)

if errors:
    print('Errors when checking libs:')
    for l in errors:
        print('-', l)

print('\nDone', f'({time() - start:.2f}s)')
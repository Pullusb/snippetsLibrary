## scan repositories in a directory recursively, printing git directory and the remote adress

import os
from pathlib import Path
import subprocess


### --- arguments (could be converted to argparse):

target_dir = 'Directory to scan'
cmd = 'git remote --v'

## --- /

target_dir = Path(target_dir)
cmd = cmd.strip().split(' ')
print('splitted command: ', cmd)
print(f'--- Scanning repos in: {target_dir}:\n')

for R,D,F in os.walk(target_dir):
    for dir_name in D:
        folder = Path(R, dir_name)

        ## Skip folder inside of .git and cache
        if any(x in str(folder) for x in ('.git', '__pycache__')):
            continue

        if (folder / '.git').exists():
            output = subprocess.check_output(cmd, cwd=str(folder))
            output = output.decode()

            ## Possible Skip condition
            # if not 'gitlab' in output:
            #     continue

            print(f'Git: {folder}\n')
            print('output: ', output)

print('Scan Done.')

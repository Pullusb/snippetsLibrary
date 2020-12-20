## Check git status of git folder recursively
import os
import subprocess
from os.path import basename, join

## enter the path where to check (recursively)
root_scan = r''

# - scanning for git folders
gits = []
for R, D, F in os.walk(root_scan):
    for d in D:
        fp = join(R, d)
        if [i for i in os.scandir(fp) if i.is_dir() and i.name == '.git']:
            print('>>>', d)
            gits.append(fp)

# - check 
print('=---=')
print(f'{len(gits)} gits found' )
print('------')

ct_ok = 0
ct_ko = 0

for folder in gits:
    # print(folder)
    os.chdir(folder)
    cmd = ['git', 'status']

    ret = subprocess.check_output(cmd)

    if 'Your branch is up to date' in ret.decode():
        # pass
        print(f'{basename(folder)} OK')
        ct_ok += 1
    else:
        print(f'{basename(folder)} is not up to date')
        print(ret.decode())
        ct_ko += 1

    print('--')


print('gits up to date : ', ct_ok)
print('gits to check   : ', ct_ko)
print('---')
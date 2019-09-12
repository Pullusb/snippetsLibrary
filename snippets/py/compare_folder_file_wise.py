# Compare files in two folder that are supposed to have similar files (but not same folder hierarchy).
# Print if some file are missing or if some files are different while having the same name.
# Carefull, double file in src/dest are not handled and get false results.
# Note : Can use the two path as argument 1 and 2 if running from terminal
import os, sys
from os.path import dirname, basename, join, exists, splitext
from filecmp import cmp

cli = True

src =  r''# enter source folder path
dest = r''# enter dest folder path

if cli:
    #CLI handle
    if len(sys.argv) < 3:
        print('not enough argument')

    else:
        file_paths = sys.argv[1:]
        src = file_paths[0]
        dest = file_paths[1]

srcf = []
srcfp = []
destf = []
destfp = []

for root, dirs, files in os.walk(src):
    for f in files:
        srcf.append(f)
        srcfp.append(join(root,f))

for root, dirs, files in os.walk(dest):
    for f in files:
        destf.append(f)
        destfp.append(join(root,f))


#missing in dest

for s, sp in zip(srcf, srcfp):
    if s not in destf:
        print('not in dest', sp)
        continue

    # print(s)
    # print('destf.index(s): ', destf.index(s))
    path_in_dest = destfp[destf.index(s)]
    if not cmp(sp, path_in_dest):
        #compare with stat() (swallow=True)
        print('!! diff:\n\t', sp, '\n\t', path_in_dest, '\n')



print(' - missing in src - ')
for f, fp in zip(destf, destfp):
    if f not in srcf:
        print('not in src', fp)


# Automatic ffmpeg img sequence to video (just give folder path) V1
# If multiple things in folder, point path of any image in sequence
# Will bypass if there is gap in seq (use check=False)

import os, sys
from os import listdir, scandir
from os.path import join, dirname, basename, exists, isfile, isdir, splitext
import re
import subprocess

def check_frame_gap(l):
    '''check if there is a gap in number of given list'''
    miss = 0
    gap = 0
    gap_list = []
    renum = re.compile(r'^(.*?)(\d+)(\D*)$')
    for i, f in enumerate(l):
        num = renum.search(l[i])
        num = int(num.group(2))
        ## rightmost
        ##num = re.search(r'\d+(?!.*\d)', l[i])
        ##num = int(num.group(0))

        if i:
            prev = re.search('^(.*?)(\d+)(\D*)$', l[i-1])
            prev = int(prev.group(2))
            res = num - prev
            if res > 1:
                gaplength = res - 1
                miss += gaplength
                gap += 1
                if res == 2:
                    mess = f"{folder}: gap {num - 1}"#simple gap -> just point missing
                else:
                    mess = f"{folder}: gap {prev+1} - {num-1} : {gaplength} files"#more then one, show range
                print(mess)
                gap_list.append(mess)

    if gap:
        resume = f'{gap} gaps found\n{miss} total missing'
        gap_list = [resume] + gap_list

    return gap_list

def to_video(fp, fps=25, check=True):
    if not exists(fp):
        print(f'not exists {fp}')
        return

    prefix = None
    init = None
    renum = re.compile(r'\d{2,}')
    regrp = re.compile(r'(.*?)(\d+)(?!.*\d)(.*)')
        ##                 1before  2num   3after 
        # renum = re.compile('\d{2-8}\.')#strict (must be near extension's dot)

    if not isdir(fp):
        # use pointed file as model for left-side of number padding
        init = regrp.search(basename(fp))
        if init:
            strlen = len(init.group(0))
            prefix = init.group(1)
            number = init.group(2)
            suffix = init.group(3)
        fp = dirname(fp)

    if init:        
        seq = sorted([f for f in scandir(fp) if prefix == regrp.search(f.name).group(1) and len(f.name) == strlen], key = lambda x: x.name)

    else:
        seqfiles = sorted([f for f in scandir(fp) if renum.search(f.name)], key = lambda x: x.name)

        # check if file of same sequence
        seqreg = regrp.search(seqfiles[0].name)
        strlen = len(seqreg.group(0))
        prefix = seqreg.group(1)
        number = seqreg.group(2)
        suffix = seqreg.group(3)
        seq = [f for f in seqfiles if prefix == regrp.search(f.name).group(1) and len(f.name) == strlen]#only if left part of the number is the same as first element


    start = int(regrp.search(seq[0].name).group(2))
    end = int(regrp.search(seq[-1].name).group(2))

    print(f'{len(seq)} imgs in {fp}')
    if check:
        gaps = check_frame_gap([i.name for i in seq])
        if gaps:
            print('/!\ gaps found in frames !!')
            for g in gaps:
                print(g)        
            # input('Press any key...')#lock if batch...
            return 
        print(f'sequence range OK : {start} - {end}')


    video = prefix.rstrip('_-.')+'.mp4'
    # video = f"{prefix}{str(start).zfill(4)}-{str(end).zfill(4)}.mp4"#include range in name
    out = join(dirname(fp), video)

    ## TODO handle case where same name already exists (overwrite for now)

    settings = ['-crf', '20', '-preset', 'slower', '-pix_fmt', 'yuv420p', '-y']
    cmd = ['ffmpeg', '-f', 'image2', '-start_number', str(start), '-i', f'{fp}/{prefix}%{str(len(number)).zfill(2)}d{suffix}', '-r', str(fps)] + settings + [out]
    print('cmd:', ' '.join(cmd))

    #launching cmd
    subprocess.call(cmd)#wait for cmd to finish before proceeding
    #subprocess.Popen(cmd)#launch all at once !
    print(f'{video} done.')
    return

# default is 25 fps

# use this for use in command line (use arguments) or with drag&drop on script file
""" if len(sys.argv) > 1:
    for path in sys.argv[:1]:
        to_video(path, fps=25, check=True) """


to_video('path/to/folder/ot/one/file/of/the/sequence')
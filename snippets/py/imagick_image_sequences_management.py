## Check, compress or fill gaps in sequences : V3 (2020-05-28)
## Use image magick for image diff (need to be in the path)
## Use PIL in some functgion but can be replaced by image magick
import os, re, shutil
from os.path import splitext, join, abspath, exists, isdir, isfile, dirname, basename
from PIL import Image
from PIL import ImageChops
from time import time

### ---------
##  images comparison utilities
### ---------

image_exts = ('.png', '.jpg', '.tiff', '.tga', '.jpeg',)
exception_list = ('thumbs.db',)

def fuzzy_match(s1, s2, similitude):
    '''Tell if two strings are similar using a similarity ratio (0 to 1) value passed as third arg'''
    from difflib import SequenceMatcher
    similarity = SequenceMatcher(None, s1, s2)
    return similarity.quick_ratio() > similitude

def imagick_comp_RSME(fp1, fp2, out = ''):
    ''' Metric Root Mean Square Error (RMSE)
    Use image magick to get a difference percentage between two image using metric
    doc : https://imagemagick.org/script/command-line-options.php#metric
    application : https://stackoverflow.com/questions/7940935/equality-test-of-images-using-imagemagick
    '''
    import subprocess
    out = out if out else 'NULL:'#redirect to null
    
    ## Calculate Root Mean Square Error (RMSE) to see how much pixels tend to differ
    result = subprocess.getoutput(['compare', '-metric', 'RMSE', fp1, fp2, out])
    result = result.split()[-1].strip(' ()')
    result = float(result)*100# convert to percentage of diff (result is 0 to 1)
    # print('result: ', result)
    if result < 0.001: # less than this percentage of global diff is considered similar.# maybe add it as a tolerance variable
        if result > 0:print(f'Difference (under tolerance percentage) : {result}% : {basename(fp1)} <-> {basename(fp2)}')
        return 0
    return result

def imagick_comp_AE(fp1, fp2, out = ''):
    ''' Metric absolute pixel count
    Use image magick to get a difference percentage between two image using metric
    doc : https://imagemagick.org/script/command-line-options.php#metric
    application : https://stackoverflow.com/questions/7940935/equality-test-of-images-using-imagemagick
    '''
    import subprocess
    out = out if out else 'NULL:'#redirect to null

    ## Pixels may only differ by 0.5% before being considered different (can be used as tolerance)
    result = subprocess.getoutput(['compare', '-metric', 'AE', '-fuzz', '0.5%', fp1, fp2, out])
    # print(f'diff {basename(fp1)}-> {basename(fp2)}: {result}')
    return int(result)


###--- compressor

def compress_sequence(fp, rename=True, dryrun=False):
    '''
    Delete redundant images
    if rename is True: write the range in name of the first img of each series
    else name stay as is and last frame is never deleted (redundant or not) to know where sequence stop.
    ex: Keep only frame 4 on identical sequence 4,5,6,7,8 and rename img_0004-0008 (fix from image 4 to 8)
    '''
    imglist = [f for f in os.listdir(fp) if splitext(f)[1].lower() in image_exts and not f in exception_list]
    imglist.sort()
    
    if not imglist or len(imglist) <= 1:
        report = f'No image sequence to scan : {fp}'
        print(report)
        return report

    start = time()
    # check if not an alredy compressed sequence (check for \d{2,5}-\d{2,5}\.?)
    for i in imglist:
        if re.search(r'\d{2,5}-\d{2,5}\.?', i):
            report = f'Image {i} is already on compressed format (range numerotation) : {fp}'
            print(report)
            return report
            
    # Check if sequence is valid
    base = re.split(r'\d+(?!.*\d)', imglist[0])[0] #split on last number and get first part
    if not base:
        report = f'Could not found number in image name: {imglist[0]} : {fp}'
        print(report)
        return report

    unmatched = [i for i in imglist if not i.startswith(base)]
    if unmatched:
        report = f'{len(unmatched)} images not starting by "{base}" : {unmatched[:3]} : {fp}'
        print(report)
        return report

    todel = []
    frame_list = [join(fp, imglist[0])]#need the first image
    stop_nums = []
    viewed = 0

    print(f' +    {splitext(imglist[0])[0]}')
    for i, f in enumerate(imglist):
        pic = join(fp,f)
        if viewed:
            if imagick_comp_AE(prev_pic, pic):# diff (> 0)
                print(f' +    {splitext(basename(pic))[0]}')
                frame_list.append(pic)
                stop_nums.append(re.search(r'\d+(?!.*\d)', basename(prev_pic)).group(0))
            else:# same (= 0)
                print(f'- {splitext(basename(pic))[0]}')
                todel.append(pic)

        prev_pic = pic
        viewed = 1

    # Without renaming must keep last frame if it was redundant one to delete
    if not rename and basename(todel[-1]) == imglist[-1]:
        frame_list.append(todel.pop())

    #add last number
    stop_nums.append(re.search(r'\d+(?!.*\d)', imglist[-1]).group(0))

    # print(f'frame keep list ({len(frame_list)}) frame stops list ({len(stop_nums)})')
    if len(frame_list) != len(stop_nums):
        report = f'Error: frame to keep ({len(frame_list)}) has no equal frame stops ({len(stop_nums)}) : {fp}'
        print(report)
        return report 

    print('Deleting duplicate...', end=' ')#, flush=True
    for im in todel:
        # print(f'remove {im}')
        if not dryrun: os.remove(im)
    print('Done')

    ## add range if renaming is on
    if rename:
        print('Renaming...', end=' ')#, flush=True
        for im, stopnum in zip(frame_list, stop_nums):
            root, ext = splitext(im)
            new = f'{root}-{stopnum}{ext}'
            print('new: ', new)
            if not dryrun: os.rename(im, new)
        print('Done')

    result = f'Compress: {len(todel)}/{len(imglist)} imgs deleted (kept: {len(frame_list)}) in {time()-start:.2f}s at : {fp}'
    print(result)
    return result


### ---------
##  Checker
### ---------

def sequence_gap_check(fp) -> int:
    '''
    Check if there is gap in sequence numerotation in folder passed.
    Make comprehensive prints
    return number of gaps
    '''

    l = [f for f in os.listdir(fp) if splitext(f)[1].lower() in image_exts and not f in exception_list]
    l.sort()
    miss = 0
    gap = 0
    i = 0
    #to update : compile regex and search for the rightmost number (might work as is)
    for f in l:
        num = re.search(r'^(.*?)(\d+)(\D*)$', l[i])
        num = int(num.group(2))
        if i:
            prev = re.search(r'^(.*?)(\d+)(\D*)$', l[i-1])
            prev = int(prev.group(2))
            res = num - prev
            if res > 1:
                gaplength = res - 1
                miss += gaplength
                gap += 1
                if res == 2:
                    print (f"gap {num - 1}")#gaplength
                else:
                    print (f"gap {prev + 1} - {num - 1} : {gaplength} files")
        i += 1

    if gap:
        print (gap, 'gap found')
        print (miss, "total missing")
    print("finished :", i, "scanned")
    return gap

### ---------
##  Filler
### ---------

def expand_sequence(fp):
    '''
    Fill gaps from compressed sequences with range in file names
    Duplicate images according to range and rename to reconstruct sequence with all images
    ex: img_0004-0008 is duplicated and renamed to recreate the sequence img_0004, img_0005...
    '''
    import shutil
    no_num = [f for f in os.listdir(fp) if splitext(f)[1].lower() in image_exts and not f in exception_list and not re.search(r'(\d{2,5})-(\d{2,5})', f)]
    imglist = [f for f in os.listdir(fp) if splitext(f)[1].lower() in image_exts and not f in exception_list and f and re.search(r'(\d{2,5})-(\d{2,5})', f)]
    ## get only range numerals
    if not imglist:
        print(f'no image with range numerotations detected in folder, abort expand : {fp}')
        return 1

    imglist.sort()

    ## check if its a compressed sequence (not needed if already filterd or mixed numerotation)
    # for i in imglist:
    #     if not re.search(r'\d{2,5}-\d{2,5}\.?', i):
    #         print(f'image {i} has no compressed format name (range numerotation), skip {fp}')
    #         return 1
    
    padding = len(re.search(r'(\d{2,5})-(\d{2,5})\.?', imglist[0]).group(1))
    ct = 0
    for img in imglist:
        # if not re.search(r'(\d{2,5})-(\d{2,5})\.?', img):
        #     print(f'No range numerotation : {img}')
        #     continue
        base, ext = re.split(r'\d{2,5}-\d{2,5}', img)
        if not base:
            print('Base name of the sequence not found')
            return 1

        pic = join(fp, img)
        re_range = re.search(r'(\d{2,5})-(\d{2,5})\.?', img)
        start = int(re_range.group(1))
        end = int(re_range.group(2))
        if start > end:
            print(f'huge problem: end smaller than start -> {img}')
            return 1
        
        # newpath = join(fp, f'{base}{str(start).zfill(padding)}{ext}')
        newpath = join(fp, img.split('-')[0] + splitext(img)[-1])#get rid of end num (or use start)
        if start == end:
            print(f'{img} is a fix')
            os.rename(pic, newpath)
            continue
        
        # clone frame
        for i in range(start+1, end+1):
            copypath = join(fp, f'{base}{str(i).zfill(padding)}{ext}')
            if not exists(copypath):
                shutil.copy2(pic, copypath)
                ct+=1
            else:
                print(f'skip (already exists): {basename(copypath)}')
        
        os.rename(pic, newpath)
    
    if no_num:
        print(f'sequence has {len(no_num)} image with single numerotations')
    print(f'Sequence expanded : {ct} images created ({len(imglist) + len(no_num)} -> {len(imglist) + len(no_num) + ct} imgs)')
    

def sequence_from_img(src, limit, overwrite=False) -> int:
    '''take a src filepath and duplicate until limit number is reached'''
    if not exists(src):
        print('file not exists:', src)
        return

    loc = dirname(src)
    fname = basename(src)
    number = re.search(r'\d{4}', fname)
    if not number:
        print('no #### number found in file')
        return

    fill = len(number.group())
    num = int(number.group())

    ct = 0
    skipped = 0
    for i in range(num+1, limit+1):#depuis le suivant, jusqu'au dernier
        new = re.sub(r'\d{4}', str(i).zfill(fill), fname)
        dst = join(loc, new)
        if not overwrite and exists(dst):
            print('skipping existing', new)
            skipped += 1
            continue
        shutil.copyfile(src, dst)#accept only full fp and replace dest
        print('copy:', dst)
        ct += 1
    print('---')
    if ct:
        print(ct, 'generated')
    if skipped:
        print(skipped, 'skipped')
    return ct

def sequence_filler(src, limit=0, extend_last=0, logit=False):
    '''
    Fill gap in sequence with duplicated frames (in classic number style sequences)
    Can specify a limit and if last frame must be extended to a certain number
    (extend_last override limit parameter)
    '''
    if not exists(src):
        print('file not exists:', src)
        return

    renum = re.compile(r'\d{4}')
    fill = 4
    if isfile(src):
        loc = dirname(src)
    else:
        loc = src

    new_files = []
    gct = 0
    filelist = sorted([i for i in os.listdir(loc) if isfile(join(loc,i))])
    #TODO, valid list with number check, (maybe reject if there renum not passing on all)

    fcount = len(filelist)-1
    for i, f in enumerate(filelist):

        add=0
        # print(f)#print file name
        sf = join(loc, f)
        #get current elem num
        num = renum.search(f)
        if not num:
            print('skipped')
            continue
        num = int(num.group())
        if i == fcount:
            # print('End file')
            break

        #get next number
        next = filelist[i+1]
        nextnum = renum.search(next)
        if not nextnum:
            print(next, 'has no number')
            continue
        nextnum = int(nextnum.group())

        #error checks
        if nextnum < num:
            print('problem: current', num, '> next', nextnum)
            continue

        diff = nextnum - num
        if diff <= 0:
            print('problem, next has same number (or negative)!')

        #gap listing
        gap = [j for j in range(num, nextnum)]
        if len(gap) <= 1:
            continue#nogap
        else:
            gct +=1
            #slice first element of list (num)
            # print('gap:', gap[1:])
            for n in gap[1:]:
                nf = renum.sub(str(n).zfill(fill), f)
                df = join(loc, nf)
                if not exists(df):
                    new_files.append(df)
                    shutil.copyfile(sf, df)#copy2 ?
                    # print('copy to:', df)
                else:
                    print('Problem, detected has gap but already existed:', df)

    #treat last image if needed:
    #TODO:standalone this
    if extend_last and num:
        sequence_from_img(sf, num+extend_last)
    if limit and num:
        sequence_from_img(sf, limit)

    if not gct:
        print('No gap detected')
    else:
        print (gct, 'gap(s) filled')
    if new_files and logit:
        log = join(dirname(loc), basename(loc) + r'_log.txt')
        print('writing log:',log)
        with open(log, 'w') as fd:
            fd.write('\n'.join(new_files))

    print('Done')
    return

### ---------
##  Exposition exporter
### ---------

def get_prefix(string, delimiter = '_', delimiter_pos = 1):
    return delimiter.join(string.split(delimiter,delimiter_pos)[:delimiter_pos])

def divide_list_by_prefix(li, delimiter = '_', delimiter_pos = 1):
    '''
    get a list of strings, 
    return a list of lists with
    '''
    # print('debug, prefix  of first entry', delimiter.join(li[0].split(delimiter,delimiter_pos)[:delimiter_pos]) )
    from itertools import groupby
    return [list(g) for k, g in groupby(li, lambda s: get_prefix(s, delimiter, delimiter_pos))]

def get_sequence_expo(fp):
    '''get a folder filepath, return a list of the expo'''

    imglist = [f for f in os.listdir(fp) if splitext(f)[1].lower() in image_exts and not f in exception_list]
    imglist.sort()

    frame_list = []
    viewed = 0
    # print(fp)
    for i, f in enumerate(imglist):
        ifp = join(fp,f)
        pic = Image.open(ifp)
        if viewed:
            diff = ImageChops.difference(pic, prev_pic)
            if diff.getbbox():
                #for knowledge : to save difference : diff.save(diff_save_location)
                print(f' {i}', end=' ', flush=True)# +1   # flush : print on same line progressively
                frame_list.append(i)# +1 
            else:# print point for same image
                print('.', end='', flush=True)
        prev_pic = pic
        viewed = 1
    print('|')
    #print(frame_list)
    return(frame_list)

def export_expo(src, export_solo=True, overwrite=True):
    '''
    Detect image change and write Export
    Export "exposition" of subfolders in txt files as index
    '''
    # ## list of file path and names with same index (could have been a dic)
    # fplist = get_all_asset_filepath()
    # print(fplist)
    outpath = src# maybe one folder up ?

    fplist = [d.path for d in os.scandir(src) if d.is_dir()]
    names = [basename(d) for d in fplist]

    t_start = time()
    # multilist = divide_list_by_similarity(names, tolerance = 0.7)#0.65
    multilist = divide_list_by_prefix(names, delimiter_pos = 2)# second optional arg delimiter to change
    
    ## print lists and quit
    # for l in multilist:
    #     print(l)
    # return
    full = []
    for l in multilist:
        multiframelist = []
        for n in l:# n is a name like 'naoufel'
            out = join(outpath, f'{n}.txt')
            if not overwrite and exists(out):#if overwrite is false
                print('SKIP (already exists):', out)
                continue

            fp = fplist[names.index(n)]#chars/naoufel folder
            """ fp = join(fp,'line')#chars/naoufel/line
            if not exists(fp):
                print('no line folder for "'+n+'" in', fp)
                continue
            """


            framelist = get_sequence_expo( fp )#get list of changing frames
            if export_solo:
                solo_out = join(outpath, f'{n}.txt')
                if not overwrite and exists(out):
                    pass
                with open(solo_out,'w') as fd:
                    fd.write(str(framelist))

            print(n, '>', len(framelist) ,'>', framelist)

            multiframelist.extend([f for f in framelist if f not in multiframelist])#merge with list of same "group"

        multiframelist.sort()#sort in place

        print('multi', len(multiframelist), multiframelist)
        
        # Save one multi file associated with prefix
        with open(join(outpath, f'{get_prefix(n, delimiter_pos = 2)}.txt'), 'w') as fd:#by prefix
            fd.write(str(multiframelist))

        # # --- #second iteration to save complete (multi) list associated with folder name
        # for n in l:
        #     with open(join(outpath, f'{n}.txt'), 'w') as fd:
        #         fd.write(str(multiframelist))

        full.extend(multiframelist)# add to full

    # Save file with all expositions (folder root name.txt, or "full.txt" ?)
    full = list(set(full))
    full.sort()
    print(f'full {len(full)} {full}')
    with open(join(outpath, f'{basename(src)}_full.txt'), 'w') as fd:#by prefix
        fd.write(str(multiframelist))

    print(f'Export expo images - Done ({time() - t_start:.1f}s)')


'''
fp = r'a/path'
frame_list = get_sequence_expo(fp)# get full expo (considering all folder)
with open(join(r'an/out/path', 'expo_out.txt'),'w') as fd:
    fd.write(str(frame_list))
'''

### ---------
##  Launch area
### ---------
print('--===--')


seqs_parent_folder = r''
# seq_filepath = r''

### -- direct function --

# export_expo(seqs_parent_folder)# Export exposition of subfolders in txt files as index (easy tweak in function)

# compress_sequence(seq_filepath)# Remove redundant images and rename *key*frame with corresponding range

# compress_sequence(seq_filepath, rename=False)# Remove redundant images, Don't touch name and keep last image even if redundant

# sequence_gap_check(seq_filepath)# Check if there is gap in sequence with comprehensive prints

# expand_sequence(seq_filepath)# Fill gaps from compressed sequences with range in file names

# sequence_filler(seq_filepath)# Fill gaps in classic numbered sequences


### -- Batch launcher --

def compress_folders(folder_path, recursive=True):
    '''compress folder (default recursive) using compress_sequence func'''
    reports = []
    if recursive:
        for root, dirs, files in os.walk(folder_path):
            for d in dirs:
                fp = join(root,d)
                if [f for f in os.listdir(fp) if splitext(f)[1].lower() in image_exts and not f in exception_list]:
                    reports.append(compress_sequence(fp))
    else:
        for d in os.scandir(folder_path):
            if d.is_dir():
                reports.append(compress_sequence(d.path))

    print('\n--Compression reports--')
    print('\n'.join(reports))


compress_folders(seqs_parent_folder)
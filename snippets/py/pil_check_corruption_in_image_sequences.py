## Check image sequences for corrupted images (V2 2020-05-28)
# import bpy
from time import time
from PIL.Image import *
import os
from os.path import join, dirname, abspath, basename, splitext

# allowed extension to be considered as images
image_exts = ('.png', '.jpg', '.tiff', '.tga', '.jpeg',)

def is_img_folder(d):
    ct = 0
    for f in os.listdir(d):
        ct += 1
        #if os.path.isfile(d)
        if splitext(f)[1].lower() not in image_exts:
            #print("not an image:", f)#Dbg
            return 0

    if not ct:#return false if nothing found
        #print('nothing in folder')
        return -1

    ###all files has been evaluated as images
    return 1

def is_full_alpha(im):
    if im.mode == 'RGBA':
        alphaData = im.tobytes("raw", "A")
        if set(alphaData) == {0}:
            #print('fully transparent !')
            return True

    return False

def check_passes_in_folder(folder, full_report=False, root=None, limit=80):
    '''
    Check passed directory for problem with images
    root:: if passed, strip this filepath from message
    fullreport::verbose mode, details per images
    limit:: allowed percentage of image full black/white/transparent, report if more than this percentage
    return a tuple (error code -> int, details -> str)
    '''

    print("check dir :", basename(folder), '->' , folder)
    path_str = folder
    if root:
        path_str = folder[len(root):].lstrip(r'\/')  #'//' + 
    #variables

    imglist = [i for i in os.listdir(folder)]
    imglist.sort()
    total = len(imglist)
    # print (imglist)
    black_ct = 0
    white_ct = 0
    alpha_ct = 0
    black_imgs = []
    white_imgs = []
    alpha_imgs = []
    
    for i, f in enumerate(imglist):
        imgfp = os.path.join(folder,f)
        img=open(imgfp)
        extrema = img.convert("L").getextrema()
        #print("extrema", extrema)#Dbg

        if extrema == (0, 0):
            black_ct+=1
            #print(f, 'black')
            if full_report:
                black_imgs.append(f)
            #is_full_alpha(img)#can be black and alpha (alpha channel for ex)

        elif extrema == (255, 255):
            white_ct+=1
            #print(f, 'white')     
            if full_report:
                white_imgs.append(f)       

        else:#check full transparency 
            if is_full_alpha(img):
                alpha_ct+=1
                #print(f, 'transparent')

                if full_report:
                    alpha_imgs.append(f)

            else:
                #print(f, 'OK')
                pass

    if full_report:
        full_list = [['black', black_imgs], ['white', white_imgs], ['transparent', alpha_imgs]]
        for sub in full_list:
            if sub[1]:
                print('   ', sub[0], 'images found:')
                for f in sub[1]:
                    print ('       ', f)

    #returning error message
    blatlist = [['black', black_ct], ['white', white_ct],['transparent', alpha_ct]]
    for blat in blatlist:
        if blat[1] == total:
            return 1, '    Only {1} images: {0}'.format(path_str, blat[0])

    #returning warning message if x% of images are black or white or transp
    for blat in blatlist:
        if (blat[1] * 100)/total >= limit:
            return 2, '    More than {1}% of the images are {2}: {0}'.format(path_str, str(limit), blat[0])

    return 0, path_str


def check_imgs_seqs(src, print_relative=True):
    '''Perform multiple imgs sequence check recursively in passed filepath'''
    t0 = time()
    empty_folders = []
    errors=[]
    warnings=[]
    for root, dirs, files in os.walk(src):
        for d in dirs:
            #path to folder
            dfp = join(root,d)
            #check folder if it contains only images (with one only ?)
            d_status = is_img_folder(dfp)
            if d_status == 1:
                #check seq of this folder:
                if print_relative:
                    code, mess = check_passes_in_folder(dfp, root=dirname(src))
                else:
                    code, mess = check_passes_in_folder(dfp)

                if code:
                    if code == 1:
                        errors.append(mess)
                    elif code == 2:
                        warnings.append(mess)

            elif d_status == -1:
                empty_folders.append(dfp)
            else:
                print("ignored:", d)
                pass


    print('-- SEQUENCE CHECK REPORT --')
    if empty_folders:
        print('\n', len(empty_folders), 'EMPTY FOLDERS:')
        for fold in empty_folders:
            print('   ', fold)
            print()

    if errors:
        print('\n', len(errors), 'ERRORS :')
        for error in errors:
            print(error)
            print()

    if warnings:
        print('\n', len(warnings), 'WARNINGS :')
        for warn in warnings:
            print(warn)
            print()


    print('time', time() - t0)
    print('-- --')
    


### LAUNCH CHECK
print ('\n---')

## starts check in render folder aside blend file
#fp = join(dirname(abspath(bpy.path.abspath(bpy.data.filepath))), 'render')

## starts check in folder containing the blend
#fp = dirname(abspath(bpy.path.abspath(bpy.data.filepath)))

fp = r''
check_imgs_seqs(fp)

# tips: print filepaths relative to loacal folder  : fp[len(dirname(bpy.data.filepath)):] #slice path until local folder
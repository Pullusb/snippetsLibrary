## functions to check for full black/white/alpha images with PIL v1
# import bpy
import os
from os.path import *
from PIL.Image import *
# from PIL import Image
# from PIL import ImageChops


def is_full_alpha(im):
    if im.mode == 'RGBA':
        alphaData = im.tobytes("raw", "A")
        if set(alphaData) == {0}:
            #print('fully transparent !')
            return True

    return False

def img_is_empty_fast(imgfp):
    '''Tell if the image is full balck, full white, full alpha or normal
    Some image can be seen has full colored even with full transparency (faster)'''
    img=open(imgfp)
    
    extrema = img.convert("L").getextrema()
    if extrema == (0, 0):
        return "Full black"

    elif extrema == (255, 255):
        return "Full white"      

    else:#check full transparency 
        if is_full_alpha(img):
            return "Full alpha"

    return "Normal"

def img_is_empty(imgfp):
    # imgfp = os.path.join(folder,f)
    img=open(imgfp)
    extrema = img.convert("L").getextrema()
    # print("extrema", extrema)#Dbg

    if is_full_alpha(img):
        return "Full alpha"

    if extrema == (0, 0):
        return "Full black"

    elif extrema == (255, 255):
        return "Full white"      

    return "Normal"

fp = r'path to imgs'

# ret = img_is_empty_fast(fp)
# ret = is_full_alpha(fp)
ret = img_is_empty(fp)


print(f'{ret} : {fp}')
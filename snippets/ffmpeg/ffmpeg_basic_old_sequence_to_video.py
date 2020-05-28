## super basic image seq to video with ffmpeg (old)
import os
import re

###SETUP
#locations (final '/' is important)
#point a folder
fold = '/disk/stuff/folder/'

# output location, Leave empty to output it on parent directory
outloc = '/Users/Desktop/'

#ffmpeg binary path, Leave empty if it's in system path
bin = '"/path/to/ffmpeg/binary"'

framerate = 25

parent = fold.rstrip('/').rsplit(r'/',1)[0]+'/'#get parent dir (not affected by trailing '/'')
outloc = parent if not outloc else outloc

bin = 'ffmpeg' if not bin else bin

##srart stuff ---
files = [i for i in os.listdir(fold)]
print(len(files), 'files detected')

reg = re.search(r'^(.*?)(\d+)(\D*)$',files[0])

if reg:
    imgnames = reg.group(1)
    startnum = reg.group(2)
    ext = reg.group(3)
    pad = str(len(startnum))
    startnum = str(int(startnum))
    outname = imgnames.rstrip('._-')
    settings = '-r ' + str(framerate) + ' -crf 20 -preset slower -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -pix_fmt yuv420p -y'

    cmd = bin + ' -f image2 -start_number ' + startnum + ' -i "' + fold + imgnames + '%0' + pad + 'd' + str(ext) + '" ' + settings + ' "' + outloc + outname + '.mp4"'
    print(cmd)
    #launch
    os.system(cmd)

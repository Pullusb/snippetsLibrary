## Change frame rate of a gif file with image magick
#cmd : 'convert -delay {delay} src.gif new.gif'

import subprocess

fps = 10
# fps = int(input('fps ? '))# standalone

delay = str(int(100 // fps))#take delay in miliseconds (int)
print(f'frame delay: {delay}ms')

src_gif = r'E:\photo\2018\Preonic\soldering_short.gif'
new_gif = src_gif.replace('.gif', f'-{fps}fps.gif')

convert_bin = 'convert'
## Need fullpath to convert on windows (convert is already a system command)
convert_bin = r'C:\Program Files\ImageMagick-6.9.3-Q16\convert.exe'

cmd = [convert_bin, '-delay', delay, src_gif, new_gif]
print('cmd: ', ' '.join(cmd))

## Popen for new process
subprocess.call(cmd)


## -- Bat drop script windows version (asking for delay) : 
#set /p delayvalue=delay (4 is 25ips, more is slower):
#convert -delay %delayvalue% "%1" "%~n1_delay-%delayvalue%.gif"
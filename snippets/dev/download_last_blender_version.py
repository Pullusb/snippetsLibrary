## download last blender experimental version (in temp dir if paht not specified or not existing)

from os.path import join, basename, exists, dirname
import re
import urllib.request
import ssl
import shutil
import tempfile
import time

def sizeof_fmt(num, suffix='B'):
    '''
    return human readable size from bytes amount
    ex: sizeof_fmt(os.stat(filename).st_size)
    '''
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def copyfileobjverbose(fsrc, fdst, size=None, length=16*1024):
    '''
    exactly like shutil.copyfileobj with a callback
    copy data from file-like object fsrc to file-like object fdst
    '''
    copied = 0
    while True:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)
        copied += len(buf)
        if size:
            print(f'downloaded: {sizeof_fmt(copied)} ({int((copied/size)*100)}%)    ', end='\r')
        else:
            print(f'downloaded: {sizeof_fmt(copied)}    ', end='\r')
    print()#print last carriage return


def dl_url(url, dest):
    '''download passed url as dest file (include,filename)'''
    import urllib.request
    import time
    start_time = time.time()
    ## simple download
    # with urllib.request.urlopen(url) as response, open(dest, 'wb') as out_file:
    #     shutil.copyfileobj(response, out_file)

    ## with displayed progression (need sizeof_fmt and copyfileobjverbose func)
    with urllib.request.urlopen(url) as response, open(dest, 'wb') as out_file:
        clength = response.getheader('content-length')#check if size available in header
        if clength: clength = int(clength)
        copyfileobjverbose(response, out_file, size=clength)

    print(f"elapsed time {time.time() - start_time:.2f}s",)


def DL_blender_experimental(destination_folder):
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

    burl = "https://builder.blender.org"
    response = urllib.request.urlopen(burl, context= ssl_context)
    data = response.read()
    body = data.decode("utf-8")
    match = re.search(r'/download/blender-\d\.\d{2}-(\w{4,20})-linux(?:-\w{2,20}-x86_)?64\.tar\.\w+',body)
    if not match:
        print(10*'=', '\nRegex failed to match download blender line on https://builder.blender.org/\n', 10*'=', '\npage code :\n', body, 10*'=')
        return 1

    hash = match.group(1)
    download_url = burl + match.group(0)
    print('hash',hash)

    real_version = re.findall(r'\d\.\d{2}[a-z]?', match.group(0))[0]
    if real_version: print('version: ', real_version)

    download_path = join(destination_folder, basename(download_url) )

    '''### super simple way
    with urllib.request.urlopen(download_url) as response, open(download_path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    '''

    ### with progress display, src https://stackoverflow.com/questions/41106599/python-3-5-urllib-request-urlopen-progress-bar-available
    dl_url(download_url, download_path)


dl_path = 'your/path/of/DL'

if not dl_path or not exists(dl_path):
    dl_path = tempfile.gettempdir()
    print('using temp dir:', dl_path)

DL_blender_experimental(dl_path)
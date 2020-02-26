### /DL utils

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
    copy data from file-like object fsrc to file-like object fdst
    Exactly like shutil.copyfileobj with added display part
    '''
    copied = 0
    while True:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)
        # Display
        copied += len(buf)
        if size:
            print(f'\rDownloaded: {sizeof_fmt(copied)} ({int((copied/size)*100)}%)', end='')
        else:
            print(f'\rDownloaded: {sizeof_fmt(copied)}', end='')
    print()# last carriage return


def dl_url(url, dest):
    '''download passed url to dest file (include filename)'''
    import urllib.request
    import time
    start_time = time.time()
    ## Simple download
    # with urllib.request.urlopen(url) as response, open(dest, 'wb') as out_file:
    #     shutil.copyfileobj(response, out_file)

    ## With displayed progression (need sizeof_fmt and copyfileobjverbose func)
    with urllib.request.urlopen(url) as response, open(dest, 'wb') as out_file:
        clength = response.getheader('content-length')#check if size available in header
        if clength: clength = int(clength)
        copyfileobjverbose(response, out_file, size=clength)

    print(f"elapsed time {time.time() - start_time:.2f}s",)

### DL utils/
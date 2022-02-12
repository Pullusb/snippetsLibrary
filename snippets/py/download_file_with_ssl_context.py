## download file with ssl context (needed on linux)

def download_url(url, dest):
    '''download passed url to dest file (include filename)'''
    import shutil
    import time
    import ssl
    import urllib.request

    ssl._create_default_https_context = ssl._create_unverified_context

    ## to specify context instead
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    # urllib.request.urlopen(burl, context= ssl_context)

    start_time = time.time()

    try:
        with urllib.request.urlopen(url) as response, open(dest, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    except Exception as e:
        print('Error trying to download\n', e)
        return e

    print(f"Download time {time.time() - start_time:.2f}s",)

url = 'http://'
dest = 'path/on/disk'
download_url(url, dest)

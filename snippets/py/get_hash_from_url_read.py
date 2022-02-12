## get file hash from web url (read data, so this method probably as long as downloading the file itself)
import os, hashlib, urllib
from time import time

def hash(remote, algorithm = "md5"):
    max_file_size = 100*1024*1024
    if algorithm == "md5":
        hash = hashlib.md5()
    elif algorithm == "sha1":
        hash = hashlib.sha1()
    elif algorithm == "sha256":
        hash = hashlib.sha256()
    elif algorithm == "sha384":
        hash = hashlib.sha384()
    elif algorithm == "sha512":
        hash = hashlib.sha512()
    else:
        print(f'Algorithm "{algorithm}" is not available')
        return -1

    total_read = 0
    while True:
        data = remote.read(4096)
        total_read += 4096

        if not data or total_read > max_file_size:
            break

        hash.update(data)

    return hash.hexdigest()

def get_remote_sum(url, algorithm = 'md5'):
    remote = urllib.request.urlopen(url)
    return hash(remote, algorithm)

start = time()

url = 'url/to/a/file'
hash_string = get_remote_sum(url, algorithm = 'md5')

print("\nhash string:", hash_string)
print("\nhash check time:", f'{time() - start:.2f}s')

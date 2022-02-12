## get file size from url if server provide file header

url = 'http://httpbin.org/html'

## method 1
from urllib.request import Request, urlopen
resp = urlopen(Request(url, method='HEAD'))
headers = resp.info()
file_size = headers['Content-Length']

## method 2
import urllib.request
d = urllib.request.urlopen(url)
file_size = int(d.getheader('Content-Length'))


print("file size:", file_size)

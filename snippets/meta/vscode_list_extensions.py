## list VScode extension (webscrap based)
import subprocess
import urllib.request
import re

exts = subprocess.check_output(['code', '--list-extensions'], shell=True) 
ext_l = exts.decode().split()

base_url = 'https://marketplace.visualstudio.com/items?itemName='

for eid in ext_l:
    url = base_url + eid
    with urllib.request.urlopen(url) as response:
        html = response.read().decode()
        res = re.search(r'<meta property="og:title" content="(.*?)&#32;-&#32;Visual&#32;Studio&#32', html)
        if res:
            title = res.group(1)
            title = title.replace('&#32;', ' ')
            ## choose what to print
            # print(title)
            # print(f'{title} --- {eid} -- {url}')
            print(f'{title} -> {url}')
        else:
            print(f'Not found for {eid}')
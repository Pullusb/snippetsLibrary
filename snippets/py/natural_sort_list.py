## Natural sort list of strings

import re

def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in _nsre.split(s)]

# Oneliner lambda
natural_sort_key = lambda x: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', x)]

mylist = ['name_12', 'name_2', 'name']
mylist.sort(key=natural_sort_key)
print(f'{mylist=}')

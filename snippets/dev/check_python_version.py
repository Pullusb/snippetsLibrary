## check python version

import sys

print('Python Version')
print('Is 3.x:', sys.version_info[0] == 3) # is python 3
print(sys.version_info[:3]) # 3 digit tupple
print(sys.version_info) # full details
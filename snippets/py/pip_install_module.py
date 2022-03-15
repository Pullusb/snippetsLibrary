import sys
import subprocess

# get path to blender python
pybin = sys.executable

# ensure pip is installed
cmd = [pybin, '-m', 'ensurepip']
subprocess.call(cmd)

# install a specific module (linux cmd)
cmd = [pybin, '-m', 'pip', 'install', 'the_module_name']
subprocess.call(cmd)

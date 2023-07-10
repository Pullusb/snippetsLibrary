## Run Blender and execute a script, with passed arguments

import subprocess

## Argument
# -d (--destination) Destination folder for the blend

bin = '/opt/blender-3.6.0/blender'
blend = '/my_file.blend'
script = '/my_script.py'
script_option = 'my_script_option'

cmd = [
bin,
'--factory-startup', # '--enable-autoexec',
'-b', blend,
'-P', script,
'--',
'-d', script_option,
]

# source_folder = ''

## add options 
# opt = ['-s', source_folder] if source_folder else []
# cmd += opt


print(' '.join(cmd))
subprocess.call(cmd)

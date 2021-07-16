import bpy
import re
from pathlib import Path

def set_outputs_version(version_pattern):
    '''Get a regex pattern to find/replace in pathes
    Set version in outputs path according to version in filename
    if no version parttern , use a default that match "_v001"
    '''
    if not bpy.data.is_saved:
        return

    # take a default pattern '_001'
    if not version_pattern:
        version_pattern = r'_v\d{3}'

    reversion = re.compile(version_pattern)

    filename = Path(bpy.data.filepath).stem
    vres = reversion.search(filename) # vres = re.search(version_pattern, filename)
    if not vres:
        print(f'Version not found in file name with regex pattern: {version_pattern}')
        return
    version = vres.group(0)

    scn = bpy.context.scene
    outs = [n for n in scn.node_tree.nodes if n.type == 'OUTPUT_FILE']

    old = scn.render.filepath
    new = reversion.sub(version, old) # new = re.sub(version_pattern, version, old)
    if old != new:
        print(f'output: {old} >> {new}')
        scn.render.filepath = new
    for fo in outs:
        for sl in fo.file_slots:
            old = sl.path

            new = reversion.sub(version, sl.path) # new = re.sub(version_pattern, version, sl.path)
            if old != new:
                print(f'slot: {old} >> {new}')
                sl.path = new

set_outputs_version(r'_v\d{3}')

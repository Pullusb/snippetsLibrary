import bpy
import re
from pathlib import Path

def set_outputs_version(version_pattern=None):
    '''Get a regex pattern to find/replace in pathes
    Set version in outputs path according to version in filename
    if no version parttern , use a default that match "_v001"
    '''
    scn = bpy.context.scene
    fp = bpy.data.filepath

    if not fp:
        return

    version_pattern = version_pattern or r'_v\d{3}'
    reversion = re.compile(version_pattern)
    
    filename = Path(bpy.data.filepath).stem
    vres = reversion.search(filename)
    if not vres:
        print('Set output warning : version "_v???" not found in file name')
        return
    version = vres.group(0)

    # scn.render.filepath = reversion.sub(scn.render.filepath) # direct
    old = scn.render.filepath
    new = reversion.sub(version, old)
    if old != new:
        print(f'output: {old} >> {new}')
        scn.render.filepath = new

    if not scn.node_tree or not scn.use_nodes:
        return

    for n in scn.node_tree.nodes:
        if n.type != 'OUTPUT_FILE':
            continue
        # n.base_path = reversion.sub(version, n.base_path) # direct
        old = n.base_path
        new = reversion.sub(version, n.base_path)
        if old != new:
            print(f'node_path: {old} >> {new}')
            n.base_path = new
        
        for sl in n.file_slots:
            # sl.path = reversion.sub(version, sl.path) # direct
            old = sl.path
            new = reversion.sub(version, sl.path)
            if old != new:
                sl.path = new


set_outputs_version(r'_v\d{3}')

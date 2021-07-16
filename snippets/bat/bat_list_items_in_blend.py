## list items in blend using blender asset tracer
from pathlib import Path
from blender_asset_tracer import blendfile

'''
Brush = BR
Object = OB
WindowManager = WM
WindowSpace = WS
Screen = SR
Collection = GR
NodeTree = NT
Palette = PL
Image = IM
Action = AC
Library = LI
Material = MA
Text = TX
Mesh = ME
'''

fp = Path('path/to/file')
print(f'Items in {str(fp)}:\n')
with blendfile.open_cached(fp) as bf:
    for item in bf.find_blocks_from_code(b'OB'):
        print(item.id_name.decode()[2:])

print('\nDone')
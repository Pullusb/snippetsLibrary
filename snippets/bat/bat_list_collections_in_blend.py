from pathlib import Path
from blender_asset_tracer import blendfile

fp = Path('path/to/file')
print(f'Collections in {str(fp)}:\n')
with blendfile.open_cached(fp) as bf:
    for col in bf.find_blocks_from_code(b'GR'):
        print(col.id_name.decode()[2:])

print('\nDone')
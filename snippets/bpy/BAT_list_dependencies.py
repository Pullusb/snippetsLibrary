## list dependancies with BAT
import bpy
from blender_asset_tracer.trace import deps
from pathlib import Path

for lib in deps(Path(bpy.data.filepath)):
    # print(lib)
    if lib.asset_path.is_absolute():
        ## print abs lib only
        print(lib)
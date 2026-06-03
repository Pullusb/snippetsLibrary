## Use python expression inline script to execute in blender with subprocess call.
## Example to trigger rendering viewport (use GUI)

import bpy
import textwrap
from pathlib import Path
from datetime import datetime
import subprocess

def last_saved(path: Path) -> str:
    """Return a human-readable timestamp of file last modified time"""
    mtime = path.stat().st_mtime
    return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")

# Use same blender as current (need to be replaced if launched externally)
blender_bin = bpy.app.binary_path

path_of_blends_to_render = "path/to/folder/containing/blends/"

blend_list = Path(path_of_blends_to_render).glob("*.blend")

for blend in blend_list:
    print(blend.name, last_saved(blend))

    python_inline_code = textwrap.dedent("""
    import bpy
    from pathlib import Path

    # Find viewports
    def get_viewports_override():
        viewports = []
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            viewports.append({'window': window, 'screen': screen, 'area': area, 'region': region})
        # filter by size
        viewports.sort(key=lambda v: v['area'].width * v['area'].height)
        return viewports
    
    viewports = get_viewports_override()
    if not viewports:
        print('No viewport found in workspace', bpy.data.filepath)
        
        ## Note: Script execution continue after wm.quit ! For True early return, Raise after to ensure script stops.
        bpy.ops.wm.quit_blender()
        assert False, 'stop script'
                                         
    # Use biggest for override (last)
    with bpy.context.temp_override(**viewports[-1]):
        # Set viewport to camera
        bpy.context.space_data.region_3d.view_perspective = 'CAMERA'
        
        # Trigger render viewport
        bpy.context.scene.render.filepath = f'//{Path(bpy.data.filepath).stem}_viewport'
        bpy.ops.render.opengl(animation=False, write_still=True)

    # Need to quit manually if not using '--background'
    bpy.ops.wm.quit_blender()
    """)

    ## Depending on usage, we may want various options: (background or not, capture to gather and store infos, etc)

    subprocess.run(
        [
            blender_bin,
            str(blend),
            # "--background", # Cannot use background mode when using GUI ops (like rendering viewport)
            "--python-expr",
            python_inline_code,
        ],
        check=False, # Do not CalledProcessError on non-zero exit code (default to False)
        # capture_output=True, # captures stdout and stderr into the returned object instead of console
        # text=True, # decodes stdout/stderr as strings rather than bytes (only usefull with capture_output)
        # timeout=600, # timeout the process takes longer by x seconds 
    )

print('Done')

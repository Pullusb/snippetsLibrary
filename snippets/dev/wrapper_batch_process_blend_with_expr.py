## Wrapper Python script that calls SCRIPT file on every file blend

import subprocess
import glob
import textwrap


BLENDER = "blender"  # or full path

for f in glob.glob("/path/to/files/**/*.blend", recursive=True):

    # In loop to change f-string variable if needed
    script_inline_code = textwrap.dedent(f"""
    import bpy
    print(bpy.path.display_name(bpy.data.filepath))
    """)

    result = subprocess.run(
        [BLENDER, "--background", f, "--python-expr", script_inline_code],
        capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        print(f"FAILED: {f}\n{result.stderr}")
    else:
        print(f"OK: {f}")
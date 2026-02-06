## Wrapper Python script that calls SCRIPT file on every file blend

import subprocess
import glob

BLENDER = "blender"  # or full path
SCRIPT = "/path/to/process_single.py"

for blend_file in glob.glob("/path/to/files/**/*.blend", recursive=True):
    result = subprocess.run(
        [BLENDER, "--background", blend_file, "--python", SCRIPT],
        capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        print(f"FAILED: {blend_file}\n{result.stderr}")
    else:
        print(f"OK: {blend_file}")
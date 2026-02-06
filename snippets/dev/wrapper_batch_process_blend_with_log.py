## Wrapper Python script that calls SCRIPT file on every blend file
## Note for sub-script: "sys.exit(1)" makes Blender quit with return code 1, which subprocess.run() will see in result.returncode.

import subprocess
import glob
import os
from datetime import datetime
from pathlib import Path

BLENDER = "blender"  # or full path
SCRIPT = "/path/to/process_single.py"
BLEND_DIR = "/path/to/files"
LOG_FILE = Path.home() / "Documents" / "blend_batch_log.txt"

blend_files = glob.glob(os.path.join(BLEND_DIR, "**/*.blend"), recursive=True)

with open(LOG_FILE, "w") as log:
    log.write(f"Batch started: {datetime.now()}\n")
    log.write(f"Files found: {len(blend_files)}\n")
    log.write("-" * 60 + "\n")

    for i, blend_file in enumerate(blend_files, 1):
        print(f"[{i}/{len(blend_files)}] {blend_file}")

        result = subprocess.run(
            [BLENDER, "--background", blend_file, "--python", SCRIPT],
            capture_output=True, text=True, timeout=120
        )

        status = "OK" if result.returncode == 0 else "FAILED"
        log.write(f"[{status}] {blend_file}\n")

        if result.returncode != 0:
            log.write(f"  stderr: {result.stderr.strip()}\n")
            print(f"  FAILED: {result.stderr.strip()}")

    log.write("-" * 60 + "\n")
    log.write(f"Batch finished: {datetime.now()}\n")

print(f"\nLog written to: {LOG_FILE}")
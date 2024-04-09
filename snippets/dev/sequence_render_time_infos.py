## Print infos on render times from a sequence folder (check creation time from frames)
## minimum, maximum, average and total time
## Use current working directory, a path can be specified as argument
## nice to use as CLI shortcut: alias sequnecetime = 'python3 path/to/script'

import sys
import os
import datetime
import numpy as np
from pathlib import Path

def check_render_time():
    folder = Path(os.getcwd())
    if len(sys.argv) > 1:
        folder = Path(sys.argv[1])

    files = [f for f in folder.iterdir() if f.is_file()]
    files.sort(key=lambda x: x.name)

    deltas = []
    for i in range(len(files)-1):
        f = files[i]
        next_f = files[i + 1]

        delta = next_f.stat().st_ctime - f.stat().st_ctime
        deltas.append(delta)

    print(f'Sequence evaluated render times in {folder.name} ({len(files)} files):')
    average = np.mean(deltas)
    print(f'Min time: {datetime.timedelta(seconds=min(deltas))}')
    print(f'Max time: {datetime.timedelta(seconds=max(deltas))}')
    print(f'Average : {datetime.timedelta(seconds=average)}')
    print()
    # Add 1 average as first frame time
    print(f'Total  : ~{datetime.timedelta(seconds=files[-1].stat().st_ctime - files[0].stat().st_ctime + average)}')

check_render_time()

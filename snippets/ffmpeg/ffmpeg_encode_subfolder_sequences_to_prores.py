## Encode sequences in subfolders to Prores

import re
from pathlib import Path
import subprocess

## Target directory containing sequence folders

paths = [
'/sequence_folder_to_encode_1',
'/sequence_folder_to_encode_2',
]

re_seq = re.compile(r'(.*?)_\d{4}')
re_num = re.compile(r'_(\d{4})\.')

from time import time

start = time()

for fp in paths:
    fp = Path(fp)
    print('\n\n---> ', fp)

    for subfolder in fp.iterdir():
        ## iterate in subfolder
        if not subfolder.is_dir():
            continue
        if not 'Smoke' in subfolder.name:
            print(f'SKIP {subfolder.name}')
            continue

        file_list = [f for f in subfolder.iterdir() if f.is_file() and re_num.search(f.name)]
        if len(file_list) < 2:
            print(subfolder.name, 'skip, not enough images')
            continue

        # print(file_list[0])
        ## /!\ important ! Sort result before groupby (otherwise multiple groups with using same key)
        file_list.sort(key=lambda x: int(re_num.search(x.name).group(1)))

        first_file = file_list[0]

        unpadded_stem = re_seq.search(first_file.name).group(1)

        num = str(int(re_num.search(first_file.name).group(1)))
        print(subfolder.name, ' with num digit: ', num)

        cmd = [
        'ffmpeg',
        '-f', 'image2',
        '-start_number', num,
        '-i', str(first_file.with_stem(f'{unpadded_stem}_%04d')), # ex: '.../render/img_%04d.png',
        '-r', '24', # 24 fps
        '-c:v', 'prores_ks',
        '-pix_fmt', 'yuva444p10le',
        '-alpha_bits', '16',
        '-profile:v', '4444',
        str(fp / f'{unpadded_stem}.mov')
        ]

        print(' '.join(cmd))
        subprocess.call(cmd)

print(f'elapsed {time() - start:.2f}s')

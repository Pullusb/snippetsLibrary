## Move mixed image sequences in their own subfolder

import re
from pathlib import Path
from itertools import groupby

## Directory with sequences to sort

paths = [
'/img_seq_folder_1',
'/img_seq_folder_2',
]

## Make sure the sequence naming convention respect the pattern 
## (any non-matching file is skipped)
## Created folder is named after regex group 1 (stem before number padding separator)

re_seq = re.compile(r'(.*?)_\d{4}')

for fp in paths:
    fp = Path(fp)

    file_list = [f for f in Path(fp).iterdir() if f.is_file() and re_seq.match(f.name)]
    ## /!\ important ! Sort result before groupby (otherwise multiple groups with using same key)
    file_list.sort(key=lambda x: x.name)

    for key, group in groupby(file_list, key=lambda x: re_seq.search(x.name).group(1)):
        ## /!\ Remember, iterable exhaust iself while iterating

        dest = fp / key
        dest.mkdir(exist_ok=True)

        for f in group:
            print(f)

            file_dest = dest / f.name
            f.rename(file_dest)

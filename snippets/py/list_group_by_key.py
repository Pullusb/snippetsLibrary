## using a list of items, create sublists groups based on a key (here by shot or sequence num)
import re
from itertools import groupby


fps = ['/z/project/sequences/sq010/sh0020/compo/PROJ_sq010_sh0020_compo_v000.aep',
'/z/project/sequences/sq010/sh0020/compo/render/PROJ_sq010_sh0020_compo_v000.mp4',
'/z/project/sequences/sq010/sh0030/compo/PROJ_sq010_sh0030_compo_v000.aep',
'/z/project/sequences/sq010/sh0030/compo/render/PROJ_sq010_sh0030_compo_v000.mp4',
'/z/project/sequences/sq010/sh0040/compo/PROJ_sq010_sh0040_compo_v000.aep',
'/z/project/sequences/sq010/sh0040/compo/render/PROJ_sq010_sh0040_compo_v000.mp4',

# problematic example (no sequence, no shots)
'/z/project/sequences/sq020/sauce/compo/render/PROJ_sq010_sh0040_compo_v000.mp4',
'/z/project/sequences/truc/sauce/compo/render/PROJ_sq010_sh0040_compo_v000.mp4',
]


pattern = r'/(sh\d{4})/' # per shots
#pattern = r'/(sq\d{3})/' # per sequence


## walrus version (python 3.8+)
grps_d = groupby(fps, key=(lambda x: match.group(1) if (match := re.search(pattern, x)) else 'no_key'))

## classic
# grps_d = groupby(fps, key=(lambda x: re.search(pattern, x).group(1) if re.search(pattern, x) else 'no_key'))


for g_key, f_list in grps_d:
    print(f'\n>> {g_key}')

    if g_key == 'no_key':
        # do something if no key found
        pass

    for f in f_list:
        print(f)

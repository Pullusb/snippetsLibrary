## run code in area by name using context manager, swapping temporarily area type
import bpy
from contextlib import contextmanager
# https://docs.python.org/3/library/contextlib.html

@contextmanager
def context(area_type: str):
    area = bpy.context.area
    former_area_type = area.type
    area.type = area_type
    try:
        yield area
    finally:
        area.type = former_area_type


## then use:
with context('NLA_EDITOR'):
    print(bpy.context.selected_nla_strips)

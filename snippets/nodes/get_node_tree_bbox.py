## Get full node tree bounding box

import bpy
from mathutils import Vector
import math

def get_dpi_factor():
    prefs = bpy.context.preferences.system
    return prefs.dpi * prefs.pixel_size / 72

def real_location(n):
    if not n.parent:
        return n.location
    return n.location + real_location(n.parent)

def get_node_tree_bbox(node_tree):
    '''Full node tree bounding box corners
    starting at top-left, clockwise
    Ignore empty frames and reroute
    '''

    dpi = get_dpi_factor()
    coords = []
    for n in node_tree.nodes:
        if n.type in ('FRAME', 'REROUTE'):
            continue
        n_size = n.dimensions / dpi
        n_loc = real_location(n) - Vector((0, n_size[1]))
        coords.append(n_loc)
        coords.append(n_loc + n_size)
        
    xmin = min([co.x for co in coords])
    xmax = max([co.x for co in coords])

    ymin = min([co.y for co in coords])
    ymax = max([co.y for co in coords])
    
    return Vector((xmin, ymax)), Vector((xmax, ymax)), Vector((xmax, ymin)), Vector((xmin, ymin))
## Get dictionnary of individual frame nodes bbox location and size

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

def bbox(f, frames):
    xs=[]
    ys=[]
    for n in frames[f]:
        # nodes of passed frame
        if n.type == 'FRAME':
            if n not in frames.keys():
                continue
            all_xs, all_ys = bbox(n, frames)
            xs += all_xs
            ys += all_ys

        else:
            loc = real_location(n)
            xs += [loc.x, loc.x + (n.dimensions.x/get_dpi_factor())]
            ys += [loc.y, loc.y - (n.dimensions.y/get_dpi_factor())]

    # return xs and ys with applied frame margin ~= 30
    return [min(xs)-30, max(xs)+30], [min(ys)-30, max(ys)+30]

def get_frames_bbox(node_tree):
    '''Return a dic with all frames loc and size
    ex: {frame_node: (location, dimension), ...}
    '''
    from collections import defaultdict

    # Create dic of frame object with his direct child nodes
    frames = defaultdict(list)
    frames_bbox = {}
    for n in node_tree.nodes:
        if not n.parent:
            continue
        # also contains frames
        frames[n.parent].append(n)

    # Dic for bbox coord
    for f, nodes in frames.items():
        # if f.parent: # skip to keep only top-level frames
        #     continue

        xs, ys = bbox(f, frames)
        # xs, ys = bbox(nodes, frames)

        ## returning: list of corner coords
        # coords = [
        #     Vector((xs[0], ys[1])),
        #     Vector((xs[1], ys[1])),
        #     Vector((xs[1], ys[0])),
        #     Vector((xs[0], ys[0])),
        # ]
        # frames_bbox[f] = coords

        ## returning: (loc vector, dimensions vector)
        frames_bbox[f] = Vector((xs[0], ys[1])), Vector((xs[1] - xs[0], ys[1] - ys[0]))

    # Better to totally ignore empty frame 
    # for f in [n for n in node_tree.nodes if n.type=='FRAME' and n not in frames.keys()]:
    #     add empty frames
    #     frames_bbox[f] = f.location.copy(), f.dimensions.copy() 

    return frames_bbox
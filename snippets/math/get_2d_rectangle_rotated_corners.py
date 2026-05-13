## Get corners 2D coordinate of a rectangle based on center coord, width and height and degree rotation

import math

def rotated_corners(cx, cy, w, h, rot_deg):
    """Return the four corners of an axis-aligned rectangle rotated around its center.

    Args:
        cx (float): Center X coord.
        cy (float): Center Y coord.
        w (float): Rectangle width.
        h (float): Rectangle height.
        rot_deg (float): Rotation in degrees, counter-clockwise in a y-up frame
            (clockwise in a y-down/screen frame).

    Returns:
        list[tuple[float, float]]: Corners as `[BL, BR, TR, TL]` (counter-clockwise winding in y-up).
    """
    hw, hh = w / 2, h / 2
    r = math.radians(rot_deg)
    c, s = math.cos(r), math.sin(r)
    return [(cx + lx*c - ly*s, cy + lx*s + ly*c)
            for lx, ly in [(-hw,-hh),(hw,-hh),(hw,hh),(-hw,hh)]]

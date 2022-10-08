## rgb color to hexadecimal and hex to rgb
import math

def convert_srgb_to_linear_rgb(srgb_color_component: float) -> float:
    """Convert from sRGB to Linear RGB
    https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ
    """
    if srgb_color_component <= 0.04045:
        return srgb_color_component / 12.92

    return math.pow((srgb_color_component + 0.055) / 1.055, 2.4)

def hex_to_rgb(hex, alpha=True, base_one=True) -> tuple:
    """Convert hexadecimal color code to linear rgb(a)
    alpha: add alpha value to returned color tuple
    base_one: return linear decimal values from 0.0 to 1.0
    if base_one is False, return non linear values from 0 to 255
    """
    hex = hex.strip('#')
    rgb = []
    for i in (0, 2, 4):
        # extract color component
        decimal = int(hex[i:i+2], 16)
        if base_one:
            # Get a number between 0.0 and 1.0
            decimal /= 255
            # convert from srgb to linear
            decimal = convert_srgb_to_linear_rgb(decimal)
        rgb.append(decimal)

    if alpha:
        alpha = 1.0 if base_one else 255
        return tuple(rgb + [alpha])
    return tuple(rgb)

def rgb_to_hex(r, g, b):
    if isinstance(r, float):
        return ('{:X}{:X}{:X}').format(int(r*255), int(g*255), int(b*255))
    else:    
        return ('{:X}{:X}{:X}').format(r, g, b)

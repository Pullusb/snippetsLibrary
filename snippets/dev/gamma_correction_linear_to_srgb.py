## color gamma correction using linear to SRGB
## Allow to get screen displayed color values from a color prop (i.e. can be used in OpenGL draw)

from math import pow

def linear_to_srgb(color_linear):
    """
    Convert a linear color value to sRGB using the approximate gamma 2.2.
    Optionally handles an alpha channel, which is passed through unchanged.

    Parameters:
    color_linear (tuple): A tuple of three or four floats representing the linear RGB values, optionally with alpha.

    Returns:
    tuple: A tuple of three or four floats representing the sRGB values, optionally with alpha.
    """
    def convert_channel(c):
        if c <= 0.0031308:
            return 12.92 * c
        else:
            return 1.055 * pow(c, 1/2.4) - 0.055

    # Apply gamma correction to RGB channels
    color_srgb = tuple(convert_channel(c) for c in color_linear[:3])

    # If an alpha channel is present, append it to the output
    if len(color_linear) == 4:
        color_srgb += (color_linear[3],)

    return color_srgb

## example by getting color from a material:
# color = bpy.data.materials['material_name'].node_tree.nodes["Principled BSDF"].inputs[0].default_value[:]

color = [0.270500, 0.270500, 0.270500, 1.0] # (format doing Ctrl+C over a color property)
print(linear_to_srgb(color))
# >> (0.5568648270521792, 0.5568648270521792, 0.5568648270521792, 1.0)

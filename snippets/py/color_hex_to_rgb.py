## rgb color to hexadecimal and otehr way around
def hex_to_rgb(hex, base_one=True):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        if base_one:
            decimal /= 255
        rgb.append(decimal)

    return tuple(rgb)

def rgb_to_hex(r, g, b):
    if isinstance(r, float):
        return ('{:X}{:X}{:X}').format(int(r*255), int(g*255), int(b*255))
    else:    
        return ('{:X}{:X}{:X}').format(r, g, b)

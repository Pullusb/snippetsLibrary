def clamp(value, minimum, maximum):
    '''Return passed value clamped within minimum to maximum range'''
    return max(min(value, maximum), minimum)
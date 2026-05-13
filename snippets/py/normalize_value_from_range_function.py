## Normalize value from 0 to 1 based on a range

def map_value_from_0_to_1(value, min, max):
    """Map a value from the range [min, max] to the range [0, 1]
    Also known as "inverse lerp" or "unlerp", inverse of linear interpolation.
    Return:
        Normalized value or 0.0 if min == max
    """
    if min == max:
        # avoid ZeroDivisionError
        return 0.0
    return (value - min) / (max - min)


## Written with same convention as bl_math.lerp
def inverse_lerp(from_value, to_value, value):
    """Map value from the range [from_value, to_value] to [0, 1].

    Inverse of bl_math.lerp: where lerp(a, b, t) returns a value given
    a blend factor t, this recovers t from the value.
    """
    if from_value == to_value:
        return 0,0
    return (value - from_value) / (to_value - from_value)

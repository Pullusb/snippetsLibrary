# Get flipped left/right name either ending with ".l/.R.001" or starting with "l./R."

def get_flipped_name(name):
    import re

    def flip(match, start=False):
        if not match.group(1) or not match.group(2):
            return

        sides = {
            'R' : 'L',
            'r' : 'l',
            'L' : 'R',
            'l' : 'r',
        }

        if start:
            side, sep = match.groups()
            return sides[side] + sep
        else:
            sep, side, num = match.groups()
            return sep + sides[side] + (num or '')

    start_reg = re.compile(r'^(l|r)([.-_])', flags=re.I)

    if start_reg.match(name):
        return start_reg.sub(lambda x: flip(x, True), name)
    else:
        return re.sub(r'([.-_])(l|r)(\.\d+)?$', flip, name, flags=re.I)

print( get_flipped_name('sauce.r.001') )
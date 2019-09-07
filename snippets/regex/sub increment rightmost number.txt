#increment rightmost number

def increment(match):
    return str(int(match.group(1))+1).zfill(len(match.group(1)))

name = 'r2d2-V3'
if re.search(r'\d+', name):#check if a number exists in string
        new = re.sub(r'(\d+)(?!.*\d)', increment, name)#rightmost number

#>>> r2d2v4
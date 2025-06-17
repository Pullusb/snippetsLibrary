## increment rightmost number

name = 'r2d2-V3'

## oneliner : increment rightmost number (keep padding)
new = re.sub(r'(\d+)(?!.*\d)', lambda x: str(int(x.group(1))+1).zfill(len(x.group(1))), name)

## oneliner using f-string
new = re.sub(r'(\d+)(?!.*\d)', lambda x: f"{int(x.group(1))+1:0{len(x.group(1))}d}", name)


## with named function
def increment(match):
    return str(int(match.group(1))+1).zfill(len(match.group(1)))
new = re.sub(r'(\d+)(?!.*\d)', increment, name) # find rightmost number

#>>> r2d2v4
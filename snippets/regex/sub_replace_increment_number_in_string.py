# replace an element based on a capture group passed to a function with re.sub

fp = "projet_02"

def increment(match):
    return str(int(match.group(1))+1).zfill(len(match.group(1)))


#pass match object to function "increment"
incremented = re.sub(r'(\d+)', increment, fp)

print(incremented)
#>>> projet_03
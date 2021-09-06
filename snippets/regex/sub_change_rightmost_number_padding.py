## change padding of the rightest number of in a string

# oneliner
# string = re.sub(r'(\d+)(?!.*\d)', lambda x : x.group(1).zfill(padding), string)

def repadd(string, padding=0):
    '''Change padding of rightmost number in string
    string is unchanged if no digit
    '''
    import re
    return re.sub(r'(\d+)(?!.*\d)', lambda x : x.group(1).zfill(padding), string)

name = 'r2d2-V3'
print(repadd(name,4))
#>>>r2d2-V0003
# number a padding with re.sub by calling a fn.

test_str = 'sauce_##_zen'
ct = 1
def number(match):
    global ct
    return str(ct).zfill(len(match.group(1)))

#passe match object to function "number"
numbered = re.sub(r'(#+)', number, test_str)
print(numbered)
#>>> 'sauce_01_zen
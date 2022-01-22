## Ways to iterate/enumerate a list in reverse order
# https://stackoverflow.com/questions/529424/traverse-a-list-in-reverse-order-in-python

l_obj = list('test')

## direct index methods with reverse slice
for i in range(len(l_obj))[::-1]:    
    if l_obj[i] == 't':
        l_obj.pop(i)

## same result with reverse range
for i in range(len(gp_objects)-1, -1, -1):
    if l_obj[i] == 't':
        l_obj.pop(i)

## reverse enumerate by preprocessing idx and item
for i, elem in ((i, l_obj[i]) for i in reversed(range(len(l_obj)))):
    if elem == 't':
        l_obj.pop(i)

## reverse enumerate using a function wrapper
def reversed_enumerate(collection: list):
    for i in range(len(collection)-1, -1, -1):
        yield i, collection[i]

for i, elem in reversed_enumerate(l_obj):
    print(i, elem)

l = [ ['apple', 3], ['banana', 5], ['orange', 2] ]
# l.sort(key=lambda x: x[1])#sort in place, #optional : , reverse = True
sorted_l = sorted(l, key=lambda x: x[1], reverse=True)#sort decreasing
def compareMatrixList(one, two):
    '''handle comparison of matrix separately due to change in precision at loading'''
    for x in range(len(one)):
        for y in range(len(one[x])):
            #print ('%.6f' % one[x][y], '%.6f' % two[x][y]) #debug-compare
            if '%.5f' % one[x][y] != '%.5f' % two[x][y]:
                return (False)
    return (True)
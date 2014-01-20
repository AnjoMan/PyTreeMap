import cProfile
from numpy import *
from collections import defaultdict




input = [True, False, False, True, True, False, True]
values= [10,   20,    5,     8,    9,    20056, 1]


def bool2int(x):
        y = 0
        for i,j in enumerate(x):
            if j: y += 1<<i
        return y




def int2bool(i,n): 
    return fromiter((False,True)[i>>j & 1] for j in range(0,n))
    

def trueIndices(i,n):
    return (j for j in range(0,n) if i>>j & 1)
    
boolVal = bool2int(input)
nVals = len(input)



res = int2bool(boolVal, nVals)

index = trueIndices(boolVal, nVals)



mask = fromiter(res, bool, count=-1)

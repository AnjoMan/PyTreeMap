from numpy import random
import numpy


a = [1,2,3]
b = ['a','b','c']
c = [50,60,70]


for out in zip(a,b,c):
    print(out)
    print(any(out))
    print(out.any())
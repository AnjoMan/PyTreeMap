import cProfile
from numpy import *
from collections import defaultdict




a = defaultdict(int)


print(a[1])

a[1] += 3
a[2] += 2
a[1] += 4
print(a)

# 
# size=20000
# input = random.randint(0,2,size=size)
# 
# input = [i>0 for i in input]
# 
# 
# def bool2int(x):
#         y = 0
#         for i,j in enumerate(x):
#             if j: y += 1<<i
#         return y
# 
# 
# 
# 
# def int2bool(i,n): 
#     return list((False,True)[i>>j & 1] for j in range(0,n)) 
#     
# 
# # 
# # interm = bool2int(input)
# # 
# # 
# # 
# # output = int2bool(interm, size)
# 
# 
# cProfile.run('bool2int(input)')
# cProfile.run('bool2int2(input)')
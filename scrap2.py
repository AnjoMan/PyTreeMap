from numpy import *
import matplotlib.pyplot as plt


L1 = [ [1,1],
      [10,15],
      [10,17],
      [20,17]]


p1 = [1,1]
p2 = [10, 15]
p3 = [8,2]


for point in L1:
    plt.scatter(L1)

plt.show()


def pointToLine(p1,p2,p3):
    p1,p2,p3 = [array(pt) for pt in [p1,p2,p3]]
    
    num = dot(p3-p1,p2-p1)
    den = dot(p2-p1,p2-p1)
    
    u = dot(p3-p1,p2-p1) / dot(p2-p1,p2-p1)
    
    if u > 1:
        return linalg.norm(p3 - p2)
    elif u < 0:
        return linalg.norm(p3-p1)
    else:
        p = p1 + u *(p2 - p1)
        return linalg.norm(p3-p)
    
    
def lineToLine(L1, L2):
    p1,p2 = [array(el) for el in L1]
    p3,p4 = [array(el) for el in L2]
    
    distances = [pointToLine(p1,p2, p) for p in [p3,p4]] + [pointToLine(p3,p4,p) for pp in [p1,p2]]
    
    return min(distances)



def pointToCompoundLine(L,P):
    Pa = L[0:-1]
    Pb = L[1:]
    
    distances = [pointToLine(pa,pb,P) for pa,pb in zip(Pa,Pb)]
    return min(distances)
    
    
out = pointToCompoundLine(L1,p3)
    
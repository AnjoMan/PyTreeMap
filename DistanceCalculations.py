from numpy import *
import matplotlib.pyplot as plt


L1 = [ [1,1],
      [10,15],
      [10,17],
      [20,17]]

L2 = [ [10,1],
       [12,1],
       [14,10],
       [18,15],
       [22,15]]

p1 = [1,1]
p2 = [10, 15]
p3 = [15,14]


for point in L1:
    plt.scatter(*point,c='r')

for (ax,ay), (bx,by) in zip(L1[0:-1], L1[1:]):
    plt.plot( [ax,bx],[ay,by], 'b')
    

plt.scatter(*p3)



for point in L2:
    plt.scatter(*point, c='r')

for (ax,ay), (bx,by) in zip(L2[0:-1], L2[1:]):
    plt.plot( [ax,bx],[ay,by], 'b')

plt.show()


def pointToSegment(p1,p2,p3):
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
    
    
def segToSeg(L1, L2):
    p1,p2 = [array(el) for el in L1]
    p3,p4 = [array(el) for el in L2]
    
    distances = [pointToLine(p1,p2, p) for p in [p3,p4]] + [pointToLine(p3,p4,p) for pp in [p1,p2]]
    
    return min(distances)



def pointToLine(L,P):
    Pa = L[0:-1]
    Pb = L[1:]
    
    distances = [pointToSegment(pa,pb,P) for pa,pb in zip(Pa,Pb)]
    return min(distances)

def lineToLine(L1,L2):
    distances = [pointToLine(L1, p) for p in L2] + [pointToLine(L2,p) for p in L1]
    return(min(distances))
    
out = lineToLine(L1,L2)
    
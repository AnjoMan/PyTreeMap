from numpy import *


def pointToPoint(p1,p2):
    return sqrt( (p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
def pointToSegment(p1,p2,p3):
    p1,p2,p3 = [array(pt) for pt in [p1,p2,p3]]
    
    num = dot(p3-p1,p2-p1)
    den = dot(p2-p1,p2-p1)
    
    u = dot(p3-p1,p2-p1) / dot(p2-p1,p2-p1)
    
    if u > 1:
        return (linalg.norm(p3 - p2),p2)
    elif u < 0:
        return (linalg.norm(p3-p1),p1)
    else:
        p = p1 + u *(p2 - p1)
        return (linalg.norm(p3-p),p)
    
    
def segToSeg(L1, L2):
    p1,p2 = [array(el) for el in L1]
    p3,p4 = [array(el) for el in L2]
    
    distances = [pointToLine(p1,p2, p) for p in [p3,p4]] + [pointToLine(p3,p4,p) for pp in [p1,p2]]
    
    return min(distances)



def pointToLine(L,P):
    Pa = L[0:-1]
    Pb = L[1:]
    
    distances = [pointToSegment(pa,pb,P) for pa,pb in zip(Pa,Pb)]
    return min(distances, key= lambda x: x[0])

def lineToLine(L1,L2):
    distances = [pointToLine(L1, p) + (array(p),) for p in L2] + [pointToLine(L2,p)+ (array(p),) for p in L1]
    return min(distances, key= lambda x:x[0])
    







if __name__ == "__main__":
    
    import matplotlib.pyplot as plt
    
    def drawLine(line):
        for point in line:
            plt.scatter(*point, c='b')
        
        
        for (ax,ay),(bx,by) in zip(line[0:-1], line[1:]):
            plt.plot([ax,bx],[ay,by], 'b')
    
    
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
#     p3 = [15,14]
    p3 = [7,8]
    
    drawLine(L1)
        
    
    plt.scatter(*p3)
    
    
    
    drawLine(L2)
    
    
    dist, p1,p2= lineToLine(L1,L2)
    plt.scatter(*p1, c='r')
    plt.scatter(*p2, c='r')
    plt.plot([p1[0],p2[0]],[p1[1],p2[1]], 'g-')
    
    dist, pt = pointToLine(L1,p3)
    plt.scatter(*pt, c='r')
    plt.plot([pt[0],p3[0]], [pt[1],p3[1]], "g-")
    
    dist, pt = pointToLine(L2,p3)
    plt.scatter(*pt, c='r')
    plt.plot([pt[0],p3[0]], [pt[1],p3[1]], "g-")

    plt.axes().set_aspect(aspect='equal')
    plt.show()
        
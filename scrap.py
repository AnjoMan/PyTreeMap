import scipy.io
import numpy as np


class mCircle:
    perimeter = None
    def __init__(self, radius=np.random.rand):
        if radius == np.random.rand:
            radius = radius()
            
        self.radius = radius
    
    def __str__(self):
        return str(self.radius)
    
    def getPerimeter(self):
        return perimeter(self.radius)



myCircles = [mCircle() for i in range(1,200)]

def perimeter(radius):
    return 100*np.pi*radius
mCircle.perimeter =  perimeter




for circle in myCircles:
    print "radius: %01.3f. perimeter: %2.3f\n" % (circle.radius,circle.getPerimeter())
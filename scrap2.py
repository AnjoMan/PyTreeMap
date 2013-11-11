


class Shape(object):
    
    
    @staticmethod
    def setConstant(val):
        Shape.val = val
    
    def getConstant(self):
        return Shape.val

class Circle(Shape):
    pass
    
    
    
    

Circle.setConstant(12)

mCircle = Circle()

print mCircle.getConstant()

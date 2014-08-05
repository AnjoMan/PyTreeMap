
import numpy as np

class Shape(object):
    def __init__(self,area):
        self.area = area;
    
    
    def dimStr(self): return 'area: %s' % str(self.area)
    def __str__(self):
        return 'I am a circle'
    def __repr__(self): 
        return '%s, %s' % (self.__class__.__name__, self.dimStr()) + ';'

class Circle(Shape):
    
    def __init__(self,radius): 
        self.radius = radius
    
    def area(self): 
        return np.pi * self.radius**2
    
    
    def dimStr(self):
        return 'radius %s' % str(self.radius)



class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def dimStr(self):
        return '%s x %s' % (str(self.width), str(self.height))
    
    def area(self):
        return self.width * self.height
    

class Square(Rectangle):
    
    def __init__(self, side):
        self.width = side
        self.height = side
        
class BoxOfShapes(object):
    
    def __init__(self, elements):
        self.elements = elements
    
    def __repr__(self):
        circles = [ el.dimStr() for el in self.elements if isinstance(el, Circle)]
        squares = [ el.dimStr() for el in self.elements if isinstance(el, Square)]
        rectangles = [el.dimStr() for el in self.elements if (isinstance(el, Rectangle) and  not isinstance(el, Square)) ]
        
        return 'Box of Shapes; Circles: %s, Squares: %s, Rectangles: %s;' % ( str(circles), str(squares), str(rectangles))
    
#     def __repr__(self):
#         return str(self.elements)
    


listOfShapes = [Rectangle(10,13),Rectangle(9,5),Circle(12),Circle(8),Circle(36),Square(10)]

myBox = BoxOfShapes(listOfShapes)

print myBox


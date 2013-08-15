import scipy.io
import numpy as np
import numbers
import copy

class Shape:
    
    Circle = '<obj type: "Circle" >'
    
    def __init__(self,id):
        self.id = id;
    
    def type(self):
        return '<obj type: "Shape" >'
    
    
    def __eq__(self, other):
        print self, other
        if self.type() == other.type():
            return True
        else:
            return False
    
    def __repr__(self):
        return "<" + self.type()[1:-1] + " id: %s " % str(self.id) + ">"


class Circle(Shape):
    
    def type(self):
        return '<obj type: "Circle" >'

class Square(Shape):
    def type(self):
        return '<obj type: "Square" >'





# mShape = Shape(1)
# mCircle = Circle(1)
# 
# 
# mShape2 = Shape(1)
# 
# 
# print mShape == mCircle
# 
# print mShape == mShape2


mShapes = [Obj(1) for Obj in [Circle, Square]]
from PySide import QtGui, QtCore

import sys
import numpy as np
import colorsys



class Circle(object):
    def __init__(self):
        self.connections = None
        
        
    
    def addConnection(self, obj):
        if not self.connections:
            self.connections = []
        
        self.connections +=[obj]

myCircle = Circle()

# myCircle.addConnection(1)

if myCircle.connections != None:
    print '1'
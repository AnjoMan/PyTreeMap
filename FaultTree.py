
import numpy as np
import colorsys
from collections import defaultdict
from PowerNetwork import *
from Treemap import layout
from FaultTreemap import *
from sets import Set
import sys


class Legend(object):
    
    def __init__(self, items):
        
        self.items = items
    
    
    def draw(self, canvas, painter):
        x,y = 20,20;
        width = 120;
        height = 30;
        
        
        for text, color in self.items:
            painter.setBrush(QtGui.QColor(color))
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRect(x,y,width,height)
            
            painter.setFont(QtGui.QFont('serif', 10))
            painter.setPen(QtCore.Qt.black)
            metrics = painter.fontMetrics()
            fw,fh = metrics.width(text),metrics.ascent()
            painter.drawText(x+ (width - fw)/2.0, y +(height+ fh)/2.0,text)
            y = y+height+2

class TreeFault(Fault):
    radius = 10
    def __init__(self, listing, reduction=None):
        super(TreeFault,self).__init__(listing, reduction=reduction)
        
        self.pos = None,None
        self.connections = []
    
    def radius(self):
        return 10 + 0.9*len(self.elements)-1
        
    def setPos(self,pos):
        self.pos = pos;

    def topConnectorPos(self):
        x,y = self.pos
#         return x,y-self.radius()
        return x,y
    
    def bottomConnectorPos(self):
        x,y = self.pos
#         return x,y+self.radius()
        return x,y
    
    def draw(self,canvas, painter):
        #this method would be called by PySideCanvas when given using PySideCanvasObj.draw(fault)
        (x,y), r = self.pos, self.radius()
        x0,y0, x_,y_ = x-r,y-r,2*r,2*r
        startAngle, arcAngle = 0, 360 * 1/len(self.elements)
        
        painter.setPen(QtCore.Qt.black)
        painter.setFont(QtGui.QFont('serif', 5))
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        
        def putText(qp,x,y,text):
            qp.setPen(QtGui.QColor(0,0,0))
            metrics = qp.fontMetrics()
            fw,fh = metrics.width(text),metrics.height()
            qp.drawText(x-fw/2,y+fh/4,text)
        
        pen = QtGui.QPen(QtGui.QColor(10,10,10), 1, QtCore.Qt.SolidLine)
        for other in self.connections:
            xT,yT = self.bottomConnectorPos()
            xB,yB = other.topConnectorPos()
            painter.drawLine(xT,yT,xB,yB)
        
        for index,element in enumerate(self.elements):
            painter.setBrush(QtGui.QColor(element.__class__.color))
            painter.setPen(QtGui.QColor(80,80,80))
            if len(self.elements) > 1:
                painter.drawPie(x0,y0,x_,y_, round(startAngle*16), round(arcAngle*16))
            else:
                painter.drawEllipse(x0,y0,x_,y_)
            lAngle = startAngle + (arcAngle/2.0)  #in degrees
            rd = 8.0/15 * r if len(self.elements) > 1 else 0
            
            yd = y - rd * np.sin(np.pi/180 * lAngle)
            xd = x + rd * np.cos(np.pi/180 * lAngle)
            
            putText(painter, xd,yd,str(element.id))
            startAngle += arcAngle
        
#         print '\n'
        painter.setRenderHint(QtGui.QPainter.Antialiasing, False)

def drawRows(myCanvas, faultTree, width, height):
    #define spacing and layout for fault-tree from a connections dictionary
    def hspacing(numEls, width):
        nominalRadius = 10;
        if numEls < 2:
            sideGap,gap = round(width/2.0), 0
        else:
            sideGap = max(round(width * (20-0.2*numEls) / 100), 10)
            gap = max(nominalRadius*2+5, round((width-2*sideGap)/(numEls-1)) )
        return sideGap, gap
    
    y = round(0.15*height)
    ygap = (height - y*2) / (len(faultTree.keys()) - 1)
    for level in faultTree.values():
        sideGap, gap = hspacing(len(level), width)
        x = sideGap
        for fault in level:
            fault.setPos((x,y))
            myCanvas.draw(fault)
            x+= gap
        
        y+= ygap
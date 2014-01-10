
import numpy as np
import colorsys
from collections import defaultdict
from PowerNetwork import *
from Treemap import layout
from PySide import QtGui, QtCore
# from FaultTreemap import *
# from sets import Set
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
            
class TreeVis(QtGui.QWidget):
    def __init__(self, pos=None, faultTree=None):
        
        super(TreeVis, self).__init__()
        
        self.faultTree = faultTree
        (x,y,w,h) = self.pos = [100,100,1800,700] if pos == None else pos
        self.move(x,y)
        self.resize(w,h)
        self.setWindowTitle('Tree Visualization')
        
        self.show()
        self.rectangles, self.colors, self.outlines,self.lines, self.objs = [],[],[],[],[]
        self.colors = []
        
        self.layoutMap()
        
        
        self.draw(Legend( [ (mClass.__name__, mClass.color) for mClass in [Branch, Bus, Gen, Transformer]]))
        
        
        
        
    def layoutMap(self):
        width, height = self.width(), self.height()
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
        ygap = (height - y*2) / (len(self.faultTree.keys()) - 1)
        
        #build for equal spacing with fixed radii
#         for levelNo,level in self.faultTree.items():
#             sideGap, gap = hspacing(len(level), width)
#             x = sideGap
#             for fault in sorted(level, key= lambda mFault: mFault.value()) :
#                 fault.setPos((x,y))
#                 fault.setParent(self)
#                 fault.setLevel(levelNo)
#                 self.draw(fault)
#                 x+= gap
#             
#             y+= ygap
        
        #build for equal spacing with radii scaled by levelContext 
        
        for levelNo, level in self.faultTree.items():
            if len(level) <2:  #case where only one fault is present
                fault = level[0]
                fault.radius = 15
                fault.setPos((width/2,y))
                fault.setLevel(levelNo)
                self.draw(fault)
                continue
            
            level = sorted(level, key= lambda mFault: mFault.value())
            
            if len(level) == 2: #case where exactly two faults are present and we want to add spacing outside
                level[0].radius, level[1].radius = (30,20) if level[0].getLevelContext() > level[1].getLevelContext() else (20,30)
                level[0].setPos( (width * 0.30+ level[0].getRadius(), y))
                level[1].setPos( (width - width*0.30 - level[1].getRadius(), y))
                level[0].setLevel(levelNo)
                level[1].setLevel(levelNo)
                self.draw(level[0])
                self.draw(level[1])
                continue
            
            else:
                x,_ = sideGap, _ = hspacing(len(level), width) # this is a little bogus since I only want 'sideGap'
                space = width-2*sideGap
                
                sizes = [fault.getLevelContext()*0.6+0.4 for fault in level] #get all levels
                
                #first try to set sizes for XX% coverage
                scale = (space *0.80)/sum(sizes)
                gap = (space*0.20)/(len(sizes)-1)
                radii = [size*scale / 2.0 for size in sizes]
                
                mMax =  max(radii)
                #if some are too big, scale them all down and increase the gap size
                if mMax > 30:
                    radii = [radius * 30 /mMax for radius in radii]
                    gap = (space - sum(radii)*2) / (len(radii)-1)
                
#                 for radius, fault in zip(radii, sorted(level, key= lambda mFault: mFault.value())) :
                for radius, fault in zip(radii, level):
                    fault.radius = radius
                    fault.setPos( (x+radius, y))
                    fault.setParent(self)
                    fault.setLevel(levelNo)
                    self.draw(fault)
                    x+= 2* radius + gap
            y+= ygap
            
    
    
    def initUI(self, width, height, title):
        self.show()
        
    def drawRectangle(self, pos, color):
        self.rectangles += [pos]
        
        self.colors += [PySideCanvas.qtColor(color)]
    
    @staticmethod
    def qtColor(colorString):
        r,g,b = [colorString[1:3],colorString[3:5], colorString[5:7]]
        r,g,b = [int(num,16) for num in [r,g,b]]
        return QtGui.QColor(r,g,b)
        
    def drawOutline(self, pos, border, color=None):
        if border > 0:
            self.outlines += [ [pos, border, (PySideCanvas.qtColor(color) if color else PySideCanvas.qtColor('#000000'))]]
            return True
        else: return False
    
    def drawLine(self, pos):
        self.lines += [pos]

    
    def draw(self, item):
        #generic draw, in which the object implements a draw method with the pen
        self.objs += [item]
    
    def drawCircle(x,y,r):
        self.circles += [[ x,y,r]]
    def paintEvent(self, e):
        
        
        
        qp = QtGui.QPainter()
        qp.begin(self)
        
#         qp.setRenderHint(QtGui.QPainter.Antialiasing)
        #draw rectangles
        
        for rectangle, color in zip(self.rectangles, self.colors):
            qp.setPen(color)
            qp.setBrush(color)
            x0,y0,xn,yn = rectangle
            qp.drawRect(x0,y0, xn-x0, yn-y0)
        
        #draw borders /outlines
        pen = QtGui.QPen(QtGui.QColor(10,10,10), 1, QtCore.Qt.SolidLine)
       
        for (x0,y0,xn,yn), border, color in self.outlines:
#             print color.red(), color.green(), color.blue()
            segments = [ [ x0,y0, xn, y0], [x0,y0,x0,yn],[x0,yn,xn,yn], [xn,y0,xn,yn]]
            pen.setColor(color)
            pen.setWidth(border)
            qp.setPen(pen)
            
            for x0,y0,xn,yn in segments:
                qp.drawLine(x0,y0,xn,yn)
        
        #draw lines
        qp.setRenderHint(QtGui.QPainter.Antialiasing,True)
        pen.setWidth(1)
        qp.setPen(pen)
        for x0,y0,xn,yn in self.lines:
            qp.drawLine(x0,y0,xn,yn)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, False)
        #draw objects
        for obj in self.objs:
            obj.draw(self, qp)
        
        qp.end()
    
    
        
class TreeFault(Fault):
    radius = 10
    def __init__(self, listing, reduction=None):
        super(TreeFault,self).__init__(listing, reduction=reduction)
        
        self.pos = None,None
        self.radius = 10;
        self.connections = []
    
    def getRadius(self):
        try:
            return self.radius
        except:
            return 10 + 0.9*len(self.elements)-1
        
    def setPos(self,pos):
        self.pos = pos;
    
    def setParent(self, parent):
        self.parent = parent
    
    def setLevel(self, level):
        self.level = level
        
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
        (x,y), r = self.pos, self.getRadius()
        x0,y0, x_,y_ = x-r,y-r,2*r,2*r
        startAngle, arcAngle = 0, 360 * 1/len(self.elements)
        
        painter.setPen(QtCore.Qt.black)
        painter.setFont(QtGui.QFont('serif', 5))
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        
        def putText(qp,x,y,text):
            qp.setPen(QtGui.QColor(0,0,0))
            metrics = qp.fontMetrics()
            fw,fh = metrics.width(text),metrics.height()
            qp.drawText(QPointF(x-fw/2,y+fh/4),text)
        
        
        
        pen = QtGui.QPen(QtGui.QColor(10,10,10), 1, QtCore.Qt.SolidLine)
        
        for other in self.connections:
            
            weight = 0.2 + 3*other.getLevelContext() + 2*self.getLevelContext()
#             weight=1
            
            xT,yT = self.bottomConnectorPos()
            xB,yB = other.topConnectorPos()
            painter.setPen(QtGui.QPen(QtCore.Qt.black, weight))
            painter.drawLine(QPointF(xT,yT),QPointF(xB,yB))
        
        
        for index,element in enumerate(self.elements):
            painter.setBrush(QtGui.QColor(element.__class__.color))
            painter.setPen(QtGui.QColor(80,80,80))
            if len(self.elements) > 1:
                painter.drawPie(QRectF(x-r,y-r,2*r,2*r), round(startAngle*16), round(arcAngle*16))
            else:
                painter.drawEllipse(QRectF(x-r,y-r,2*r,2*r))
            lAngle = startAngle + (arcAngle/2.0)  #in degrees
            rd = 8.0/15 * r if len(self.elements) > 1 else 0
            
            yd = y - rd * np.sin(np.pi/180 * lAngle)
            xd = x + rd * np.cos(np.pi/180 * lAngle)
            
            putText(painter, xd,yd,str(element.id))
            startAngle += arcAngle
        
#         print '\n'
        painter.setRenderHint(QtGui.QPainter.Antialiasing, False)


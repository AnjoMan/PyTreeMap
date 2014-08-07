"""
    written by Anton Lodder 2012-2014
    all rights reserved.
    
    This software is the property of the author and may not be copied,
    sold or redistributed without expressed consent of the author.
"""

if __name__ == '__main__':
    import sys, os, inspect
    try:
        import pytreemap
    except:
        #walk up to 'pytreemap' and add to path.
        realpath = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
        (realpath, filename) = os.path.split(realpath)
        while filename != 'pytreemap':
            (realpath, filename) = os.path.split(realpath)
        sys.path.append(realpath)
        import pytreemap
    
import numpy as np
import colorsys
from collections import defaultdict
from pytreemap.visualize.VisBuilder import getFaults, JSON_systemFile
from pytreemap.system.PowerNetwork import Fault, Branch, Bus, Gen, Transformer
from pytreemap.Treemap import layout
from PySide.QtGui import *
from PySide.QtCore import *
# from FaultTreemap import *
# from sets import Set
import sys



def main():
    
    mCase =( 'case30_geometry.json','cpfResults_tree.json')
    mCase =( os.path.join(pytreemap.system.__path__[0],mCase[0]), os.path.join(pytreemap.__path__[0], 'sample_results',mCase[1]))
    
    
    
    
    
    app = QApplication(sys.argv)
    
    mVis = ContingencyTree(*mCase)
    
    sys.exit(app.exec_())
    

class Legend(object):
    
    def __init__(self, items):
        
        self.items = items
    
    
    def draw(self, canvas, painter):
        x,y = 20,20;
        width = 120;
        height = 25;
        
        
        for text, color in self.items:
            painter.setBrush(QColor(color))
            painter.setPen(Qt.NoPen)
            painter.drawRect(x,y,width,height)
            
            painter.setFont(QFont('serif', 10))
            painter.setPen(Qt.black)
            metrics = painter.fontMetrics()
            fw,fh = metrics.width(text),metrics.ascent()
            painter.drawText(x+ (width - fw)/2.0, y +(height+ fh)/2.0,text)
            y = y+height+2
            

        
class TreeVis(QWidget):
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
        self.levelLabels = []
        self.layoutMap()
        
        
        self.draw(Legend( [ (mClass.__name__, mClass.color) for mClass in [Branch, Bus, Gen, Transformer]]))
        
class ContingencyTree(TreeVis):
    
    def __init__(self, system_file, resultsFile, pos=[20,20,1600,700]):
        
        (faults, faultTree) = getFaults(TreeFault, JSON_systemFile(system_file, resultsFile))
        
        super().__init__(pos, faultTree)
        
        
        
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
        
#         build for equal spacing with fixed radii
        for levelNo,level in self.faultTree.items():
            
            self.levelLabels.append( (levelNo, 80, y))
            sideGap, gap = hspacing(len(level), width)
            x = sideGap
#             for fault in sorted(level, key= lambda mFault: mFault.value) :
            for fault in level:
                fault.radius =  20
                fault.setPos((x,y))
                fault.setParent(self)
                fault.setLevel(levelNo)
                self.draw(fault)
                x+= gap
            
            y+= ygap
        
#         #build for equal spacing with radii scaled by levelContext 
#         
#         for levelNo, level in self.faultTree.items():
#             self.levelLabels.append( (levelNo, 80, y))
#             if len(level) <2:  #case where only one fault is present
#                 fault = level[0]
#                 fault.radius = 15
#                 fault.setPos((width/2,y))
#                 fault.setLevel(levelNo)
#                 self.draw(fault)
#             elif len(level) == 2: #case where exactly two faults are present and we want to add spacing outside
#                 level[0].radius, level[1].radius = (30,20) if level[0].getLevelContext() > level[1].getLevelContext() else (20,30)
#                 level[0].setPos( (width * 0.30+ level[0].getRadius(), y))
#                 level[1].setPos( (width - width*0.30 - level[1].getRadius(), y))
#                 level[0].setLevel(levelNo)
#                 level[1].setLevel(levelNo)
#                 self.draw(level[0])
#                 self.draw(level[1])
#             else:
#                 x,_ = sideGap, _ = hspacing(len(level), width) # this is a little bogus since I only want 'sideGap'
#                 space = width-2*sideGap
#                 
#                 sizes = [fault.getLevelContext()*0.6+0.4 for fault in level] #get all levels
#                 
#                 #first try to set sizes for XX% coverage
#                 scale = (space *0.80)/sum(sizes)
#                 gap = (space*0.20)/(len(sizes)) #change this divisor to change spacing
#                 radii = [size*scale / 2.0 for size in sizes]
#                 
#                 mMax =  max(radii)
#                 #if some are too big, scale them all down and increase the gap size
#                 if mMax > 30:
#                     radii = [radius * 30 /mMax for radius in radii]
#                     gap = (space - sum(radii)*2) / (len(radii))#change this divisor to change spacing
#                 
#                 x+= gap/2
# #                 for radius, fault in zip(radii, sorted(level, key= lambda mFault: mFault.value())) :
#                 for radius, fault in zip(radii, level):
#                     fault.radius = radius
#                     fault.setPos( (x+radius, y))
#                     fault.setParent(self)
#                     fault.setLevel(levelNo)
#                     self.draw(fault)
#                     x+= 2* radius + gap
#             y+= ygap
            
    
    
    def initUI(self, width, height, title):
        self.show()
        
    def drawRectangle(self, pos, color):
        self.rectangles += [pos]
        
        self.colors += [PySideCanvas.qtColor(color)]
    
    @staticmethod
    def qtColor(colorString):
        r,g,b = [colorString[1:3],colorString[3:5], colorString[5:7]]
        r,g,b = [int(num,16) for num in [r,g,b]]
        return QColor(r,g,b)
        
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
        
        
        
        qp = QPainter()
        qp.begin(self)
        
#         qp.setRenderHint(QPainter.Antialiasing)
        #draw rectangles
        
        for rectangle, color in zip(self.rectangles, self.colors):
            qp.setPen(color)
            qp.setBrush(color)
            x0,y0,xn,yn = rectangle
            qp.drawRect(x0,y0, xn-x0, yn-y0)
        
        #draw borders /outlines
        pen = QPen(QColor(10,10,10), 1, Qt.SolidLine)
       
        for (x0,y0,xn,yn), border, color in self.outlines:
#             print color.red(), color.green(), color.blue()
            segments = [ [ x0,y0, xn, y0], [x0,y0,x0,yn],[x0,yn,xn,yn], [xn,y0,xn,yn]]
            pen.setColor(color)
            pen.setWidth(border)
            qp.setPen(pen)
            
            for x0,y0,xn,yn in segments:
                qp.drawLine(x0,y0,xn,yn)
        
        #draw lines
        qp.setRenderHint(QPainter.Antialiasing,True)
        pen.setWidth(1)
        qp.setPen(pen)
        for x0,y0,xn,yn in self.lines:
            qp.drawLine(x0,y0,xn,yn)
        qp.setRenderHint(QPainter.Antialiasing, False)
        #draw objects
        for obj in self.objs:
            obj.draw(self, qp)
        
        
        #draw level labels:
        
        qp.setPen(Qt.black)
        qp.setBrush(Qt.NoBrush)
        mFont = QFont()
        mFont.setPointSize(25)
        qp.setFont(mFont)
        for level,x, y in self.levelLabels:
            fh = qp.fontMetrics().height()
            qp.drawText(QPointF(x,y+fh/4), "n-{:d}".format(level))
            
        
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
        
        #scale the font to the radius
        mFont = QFont('serif', round((r*0.9 if len(self.elements)>1 else 1.8*r) *.6)) #QFont('serif', 5)
        
        painter.setPen(Qt.black)
        painter.setFont(mFont)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        def putText(qp,x,y,text):
            qp.setPen(QColor(0,0,0))
            metrics = qp.fontMetrics()
            fw,fh = metrics.width(text),metrics.height()
            qp.drawText(QPointF(x-fw/2,y+fh/4),text)
        
        
        
        pen = QPen(QColor(10,10,10), 1, Qt.SolidLine)
        
        for other in self.connections:
            
            weight = 0.2 + 3*other.getLevelContext() + 2*self.getLevelContext()
#             weight=1
            
            xT,yT = self.bottomConnectorPos()
            xB,yB = other.topConnectorPos()
            painter.setPen(QPen(Qt.black, weight))
            painter.drawLine(QPointF(xT,yT),QPointF(xB,yB))
        
        
        for index,element in enumerate(self.elements):
            painter.setBrush(QColor(element.__class__.color))
            painter.setPen(QColor(80,80,80))
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
        painter.setRenderHint(QPainter.Antialiasing, False)

if __name__ == "__main__":
    main()

from numpy import *
from matplotlib import pyplot as plt
from collections import defaultdict
import weakref
from PySide.QtGui import *
from PySide.QtCore import *
import sys
import warnings


class OneLineWidget(QWidget):
    
    def __init__(self, shape):
        
    
        super(self.__class__,self).__init__()
        x,y,w,h = shape
        
        self.move(x,y)
        self.resize(w,h)
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(*shape)
        
        
        self.view = QGraphicsView(self.scene)
        
        self.view.setGeometry(300,300,900,900)
        
        self.view.setCacheMode(QGraphicsView.CacheBackground)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        
        layout = QHBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.elements = []
        
        self.show()
    
    def addElement(self, element):
        self.elements += [element]
        self.scene.addItem(element)
        element.show()

class OneLineScene(QGraphicsScene):
    def __init__(self, shape):
        super(self.__class__,self).__init__()
        
        

        
        self.elements = []
    
    def addElement(self, element):
        self.elements += [element]
        self.addItem(element)
        element.setGraph(self)
        element.show()

class OneLine(QGraphicsView):
    def __init__(self, shape):
        super(self.__class__,self).__init__()
        
        x,y,w,h = shape
        
        self.move(x,y)
        self.resize(w,h)
        
#         self.setGeometry(*shape)
        scene = QGraphicsScene(self)
        scene.setSceneRect(10,10,shape[2]-20, shape[3]-20)
        self.setScene(scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
#         self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        
        self.elements = [Element]
        
        
#         self.show()
    
    def addElement(self, element):
        self.elements += [element]
        self.scene().addItem(element)
        element.setGraph(self)
        element.show()
        
    
class Element(QGraphicsItem,object ):
    color = '#F0F0F0'
    weight = 10
    geo = defaultdict(None)
    hColor= {False: Qt.darkGray, True: Qt.darkRed}
    
    def __init__(self,id, pos):
        super(Element, self).__init__()
        self.id=id
        self.pos = pos
        
        #
#         if oneline != None:
#             self.graph = weakref.ref(oneline)
        
        self.newPos = QPointF()
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setZValue(-1)
        self.highlight = False
    
    
    def __repr__(self): return self.__class__.__name__ + " %04d" % self.id
    def __eq__(self, other): 
        return True if self.__class__.__name__ == other.__class__.__name__ and self.id == other.id else False
    
    def __cmp__(self, other):
        if self.__class__.__name__ < other.__class__.__name__: return -1
        elif self.__class__.__name__ > other.__class__.__name__: return 1        
        else: return self.id - other.id
    
    def __hash__(self): return hash(str(self))
    
    def getGeo(self): return Element.geo[self.__class__][self.id]
    def getPos(self): return self.pos
    def secondary(self): return self.getGeo()
    
    def addFault(self,fault):
        try: self.faults += [fault]
        except AttributeError: self.faults = [fault]
            
    def boundingRect(self): return QRectF(* list(array(self.getPos())-Element.weight) + [2*Element.weight]*2)

    
    def fitIn(self, newBox, oldBox):
        #the default fitIn behaviour is to scale whatever comes from self.getPos()
        point = self.getPos()
        point = self.scalePoint(point, newBox, oldBox)
        self.pos = point
        
    def scalePoint(self, point, newBox, oldBox):
        #scale point in 'oldBox' to fit in box (x0,y0,xn,yn)
        x0,y0,xn,yn = newBox
        width,height = xn-x0,yn-y0
        
        
        widthL = oldBox[2]-oldBox[0]
        heightL = oldBox[3]-oldBox[1]
        xL,yL = oldBox[0],oldBox[1]
        def scale(x,y):
            x = x0 + width *  (x-xL)/widthL
            y = y0 + height * (y-yL)/heightL
            return [x,y]
        
        return scale(*point)

    
    #
    def shape(self):
        path = QPainterPath()
        
        pos = self.getPos()
        radius = self.__class__.weight
        path.moveTo(QPointF(*pos))
        path.addEllipse( QRectF(pos[0]-radius, pos[1]-radius, 2*radius, 2*radius))
        return path
    
    def paint(self, painter, option, widget):
        mColor = Element.hColor[self.highlight]
        painter.setPen(mColor)
        painter.setBrush(mColor)
        painter.drawPath(self.shape())
    
    def mousePressEvent(self, event):
        self.highlight = not self.highlight
        print(self.highlight)
        print(str(self))
        self.update(self.boundingRect())
    
    def toggleHighlight(self):
        self.highlight = not self.highlight
        self.update(self.boundingRect())
        
    def setGraph(self,graph):
        self.graph = weakref.ref(graph)

class Branch(Element):
    color = '#DB0058'
    radius = 1
    def __init__(self,id,line):
        self.line = line
        super(self.__class__, self).__init__(id, [None,None])
        
    def secondary(self):
        return Line(self.pos).getPosition()
    
    def boundingRect(self):
        x,y = array(self.line).transpose()
        return QRectF(min(x), min(y), max(x)-min(x), max(y)-min(y))
    
    def fitIn(self, newBox, oldBox):
        points = self.line
        self.line = [self.scalePoint(point, newBox, oldBox) for point in points]
    
    
    def shape(self):
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        
        radius =  Branch.radius
        rotation = array( [[0,-1],[1,0]])
        
        points = zip(self.line[0:-1], self.line[1:])
        
        for p0, pn in points:
            (x0,y0),(xn,yn) = p0,pn
            dx,dy = array(pn) - array(p0)
            
            dV = array([dx,dy])
            mag_dV = linalg.norm(dV)
            
            v = dot(rotation, dV) * radius / mag_dV
            startAngle = arctan2(*v) * 180/pi + 90
            
            path.moveTo(QPointF(*p0-v))
            
            #starting arc
            path.addEllipse(x0-radius, y0-radius,2*radius,2*radius)
            #rectangular part
            
            path.lineTo(QPointF(*p0-v))
            path.lineTo(QPointF(*pn-v))
            path.lineTo(QPointF(*pn+v))
            path.lineTo(QPointF(*p0+v))
        
        path.moveTo(QPointF(*pn+v))
        path.addEllipse(QRectF(xn-radius, yn-radius, 2*radius, 2*radius))
        
        return path.simplified()
        
class Bus(Element): 
    color = '#408Ad2'
    
    w,h = 70,5
    def shape(self):
        x,y = self.getPos()
        path = QPainterPath()
        path.moveTo(x,y)
        path.addRect(QRectF(x-Bus.w/2, y-Bus.h/2, Bus.w, Bus.h))
        return path

class Gen(Element):
    color = '#FF9700'
    def __init__(self, id, bus):
        super(self.__class__, self).__init__(id, [None,None])
        self.bus = bus
    
    def getPos(self):
        return self.bus.getPos()

class Transformer(Element):
    color = '#80E800'
    
    def __init__(self, *args):
        self.id = id
        self.elements = args[1]
        args = (args[0], [None, None])
        super(self.__class__, self).__init__(*args)
    
    def getPos(self):
        pos = [el.getPos() for el in self.elements]
        return mean(a,0)
    
    def boundingRect(self):
        rects = [list(el.boundingRect().getRect()) for el in self.elements]
        
        x0,y0,xn,yn = transpose([ rect[0:2] + [rect[0]+rect[2], rect[1]+rect[3]] for rect in rects])
        return QRectF( min(x0), min(y0), max(xn), max(yn))
    
    def fitIn(self, *args):
        pass
    
class Fault(object):
    levelContext = defaultdict(list)
    globalContext = defaultdict(list)
    cumulativeContext = defaultdict(list)
    
    def __init__(self,listing, reduction = None):
        #listing is a dictionary containing: label, elements
        self.reduction = reduction
        self.label = listing['label'] if 'label' in listing else 'none'
        if 'label' in listing: del listing['label']
        
        self.elements = listing['elements']
        self.connections = []
        self.elements.sort(key=hash)
        for element in self.elements:
            element.addFault(self)
        
    

    def isParentOf(self, other):
        #return true if contains same elements as 'other' plus extras
        nSelf, nOther = len(self.elements), len(other.elements)
        
        #only a direct child if there is one more element
        if nOther != nSelf + 1: return false
        
        s,o= 0,0
        matches = 0;
        nomatch = 0;
        while matches < nSelf:
            if s >= nSelf or o >= nOther: #if we passed the end of either array but not all in self.elements are matched
                return False
                
            if self.elements[s] == other.elements[o]:
                #increment matches count and move forward in both lists
                matches += 1
                s+=1
                o+=1
            else:
                #increment nomatch count and move forward only in child list
                nomatch+=1
                o+=1
            
            if nomatch > 2: #if we count more than 1 nomatch it can't be a direct child
                return False
        
        #if matches == nSelf, all in self.elements are matched and loop stops. is parent.
        return True
        
            
        
    def __repr__(self):
        return 'Fault ({})'.format(repr(self.elements))
    def __str__(self):
        return repr(self)
    
    @staticmethod
    def setGlobalContext(floor, ceiling):
        Fault.globalContext = {'floor': floor, 'ceiling':ceiling}
    
    @staticmethod
    def setLevelContext(level, floor, ceiling):
        Fault.levelContext[level] = {'floor':floor, 'ceiling':ceiling}
    
    @staticmethod
    def setCumulativeContext(level,floor,ceiling):
        Fault.cumulativeContext[level] = {'floor': floor, 'ceiling': ceiling}
    
    def getGlobalContext(self):
        try:
            min = self.globalContext['floor']
            max = self.globalContext['ceiling']
            return (self.value() - min) / (max-min) if (max-min) > 0 else 0
        except: return 0
    
    def getLevelContext(self):
        try:
            min = self.levelContext[len(self.elements)]['floor']
            max = self.levelContext[len(self.elements)]['ceiling']
            return (self.value() - min) / (max-min) if (max-min) > 0 else 0
        except: return 0
    
    def getCumulativeContext(self):
        try:
            min = self.cumulativeContext[len(self.elements)]['floor']
            max = self.cumulativeContext[len(self.elements)]['ceiling']
            return (self.subTreeValue() - min) / (max-min) if (max-min) > 0 else 0
        except: return 0
            
    def value(self):
        return self.reduction
    
    def subTreeValue(self): return self.value() + sum([subFault.subTreeValue() for subFault in self.connections])
    
    def getElements(self):
        return self.elements
    
    def addConnection(self,connection):
        self.connections += [connection]
        
    def strip(self, stripElement):
        self.elements, strip = [el for el in self.elements if el != stripElement], [el for el in self.elements if el == stripElement]
        return strip
    
    def subFault(self, element):
        from copy import copy
        newFault = copy(self)
        strip = newFault.strip(element)
        newFault.siblings += strip
        return newFault

class Line:
    def __init__(self, myNodes):
        self.nodesX = myNodes[0]
        self.nodesY = myNodes[1]
    
    def draw(self,axes, color="#0000FF"):
        for index in range(0, len(self.nodesX)-1):
            axes.plot( self.nodesX[index:index+2], self.nodesY[index:index+2], c=color)
    
    def getLength(self):
        sum = 0;
        for index in range(0,len(self.nodesX)-1):
            sum += sqrt(  (self.nodesX[index+1]-self.nodesX[index])**2 + (self.nodesY[index+1]-self.nodesY[index])**2)
        return sum
    
    def getMidpoint(self):
        
        if not hasattr(self, 'midPoint'):
            #get distance between each point
            deltaDistances = lambda array: [b-a for a,b in zip(array[0:-1],array[1:])]
            
            dxs,dys = deltaDistances(self.nodesX), deltaDistances(self.nodesY)
            
            
            distances = [0] + [ sqrt(dx**2 + dy**2) for dx,dy in zip(dxs, dys)]  
            
            length = sum(distances);
            
            cumDistances = cumsum(distances)
            
            #max index of distances s.t. cumsum <= half total length
            ltHalves = [index for index,value in enumerate(cumDistances) if value <= length/2]
            lt_half = max(ltHalves)
            
            percentAlong = (length/2 - cumDistances[lt_half])/ distances[lt_half+1]
            
            lineBisect = lambda array: array[0] + percentAlong * (array[1]-array[0])
            xM,yM = lineBisect(self.nodesX[lt_half:lt_half+2]), lineBisect(self.nodesY[lt_half:lt_half+2])
            
            self.midPoint = xM,yM
        
        return self.midPoint
    
    def getPosition(self):
        return self.getMidpoint()


def flatten(l, ltypes=(list, tuple)):
    # method to flatten an arbitrarily deep nested list into a flat list
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)
    


def main():
    pass
#     
#     app = QApplication(sys.argv)
#     
#     ex = OneLineWidget([0,0,900,900])
#     ex.addElement(Element(1,[100,100]))
#     sys.exit(app.exec_())


    
if __name__ == "__main__":
    main()
import numpy as np
from matplotlib import pyplot as plt
from collections import defaultdict
import weakref
from PySide.QtGui import *
from PySide.QtCore import *



class OneLine(QGraphicsView):
    def __init__(self, shape):
        super(self.__class__,self).__init__()
        
        
        self.setGeometry(*shape)
        scene = QGraphicsScene(self)
        scene.setSceneRect(10,10,shape[2]-20, shape[3]-20)
        self.setScene(scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AncherViewCenter)
        
        self.elements = [Element]
    
    def addElement(self, element):
        self.elements += [element]
        self.scene().addItem(element)
        item.setGraph(self)
        item.show()
        
    
class Element(QGraphicsItem,object ):
    color = '#F0F0F0'
    weight = 10
    geo = defaultdict(None)
    
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
    
    
    def __repr__(self):
        return self.__class__.__name__ + " %04d" % self.id
    
    def __eq__(self, other):
        return True if self.__class__.__name__ == other.__class__.__name__ and self.id == other.id else False
    
    def __hash__(self):
        #has the string representation of the element, eg 'bus 01'
        return hash(str(self))
    
    def getGeo(self):
        return Element.geo[self.__class__][self.id]
    
    def getPos(self):
        return self.pos
    def secondary(self):
        geo = self.getGeo()
        return geo
    
    def boundingRect(self):
        try:
            return QRectF(* list(np.array(self.getPos())-Element.weight) + [2*Element.weight]*2)
        except:
            import pdb; pdb.set_trace()
            print '1'
    
    def fitIn(self, newBox, oldBox):
        #the default fitIn behaviour is to scale whatever comes from self.getPos()
        point = self.getPos()
        self.scalePoint(point, box, oldBox)
        
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
        
        radius = self.__class__.weight
        path.moveTo(QPointF(*self.pos))
        path.addEllipse( QRectF(self.pos[0]-radius, self.pos[1]-radius, 2*radius, 2*radius))
        return path
    
    def paint(self, painter, option, widget):
        painter.setPen(Qt.darkGray)
        painter.setBrush(Qt.darkGray)
        painter.drawPath(self.shape())
    
    def mousePressEvent(self, event):
        print str(self)
        
    def setGraph(self,graph):
        self.graph = weakref.ref(graph)

class Branch(Element):
    color = '#DB0058'
    
    def __init__(self,id,line):
        self.line = line
        super(self.__class__, self).__init__(id, [None,None])
        
    def secondary(self):
        return Line(self.pos).getPosition()
    
    def boundingRect(self):
        x,y = np.array(self.line).transpose()
        return QRectF(min(x), min(y), max(x)-min(x), max(y)-min(y))
    
    def fitIn(self, newBox, oldBox):
        points = self.line
        self.line = [self.scalePoint(point, newBox, oldBox) for point in points]
        
class Bus(Element): 
    color = '#408Ad2'

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
        rects = [el.boundingRect() for el in self.elements]
        x0,y0,xn,yn = transpose([ rect[0:2] + [rect[0]+rect[2], rect[1]+rect[3]] for rect in rects])
        return QRectF( min(x0), min(y0), max(xn), max(yn))
    
    def fitIn(self, *args):
        pass
    
class Fault(object):
    
    def __init__(self,listing, reduction = None):
        #listing is a dictionary containing: label, elements
        self.reduction = reduction
        self.label = listing['label'] if 'label' in listing else 'none'
        if 'label' in listing: del listing['label']
        
        self.elements = listing['elements']
        self.connections = []
        
    
    
    def __repr__(self):
        return 'Fault ({})'.format(repr(self.elements))
    def __str__(self):
#         def typeIds(mType): return [el.id for el in self.elements if el.__class__.__name__ == mType]
#         branch, bus, gen = [typeIds(mType) for mType in [Element.Branch, Element.Bus, Element.Gen]]
#         string = '\t\t'.join([self.label, 'CPF: %.3f' % self.reduction, 'elements:', str(branch), str(bus), str(gen)])
#         string = '\n%s' % string
#         
#         return string
        return repr(self)
    
    
    def value(self):
        return self.reduction
    
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
            sum += np.sqrt(  (self.nodesX[index+1]-self.nodesX[index])**2 + (self.nodesY[index+1]-self.nodesY[index])**2)
        return sum
    
    def getMidpoint(self):
        
        if not hasattr(self, 'midPoint'):
            #get distance between each point
            deltaDistances = lambda array: [b-a for a,b in zip(array[0:-1],array[1:])]
            
            dxs,dys = deltaDistances(self.nodesX), deltaDistances(self.nodesY)
            
            
            distances = [0] + [ np.sqrt(dx**2 + dy**2) for dx,dy in zip(dxs, dys)]  
            
            length = np.sum(distances);
            
            cumDistances = np.cumsum(distances)
            
            #max index of distances s.t. cumsum <= half total length
            ltHalves = [index for index,value in enumerate(cumDistances) if value <= length/2]
            lt_half = np.max(ltHalves)
            
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
    
    X = [1,2,2+1/np.sqrt(2)]
    Y = [4,5,5+1/np.sqrt(2)]
    
    a = Line(np.array([ X,Y]))
    
    x,y = a.getPosition()
    
    
    plt.scatter(X,Y);
    
    plt.scatter(x,y,c="#00FF00")
    plt.show()


    
if __name__ == "__main__":
    main()
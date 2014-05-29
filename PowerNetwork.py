from numpy import *
from matplotlib import pyplot as plt
from collections import defaultdict
import weakref


import DistanceCalculations as DC
from PySide.QtGui import *
from PySide.QtCore import *
import sys
import warnings



## test

""" The simple test for PowerNetwork is to buid a one-line diagram from a case.
    Further testing should include testing distance calculations and other
    aspects of the code """


def main():
    
    from PowerNetwork import Bus, Branch
    from VisBuilder import CPFfile
    from DetailsWidget import DetailsWidget
    
    
    mCPFfile = CPFfile('cpfResults_case30_1level') #open a default cpf file
    mElements = mCPFfile.Branches + mCPFfile.Buses
    
    
    
    
    app = QApplication(sys.argv)
    
    mDetails = DetailsWidget()
    mOneline = OneLineWidget(mElements,shape = [0,0,900,700], details = mDetails)
    mVis = Vis(oneline =mOneline, details = mDetails)
    sys.exit(app.exec_())
    
    
    
    
    
    
    


## code


def boundingRect(elList):
    bounds = array([list(el.boundingRect().getCoords()) for el in elList])
    boundingRect = [min(bounds[:,0]), min(bounds[:,1]), max(bounds[:,2]), max(bounds[:,3])]
        
    return boundingRect
    



class Vis(QMainWindow):
    
    def __init__(self, oneline = None, details = None):
        super().__init__()
        
        self.oneline = oneline
        
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        
        
        
        oneline.setParent(self.widget)
        
        layout = QGridLayout()
        
        
        self.widget.setLayout(layout)
        
#         layout.addLayout(self.widget)
        
        layout.setSpacing(0)
        layout.addWidget(details,1,0,3,1)
        layout.addWidget(oneline,4,0,1,1)
        
        
        
        
        
        
        self.setGeometry(20,20,900,900)
        self.setWindowTitle('Visualize')
        
        self.show()
        
        
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)

    
        
#         log('visualization created')


class OneLineWidget(QGraphicsView):
    """ A widget in which a oneline is drawn. contains a graphics scene """
    
    def __init__(self, elList, shape=None,details = None):
        QGraphicsView.__init__(self)
        
        if shape:
            x,y,w,h =  shape
            self.move(x,y)
            self.resize(w,h)
        
        diagramBound = boundingRect(elList)
        
        self.details = details
        #build a graphicsscene
        self.scene =  QGraphicsScene(self)
        
        if diagramBound:
            xa,ya,w_,h_ = diagramBound
            xa, ya, w_,h_ = round(xa-40), round(ya-40),round(w_ + 40 ),round(h_+40)
            self.setSceneRect(xa,ya,w_,h_)
            scale = min([w/w_, h/h_]) * 0.99
        else:
            self.setSceneRect(*shape)
            scale = 1
        
        self.setScene(self.scene)
        
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        
        self.elements = []
        
        
        self.addElement(elList)
        self.scale(scale,scale)
        self.setWindowTitle('Oneline')
#         self.show()
    
    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, event.delta()/240.0))
    
    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)
        
    def addElement(self, element):
        
        try:
            if type(element) is dict: element = element.values()
        
            for el in element :
                self.addElement(el)
        except TypeError:
            self.elements += [element]
            self.scene.addItem(element)
        
        self.show()

        
    
class Element(QGraphicsItem,object ):
    """ Object representing single grid elements, with child types such as 
        branch, bus, generator and transformer. Has methods for comparing
        elements for equality, storing position information, as well as
        implements the necessary functions to be drawn in a one-line diagram."""
        
        
    color = '#F0F0F0'
    
    weight = 10
    geo = defaultdict(None)
    hColor= {False: Qt.darkGray, True: Qt.darkRed}
    
    hColor = {False: QColor("#b2b8c8"), True: QColor("#e45353")}
#     hColor = {False: QColor("#b6cdc1"), True: QColor("#e45353")}
    
    def __init__(self,id, pos, connected=None):
        super(Element, self).__init__()
        self.id=id
        self.pos = pos
        self.faults = []
        
        if connected: self.connected = list(connected)
            #self.connected will always be a list.
        else:
            self.connected = []
        
        self.setAcceptHoverEvents(True)
        self.newPos = QPointF()
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setZValue(-1)
        self.highlight = False
    
    def html_name(self):
        return "<p>{}</p>{}".format(self.__class__.__name__, self.id)
        
    def html_connected(self):
        elList = "<ul>{}</ul>".format( "".join([ "<li>{}</li>".format(el.html_name()) for el in self.connected]))
        return "<div class='info'><p>Connections:</p>{}</div>".format(elList)
        
        
    def html_percentage(self):
        return "<div class='info'><p>Pct. Loadability:</p>{:.3f}%</div>".format(-1)
        
        

    
    def html(self):
        return "<div class='el'><h>{}</h>{}{}</div>".format( str(self), self.html_connected(), self.html_percentage())
        
    def setDetails(self):
        if self.scene().parent().details:
            self.scene().parent().details.setContent(self.html())
    def __repr__(self): 
        string = "{:6s} {:04d}".format(self.__class__.__name__ ,self.id)
        return string
    
    def shortRepr(self): 
#         return "{:.2s}{:d}".format(self.__class__.__name__, self.id)
        return str(self.id)
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
        try: self.faults.append(fault)
        except AttributeError: self.faults = [fault]
            
    def boundingRect(self):
#          return QRectF(* list(array(self.getPos())-Element.weight) + [2*Element.weight]*2)
        pos = self.getPos()
        return QRectF([pos[0],pos[1],0,0])
    
    
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
        try:
            return self.mShape
        except:
            self.mShape = self.defineShape()
            return self.mShape
        
    def defineShape(self):
        path = QPainterPath()
        
        pos = self.getPos()
        radius = self.__class__.weight
        path.moveTo(QPointF(*pos))
        path.addEllipse( QRectF(pos[0]-radius, pos[1]-radius, 2*radius, 2*radius))
        return path
        
    def paint(self, painter, option, widget):
        mColor = Element.hColor[self.highlight] # or self.isUnderMouse()]
        painter.setPen(mColor)
        painter.setBrush(mColor)
        painter.drawPath(self.shape())
        
        
    def hoverEnterEvent(self, event):
        self.update(self.boundingRect())
    
    def hoverLeaveEvent(self,event):
        self.update(self.boundingRect())
        
    def mousePressEvent(self, event):
        print(str(self))
        self.toggleHighlight()
        
        for fault in self.faults: fault.toggleHighlight()
        
        
        self.setDetails()
        
    
    def toggleHighlight(self):
        self.highlight = not self.highlight
        self.update(self.boundingRect())
    
    def setHighlight(self, set = False):
        if self.highlight != set:
            self.toggleHighlight()
        
    def setGraph(self,graph):
        self.graph = weakref.ref(graph)
    
    def distanceFrom(self, other):
        return sqrt(self.getPos()**2 + other.getPos()**2)

class Branch(Element):
    color = '#DB0058'
    radius = 1
    
    def __init__(self,id, pos, buses=None):
        
        super().__init__(id,pos, buses)
#         self.connected = list(buses) #call list to ensure iterable
        
        #assign self to buses
        if buses:
            for bus in buses: bus.connected.append(self)
                
        
    def boundingRect(self):
        x,y = array(self.pos).transpose()
        return QRectF(min(x), min(y), max(x)-min(x), max(y)-min(y))
    
    def fitIn(self, newBox, oldBox):
        points = self.pos
        self.pos = [self.scalePoint(point, newBox, oldBox) for point in points]
    
    
    def defineShape(self):
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        
        radius =  Branch.radius
        rotation = array( [[0,-1],[1,0]])
        
        points = zip(self.pos[0:-1], self.pos[1:])
        
        for p0, pn in points:
            (x0,y0),(xn,yn) = p0,pn
            dx,dy = array(pn) - array(p0)
            
            dV = array([dx,dy])
            mag_dV = linalg.norm(dV)
            
            if mag_dV == 0:
                break;
           
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
    
    def distanceFrom(self,other):
        if type(other) is Transformer: #if transformer, return the smallest distance from all elements in the transformer.
            return other.distanceFrom(self)
        elif type(other) is Branch: #if the other is a line, 
            return DC.lineToLine(self.pos, other.pos)[0]
        else:
            return DC.pointToLine(self.pos, other.getPos())[0]
        
        
class Bus(Element): 
    color = '#408Ad2'
    
    w,h = 16,5
    def defineShape(self):
        x,y = self.getPos()
        path = QPainterPath()
        path.moveTo(x,y)
        path.addRect(QRectF(x-Bus.w/2, y-Bus.h/2, Bus.w, Bus.h))
        return path
    
    def boundingRect(self):
        x,y = self.getPos()
        return QRectF(*[x-Bus.w/2, y-Bus.h/2, Bus.w,Bus.h])
    
    def distanceFrom(self, other):
        if type(other) is not type(self):
            return other.distanceFrom(self)
        else: 
            return DC.pointToPoint(self.getPos(), other.getPos())
        

class Gen(Element):
    color = '#FF9700'
    def __init__(self, id, bus):
        super().__init__(id, [None,None],[bus])
#         self.bus = bus
#         self.connected = [bus] 

    @property
    def bus(self):
        return self.connected[0]
    
    
    
    def getPos(self):
        return self.connected[0].getPos()
    
    def boundingRect(self):
        return self.connected[0].boundingRect()
        
    def distanceFrom(self, other):
        return other.distanceFrom(self.connected[0])

class Transformer(Element):
    color = '#80E800'
    
    def __init__(self, id, elements):
        super().__init__(id,[], elements)
    
#     def __init__(self, id, elements):
# #         self.elements = elements
#         super().__init__(id, [None,None])
    
#     @property
#     def connected(self):
#         return self.elements
#     
#     @connected.setter
#     def connected(self):
#         pass
    
    def getPos(self):
        pos = []
        for el in self.connected:
            if type(el) is Branch:
                pos += el.getPos()
            else:
                pos.append(el.getPos())
                
# #         pos = [el.getPos() for el in self.elements]
        return pos
#         return mean(pos,0)
    
    def toggleHighlight(self):
        for el in self.connected:
            el.toggleHighlight()
    
    def boundingRect(self):
        rects = array([list(el.boundingRect().getRect()) for el in self.connected])
        points = [rects[:,0].transpose(), rects[:,1].transpose(), rects[:,0]+rects[:,2], rects[:,1] + rects[:,3]]
        
        x0,y0,xn,yn = min(points[0]), min(points[1]), max(points[2]), max(points[3])
        return QRectF( x0,y0, xn-x0, yn-y0)
    
    def fitIn(self, *args):
        pass
    
    def distanceFrom(self,other):
        if type(other) == type(self):
            distances = []
            for EL in self.connected:
                for el in other.connected:
                    distances.append(EL.distanceFrom(el))
            return min(distances)
        else:
            return min([el.distanceFrom(other) for el in self.connected])
            
    
class Fault(object):
    """ Object represents a system fault from a power system perspective.
        Includes information about elements involved as well as any child faults
        [these must be specified using .addConnection()]. Does not implement any
        UI related methods for including in a Treemap or Treemap/Oneline combo
        
        """
    
    levelContext = defaultdict(list)
    globalContext = defaultdict(list)
    cumulativeContext = defaultdict(list)
    
    def __init__(self,listing, reduction = None):
        #listing is a dictionary containing: label, elements
        
        self.value = reduction
        self._subValue = None
        
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
            
#     def value(self):
#         return self.reduction

    @property
    def secondary(self):
        try:
            return self._secondary
        except:
            
            if len(self.elements) == 1:
                self._secondary = None
            else:
                import itertools
                distances = [ elA.distanceFrom(elB) for elA, elB in itertools.combinations(self.elements,2)]
                self._secondary = mean(distances)
            
            return self._secondary

    @secondary.setter
    def secondary(self,x):
        self._secondary = x
        
    @property
    def subValue(self): 
        return self._subValue or self.value + sum([subFault.subValue for subFault in self.connections])
    
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
        
    def html_elements(self):
        elList = "<ul>{}</ul>".format( "".join([ "<li>{}</li>".format(el.html_name()) for el in self.elements]))
        return "<div class='info'><p>Elements:</p>{}</div>".format(elList)
    def html_reduction(self):
        return "<div class='info'><p>Reduction:</p>{:.3f}MW</div>".format(self.value)
    def html(self):
        return "<div class='el'><h>Fault</h>{}{}</div>".format(self.html_elements(), self.html_reduction())
    
    

class Line:
    """
    Construct for getting basic properties of a multi-segment branch/line
    geometry. May be obsolete.
    """
    def __init__(self, myNodes):
        self.nodesX = myNodes[0]
        self.nodesY = myNodes[1]
        
    def __str__(self):
        return 'Line object'
    
    def __repr__(self):
        return '<PowerNetwork.Line ['+ ', '.join([ '({0:.1f},{1:.1f})'.format(x,y) for x,y in zip(self.nodesX, self.nodesY)]) +'] object>'
    
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
            branch_geo =array([self.nodesX,self.nodesY]).transpose() 
            
            #get distance between each point
            distances = [0] + list( sqrt(sum(square(branch_geo[1:,:] - branch_geo[0:-1,:])),1)) 
            
            ltHalf = where(distances < sum(distances)/2)[0][-1] 
                #index the tuple returned by where, then take the last index for which the condition is still true

            percentAlong = (sum(distances)/2 - cumsum(distances)[lt_half])/ distances[lt_half+1]
            
            xM,yM = branch_geo[ltHalf,:] + percentAlong * ( branch_geo[ltHalf+1] - branch_geo[ltHalf])
            
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
    





    
if __name__ == "__main__":
    main()
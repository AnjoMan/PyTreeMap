import scipy.io
import numpy as np
import Tkinter as Tk
# from mlabwrap import mlab
import colorsys
from collections import defaultdict
from PowerNetwork import *
from Treemap import layout
from FaultTreemap import *
from sets import Set
import sys


def compare(parentValue, childValue):
    x1,y1 = parentValue
    x2,y2 = childValue
    return np.sqrt( (x1-x2)**2 + (y1-y2)**2)
#     return np.random.rand()





def main():
    #sample usage generator
    myTreemap = Treemap();
    myTreemap.setChildren();
    
    for child in myTreemap.children:
        child.setChildren(values=np.random.rand(5))
        
        for subChild in child.children:
            subChild.setChildren(values = np.random.rand(8))
    
    myTreemap.draw()




   
#load cpf results from matlab file
cpfResults = scipy.io.loadmat('cpfResults', struct_as_record=False)


#get loading, reductions, and corresponding faults    
baseLoad = cpfResults['baseLoad'][0,0]
CPF_reductions = baseLoad- cpfResults['CPFloads'][0];
CPFbranches = cpfResults['branchFaults'][0]
base = cpfResults['base'][0,0]





#convert fault listings into simple lists instead of scipy matlab structures
def collapse(listing):
    branch, bus, gen, trans = [list(el[0]) if len(el) == 1 else list(el) for el in [listing.branch, listing.bus, listing.gen, listing.trans]]
    relisting = defaultdict(list)
    relisting['label'], relisting[Branch], relisting[Bus], relisting[Gen], relisting[Transformer] =str(listing.label[0]), branch, bus, gen, trans
    return relisting

CPFbranches = [ collapse(listing[0][0]) for listing in CPFbranches]




branchBusEnds = [ [int(el) for el in listing[0:2]] for listing in base.branch]




def getGeo(base):
    def getBranchId(busEnds):
        #find the branch index of a branch from the busses it connects to.
        busEnds = Set(busEnds)
        mIndex = -1
        for index, branch in enumerate(branchBusEnds):
            mBranch = Set(branch)
            intersection = Set.intersection(mBranch, busEnds)
            if len( intersection) > 1: return index
        return mIndex
    
    nBranches = len(base.branch_geo[0])
    nBusses = len(base.bus_geo[0])
    nGens = len(base.gen)
    nTrans = len(base.trans[0])
    #get list of positions
    geo = defaultdict(None);
    geo[Branch] = {int(id): list([list(point) for point in el]) for id,el in zip(range(1, nBranches+1), base.branch_geo[0])}
    geo[Bus] = {int(id): list(el) for id,el in zip( base.bus.transpose()[0],base.bus_geo)}
    genBusses = [int(el) for el in base.gen.transpose()[0]]
    geo[Gen] = {int(id): geo[Bus][busNo] for  id,busNo in zip(range(1, nGens+1),genBusses)}
    
    def getTransPos(trans):
        transPos = []        
        transPos += [ list(Line(geo[Branch][getBranchId(busEnds)]).getMidpoint()) for busEnds in (trans[0][0] if len(trans[0]) > 0 else [])]
        transPos += [ geo[Bus][id] for id in (trans[0][1][0] if len(trans[0][1]) > 0 else [])]
        transPos += [ geo[Bus][id] for id in (trans[0][2][0] if len(trans[0][2]) > 0 else [])]#transformers list the branch by which bus they are connected to, the bus itself, and the gen by which bus it is connected to
        x,y = (np.array(transPos)).transpose()
        return  [np.average(x), np.average(y)]
    
    geo[Transformer] = { id+1: getTransPos(trans) for id, trans in enumerate(base.trans[0])}
    return geo
    #give 'Element' class a list of positions that elements could have

#get geo-points for different elements
Element.setgeo(getGeo(base))

# for trans in base.trans[0]:
#     print len(trans[0])
#     print '\n'


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
    
    def addConnection(self,connection):
        self.connections += [connection]
    
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

#get faults
faults = [ TreeFault(listing, reduction) for listing, reduction in zip(CPFbranches, CPF_reductions) if reduction > 0]

faultTree = defaultdict(list)

for fault in faults:
    faultTree[len(fault.getElements())] += [fault]

print faultTree[0]
del faultTree[0]

from sets import Set

connections = defaultdict(dict)
keys = sorted(faultTree.keys())
for level, nextLevel in zip( keys[0:-1], keys[1:]):
    for fault in faultTree[level]:
        faultEls = Set(fault.elements)
        for subFault in faultTree[nextLevel]:
            if faultEls.issubset(Set(subFault.elements)):
                fault.addConnection(subFault)
        

myFault = TreeFault( {Branch:[1,2,3], Gen:[4], Bus:[8,9], Transformer:[]})
myFault.pos = 30,30


width, height=  1700,800




def drawRows(faultTree, width, height):
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
    

# app = QtGui.QApplication(sys.argv)
# myCanvas = PySideCanvas(width, height, 'Fault Tree')
# myCanvas.drawOutline([0,0,1700,800],1)
# 
# 
# drawRows(faultTree, width, height)
# 
# 
# legend = Legend( [ (mClass.__name__, mClass.color) for mClass in [Branch, Bus, Gen, Transformer]])
# myCanvas.draw(legend)
# sys.exit(app.exec_())


Treemap.compare = compare
myTreemap = buildTreemap(faults)
myTreemap.draw()

# print myTreemap0
# myTreemap.draw()
#     
# if __name__ == "__main__":
#     main()


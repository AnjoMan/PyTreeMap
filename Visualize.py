import scipy.io
import numpy as np
import Tkinter as Tk
# from mlabwrap import mlab
import colorsys
from collections import defaultdict
from PowerNetwork import *
from Treemap import layout
from FaultTreemap import *
from FaultTree import *
from TreemapDraw import *
from sets import Set
import sys


def compare(parentValue, childValue):
    x1,y1 = parentValue
    x2,y2 = childValue
    return np.sqrt( (x1-x2)**2 + (y1-y2)**2)
#     return np.random.rand()



   
#load cpf results from matlab file
cpfResults = scipy.io.loadmat('cpfResults', struct_as_record=False)


#get loading, reductions, and corresponding faults    
baseLoad = cpfResults['baseLoad'][0,0]
CPF_reductions = baseLoad- cpfResults['CPFloads'][0];
CPFbranches = cpfResults['branchFaults'][0]
base = cpfResults['base'][0,0]











branchBusEnds = [ [int(el) for el in listing[0:2]] for listing in base.branch]

nBranches = len(base.branch)
nBusses = len(base.bus)
nGens = len(base.gen)
nTrans = len(base.trans[0])
elements = defaultdict(list)

def getBranchId(busEnds):
    #find the branch index of a branch from the busses it connects to.
    busEnds = Set(busEnds)
    mIndex = -1
    for index, branch in enumerate(branchBusEnds):
        mBranch = Set(branch)
        intersection = Set.intersection(mBranch, busEnds)
        if len( intersection) > 1: return index
    return mIndex

def getGenId(bus):
    #find the id of a generator given the bus it is in
    return 1 + [ int(el) for el in base.gen.transpose()[0]].index(bus)

def getTransEls(trans):
    transEls = []
    #get branches involved
    transEls += [ elements[Branch][getBranchId(listing)] for listing in (trans[0][0] if len(trans[0]) > 0 else [])]
    #get busses involved
#     import pdb; pdb.set_trace()
    transEls += [ elements[Bus][id] for id in (trans[0][1][0] if len(trans[0][1]) > 0 else [])]
     #get gens involved
    transEls += [ elements[Bus][getGenId(bus)] for bus in ( trans[0][2][0] if len(trans[0][2]) > 0 else [])]
    return transEls

def negateY(element):
    element = transpose(array(element))
    element = transpose([list(element[0]), list(element[1]*-1)])
    element = [list(point) for point in element]
    return element

# build elements
busIds, busPos = [int(el) for el in base.bus.transpose()[0]], base.bus_geo
elements[Bus] = {id: Bus(id, pos) for id, pos in  zip(busIds, busPos)} 
# import pdb; pdb.set_trace()

branchPos = [negateY(element) for element in base.branch_geo[0]]
elements[Branch] = {int(id): Branch(id, list ([ list(point) for point in el])) for id, el in zip(range(1,nBranches+1), branchPos)}

genBusses = [int(el) for el in base.gen.transpose()[0]]

elements[Gen] = {int(id): Gen(id, elements[Bus][bus]) for id, bus in zip(range(1,nGens+1), genBusses)}
elements[Transformer] = { int(id): Transformer(id, getTransEls(trans)) for id, trans in zip( range(1,nTrans+1), base.trans[0])}
elList = []
for dict in elements.values():
    elList += dict.values()

#convert fault listings into simple lists instead of scipy matlab structures
def collapse(listing):
    branch, bus, gen, trans = [list(el[0]) if len(el) == 1 else list(el) for el in [listing.branch, listing.bus, listing.gen, listing.trans]]
    
    
    faultEls = [];
    for Type, typelist in zip([Branch, Bus, Gen, Transformer], [branch, bus, gen, trans]):
        faultEls += [elements[Type][id] for id in typelist]
    
    relisting = defaultdict(list)
    relisting['label'], relisting['elements'] = str(listing.label[0]), faultEls
    return relisting

CPFbranches = [ collapse(listing[0][0]) for listing in CPFbranches]



def getFaults(FaultType, CPFbranches, CPF_reductions):
    #get faults
    faults = [ FaultType(listing, reduction) for listing, reduction in zip(CPFbranches, CPF_reductions) if reduction > 0]
    
    faultTree = defaultdict(list)
    
    #sort faults by number of element in each
    for fault in faults:
        faultTree[len(fault.getElements())] += [fault]
    
    print faultTree[0]
    del faultTree[0]
    
    from sets import Set
    
    #identify connections
    connections = defaultdict(list)
    keys = sorted(faultTree.keys())
    for level, nextLevel in zip( keys[0:-1], keys[1:]):
        for fault in faultTree[level]:
            faultEls = Set(fault.elements)
            for subFault in faultTree[nextLevel]:
                if faultEls.issubset(Set(subFault.elements)):
                    fault.addConnection(subFault)
            
    
    return faults, faultTree



width, height=  1700,800






 


class Visualization(QWidget):
    
    def __init__(self, treemap = None, oneline = None):
        super(self.__class__, self).__init__()
        
        
        hbox = QHBoxLayout()
        hbox.addWidget(treemap)
        hbox.addWidget(oneline)
        
        treemap.show()
        self.setLayout(hbox)
        self.setGeometry(100,100,1800,1000)
        self.setWindowTitle('Visualize')
        self.show()


## draw a responsive tree diagram
app = QtGui.QApplication(sys.argv)

(faults, faultTree) = getFaults(TreeMapFault, CPFbranches, CPF_reductions)


# get bounds for elList
rects = [list(el.boundingRect().getRect()) for el in elements[Bus].values() + elements[Branch].values()]
x0,y0,xn,yn = np.transpose([ rect[0:2] + [rect[0]+rect[2], rect[1]+rect[3]] for rect in rects])
bound = [min(x0), min(y0), max(xn), max(yn)]

# [element.fitIn([0,0,880,880], bound) for element in elList]


mOneline = OneLine([100,100,900,900])
[mOneline.addElement(el) for el in elements[Bus].values()]
[mOneline.addElement(el) for el in elements[Branch].values()]



mTreemap = TreemapVis(pos = [50,50,900,900],faultTree=faultTree)

mVis = Visualization( oneline = mOneline, treemap=mTreemap)


sys.exit(app.exec_())

    
    
## draw a  tree diagram
# app = QtGui.QApplication(sys.argv)
# myCanvas = PySideCanvas(width, height, 'Fault Tree')
# myCanvas.drawOutline([0,0,1700,800],1)
# 
# drawRows(myCanvas,faultTree, width, height)
#  
# legend = Legend( [ (mClass.__name__, mClass.color) for mClass in [Branch, Bus, Gen, Transformer]])
# myCanvas.draw(legend)
# sys.exit(app.exec_())

## draw a treemap diagram
# Treemap.compare = compare
# myTreemap = buildTreemap(faults)
# myTreemap.draw()


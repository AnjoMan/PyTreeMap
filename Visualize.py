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
    connections = defaultdict(dict)
    keys = sorted(faultTree.keys())
    for level, nextLevel in zip( keys[0:-1], keys[1:]):
        for fault in faultTree[level]:
            faultEls = Set(fault.elements)
            for subFault in faultTree[nextLevel]:
                if faultEls.issubset(Set(subFault.elements)):
                    fault.addConnection(subFault)
            
    
    return faults, faultTree



width, height=  1700,800



def subTreeValue(fault):
    total=fault.value() + sum([subTreeValue(subFault) for subFault in fault.connections])
    return total

def mBuildTreeMap(mWindow,faultTree,square, level = 3):
    
    def recursive_build(faultList, square, level):

        x0,y0,xn,yn = square
        square = [x0+1,y0+1,xn-1,yn-1]
        if len(faultList) == 0:
            return None
        
        #lay out faults
        rectangles = layout([subTreeValue(fault) for fault in faultList], square)
#         import pdb; pdb.set_trace()
        if len(faultList[0].elements) >= level:
            #lay out faults and add a rectangle widget to each fault
            for fault,rectangle in zip(faultList,rectangles):
                xa,ya,xb,yb = rectangle
                fault.addRectangle(mWindow,[xa,ya, xb-xa, yb-ya])
#                 mWindow.addWidget(fault)
        else:
            for fault, rectangle in zip(faultList, rectangles):
                randomColor(len(fault.elements))
                recursive_build(fault.connections, rectangle, level)
    
    recursive_build(faultTree[1], square, level)
 



## draw a responsive tree diagram
# app = QtGui.QApplication(sys.argv)
# 
# (faults, faultTree) = getFaults(TreeMapFault, CPFbranches, CPF_reductions)
# 
# 
# 
# mWindow = Window()
# mBuildTreeMap(mWindow,faultTree,[10,10,890,890])
#     
    
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


import scipy.io
import numpy as np
# from mlabwrap import mlab
import colorsys
from collections import defaultdict
from PowerNetwork import *
from Treemap import layout
# from FaultTreemap import *
from FaultTree import *
from TreemapDraw import *
import sys
from PySide import QtGui, QtCore


# file = 'cpfResults'
file = 'cpfResults_mid'
# file ='cpfResults_med'
# file = 'cpfResults_case30_full_3_levels'




print("\n\n\n")
def log(string):
    print("\t" + '|| ' + string)


    
import cProfile
pr = cProfile.Profile()



def compare(parentValue, childValue):
    x1,y1 = parentValue
    x2,y2 = childValue
    return np.sqrt( (x1-x2)**2 + (y1-y2)**2)
#     return np.random.rand()






pr.enable()
   
   
   
   
   
   
#load cpf results from matlab file
cpfResults = scipy.io.loadmat(file, struct_as_record=False)


log('.mat file loaded')

#get loading, reductions, and corresponding faults    
baseLoad = cpfResults['baseLoad'][0,0]
loads = cpfResults['CPFloads'][0]
CPF_reductions = baseLoad - loads

CPFbranches = cpfResults['branchFaults'][0]
base = cpfResults['base'][0,0]



branchBusEnds = [ [int(el) for el in listing[0:2]] for listing in base.branch]
nBranches = len(base.branch)
nBusses = len(base.bus)
nGens = len(base.gen)
nTrans = len(base.trans[0])
elements = defaultdict(list)





pr.disable()








def getBranchId(busEnds):
    #find the branch index of a branch from the busses it connects to.
    busEnds = set(busEnds)
    mIndex = -1
    for index, branch in enumerate(branchBusEnds):
        mBranch = set(branch)
        intersection = set.intersection(mBranch, busEnds)
        if len( intersection) > 1: return index
    return mIndex

def getGenId(bus):
    #find the id of a generator given the bus it is in
    try:
        return 1 + [ int(el) for el in base.gen.transpose()[0]].index(bus)
    except ValueError:
        return -1

def defaultIZE(dictionary,default_factory=list):
    newDict = defaultdict(default_factory)
    for k,v in dictionary.items():
        newDict[k]=v
    
    return newDict
    
def getTransEls(trans):
    transEls = []
    #get branches involved
    transEls += [ elements[Branch][getBranchId(listing)] for listing in (trans[0][0] if len(trans[0]) > 0 else [])]
    #get busses involved
#     import pdb; pdb.set_trace()
    mBusses = defaultIZE(elements[Bus])
    transEls += [mBusses[id] for id in (trans[0][1][0] if len(trans[0][1]) > 0 else [])]
     #get gens involved
    
    
    transEls += [ mBusses[getGenId(bus)] for bus in ( trans[0][2][0] if len(trans[0][2]) > 0 else [])]
    transEls = [el for el in transEls if el != []]
    return transEls

def negateY(element):
    element = transpose(array(element))
    element = transpose([list(element[0]), list(element[1]*-1)])
    element = [list(point) for point in element]
    return element


    
# build elements
busIds, busPos = [int(el) for el in base.bus.transpose()[0]], base.bus_geo
elements[Bus] = {id: Bus(id, pos) for id, pos in  zip(busIds, busPos)}

branchPos = [negateY(element) for element in base.branch_geo[0]]
elements[Branch] ={int(id): Branch(id, list ([ list(point) for point in el])) for id, el in zip(range(1,nBranches+1), branchPos)}


genBusses = [int(el) for el in base.gen.transpose()[0]]

elements[Gen] = {int(id): Gen(id, elements[Bus][bus]) for id, bus in zip(range(1,nGens+1), genBusses)}
elements[Transformer] = { int(id): Transformer(id, getTransEls(trans)) for id, trans in zip( range(1,nTrans+1), base.trans[0])}



elList = []
for dict in elements.values():
    elList += dict.values()

log('Grid Elements Created')
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



def getFaults(FaultType, CPFbranches, CPF_loads, baseLoad, filter=0):
    #get faults
    
    faults = [ FaultType(listing, baseLoad-load) for listing, load in zip(CPFbranches, CPF_loads) if (baseLoad-load)/baseLoad > filter]

    log('faults created')
    
    
    faultTree = defaultdict(list)
    #sort faults by number of element in each
    for fault in faults:
        faultTree[len(fault.getElements())] += [fault]
    
    if 0 in faultTree:
        del faultTree[0]
    
    log('faultTree created')
    
    
    
    
    
    #get fault position masks by element    
    maskLength = len(faults)
#     faultByElement = {element: [False]*maskLength for element in elList}
    faultByElement = defaultdict(int)
    for index, fault in enumerate(faults):
        for element in fault.elements:
            faultByElement[element] += 1<<index
    
#     
    def int2bool(i,n): 
        return list((False,True)[i>>j & 1] for j in range(0,n)) 
    
    
#     faultByElement = {key: bool2int(value) for key,value in faultByElement.items()}
    
    #     import pdb; pdb.set_trace()
    log('fault indexes listed per-element')
    
    
    keys = sorted(faultTree.keys())
    keys.reverse()
    
    pr = cProfile.Profile()
    pr.enable()
    
    
#     identify connections
    keys = sorted(faultTree.keys())
    for level, nextLevel in zip( keys[0:-1], keys[1:]):
        print(level)
        for fault in faultTree[level]:
            for subFault in faultTree[nextLevel]:
                if fault.isParentOf(subFault):
                    fault.addConnection(subFault)
#     
#     #identify connections
#     keys = sorted(faultTree.keys())
#     for level in keys[0:-1]:
#         print(level)
#         for fault in faultTree[level]:
#             masks = [faultByElement[element] for element in fault.elements]
#             mask = masks.pop()
#             for el in masks:
#                 mask = mask & el
#             
#             mask  = array(int2bool(mask,maskLength))
#             subFaults = [subFault for subFault in array(faults)[mask] if len(subFault.elements) == 1+ level]
#             for subFault in subFaults:
#                 fault.addConnection(subFault)
            
    pr.disable()

    
    log('connections built')
    #set limits for context getter.
    values = [fault.value() for fault in faults]
    FaultType.setGlobalContext(min(values),  max(values))
    for level, levelFaults in faultTree.items():
        values = [fault.value() for fault in levelFaults]
        FaultType.setLevelContext(level, min(values), max(values))
        
        values = [fault.subTreeValue() for fault in levelFaults]
        FaultType.setCumulativeContext(level, min(values), max(values))

        
    
    log('limits found')
    return faults, faultTree, pr

    p.join()

width, height=  1700,800






 


class Visualization(QMainWindow):
    
    def __init__(self, treemap = None, oneline = None):
        super(self.__class__, self).__init__()
        
        
        self.widget = QWidget()
        
        self.oneline = oneline
        self.treemap = treemap
        
        self.treemap.setParent(self.widget)
        self.oneline.setParent(self.widget)
#         
#         hbox = QHBoxLayout()
#         hbox.addWidget(self.treemap)
#         hbox.addWidget(self.oneline)
#         self.widget.setLayout(hbox)
        
        self.treemap.setGeometry(0,0,900,900)
        self.oneline.setGeometry(900,0,900,900)
        self.setCentralWidget(self.widget)
#         self.setLayout(hbox)
        self.setGeometry(20,20,1800,950)
        self.setWindowTitle('Visualize')
        
#         self.treemap.show()
#         self.oneline.show()
        self.show()
        
        log('visualization created')
    
    
    def createView(self, scene):
        
        view = QGraphicsView(scene)
        
        view.setCacheMode(QGraphicsView.CacheBackground)
        view.setRenderHint(QPainter.Antialiasing)
        view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
#         self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
    
        return view

if __name__ == '__main__':
    
    
    
    ## draw a responsive treemap diagram
    
    
    (faults, faultTree,pr) = getFaults(TreeMapFault, CPFbranches, loads, baseLoad, filter=0)
    pr.print_stats(sort='cumulative')
    
    
    
    # get bounds for elList
    rects = [list(el.boundingRect().getRect()) for el in list(elements[Bus].values()) + list(elements[Branch].values())]
    x0,y0,xn,yn = np.transpose([ rect[0:2] + [rect[0]+rect[2], rect[1]+rect[3]] for rect in rects])
    bound = [min(x0), min(y0), max(xn), max(yn)]
    
    [element.fitIn([0,0,880,880], bound) for element in elList]
    
    
    app = QtGui.QApplication(sys.argv)
    mOneline = OneLineWidget([0,0,900,900])
    [mOneline.addElement(el) for el in elements[Bus].values()]
    [mOneline.addElement(el) for el in elements[Branch].values()]
    mTreemap = None
    mTreemap = TreemapVis(pos = [50,50,900,900],faultTree=faultTree)
    mVis = Visualization( oneline = mOneline, treemap=mTreemap) 
    sys.exit(app.exec_())
    
        
        
    ## draw a  tree diagram
    
    
    
    
#     (faults, faultTree, pr) = getFaults(TreeFault, CPFbranches, loads, baseLoad, filter=0)
#     
#     pr.print_stats(sort='cumulative')
#     # 
#     
#     
#     
#     # values = [fault.getGlobalContext() for fault in faults]
#     
#     
#     # from matplotlib import pyplot
#     # 
#     # mVals = list(loads) + [baseLoad]
#     # pyplot.bar(range(1,len(mVals)+1),mVals)
#     # pyplot.show()
#     
#     
#     
#     
#     app = QtGui.QApplication(sys.argv)
#     mTreeVis = TreeVis(faultTree=faultTree, pos=[10,10,1800,1000])
#     sys.exit(app.exec_())
#     

##


    pr.print_stats(sort='cumulative')

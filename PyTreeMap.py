import scipy.io
import numpy as np
import Tkinter as Tk
from mlabwrap import mlab
import colorsys
from collections import defaultdict
from PowerNetwork import Line


class Treemap:
    
    compareSecondary = None;
    
    def __init__(self, value=1, parent=None, secondary = None):
        self.value, self.parent,  self.secondary,self.children, = value, parent, secondary, []

        try: self.level = parent + 1
        except: self.level = 0 #error if parent does not implement __add__()
    
    def __add__(self, other): #use this to get the level of a Treemap and increment it
        return self.level + other;
    
    def __radd__(self,other):
        self.__add__(other)
        
    def __str__(self):
        string = " | "*self.level + "Treemap node, value = " + ("%8.2f" % self.value)
        string += ", subvalue = " + str(self.secondary) if self.secondary != None else ""
        string += ", level: " + str(self.level) + "; " 
        string += ("%d sub-nodes" % len(self.children)) if len(self.children)>0 else ""
        
        for child in self.children:
            string += "\n" + child.__str__()
        
        return string
    
    def hasChildren(self):
        return len(self.children) > 0
        
    def setChildren(self,values=np.random.rand(20)):
        self.children = [Treemap(value, level=self.level+1) for value in values]
    
    def addChild(self, value=np.random.rand(), secondary=None):
        self.children += [Treemap(value, parent=self, secondary=secondary)]
        return self.children[-1]
    
    def append(self, child=None):
        if child == None:
            child=Treemap(value=np.random.rand(), level = self.level+1)
        
        self.children += [child]
        return self.children[-1]
    
    @staticmethod
    def canvas_drawRectangle(myCanvas, pos, sliver=0, color="#FF0000"):
        x1,y1,xn,yn = pos;
        x1,y1,xn,yn = x1+sliver, y1+sliver,xn-sliver, yn-sliver
        
        #toolbox-specific code to draw a rectangle
        myCanvas.create_rectangle(x1,y1, xn, yn, fill=color, width=0)
    
    
    @staticmethod
    def defineCanvasObject(width,height,border, name="Treemap"):
        #toolbox-specific code to define drawing space
        master = Tk.Tk(); 
        master.title("Fault TreeMap")
        myCanvas = Tk.Canvas(master, width=width, height=height)
        myCanvas.pack()
        return myCanvas
    
    
    
    def randomColor(self, h=None, s=0.3, v=0.7, seed='#998899', secondary_weight = None):
        def clamp(*vals): 
            lst = [max( min( (val, 1) ),0) for val in vals]
            return lst if len(lst) > 1 else lst[0]
        
        #how to convert from decimal h,s,v to "#RRggBB" string
        def rgb(h,s,v): return '#%02X%02X%02X' % tuple( [ int(np.round(el*255)) for el in colorsys.hsv_to_rgb(h,s,v)])
        
        #how to convert from "#RRGGBB string to decimal h,s,v
        def hsv(rgb): return colorsys.rgb_to_hsv(*[ int(el,16)/255.0 for el in (rgb[1:3],rgb[3:5],rgb[5:7]) ])
        
        
        #no color will be drawn for level 0
        if self.level==0:
            return '#998899'
        
        #for level 1, pick a random hue
        elif self.level==1:
        
            if not type(h) == float: 
                h=float(np.random.rand())
            return rgb(h,s,v)
        
        #for levels beyond 1, vary the hue given by seed
        elif self.level > 1:
            h,s,v = hsv(seed)
            h = h + ( np.random.rand() - 0.5 ) *2/10
            s = (secondary_weight)*0.7+0.15 if secondary_weight != None else s + (np.random.rand()-0.5)*2/10
            v = (1-secondary_weight)*0.4+0.3 if secondary_weight != None else s+ (np.random.rand()-0.5)*1/10
            h,s,v = clamp(h,s,v)
            
            return rgb(h,s,v)
    
    def drawOutline(self,myCanvas, pos, borderColor="#000000"):
        x1,y1,xn,yn = pos
        borderWidth= max(0,2-self.level);
        
        #toolbox-specific code to draw outline
        myCanvas.create_rectangle(x1,y1,xn,yn, width = borderWidth, outline = borderColor)
        
    def drawTreeMap(self, myCanvas,pos,sliver=0, secondary_weight=None, colorSeed=None):
        
        color = self.randomColor(seed=colorSeed, secondary_weight = secondary_weight)
        
        if self.hasChildren():
            #draw sub-tree
            values = [treemap.value for treemap in self.children]
            secondaries = [treemap.secondary for treemap in self.children]
            secondary_weights = [compare(self.secondary, secondary) for secondary in secondaries]
            
            def normalize(array):
                array = np.array(array)
                max,min = np.max(array), np.min(array)
                return (array-min)/max
            
            secondary_weights = normalize(secondary_weights)
            
            rectangles = mlab.treemap(values)
            
            width, height = pos[2]-pos[0], pos[3]-pos[1]
            
            x1,y1,w,h = rectangles
            x1,y1 = pos[0] + x1*width, pos[1] + y1*height
            xn, yn = x1+ w*width, y1 + h*height
            
            x1 = [max(pos[0], x) for x in x1]
            y1 = [max(pos[1], y) for y in y1]
            xn = [min(x, pos[2]) for x in xn]
            yn = [  min(y, pos[3]) for y in yn]

            rectangles = zip(x1,y1,xn,yn)
            
            for index,child in enumerate(self.children):
                child.drawTreeMap(myCanvas, rectangles[index], secondary_weight = secondary_weights[index],colorSeed=color)
            
            #draw outlines
            for index,rectangle in enumerate(rectangles):
                borderColor = "#%02X%02X%02X" % tuple([int( (self.level) * 255 *2/10)]*3)
                self.drawOutline(myCanvas, rectangles[index], borderColor=borderColor)
        else:
            Treemap.canvas_drawRectangle(myCanvas, pos, sliver=sliver, color=color)
    
    def draw(self,canvasX=810, canvasY=810, space=10):
        # start drawing the treemap. should be called only by top of drawing
        
        #get a canvas object for drawing
        myCanvas = Treemap.defineCanvasObject(canvasX,canvasY,space)
       
        #define rectangle in which to draw treemap
        pos = [space,space, canvasX-space, canvasX-space]
        
        self.drawTreeMap(myCanvas,pos, sliver=space)
        
        Tk.mainloop()
        









    
def flatten(l, ltypes=(list, tuple)):
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
    


def compare(parentValue, childValue):
#     x1,y1 = parentValue
#     x2,y2 = childValue
#     return np.sqrt( (x1-x2)**2 + (y1-y2)**2)
    return np.random.rand()

def buildTreemap(CPF_reductions, CPFbranches,parent=None, secondary_values = None):
    """Builds a Treemap given a list of faults (elements in each fault, value of reduction for that fault case)"""
    
    def clean_faultList(key, faultList):
        """remove key from each cases element list (unless len == 1, which is assumed to be the fault involving that key alone"""
        return [[el for el in fault if el != key] if len(fault)>1 else fault for fault in faultList]
    
    if parent==None: #top of the tree -> build parent node
        parent = Treemap(value = np.sum(CPF_reductions), secondary = (1,1))
    
   
    if parent.level > 20: return [] #depth limit
    else:
        #get list of different branch elements in the fault list
        branchElements = set(flatten(CPFbranches))
        
        branchResultIndexes = defaultdict(list);
        
        for index,fault in enumerate(CPFbranches):
            for element in fault:
                branchResultIndexes[element] += [index]
        
        value = np.sum(CPF_reductions)
        
        subCPFbranches = {key: [CPFbranches[index] for index in value] for key,value in branchResultIndexes.items()}
        subCPF_reductions = { key: [CPF_reductions[index] for index in value] for key,value in branchResultIndexes.items()}
        subAreas = {key: np.sum(value) for key,value in subCPF_reductions.items()}
        
        
        cleanCPFbranches = {key: clean_faultList(key, faultList) for key, faultList in subCPFbranches.items()}
        
        for key in subCPF_reductions.keys():
            child = parent.addChild(value=subAreas[key], secondary=secondary_values[key])
            
            if len(cleanCPFbranches[key]) >1:#stop building tree when you reach single elements.
                buildTreemap(subCPF_reductions[key],cleanCPFbranches[key],secondary_values = secondary_values,parent = child)
        
        return parent

def myBuildTreemap(faultList, parent=None, secondary_values=None):
    """Builds a Treemap given a list of faults (elements in each fault, value of reduction for that fault case)"""
    
    
    if parent == None:
        parent = Treemap(value = np.sum( fault.value() for fault in faultList))
    
    if parent.level > 20:
        return [] #depth limit
    else:
        #get list of unique elements in faultList
        elements = set(flatten([ fault.getElements() for fault in faultList]))
        
        #get sum values for all faults in tree
        value = np.sum( [fault.value() for fault in faultList])
        
        #for each element, make a list of faults it is involved in
        subFaults = defaultdict(list)
        
        for fault in faultList:
            #for each element, copy the fault, strip the element, and add it to element's list.
            for element in fault.getElements():
                subFaults[element] += [fault.subFault(element)]
        
        
        
        for faultList in subFaults.values():
            child = parent.addChild(value = sum(fault.value() for fault in faultList), secondary = np.random.rand());
            
            if len(faultList) > 1:
                myBuildTreemap(faultList, parent=child)
    
    return parent


class Element():
    
    def __init__(self, type=None, id=0, value=None):
        self.type=type
        self.id=id
        if value==None:
            self.value = np.random.rand()
    
    def __str__(self):
        return self.type + " %04d" % self.id
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        return True if self.type == other.type and self.id == other.id else false
    
    def __hash__(self):
        #has the string representation of the element, eg 'bus 01'
        return hash(str(self))

class Fault:


    
    def __init__(self,listing, reduction = None):
        listing = listing[0][0]
        self.label = str(listing.label[0])
        self.reduction = reduction
        
        def getList(myList):
            zeroDim = [element for element in myList.shape if element != 0L]
            return [element for element in listing.branch[0]] if len(zeroDim) > 1 else []
        
        self.branch = [Element(type='branch',id=item) for item in getList(listing.branch)]
        self.bus = [Element(type='bus', id=item) for item in getList(listing.bus)]
        self.gen = [Element(type='gen', id=item) for item in getList(listing.gen)]
    
    def __repr__(self):
        return str(self);
    def __str__(self):
        branch = [el.id for el in self.branch]
        bus = [el.id for el in self.bus]
        gen = [el.id for el in self.gen]
        string = '\t\t'.join([self.label, 'CPF: %.3f' % self.reduction, 'elements:', str(branch), str(bus), str(gen)])
        string = '\n%s' % string
#         string = '%30s\t%20s\t%20s\t%20s' % self.label, str(self.branch), str(self.bus), str(self.gen)
        return string
    
    def value(self):
        return self.reduction
    
    def getElements(self):
        return self.branch + self.bus + self.gen
    
    def strip(self, stripElement):
        def removeElement(mList, mElement): return [el for el in mList if el != mElement]
        self.branch, self.bus, self.gen = [ removeElement(mList, stripElement) for mList in [self.branch, self.bus, self.gen]]
    
    def subFault(self, element):
        from copy import copy
        newFault = copy(self)
        newFault.strip(element)
        return newFault


def main():
    #sample usage generator
    myTreemap = Treemap();
    myTreemap.setChildren();
    
    for child in myTreemap.children:
        child.setChildren(values=np.random.rand(5))
        
        for subChild in child.children:
            subChild.setChildren(values = np.random.rand(8))
    
    myTreemap.draw()




   
    
print __name__

cpfResults = scipy.io.loadmat('cpfResults', struct_as_record=False)

# cpfResults = scipy.io.loadmat('cpfResults')


print [key for key in cpfResults.keys()]
    
baseLoad = cpfResults['baseLoad'][0,0]

CPF_reductions = baseLoad- cpfResults['CPFloads'][0];

#CPFbranches should contain keys that refer to each element.
CPFbranches = cpfResults['branchFaults'][0]
base = cpfResults['base'][0,0]

faults = [ Fault(listing, reduction) for listing, reduction in zip(CPFbranches, CPF_reductions)]

    
myTreemap = myBuildTreemap(faults, secondary_values = np.random.rand(len(faults)));
myTreemap.draw()
# nBranches, rows = base.branch.shape
# CPFbranches = [ list(branchList.flatten()) for branchList in CPFbranches]
# 
# branch_geo = {id: line_geo for id,line_geo in zip( range(1, nBranches+1), base.branch_geo[0]) }
# branch_positions = {key: Line(line_geo).getPosition() for key, line_geo in branch_geo.items()}

# myTreemap = buildTreemap(CPF_reductions, CPFbranches, secondary_values = branch_positions)

# print myTreemap

# Treemap.compare = compare
# myTreemap.draw()
#     
# if __name__ == "__main__":
#     main()


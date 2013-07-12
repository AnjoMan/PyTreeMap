import scipy.io
import numpy as np
import Tkinter as Tk
from mlabwrap import mlab
import colorsys
from collections import defaultdict


class Treemap:
    
    def __init__(self, value=1, level=0):
        self.value = value
        self.level = level
        self.children = []
    
    def __str__(self):
        string = " | "*self.level + "Treemap node, value = " + ("%8.2f" % self.value) + ", level: " + str(self.level) + "; " + ( ("%d sub-nodes" % len(self.children)) if len(self.children)>0 else "")
        
        for child in self.children:
            string += "\n" + child.__str__()
        
        return string
    
    def hasChildren(self):
        return len(self.children) > 0
        
    def setChildren(self,values=np.random.rand(20)):
        self.children = [Treemap(value, level=self.level+1) for value in values]
    
    def addChild(self, value=np.random.rand()):
        self.children += [Treemap(value, level = self.level+1)]
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
    

    
    def randomColor(self, h=None, s=0.3, v=0.7, seed='#998899'):
        def clamp(val): return max( min( (val, 1) ),0)
        
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
            s = s + ( np.random.rand() - 0.5) * 2/10
            v = v + (np.random.rand() - 0.5)*1/10
            h = clamp(h)
            return rgb(h,s,v)
    
    def drawOutline(self,myCanvas, pos, borderColor="#000000"):
        x1,y1,xn,yn = pos
        borderWidth= max(0,2-self.level);
        myCanvas.create_rectangle(x1,y1,xn,yn, width = borderWidth, outline = borderColor)
        
    def drawTreeMap(self, myCanvas,pos,sliver=0, colorSeed=None):
        
        color = self.randomColor(seed=colorSeed)
        
        if self.hasChildren():
            #draw sub-tree
            values = [treemap.value for treemap in self.children]
            rectangles = mlab.treemap(values)
            
            width, height = pos[2]-pos[0], pos[3]-pos[1]
            
            x1,y1,w,h = rectangles
            x1,y1 = pos[0] + x1*width, pos[1] + y1*height
            xn, yn = x1+ w*width, y1 + h*height
            
            rectangles = zip(x1,y1,xn,yn)
            
            for index,child in enumerate(self.children):
                child.drawTreeMap(myCanvas, rectangles[index], colorSeed=color)
            
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
    

def clean_faultList(key, faultList):
    #remove key from each cases element list (unless len == 1, which is assumed to be the fault involving that key alone
    return [[el for el in fault if el != key] if len(fault)>1 else fault for fault in faultList]


def buildTreemap(CPF_reductions, CPFbranches,parent=None, level=0):
    
    
    if parent==None:
        parent = Treemap(value = np.sum(CPF_reductions))
    
    thisLevel = parent.level+1
    
    if thisLevel > 4: return []
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
        
#         key = 1;
        
        for key in subCPF_reductions.keys():
            child = parent.addChild(value=subAreas[key])
            if len(cleanCPFbranches[key]) >1:
                buildTreemap(subCPF_reductions[key],cleanCPFbranches[key],parent = child)
        
        return parent
        
        
    
    
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

print [key for key in cpfResults.keys()]
    
baseLoad = cpfResults['baseLoad'][0,0]

CPF_reductions = baseLoad- cpfResults['CPFloads'][0];
CPFbranches = cpfResults['branchFaults'][0]
base = cpfResults['base'][0,0]


nBranches, rows = base.branch.shape
CPFbranches = [ list(branchList.flatten()) for branchList in CPFbranches]

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


cleanCPFbranches = dict()

for key,faultList in subCPFbranches.items():
    cleanCPFbranches[key] = clean_faultList(key, faultList)
#     
# CPFbranches = cleanCPFbranches[1]
# CPFreductions = subCPF_reductions[1]
#from loads and accompanying branches, generate a treemap
myTreemap = buildTreemap(CPF_reductions, CPFbranches)
print myTreemap
# myTreemap = Treemap(value)
# myTreemap.setChildren(subAreas.values())
myTreemap.draw()
#     
# if __name__ == "__main__":
#     main()


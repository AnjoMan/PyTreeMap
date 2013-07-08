import scipy.io
import numpy as np
import Tkinter as Tk
from mlabwrap import mlab


class Treemap:
    children = []
    
    def __init__(self, value=1):
        self.value = value
    
    def hasChildren(self):
        return self.children==True
        
    def setChildren(self,values=np.random.rand(20)):
        self.children = [Treemap(value) for value in values]
    
    def drawTreeMap(self, myCanvas,pos,sliver):
        
        if self.hasChildren():
            #draw sub
    
    @staticmethod
    def defineCanvasObject(width,height,border, name="Treemap"):
         master = Tk.Tk(); 
        master.title("Fault TreeMap")
        myCanvas = Tk.Canvas(master, width=canvasX, height=canvasY)
        myCanvas.pack()
        return myCanvas
    
    
    def draw(self,canvasX=810, canvasY=810, space=10):
        #get a canvas object for drawing
        myCanvas = defineCanvasObject(canvasX,canvasY,space)
       
        #define rectangle in which to draw treemap
        pos = [space,space, canvasX-space, canvasX-space]
        
        drawTreeMap(myCanvas,pos)
        
        # start drawing the treemap. should be called only by top of drawing
        #layout
        values = [treemap.value for treemap in self.children]
        rectangles = mlab.treemap(values)
        
        x1,y1,w,h = rectangles
    
        x1 = space + x1 * canvasX
        y1 = space + y1 * canvasY
        xn = x1 + w*canvasX
        yn = y1 + h*canvasY
        
        rectangles = zip(x1,y1,xn,yn)
        
        r = lambda: np.random.randint(0,255)
        rC = lambda: '#%02X%02X%02X' % (r(),r(),r())
        
        
        
        
        for rectangle in rectangles:
            x1,y1,xn,yn = rectangle
            print x1,y1,xn,yn
            myCanvas.create_rectangle(x1,y1,xn,yn, fill=rC(), width=0)
        

        
        
#         self.drawTreeMap(myCanvas, [space,space,canvasX-space, canvasY-space], rectangles)
        
        
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
    






cpfResults = scipy.io.loadmat('cpfResults', struct_as_record=False)

print [key for key in cpfResults.keys()]

CPFloads = cpfResults['CPFloads'][0];
CPFbranches = cpfResults['branchFaults'][0]
base = cpfResults['base'][0,0]


nBranches, rows = base.branch.shape
CPFbranches = [ list(branchList.flatten()) for branchList in CPFbranches]
branchElements = set(flatten(CPFbranches))

branchResultIndexes = dict();


myTreemap = Treemap();
myTreemap.setChildren();

myTreemap.draw()
# 
# for index, faultElements in enumerate(CPFbranches):
#     branchResultIndexes[tuple(faultElements)] = index
    
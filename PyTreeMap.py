import scipy.io
import numpy as np
import Tkinter as Tk
from mlabwrap import mlab
import colorsys


class Treemap:
    children = []
    
    def __init__(self, value=1, level=0):
        self.value = value
        self.level = level
    
    def hasChildren(self):
        return len(self.children) > 0
        
    def setChildren(self,values=np.random.rand(20)):
        self.children = [Treemap(value, level=self.level+1) for value in values]
    
    @staticmethod
    def canvas_drawRectangle(myCanvas, pos, sliver=0, color="#FF0000"):
        x1,y1,xn,yn = pos;
        x1,y1 = x1+sliver, y1+sliver
        xn,yn = xn-sliver, yn-sliver
        
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
     

        clamp = lambda val: max( min( (val, 1) ),0)
        
        #how to convert from decimal h,s,v to "#RRggBB" string
#         rgb = lambda h,s,v: '#%02X%02X%02X' % tuple( [ int(np.round(el*255)) for el in  colorsys.hsv_to_rgb(h,s,v) ])
        def rgb(h,s,v):
            r,g,b = colorsys.hsv_to_rgb(h,s,v)
            
            print r,g,b
            
            return '#%02X%02X%02X' % tuple( [ int(np.round(el*255)) for el in (r,g,b)])
        
        
        #how to convert from "#RRGGBB string to decimal h,s,v
#         hsv = lambda rgb: tuple( [int(el,16)/255 for el in (rgb[1:3],rgb[3:5],rgb[5:7]) ])
        def hsv(rgb):
            r,g,b = [ int(el,16)/255.0 for el in (rgb[1:3],rgb[3:5],rgb[5:7]) ]
            h,s,v = colorsys.rgb_to_hsv(r,g,b)
            return h,s,v
        
        
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
#             print "Seed: ", seed, "   HSV: ",h,s,v
            h = h + ( np.random.rand() - 0.5 ) *2/10
            v = v + (np.random.rand() - 0.5)*1/10
            h = clamp(h)
#             return seed
            return rgb(h,s,v)
    
    def drawOutline(self,myCanvas, pos):
        x1,y1,xn,yn = pos
        borderWidth= max(0,2-self.level);
        myCanvas.create_rectangle(x1,y1,xn,yn, width = borderWidth)
        
    def drawTreeMap(self, myCanvas,pos,sliver=0, colorSeed=None):
        
        color = self.randomColor(seed=colorSeed)
        
        
        if self.hasChildren():
            
#             print self.level
            #draw sub-tree
            values = [treemap.value for treemap in self.children]
            rectangles = mlab.treemap(values)
            
            width, height = pos[2]-pos[0], pos[3]-pos[1]
            
            x1,y1,w,h = rectangles
            x1,y1 = pos[0] + x1*width, pos[1] + y1*height
            xn, yn = x1+ w*width, y1 + h*height
            
#             print len(self.children), width, height, pos
            rectangles = zip(x1,y1,xn,yn)
            
            for index,child in enumerate(self.children):
#                 print rectangles[index]
                child.drawTreeMap(myCanvas, rectangles[index], colorSeed=color)
            
            for index,rectangle in enumerate(rectangles):
                self.drawOutline(myCanvas, rectangles[index])
            
            
        else:
#             print pos
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

for child in myTreemap.children:
    child.setChildren(values=np.random.rand(5))

myTreemap.draw()
# 
# for index, faultElements in enumerate(CPFbranches):
#     branchResultIndexes[tuple(faultElements)] = index
    
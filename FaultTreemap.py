import scipy.io
import numpy as np
import Tkinter as Tk
# from mlabwrap import mlab
import colorsys
from collections import defaultdict
from PowerNetwork import *
from Treemap import layout

from PySideCanvas import *
import sys

    
def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate

class Treemap:
    
    @staticmethod
    def compare(self, other):
        return np.random.rand()
    
    def __init__(self, value=1,element=None, parent=None, secondary = None):
        self.value, self.parent,  self.secondary,self.children, = value, parent, secondary, []
        self.element = element;
        if self.element != None:
            self.secondary = element.secondary()
        else:
            self.secondary = secondary
        
        try: self.level = parent + 1
        except: self.level = 0 #error if parent does not implement __add__()

    #use this to get the level of a Treemap and increment it:
    def __add__(self, other): return self.level + other;
    def __radd__(self,other): self.__add__(other)
        
    def __str__(self):
        string = " | "*self.level + "Treemap node, value = " + ("%8.2f" % self.value)
#         string += ", subvalue = " + str([int(r) for r in self.secondary]) if self.secondary != None else ""
        string += ", level: " + str(self.level) + "; " 
        string += ("%d sub-nodes" % len(self.children)) if len(self.children)>0 else ""
        for child in self.children: string += "\n" + child.__str__()
        return string
    
    def __repr__(self): return str(self)
    
    def hasChildren(self): return len(self.children) > 0
        
    def setChildren(self,values=np.random.rand(20)): self.children = [Treemap(value, level=self.level+1) for value in values]
    
    def addChild(self, element = None, value=np.random.rand(), secondary=None):
        self.children += [Treemap(value,element = element, parent=self, secondary=secondary)]
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
        myCanvas.drawRectangle([x1,y1,xn,yn], color=color)
    
    def drawOutline(self,myCanvas, pos, borderColor="#000000"):
        x1,y1,xn,yn = pos
        borderWidth= max(0,3-self.level);
        colorWeight = round(max(0,self.level)/15.0 * 255)
#         print self.level, colorWeight
        borderColor = '#%02X%02X%02X' % (colorWeight, colorWeight, colorWeight)
        #toolbox-specific code to draw outline
        myCanvas.drawOutline(pos, borderWidth, color = borderColor)

    @staticmethod
    def defineCanvasObject(width,height,border, name="Treemap"):
        #toolbox-specific code to define drawing space
        return PySideCanvas(width, height, name)

    
    
    @static_var('seed', 0)
    def randomColor(self, h=None, s=0.6, v=0.7, seed='#998899', secondary_weight = None):
        def clamp(*vals): #keep values in range 0-1 with capping
            lst = [min(1,max(0,val)) for val in vals]
            return lst if len(lst) > 1 else lst[0]
        
        def mod(*vals):#keep values in range 0-1 with rollover
            lst = [(10*val)%10/10.0 for val in vals]
            return lst if len(lst) > 1 else lst[0]
        
        #how to convert from decimal h,s,v to "#RRggBB" string
        def rgb(h,s,v): return '#%02X%02X%02X' % tuple( [ int(np.round(el*255)) for el in colorsys.hsv_to_rgb(h,s,v)])
        #how to convert from "#RRGGBB string to decimal h,s,v
        def hsv(rgb): return colorsys.rgb_to_hsv(*[ int(el,16)/255.0 for el in (rgb[1:3],rgb[3:5],rgb[5:7]) ])
        
        
        #no color will be drawn for level 0
        if self.level==0: return '#998899'
        
        #for level 1, pick a random hue
        elif self.level==1:
            if not type(h) == float: 
#                 h=round(np.random.rand(),1)
                h = self.randomColor.__func__.seed + 0.3 + round(np.random.rand()/20.0,1)
                self.randomColor.__func__.seed = h
            return rgb(h,s,v)
        
        #for levels beyond 1, vary the hue given by seed
        elif self.level > 1:
            h,s,v = hsv(seed)
#             h = h + ( np.random.rand()  ) *3/10.0 * np.log10(2)/np.log10(self.level)
            h = h + (np.random.rand()) * 7/10.0 * 1/(self.level**2)
            s = (secondary_weight)*0.4+0.3 if secondary_weight != None else s + (np.random.rand()-0.5)*2/10
#             v = (1-secondary_weight)*0.4+0.5 if secondary_weight != None else s+ (np.random.rand()-0.5)*1/10
            v = (1-secondary_weight)*0.5+0.5 if secondary_weight != None else s+ (np.random.rand()-0.5)*1/10
# s,v = 0.3,0.7
            h,s,v = [mod(h)]+ clamp(s,v)
            return rgb(h,s,v)
    
    
        
    def drawTreeMap(self, myCanvas,pos,sliver=0, secondary_weight=None, colorSeed=None):
        
        color = self.randomColor(seed=colorSeed, secondary_weight = secondary_weight)
        if self.hasChildren():
            #draw sub-tree
            values = [treemap.value for treemap in self.children]
            secondaries = [treemap.secondary for treemap in self.children]
            secondary_weights = [compare(self.secondary, secondary) for secondary in secondaries]
            
            def normalize(array):
                array = np.array(array)
                return (array-np.min(array))/np.max(array)
            
            secondary_weights = normalize(secondary_weights)
            rectangles = layout(values, pos)
            
            for index,child in enumerate(self.children):
                child.drawTreeMap(myCanvas, rectangles[index], secondary_weight = secondary_weights[index],colorSeed=color)
            
            #draw outlines
            for index,rectangle in enumerate(rectangles):
                borderColor = "#%02X%02X%02X" % tuple([int( (self.level) * 255 *2/10)]*3)
                self.drawOutline(myCanvas, rectangles[index])
        else:
            sliver= max(0,2-self.level);
            Treemap.canvas_drawRectangle(myCanvas, pos, color=color)
            
    
    
    def draw(self, canvasX=810,canvasY=810,space=10):
        
        
        self.drawPySide(canvasX, canvasY, space)
        
        
        
    def drawPySide(self, canvasX,canvasY, space):
        
        app = QtGui.QApplication(sys.argv)
        
          #get a canvas object for drawing
        myCanvas = Treemap.defineCanvasObject(canvasX,canvasY,space)
        
        pos = [space, space, canvasX-space, canvasY-space]
        self.drawTreeMap(myCanvas,pos, sliver=space)
        
        myCanvas.drawOutline(pos,3)
        sys.exit(app.exec_())



def compare(parentValue, childValue):
    x1,y1 = parentValue
    x2,y2 = childValue
    return np.sqrt( (x1-x2)**2 + (y1-y2)**2)
#     return np.random.rand()

def buildTreemap(faultList, parent=None, secondary_values=None):
    """Builds a Treemap given a list of faults (elements in each fault, value of reduction for that fault case)"""
    
    
    if parent == None:
        parent = Treemap(value = np.sum( fault.value() for fault in faultList), secondary = (1,1))
    
    if parent.level >= 4:
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
        
        
        for element,faultList in subFaults.items():
            child = parent.addChild(element = element, value = sum(fault.value() for fault in faultList), secondary = np.random.rand());
            
            if len(faultList) > 1:
                buildTreemap(faultList, parent=child)
        
    
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




# print myTreemap

# myTreemap.draw()
#     
# if __name__ == "__main__":
#     main()


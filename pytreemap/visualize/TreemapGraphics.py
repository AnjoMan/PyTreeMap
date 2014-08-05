"""
    written by Anton Lodder 2012-2014
    all rights reserved.
    
    This software is the property of the author and may not be copied,
    sold or redistributed without expressed consent of the author.
"""



import sys, os, inspect
try:
    import pytreemap
except:
    #walk up to 'pytreemap' and add to path.
    realpath = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
    (realpath, filename) = os.path.split(realpath)
    while filename != 'pytreemap':
        (realpath, filename) = os.path.split(realpath)
    sys.path.append(realpath)
    import pytreemap
    
    

from PySide.QtCore import *
from PySide.QtGui import *
import sys
# from PowerNetwork import *
import colorsys
from numpy import *
from pytreemap.Treemap import layout


from pytreemap.visualize.VisBuilder import MATLAB_systemFile, JSON_systemFile, getFaults
from pytreemap.system.PowerNetwork import Fault


def main():
    from pytreemap.visualize.TreemapGraphics import TreemapFault, TreemapGraphicsVis
    
    
    def getFullFileNames(geoFile, resultFile):
        return (os.path.join(pytreemap.system.__path__[0], geoFile), os.path.join(pytreemap.__path__[0], 'sample_results', resultFile))
    
#     mCase = ('case118_geometry.json', 'cpfResults_case118_2level.json')
    mCase = ('case30_geometry.json', 'cpfResults_case30_2level.json')
#     mCase = ('case30_geometry.json', 'cpfResults_small.json')
    
    
#     mSys = 'case118_geometry.json'
#     mRes = 'cpfResults_case118_2level.json'
    
    mCase = getFullFileNames(*mCase)
    mCPFresults = JSON_systemFile(*mCase)
    
    (faults, faultTree) = getFaults(TreemapFault, mCPFresults)
    
    
# #     file = 'cpfResults_4branches'
# #     file = 'cpfResults_case30_2level'
#     file = 'cpfResults'
# #     file = 'cpfResults_case118_2level'
# #     

#     (faults, faultTree) = getFaults(TreemapFault, CPFfile(file))
# #     
# #     values = [14, 1, 17, 14, 17, 18, 8, 8, 6, 10, 2, 1, 4, 9, 10, 0, 16, 13, 8, 12, 6, 17, 5, 1, 19, 4, 11, 16, 11, 5, 17, 16, 4, 7, 17, 14, 11, 16, 13, 19]
# #     
# #     values = [flt.subValue for flt in faultTree[1][1].connections]
# #     
    app = QApplication(sys.argv)
    
    ex = TreemapGraphicsVis(pos = [100,100,700,700],faultTree = faultTree)
#     ex = TreemapGraphicsVis(pos = [100,100,100,100],faultTree = faultTree)
#     ex = TreemapGraphicsVis(pos = [100,100,100,100],values = values)


#     ex2 = TreemapGraphicsVis( pos=[1100,50,400,400],values = values, name="Treemap of Random Values")
    
    sys.exit(app.exec_())














def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate

def randomColor(level=1, secondary = None):
    def rgb(h,s,v): return '#%02X%02X%02X' % tuple( [ int(round(el*255)) for el in colorsys.hsv_to_rgb(h,s,v)])

    
    h = 0.32*(1+level)%1
#     secondary = None
    if secondary is not None:
        
        s = (secondary**(1/2)) * 0.4 + 0.2
        v = (secondary**(1/2)) * 0.5 + 0.5
    else:
        s = 0.4
        v = 0.8 
    
    return QColor(rgb(h,s,v))
    



class TreemapGraphicsVis(QGraphicsView):
    border = 10;
    
    def __init__(self, pos=None, faultTree=None, values=None, name="TreemapGraphics", details= None):
        super().__init__()
        
#         if not pos: pos = [50,50,900,900]
        self.pos = pos
        (x,y,w,h) = pos
        
        self.setMinimumSize(w,h)
        
        
        self.outlines = []
        self.widgets = []
        self.details = details


        self.scene = QGraphicsScene(self)
        self.setSceneRect(10,10,w-20,h-20)
          
            
        if faultTree:
            self.build_fromFaultTree(faultTree,[0,0,w-20,h-20])
        elif values:
            self.build(values)
        
        
        self.setScene(self.scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
#         self.setRenderHint(QPainter.Antialiasing)
        
        self.setWindowTitle(name)
        self.show()
#         self.scale(.99
    
    def sizeHint(self):
        return QSize(*self.pos[2:4])
        
    def addWidget(self,widget):
        self.widgets.append(widget)
        self.scene.addItem(widget)
    
    def addOutline(self, xa, ya, xb, yb, level):
        self.outlines.append( ((xa,ya,xb,yb),level) )
        
    def drawForeground(self, painter,rect):
        painter.setPen(Qt.black)
        painter.setBrush(Qt.NoBrush)
        
        for (xa,ya,xb,yb), level in self.outlines:
            painter.setPen(QColor(*([15*level]*3)))
            painter.drawLine(xa,ya, xb,ya)
            painter.drawLine(xb,ya,xb,yb)
            painter.drawLine(xb,yb,xa,yb)
            painter.drawLine(xa,yb,xa,ya)
        
    def build(self,values):
        """ build a treemap from a list of numbers 
            
            This funciton is for building a fault-tree without a tree-structure.
            It takes 'values' as a list of numbers and builds a single-level
            treemap out of that.
        """
        pos = self.sceneRect().getRect()
        
        x0,y0,w,h = pos
        
        self.addOutline( x0,y0,x0+w,y0+h, 1)
        rectangles, _ = layout(values, [x0+1,y0+1,x0+w-1,y0+h-1])
        
        for el in rectangles:
            if el:
                xa,ya,xb,yb = el
                Rectangle(self,[xa,ya,xb-xa,yb-ya])

            
    def build_fromFaultTree(self,
                            faultTree,
                            square,
                            startLimit=1, 
                            depthLimit =2):
        """ build a treemap from a list of faults. """
        border = TreemapGraphicsVis.border
        square = [border,border,self.width()-border*2, self.height()-border*2]
        
        def recursive_build(faultList, square, mLevel, parent = None):

            mLevel = len(faultList[0].elements)
#             
            x0,y0,xn,yn = square
            self.addOutline(x0,y0,xn,yn, mLevel)
            
            square = [x0+1,y0+1,xn-1,yn-1]
            if len(faultList) == 0:
                return None
            
            #lay out faults
            rectangles, leftovers = layout(([parent.value] if parent is not None else [])+[fault.subValue for fault in faultList], square)
            
#             rectangles, leftovers = layout(([parent.value()] if parent is not None else [])+[fault.value() for fault in faultList], square)
            
            if parent is not None:
                parentRect = rectangles.pop(0)
            
            
            #rectangle representing elements that were too small
            if len(faultList) < len(rectangles):
                xa,ya,xb,yb = rectangles.pop()
                leftoverRect = Rectangle(self,[xa,ya,xb-xa,yb-ya], fill=Qt.Dense3Pattern);
                
                leftoverRect.color = randomColor(mLevel)
                self.addOutline(xa,ya,xb,yb,mLevel+1)
            
            
            #rectangle representing the parent fault
            if parent is not None and parentRect:
                    fault = parent
                    xa,ya,xb,yb = parentRect
                    fault.addRectangle(Rectangle(self,[xa,ya,xb-xa,yb-ya]))
                    self.addOutline(xa,ya,xb,yb, mLevel+1)
            
            if mLevel >= depthLimit:
                #lay out faults and add a rectangle widget to each fault
#                 
                
                for fault,rectangle in zip(faultList,rectangles):
                    if not rectangle: continue
                    xa,ya,xb,yb = rectangle
                    fault.addRectangle(Rectangle(self, [xa,ya,xb-xa,yb-ya]))
                    self.addOutline(xa,ya,xb,yb,mLevel+1)
    #                 mWindow.addWidget(fault)
            else:
                """
                    There should be some limit here as to how small a rectangle
                    gets recursively built.
                """
                for fault, rectangle in zip(faultList, rectangles):
                    if not rectangle: continue
                    xa,ya,xb,yb = rectangle
                    
                    if (xb-xa)*(yb-ya) > 10*10 and fault.connections:
                        randomColor(mLevel-startLimit+1)#prime random colour generator
                        recursive_build(fault.connections, rectangle, mLevel+1, parent  = fault)
                    else:
#                         print( "{},...".format(rectangle))
                        self.addOutline(xa,ya,xb,yb,mLevel + 1)
                        self.addOutline(xa+1,ya+1, xb-1, yb-1, mLevel+2)
                        fault.addRectangle(Rectangle(self,[xa+1,ya+1,xb-xa-2,yb-ya-2]))
        
        recursive_build(faultTree[startLimit], square, startLimit)
            











class TreemapFault(Fault):
    def __init__(self, listing, reduction=None):
        super().__init__(listing, reduction)
        self.rectangles = []
    
    def toggleHighlight(self):
        for rect in self.rectangles: rect.toggleHighlight()

    def addRectangle(self,newRectangle, level=None):
        newRectangle.color = randomColor(len(self.elements), self.secondary)
        newRectangle.fault = self
        self.rectangles.append(newRectangle)
        return newRectangle
        

class Rectangle(QGraphicsItem,object):
    
    
    def __init__(self,mGraphicsView, pos, fill=Qt.SolidPattern): #...parent=None,  color=QColor(200,100,100)):
        super().__init__()
        
        
#         xa,ya,xb,yb = pos
#         xb,yb = xb+1,yb+1 #widget space is defined from left of xa to left of xb, I need to expand it to [left of xa, right of xb]. (same argument for y)

        self.pos = QRectF(*pos)
        self.color = QColor(200,100,100)
        self.highlight = False
        self.fill = fill
        
        self.fault = None
        
        
        if mGraphicsView: mGraphicsView.addWidget(self)
        
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        
    
    def mousePressEvent(self, event): 
        if self.fault:
            print("{}. reduced loadability: {:.0f}, area: {:.0f}.".format(self.fault, self.fault.value, self.pos.width()*self.pos.height()))
            self.setDetails()
        else: print(str(self))
        
        
            
    def hoverEnterEvent(self, event): 
#         import cProfile
#         print('<hover enter>')
        self.toggleHighlight()
        if self.fault:
            for el in self.fault.elements: el.toggleHighlight()
    def hoverLeaveEvent(self, event):
#         print('<hover leave>')
        self.toggleHighlight()
        if self.fault:
            for el in self.fault.elements: el.toggleHighlight()
    
    def toggleHighlight(self, list=None):
        self.highlight = not self.highlight
        self.update(self.boundingRect())
        
    def boundingRect(self):
        return QRectF(self.pos)
        
        
    def paint(self, painter, option, widget):
        
        painter.setPen(Qt.black)
        brush = QBrush(self.fill)
        if self.highlight: brush.setColor(QColor.fromHsv(self.color.hue(), self.color.saturation() * 0.6, 80))
        else: brush.setColor(self.color)
            
        painter.setBrush(brush)
        painter.drawRect(self.pos)
    
    
    
    
#         add annotations
        
#         mText = QGraphicsSimpleTextItem(", ".join([el.shortRepr() for el in self.fault.elements]), parent=self)
#         mText.setPos(*self.pos.getRect()[0:2])
#         mText.setFont(QFont('sans-serif', 20))
        
    def setDetails(self):
        if self.scene().parent().details:
            self.scene().parent().details.setContent(self.fault.html())

if __name__ == "__main__":
    main()
from PySide.QtCore import *
from PySide.QtGui import *
import sys
from PowerNetwork import *
import colorsys
from numpy import *
from Treemap import layout
from VisBuilder import *


def main():
    from TreemapGraphics import TreemapFault
    
    
    
    
#     (faults, faultTree) = getFaults(TreemapFault, CPFfile('cpfResults_case118_2level'))
    (faults, faultTree) = getFaults(TreemapFault, CPFfile())
    
    app = QApplication(sys.argv)
    
    
    
    
    ex = TreemapGraphicsVis(faultTree = faultTree)
    
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
    
    def __init__(self, pos=None, faultTree=None, values=[14, 1, 17, 14, 17, 18, 8, 8, 6, 10, 2, 1, 4, 9, 10, 0, 16, 13, 8, 12, 6, 17, 5, 1, 19, 4, 11, 16, 11, 5, 17, 16, 4, 7, 17, 14, 11, 16, 13, 19]):
        super().__init__()
        
        if not pos: pos = [50,50,900,900]
        
        (x,y,w,h) = pos
        self.resize(w,h)
        self.move(x,y)
        
        self.outlines = []
        self.widgets = []
#         self.elements = []



        self.scene = QGraphicsScene(self)
        self.setSceneRect(*pos)
          
            
        if faultTree!=None:
            self.build(faultTree,[10,10,900,900])
        
#         self.build(values)
        
        
        self.setScene(self.scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
#         self.setRenderHint(QPainter.Antialiasing)
        
        self.setWindowTitle('TreemapGraphics')
        self.show()
        self.scale(.9,.9)
    
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
            
            
            
            
            
            
            
            
#         
#     def build(self,values):
#         pos = self.sceneRect().getRect()
#         
#         x0,y0,w,h = pos
#         
#         self.addOutline( x0,y0,x0+w,y0+h, 1)
#         rectangles, _ = layout(values, [x0+1,y0+1,x0+w-1,y0+h-1])
#         
#         for el in rectangles:
#             xa,ya,xb,yb = el
#             self.addWidget( Rectangle([xa,ya,xb-xa,yb-ya]))
#             
#         def addOutline():
#             self.addOutline( 100,100,300,300,1)
#         
#         addOutline()
            
    def build(self,faultTree,square,startLimit=1, depthLimit =2):
        
        square = [TreemapVis.border,TreemapVis.border,self.width()-TreemapVis.border*2, self.height()-TreemapVis.border*2]
        
        def recursive_build(faultList, square, mLevel, parent = None):

            mLevel = len(faultList[0].elements)
#             
            x0,y0,xn,yn = square
            self.addOutline(x0,y0,xn,yn, mLevel)
            
            square = [x0+1,y0+1,xn-1,yn-1]
            if len(faultList) == 0:
                return None
            
            #lay out faults
            rectangles, leftovers = layout(([parent.value()] if parent is not None else [])+[fault.subValue() for fault in faultList], square)
            
#             rectangles, leftovers = layout(([parent.value()] if parent is not None else [])+[fault.value() for fault in faultList], square)
            
            if parent is not None:
                parentRect = rectangles.pop(0)
            
            if len(faultList) < len(rectangles):
                xa,ya,xb,yb = rectangles.pop()
                leftoverRect = Rectangle([xa,ya,xb-xa,yb-ya]);
                
                leftoverRect.setColor(mLevel)
                self.addWidget(leftoverRect)
                self.addOutline(xa,ya,xb,yb,mLevel+1)
            
            if parent is not None and parentRect:
                    fault = parent
                    xa,ya,xb,yb = parentRect
                    fault.addRectangle(self, [xa,ya,xb-xa,yb-ya], level = mLevel - startLimit)
                    self.addOutline(xa,ya,xb,yb, mLevel+1)
            
            if mLevel >= depthLimit:
                #lay out faults and add a rectangle widget to each fault
#                 
                
                for fault,rectangle in zip(faultList,rectangles):
                    if not rectangle: continue
                    xa,ya,xb,yb = rectangle
                    fault.addRectangle(self,[xa,ya, xb-xa, yb-ya], level=mLevel-startLimit+1)
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
#                         fault.addRectangle(self, [xa, ya, xb-xa, yb-ya])
                        self.addOutline(xa+1,ya+1, xb-1, yb-1, mLevel+2)
                        fault.addRectangle(self, [xa+1,ya+1,xb-xa-2,yb-ya-2])
        
        recursive_build(faultTree[startLimit], square, startLimit)











class TreemapFault(Fault):
    def __init__(self, listing, reduction):
        super().__init__(listing, reduction)
        self.rectangles = []
    
    def toggleHighlight(self):
        for rect in self.rectangles: rect.toggleHighlight()
        
    def addRectangle(self, mWindow, pos, level=None):
        newRectangle = Rectangle(pos, fault=self)
        newRectangle.setColor(len(self.elements))
        self.rectangles.append(newRectangle)
        mWindow.addWidget(newRectangle)
        return newRectangle

class Rectangle(QGraphicsItem,object):
    
    
    def __init__(self, pos, fault=None, secondary = None): #...parent=None,  color=QColor(200,100,100)):
        super().__init__()
        
#         xa,ya,xb,yb = pos
#         xb,yb = xb+1,yb+1 #widget space is defined from left of xa to left of xb, I need to expand it to [left of xa, right of xb]. (same argument for y)
        
        self.pos = QRectF(*pos)
        self.color = QColor(200,100,100)
        self._highlight = False
        
        
        self.fault = fault
        if self.fault and len(self.fault.elements) > 1: self.secondary = self.fault.secondary()
        else: self.secondary =   secondary
        
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        
    
    def mousePressEvent(self, event): 
        print(str(self))
        if self.fault:
            print("{}. reduced loadability: {:.0f}, area: {:d}.".format(self.fault, self.fault.value(), self.width()*self.height()))
            
    def hoverEnterEvent(self, event): 
        self.toggleHighlight()
        if self.fault:
            for el in self.fault.elements: el.toggleHighlight()
    def hoverLeaveEvent(self, event):
        self.toggleHighlight()
        if self.fault:
            for el in self.fault.elements: el.toggleHighlight()
    
    def toggleHighlight(self, list=None):
        self._highlight = not self._highlight
        self.update(self.boundingRect())
        
      
      
      
      
    def boundingRect(self):
        return QRectF(self.pos)
    
    def setColor(self,level):
        self.color=randomColor(level, secondary=self.secondary)
        
    def paint(self, painter, option, widget):
        
        painter.setPen(Qt.black)
        brush = QBrush(Qt.SolidPattern) if self.fault else QBrush(Qt.Dense3Pattern)
        
        if self._highlight: brush.setColor(QColor.fromHsv(self.color.hue(), self.color.saturation() * 0.6, 80))
        else: brush.setColor(self.color)
            
        painter.setBrush(brush)
        painter.drawRect(self.pos)
    
    
    
    
    
    
    def setFault(self, fault): #may be unneeded
        self.fault = fault
        
#         add annotations
#         painter.setPen(Qt.black)
#         painter.setFont(QFont('serif', 12))
#         if self.fault:
#             painter.drawText( QPoint(8,painter.fontMetrics().height()*.75+2),", ".join([el.shortRepr() for el in self.fault.elements]))
        
                    

if __name__ == "__main__":
    main()
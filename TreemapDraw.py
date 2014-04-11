from PySide.QtCore import *
from PySide.QtGui import *
import sys
from PowerNetwork import *
import colorsys
from numpy import *
from Treemap import layout

def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate


# @static_var('mods', [0])
# def randomColor(level=1, secondary = None):
#     def rgb(h,s,v): return '#%02X%02X%02X' % tuple( [ int(round(el*255)) for el in colorsys.hsv_to_rgb(h,s,v)])
# 
#     if level == 1:
# #         print randomColor.mods
#         randomColor.mods = [(randomColor.mods[0] + 0.3)%1, 1]
#     elif level > 1:
#         randomColor.mods = randomColor.mods[0:level-1] + [(random.rand()-0.5)*4.0/10 * 1/level]
# #         randomColor.h += random.rand() * 7.0/10 * 1/self.level**2
# #     print randomColor.mods
#     
#     h = sum(randomColor.mods) %1
#     h = randomColor.mods[0]%1
#     
#     
# #     secondary=None
#     if secondary is not None:
#         
#         s = (secondary**(1/2)) * 0.4 + 0.2
#         v = (secondary**(1/2)) * 0.6 + 0.4
#     else:
#         s = 0.4
#         v = 0.7
#     return QColor(rgb(h,s,v))     

def randomColor(level=1, secondary = None):
    def rgb(h,s,v): return '#%02X%02X%02X' % tuple( [ int(round(el*255)) for el in colorsys.hsv_to_rgb(h,s,v)])

    
    h = 0.32*(1+level)%1
    secondary = None
    if secondary is not None:
        
        s = (secondary**(1/2)) * 0.4 + 0.2
        v = (secondary**(1/2)) * 0.6 + 0.4
    else:
        s = 0.4
        v = 0.8 
    
    return QColor(rgb(h,s,v))
        
class TreemapVis(QWidget):
    border = 10
    def __init__(self, pos=None, faultTree=None):
        super(self.__class__, self).__init__()
        
        (x,y,w,h) = (50,50,900,900) if pos == None else pos
        self.resize(w,h)
#         self.move(x,y)
        
        self.outlines = []
        
        if faultTree!=None:
            self.build(faultTree,[10,10,900,900])
        
        
        self.widgets = []
        self.setMouseTracking(True)
        self.setWindowTitle('Treemap')
        self.show()
        
        self.elements = []

    def addWidget(self, widget):
#         print 'addedWidget'
        self.widgets += [widget]
        widget.setParent(self)
        widget.show()
        self.update()
    
    def addElement(self, element):
        self.elements += [element]
    
    def addOutline(self, xa, ya, xb, yb, level):
        self.outlines.append( ((xa,ya,xb,yb),level) )
        
    def paintEvent(self,e):
        super(self.__class__, self).paintEvent(e)
        
        painter= QPainter(self)
        pen = QPen()
        pen.setWidth(1)
        pen.setBrush(Qt.black)
        
        painter.setPen(pen)
        for (xa,ya,xb,yb), level in self.outlines:
            painter.setPen(QColor(*([15*level]*3)))
            painter.drawLine(xa,ya, xb,ya)
#             if level<2:
            painter.drawLine(xb,ya,xb,yb)
            painter.drawLine(xb,yb,xa,yb)
            painter.drawLine(xa,yb,xa,ya)
            
        for el in self.elements:
            el.draw(self)

    def mousePressEvent(self, e):
        for widget in self.widgets:
            print(widget.geometry())
    
    def resizeEvent(self, e):
        print( 'Resized!')
        
    def build(self,faultTree,square,startLimit=1, depthLimit =3):
        
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
                leftoverRect = Rectangle([xa,ya,xb-xa,yb-ya], parent=self, color=QColor(150,150,150));
                leftoverRect.setColor(mLevel)
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
                    
                    if (xb-xa)*(yb-ya) > 50*50 and fault.connections:
                        randomColor(mLevel-startLimit+1)#prime random colour generator
                        recursive_build(fault.connections, rectangle, mLevel+1, parent  = fault)
                    else:
#                         print( "{},...".format(rectangle))
                        self.addOutline(xa,ya,xb,yb,mLevel + 1)
#                         fault.addRectangle(self, [xa, ya, xb-xa, yb-ya])
                        self.addOutline(xa+1,ya+1, xb-1, yb-1, mLevel+2)
                        fault.addRectangle(self, [xa+1,ya+1,xb-xa-2,yb-ya-2])
        
        recursive_build(faultTree[startLimit], square, startLimit)
    
class TreeMapFault(Fault):
    
    def __init__(self, listing, reduction):
        super(self.__class__, self).__init__(listing, reduction)
        self.visuals = []
        self.rectangles = []
    
    def toggleHighlight(self):
        for rect in self.rectangles:
            rect.toggleHighlight()
        
    def addRectangle(self, mWindow, pos, level=None):
        newRectangle = Rectangle(pos, parent=mWindow, fault=self)
#         newRectangle.setColor(level if level else len(self.elements))
        newRectangle.setColor(len(self.elements))
        newRectangle.setFault(self)
        newRectangle.show()
        self.rectangles.append(newRectangle)
        return newRectangle
        
    
class Rectangle(QWidget):
    
    def __init__(self, pos, parent=None, fault=None, color=QColor(200,100,100), secondary=None):
        
        super(self.__class__,self).__init__(parent)
        if parent != None: self.show()
        
        
        self.fault = fault
        if self.fault and len(self.fault.elements) > 1:
            self.secondary = self.fault.secondary()
        else:
            self.secondary =   secondary
            
        xa,ya,xb,yb = pos
        xb,yb = xb+1,yb+1 #widget space is defined from left of xa to left of xb, I need to expand it to [left of xa, right of xb]. (same argument for y)
        self.setGeometry(*pos)
        self.color = color
        self.highlight = False
    
    def setColor(self,level):
        self.color=randomColor(level, secondary=self.secondary)
    def enterEvent(self, e):
        self.toggleHighlight()
        try:
            for element in self.fault.elements:
                element.toggleHighlight()
        except:
            pass
            #if the Rectangle has no associated faults (e.g. a generic filler replacing very small faults)
    
    def leaveEvent(self, e):
        self.toggleHighlight()
        try:
            for element in self.fault.elements:
                element.toggleHighlight()
        except:
            pass
            #if the rectangle has no associated faults
    
    def mousePressEvent(self,e):
        if self.fault:
            print("{}. reduced loadability: {:.0f}, area: {:d}.".format(self.fault, self.fault.value(), self.width()*self.height()))
        else: print(self.fault)
        
    def paintEvent(self, e):
        
#         print 'Painted: ',self.geometry(), self.color
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        
        brush = QBrush(Qt.SolidPattern) if self.fault else QBrush(Qt.Dense3Pattern)

        
        if self.highlight:
            h,s,v = self.color.hue(), self.color.saturation(), self.color.value()
            intensity = 80
            brush.setColor(QColor.fromHsv(h, s*0.6, intensity))
        else:
            brush.setColor(self.color)

        painter.setBrush(brush)
        painter.drawRect(QRectF(1,1,self.width()-1, self.height()-1)) #rectangles are drawn so that border ends on the right side of xb, but widgets end on the left side of xb. Thus, make rectangle one smaller. (ditto for y)
            #with Qt.NoPen, rectangle moves over and fills the space of the border, so we need to offset by 1
        
#         add annotations
        painter.setPen(Qt.black)
        painter.setFont(QFont('serif', 25))
        if self.fault:
            painter.drawText( QPoint(8,painter.fontMetrics().height()*.75+2),", ".join([el.shortRepr() for el in self.fault.elements]))
        
        painter.end()
    
    def toggleHighlight(self):
        self.highlight = not self.highlight
        self.update()
    
    def setFault(self, fault):
        self.fault = fault
       

if __name__ == "__main__":
    app= QApplication(sys.argv)
    
    mWindow =TreemapVis()
    mRectangle = Rectangle([20,40,100,80], parent=mWindow)
    sys.exit(app.exec_())
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


@static_var('mods', [0])
def randomColor(level=1):
    def rgb(h,s,v): return '#%02X%02X%02X' % tuple( [ int(round(el*255)) for el in colorsys.hsv_to_rgb(h,s,v)])

    if level == 1:
#         print randomColor.mods
        randomColor.mods = [(randomColor.mods[0] + 0.3)%1, 1]
    elif level > 1:
        randomColor.mods = randomColor.mods[0:level-1] + [(random.rand()-0.5)*4.0/10 * 1/level]
#         randomColor.h += random.rand() * 7.0/10 * 1/self.level**2
#     print randomColor.mods
    return QColor(rgb(sum(randomColor.mods)%1,0.3,0.7))     

        
        
        
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
        
    def build(self,faultTree,square, level =1):
        
        square = [TreemapVis.border,TreemapVis.border,self.width()-TreemapVis.border*2, self.height()-TreemapVis.border*2]
        def subTreeValue(fault):
            total=fault.value() + sum([subTreeValue(subFault) for subFault in fault.connections])
            return total
        
        def recursive_build(faultList, square, level):
            
            mLevel = len(faultList[0].elements)
            x0,y0,xn,yn = square
            self.addOutline(x0,y0,xn,yn, mLevel)
            
            square = [x0+1,y0+1,xn-1,yn-1]
            if len(faultList) == 0:
                return None
            
            #lay out faults
            rectangles, leftovers = layout([subTreeValue(fault) for fault in faultList], square)
            
            flag = False;
            for el in rectangles:
                if len(el) < 1:
                    flag = True;
                    
            if flag:
                print('wait');
            #remove elements that are not in list (eg. rejected because of quantization or because they are smaller than 1/2 pixel)
            faultList = [el for index,el in enumerate(faultList) if index not in leftovers]
            
            if len(faultList) < len(rectangles):
            
                xa,ya,xb,yb = rectangles[len(faultList)]
                leftoverRect = Rectangle([xa,ya,xb-xa,yb-ya], parent=self, color=QColor(100,100,100));
                self.addOutline(xa,ya,xb,yb,mLevel+1)
            
            if mLevel >= level:
                #lay out faults and add a rectangle widget to each fault
                
                
                for fault,rectangle in zip(faultList,rectangles):
                    if len(rectangle) == 0:
                        print('pause')
                    xa,ya,xb,yb = rectangle
                    fault.addRectangle(self,[xa,ya, xb-xa, yb-ya])
                    self.addOutline(xa,ya,xb,yb,mLevel+1)
    #                 mWindow.addWidget(fault)
            else:
                """
                    There should be some limit here as to how small a rectangle
                    gets recursively built.
                """
                for fault, rectangle in zip(faultList, rectangles):
                    randomColor(len(fault.elements))
                    recursive_build(fault.connections, rectangle, level)
        
        recursive_build(faultTree[1], square, level)
    
class TreeMapFault(Fault):
    
    def __init__(self, listing, reduction):
        super(self.__class__, self).__init__(listing, reduction)
        self.visuals = []
        self.rectangles = []
    
    def toggleHighlight(self):
        for rect in self.rectangles:
            rect.toggleHighlight()
        
    def addRectangle(self, mWindow, pos):
        newRectangle = Rectangle(pos, parent=mWindow, fault=self)
        newRectangle.setColor(len(self.elements))
#         newRectangle.setFault(self)
        newRectangle.show()
        self.rectangles.append(newRectangle)
        return newRectangle
        
    
class Rectangle(QWidget):
    
    def __init__(self, pos, parent=None, fault=None, color=QColor(200,100,100)):
        
        super(self.__class__,self).__init__(parent)
        if parent != None: self.show()
        self.fault = fault
#         print self.fault
        xa,ya,xb,yb = pos
        xb,yb = xb+1,yb+1 #widget space is defined from left of xa to left of xb, I need to expand it to [left of xa, right of xb]. (same argument for y)
        self.setGeometry(*pos)
        self.color = color
        self.highlight = False
#         for element in self.fault.elements:
#             self.enterEvent.connect(element.toggleHighlight)
#             self.leaveEvent.connect(element.toggleHighlight)
    
    def setColor(self,level):
        self.color=randomColor(level)
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

    def paintEvent(self, e):
        
#         print 'Painted: ',self.geometry(), self.color
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        
        if self.highlight:
            r,b,g = self.color.red(), self.color.blue(), self.color.green()
            h,s,v = self.color.hue(), self.color.saturation(), self.color.value()
            intensity = 130
            painter.setBrush(QColor.fromHsv(h, s*0.6, 120))
        else:
            painter.setBrush(self.color)
#             painter.setPen(self.color)
#             painter.setBrush(Qt.NoBrush)
        painter.drawRect(QRectF(1,1,self.width()-1, self.height()-1)) #rectangles are drawn so that border ends on the right side of xb, but widgets end on the left side of xb. Thus, make rectangle one smaller. (ditto for y)
            #with Qt.NoPen, rectangle moves over and fills the space of the border, so we need to offset by 1
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
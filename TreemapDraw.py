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
        randomColor.mods = randomColor.mods[0:level-1] + [random.rand()*4.0/10 * 1/level]
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
    
    def paintEvent(self,e):
        super(self.__class__, self).paintEvent(e)
        for el in self.elements:
            el.draw(self)

    def mousePressEvent(self, e):
        for widget in self.widgets:
            print widget.geometry()
    
    def resizeEvent(self, e):
        print 'Resized!'
        
    def build(self,faultTree,square, level = 2):
        
        square = [TreemapVis.border,TreemapVis.border,self.width()-TreemapVis.border*2, self.height()-TreemapVis.border*2]
        def subTreeValue(fault):
            total=fault.value() + sum([subTreeValue(subFault) for subFault in fault.connections])
            return total
        
        def recursive_build(faultList, square, level):
    
            x0,y0,xn,yn = square
            square = [x0+1,y0+1,xn-1,yn-1]
            if len(faultList) == 0:
                return None
            
            #lay out faults
            rectangles = layout([subTreeValue(fault) for fault in faultList], square)
            if len(faultList[0].elements) >= level:
                #lay out faults and add a rectangle widget to each fault
                for fault,rectangle in zip(faultList,rectangles):
                    xa,ya,xb,yb = rectangle
                    fault.addRectangle(self,[xa,ya, xb-xa, yb-ya])
    #                 mWindow.addWidget(fault)
            else:
                for fault, rectangle in zip(faultList, rectangles):
                    randomColor(len(fault.elements))
                    recursive_build(fault.connections, rectangle, level)
        
        recursive_build(faultTree[1], square, level)
    
class TreeMapFault(Fault):
    
    def __init__(self, listing, reduction):
        super(self.__class__, self).__init__(listing, reduction)
        self.visuals = []
    
    def addRectangle(self, mWindow, pos):
        newRectangle = Rectangle(pos, parent=mWindow, fault=self)
        newRectangle.setColor(len(self.elements))
#         newRectangle.setFault(self)
        newRectangle.show()
        return newRectangle
        
    
class Rectangle(QWidget):
    
    def __init__(self, pos, parent=None, fault=None):
        
        super(self.__class__,self).__init__(parent)
        if parent != None: self.show()
        self.fault = fault
#         print self.fault
        self.setGeometry(*pos)
        self.color = QColor(200,100,100)
        
#         for element in self.fault.elements:
#             self.enterEvent.connect(element.toggleHighlight)
#             self.leaveEvent.connect(element.toggleHighlight)
    
    def setColor(self,level):
        self.color=randomColor(level)
    def enterEvent(self, e):
        for element in self.fault.elements:
            element.toggleHighlight()
    
    def leaveEvent(self, e):
        for element in self.fault.elements:
            element.toggleHighlight()

    def paintEvent(self, e):
        
#         print 'Painted: ',self.geometry(), self.color
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
#         painter.setBrush(Qt.NoBrush)
        painter.drawRect(1,1,self.width()-2, self.height()-2)
        painter.end()
    
    def setFault(self, fault):
        self.fault = fault
       

if __name__ == "__main__":
    app= QApplication(sys.argv)
    
    mWindow =TreemapVis()
    mRectangle = Rectangle([20,40,100,80], parent=mWindow)
    sys.exit(app.exec_())
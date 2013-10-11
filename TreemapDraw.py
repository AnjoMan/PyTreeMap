from PySide.QtCore import *
from PySide.QtGui import *
import sys
from PowerNetwork import *
import colorsys


def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate


@static_var('mods', [0])
def randomColor(level=1):
    def rgb(h,s,v): return '#%02X%02X%02X' % tuple( [ int(np.round(el*255)) for el in colorsys.hsv_to_rgb(h,s,v)])

    if level == 1:
        print randomColor.mods
        randomColor.mods = [(randomColor.mods[0] + 0.3)%1, 1]
    elif level > 1:
        randomColor.mods = randomColor.mods[0:level-1] + [np.random.rand()*4.0/10 * 1/level]
#         randomColor.h += np.random.rand() * 7.0/10 * 1/self.level**2
    print randomColor.mods
    return QColor(rgb(sum(randomColor.mods)%1,0.3,0.7))     

        
        
        
class Window(QWidget):
    
    def __init__(self):
        super(self.__class__, self).__init__()
        
        self.widgets = []
        self.setMouseTracking(True)
        self.setGeometry(100,100,900,900)
        self.setWindowTitle('Window')
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
    
class TreeMapFault(Fault):
    
    def __init__(self, listing, reduction):
        super(self.__class__, self).__init__(listing, reduction)
        self.visuals = []
    
    def addRectangle(self, mWindow, pos):
        newRectangle = Rectangle(pos, mWindow)
        newRectangle.setColor(len(self.elements))
        
    
class Rectangle(QWidget):
    
    def __init__(self, pos, parent=None):
        
        super(self.__class__,self).__init__(parent)
        if parent != None: self.show()
        self.setGeometry(*pos)
    
    def setColor(self,level):
        self.color=randomColor(level)
    def enterEvent(self, e):
        print 'Enter'
    
    def leaveEvent(self, e):
        print 'Leave'

    def paintEvent(self, e):
        
        print 'Painted: ',self.geometry(), self.color
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
    
    mWindow = Window()
    mRectangle = Rectangle([20,40,100,80], parent=mWindow)
    sys.exit(app.exec_())
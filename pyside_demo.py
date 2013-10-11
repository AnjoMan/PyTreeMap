

from PySide.QtCore import *
from PySide.QtGui import *
import sys
import colorsys
import numpy as np

class CustomRect(QWidget):
    
    def __init__(self,parent,pos=[20,20,100,80]):
        super(self.__class__, self).__init__(parent)
        x,y,x_,y_ = pos
        self.setMouseTracking(True)
        self.setGeometry(x,y,x_,y_)
        self.pos = pos
    
    def enterEvent(self, event):
        print 'Entered'
    
    def leaveEvent(self, event):
        print 'Exited'
    
    def paintEvent(self,ev):
        def rgb(h,s,v): return '#%02X%02X%02X' % tuple( [ int(np.round(el*255)) for el in colorsys.hsv_to_rgb(h,s,v)])
        
        painter = QPainter(self)
        x,y,x_,y_ = self.pos
        
        painter.setBrush(QColor(rgb(0,0.5,0.5)))
        painter.drawRect(x,y,x_-1,y_-1)
        
        painter.end()
        
        

class MyMainWindow(QMainWindow):
    def __init__(self,parent):
        super(self.__class__, self).__init__()
        
        self.block = CustomRect(self)
        self.setGeometry(300,300,800,600)
        self.setWindowTitle('Main Window')
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    sw = MyMainWindow(None)
    sys.exit(app.exec_())
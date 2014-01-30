from PySide.QtCore import *
from PySide.QtGui import *



import sys

class Rectangle(QWidget):
    
    def __init__(self,pos):
        super().__init__()
        
        xa,ya,xb,yb = pos
        
        xb,yb = xb+1,yb+1
        self.setGeometry(xa,ya,xb,yb)
    
    
    def paintEvent(self,e):
        
        
        
        painter = QPainter(self)
        painter.setBrush(QColor(200,100,100))
        painter.setPen(Qt.NoPen)
        
        painter.drawRect(QRectF(0,0,self.width()-1, self.height()-1))
        
        painter.end()
        
    def enterEvent(self,e):
        pos = QCursor.pos()
        print(pos)
        

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        self.widgets = []
        
        self.addWidget(Rectangle( [200,40,100,100]))
        self.setGeometry(100,100,400,400)
        self.show()
    
    
    def addWidget(self, widget):
#         print 'addedWidget'
        self.widgets += [widget]
        widget.setParent(self)
        widget.show()
        self.update()
        
    def paintEvent(self, e):
        
        
        painter = QPainter(self)
           
        painter.setBrush(Qt.NoBrush)
        painter.setPen(Qt.black)
        
        painter.drawLine(QLineF(40,0,40,400))
        painter.drawLine(QLineF(0,40,400,40))
        painter.drawLine(QLineF(0,140,400,140))
        painter.drawLine(QLineF(140,0,140,400))
        
        painter.drawLine(QLineF(200,0,200,400))
        painter.drawLine(QLineF(300,0,300,400))
        painter.setBrush(QColor(200,100,100))
        painter.setPen(Qt.NoPen)
        painter.drawRect(QRectF(40,40,100,100))
     
        
        
       
        
        
        
        painter.end()
    

if __name__ == '__main__':
    
    
    app = QApplication(sys.argv)
    
    
    
    ex = Example()
    
    
    
    sys.exit(app.exec_())

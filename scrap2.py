from PySide.QtGui import *
from PySide.QtCore import *
import sys


class Example(QWidget):
    
    def __init__(self):
        super(self.__class__, self).__init__()
        
        
        
        self.setGeometry(300,300,300,300)
        self.show()
        
        
    def paintEvent(self, e):
        painter = QPainter(self)
        
        
        
        
        painter.drawEllipse(30,30,50,50)
        
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.drawEllipse(QRect(100,50,50,50))
        
        painter.drawEllipse(QRectF(30.0,100.0,50.0,50.0))
        
        painter.end()


app = QApplication(sys.argv)



ex = Example()



sys.exit(app.exec_())
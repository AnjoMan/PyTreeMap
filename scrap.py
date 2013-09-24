from PySide import QtGui, QtCore

import sys




class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
    
    def initUI(self):
        
        self.setGeometry(300,300,250,250)
        self.setWindowTitle('Drawing Pies')
        self.show()
    
    def paintEvent(self,e):
        
        qp = QtGui.QPainter()
        
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.setBrush(QtGui.QColor('#19005A'))
        qp.setPen(QtGui.QColor(100,100,100))
        qp.drawPie( 100,100,80,80, 0, (16*360) * 0.3)
        qp.end() 



app = QtGui.QApplication(sys.argv)

ex = Example()



sys.exit(app.exec_())
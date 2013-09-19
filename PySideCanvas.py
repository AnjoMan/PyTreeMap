from PySide import *

class PySideCanvas(QtGui.QWidget):
    def __init__(self, width, height, title):
        super(PySideCanvas, self).__init__()
        self.initUI(width, height, title)
        self.rectangles = []
        self.colors = []
        self.outlines = []
        
        self.objs  = []
        
        
    def addRectangle(self, pos, color):
        self.rectangles += [pos]
        
        r,g,b = [color[1:3], color[3:5], color[5:7]]
        r,g,b = [int(num, 16) for num in [r,g,b]]
        self.colors += [QtGui.QColor(r,g,b)]
    
    def drawOutline(self, pos, border):
        if border > 0:
            self.outlines += [ [pos, border]]
            return True
        else: return False
    
    def initUI(self, width, height, title):
        sX = sY = 100
        scrollArea = QtGui.QScrollArea(self)
#         scrollArea.setWidget(self)
        self.setGeometry(sX,sY, sX+width, sX+height)
        self.setWindowTitle(title)
        self.show()
    
    def draw(self, item):
        #generic draw, in which the object implements a draw method with the pen
        self.objs += [item]
    
    def drawCircle(x,y,r):
        self.circles += [[ x,y,r]]
    def paintEvent(self, e):
        
        
        
        qp = QtGui.QPainter()
        qp.begin(self)
        
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        #draw rectangles
        
        for rectangle, color in zip(self.rectangles, self.colors):
            qp.setPen(color)
            qp.setBrush(color)
            x0,y0,xn,yn = rectangle
            qp.drawRect(x0,y0, xn-x0, yn-y0)
        
        #draw borders
        pen = QtGui.QPen(QtGui.QColor(10,10,10), 1, QtCore.Qt.SolidLine)
       
        for (x0,y0,xn,yn), border in self.outlines:
            segments = [ [ x0,y0, xn, y0], [x0,y0,x0,yn],[x0,yn,xn,yn], [xn,y0,xn,yn]]
            pen.setWidth(border)
            qp.setPen(pen)
            
            for x0,y0,xn,yn in segments:
                qp.drawLine(x0,y0,xn,yn)
        
        
        for obj in self.objs:
            obj.draw(self, qp)
        
        qp.end()
from PySide import *

class PySideCanvas(QtGui.QWidget):
    def __init__(self, width, height, title):
        super(PySideCanvas, self).__init__()
        self.initUI(width, height, title)
        self.rectangles = []
        self.colors = []
        self.outlines = []
        self.lines = []
        self.objs  = []
    
    def initUI(self, width, height, title):
        sX = sY = 100
        
        self.setGeometry(sX,sY, sX+width, sX+height)
        self.setWindowTitle(title)
        self.resize(width, height)
        self.show()
        
    def drawRectangle(self, pos, color):
        self.rectangles += [pos]
        
        self.colors += [PySideCanvas.qtColor(color)]
    
    @staticmethod
    def qtColor(colorString):
        r,g,b = [colorString[1:3],colorString[3:5], colorString[5:7]]
        r,g,b = [int(num,16) for num in [r,g,b]]
        return QtGui.QColor(r,g,b)
        
    def drawOutline(self, pos, border, color=None):
        if border > 0:
            self.outlines += [ [pos, border, (PySideCanvas.qtColor(color) if color else PySideCanvas.qtColor('#000000'))]]
            return True
        else: return False
    
    def drawLine(self, pos):
        self.lines += [pos]

    
    def draw(self, item):
        #generic draw, in which the object implements a draw method with the pen
        self.objs += [item]
    
    def drawCircle(x,y,r):
        self.circles += [[ x,y,r]]
    def paintEvent(self, e):
        
        
        
        qp = QtGui.QPainter()
        qp.begin(self)
        
#         qp.setRenderHint(QtGui.QPainter.Antialiasing)
        #draw rectangles
        
        for rectangle, color in zip(self.rectangles, self.colors):
            qp.setPen(color)
            qp.setBrush(color)
            x0,y0,xn,yn = rectangle
            qp.drawRect(x0,y0, xn-x0, yn-y0)
        
        #draw borders /outlines
        pen = QtGui.QPen(QtGui.QColor(10,10,10), 1, QtCore.Qt.SolidLine)
       
        for (x0,y0,xn,yn), border, color in self.outlines:
#             print color.red(), color.green(), color.blue()
            segments = [ [ x0,y0, xn, y0], [x0,y0,x0,yn],[x0,yn,xn,yn], [xn,y0,xn,yn]]
            pen.setColor(color)
            pen.setWidth(border)
            qp.setPen(pen)
            
            for x0,y0,xn,yn in segments:
                qp.drawLine(x0,y0,xn,yn)
        
        #draw lines
        qp.setRenderHint(QtGui.QPainter.Antialiasing,True)
        pen.setWidth(1)
        qp.setPen(pen)
        for x0,y0,xn,yn in self.lines:
            qp.drawLine(x0,y0,xn,yn)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, False)
        #draw objects
        for obj in self.objs:
            obj.draw(self, qp)
        
        qp.end()
from PySide import QtGui, QtCore
import math
import sys
import weakref
from numpy import *


class Node(QtGui.QGraphicsItem):
    Type = QtGui.QGraphicsItem.UserType+1
    
    def __init__(self, graphWidget, line):
        
        super(self.__class__, self).__init__()
        self.line = line
        
        print line
        self.graph = weakref.ref(graphWidget)
        
        self.newPos = QtCore.QPointF()
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setZValue(-1)
    
    def type(self): return Node.Type
    
    def advance(self): 
        if self.newPos == self.pos(): return false
        
        self.setPos(self.newPos); return True
        
    def boundingRect(self):
        adjust = 2.0
        return QtCore.QRectF(-10 - adjust, -10-adjust, 23+adjust, 23+adjust)
    
    def shape(self):
        (x0,y0), (xn,yn) = p0, pn = self.line
        
        dx,dy = xn-x0, yn-y0
        
        dV = np.array([dx,dy])
        mag_dV = linalg.norm(dV)
        
        rotation = array( [0,-1],[1,0]])
        
        p = [x0,y0] + dot(rotation, dV) * 3/nag_dV 
        path = QtGui.QPainterPath()
        path.addEllipse(-10,-10,20,20)
        return path
    
    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)
        painter.drawEllipse(-7,-7,20,20)
        
        gradient = QtGui.QRadialGradient(-3,-3,10)
        
        if option.state & QtGui.QStyle.State_Sunken:
            gradient.setCenter(3,3)
            gradient.setFocalPoint(3,3)
            gradient.setColorAt(1, QtGui.QColor(QtCore.Qt.yellow).lighter(120))
            gradient.setColorAt(0, QtGui.QColor(QtCore.Qt.darkYellow).lighter(120))
        else:
            gradient.setColorAt(0, QtCore.Qt.yellow)
            gradient.setColorAt(1, QtCore.Qt.darkYellow)
        
        painter.setBrush(QtGui.QBrush(gradient))
        painter.setPen(QtGui.QPen(QtCore.Qt.black,0))
        painter.drawEllipse(-10,-10,20,20)
    
    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemPositionChange:
            self.graph().itemMoved()
        
        return QtGui.QGraphicsItem.itemChange(self, change, value)
        
    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self,event)
    
    def mouseReleaseEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)
    
class GraphWidget(QtGui.QGraphicsView):
    def __init__(self):
        super(self.__class__, self).__init__()
        
        self.timerId = 0
        
        scene = QtGui.QGraphicsScene(self)
        scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        scene.setSceneRect(-200,-200,400,400)
        self.setScene(scene)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        
#         self.centerNode = Node(self, [[-100,-100],[0,-70], [0,0],[20,80]])
        self.centerNode = Node(self, [[-100,-100],[0,-70]])

        scene.addItem(self.centerNode)
        
        self.centerNode.setPos(0,0)
        self.scale(0.8,0.8)
        self.setMinimumSize(400,400)
        self.setWindowTitle(self.tr("Elastic Nodes"))
    
    def itemMoved(self):
        if not self.timerId:
            self.timerId = self.startTimer(1000/25)
    
    

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    QtCore.qsrand(QtCore.QTime(0,0,0).secsTo(QtCore.QTime.currentTime()))
    
    widget = GraphWidget()
    widget.show()
    
    sys.exit(app.exec_())
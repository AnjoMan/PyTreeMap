# from PySide import QtGui, QtCore
import math
import sys
import weakref
from numpy import *
from PySide.QtGui import *
from PySide.QtCore import *


class Node(QGraphicsItem):
    Type = QGraphicsItem.UserType+1
    
    def __init__(self, graphWidget, line):
        
        super(self.__class__, self).__init__()
        self.line = line
        
        print line
        self.graph = weakref.ref(graphWidget)
        self.radius = 1
        
        
        
        self.newPos = QPointF()
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setZValue(-1)
    
    def type(self): return Node.Type
    
    def advance(self): 
        if self.newPos == self.pos(): return false
        
        self.setPos(self.newPos); return True
        
    def boundingRect(self):
        adjust = 10.0
        x,y = array(self.line).transpose()
        rect = [min(x)-self.radius, min(y)-self.radius, max(x)-min(x)+2*self.radius, max(y)-min(y)+2*self.radius]
        
        print rect
#         return QRectF(-120,-120,100,100)
        return QRectF(*rect)
    
    def shape(self):
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        
        radius =  self.radius
        rotation = array( [[0,-1],[1,0]])
        
        points = zip(self.line[0:-1], self.line[1:])
        
        print points[0], points[1]
        for p0, pn in points:
            print "FUUUUUCK", p0, "YOOO",pn
            (x0,y0), (xn,yn) = p0, pn # = self.line[0], self.line[1]
            dx,dy = xn-x0, yn-y0
            
            dV = array([dx,dy])
            mag_dV = linalg.norm(dV)
            
            v = dot(rotation, dV) * radius / mag_dV
            startAngle = arctan2(*v) * 180/pi + 90
            
            
            
            path.moveTo(QPointF(*p0-v))
            
            path.arcTo(QRectF(x0-radius, y0-radius, 2*radius, 2*radius), startAngle, 180)
            path.lineTo(QPointF(*p0+v))
            path.lineTo(QPointF(*pn+v))
            path.lineTo(QPointF(*pn-v))

        path.arcTo(QRectF(xn-radius, yn-radius, 2*radius, 2*radius), startAngle + 180, 180)
        
        return path

    
    def paint(self, painter, option, widget):
        painter.setPen(Qt.darkGray)
        painter.setBrush(Qt.darkGray)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPath(self.shape())

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            self.graph().itemMoved()
        
        return QGraphicsItem.itemChange(self, change, value)
        
    def mousePressEvent(self, event):
        self.update()
        QGraphicsItem.mousePressEvent(self,event)
    
    def mouseReleaseEvent(self, event):
        self.update()
        QGraphicsItem.mouseReleaseEvent(self, event)
    
class GraphWidget(QGraphicsView):
    def __init__(self):
        super(self.__class__, self).__init__()
        
        self.timerId = 0
        
        scene = QGraphicsScene(self)
        scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        scene.setSceneRect(-200,-200,400,400)
        self.setScene(scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        
#         self.centerNode = Node(self, [[-100,-100],[0,-70], [0,0],[20,80]])
        self.centerNode = Node(self, [[-100,-100],[0,-70], [100, -100], [100,200]])
        self.secondNode = Node(self, [[-100,200], [-130,210], [100,200] ])
        scene.addItem(self.centerNode)
        scene.addItem(self.secondNode)
        
        
        self.centerNode.setPos(0,0)
        self.secondNode.setPos(0,0)
        self.scale(0.8,0.8)
        self.setMinimumSize(400,400)
        self.setWindowTitle(self.tr("Elastic Nodes"))
    
    def itemMoved(self):
        if not self.timerId:
            self.timerId = self.startTimer(1000/25)
    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qsrand(QTime(0,0,0).secsTo(QTime.currentTime()))
    
    widget = GraphWidget()
    widget.show()
    
    sys.exit(app.exec_())
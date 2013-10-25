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
        self.radius = 10
        
        
        
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
        
        radius =  10
        rotation = array( [[0,-1],[1,0]])
        
        def linePath(p0,pn, path, radius, rotation):
            (x0,y0), (xn,yn) = p0, pn = self.line[0], self.line[1]
            dx,dy = xn-x0, yn-y0
            
            dV = array([dx,dy])
            mag_dV = linalg.norm(dV)
            
            v = dot(rotation, dV) * radius / mag_dV
            startAngle = arctan2(*v) * 180/pi + 90
            
            
#             path = QPainterPath()
#             path.setFillRule(Qt.WindingFill)
            
            path.moveTo(*p0-v)
            path.lineTo(*p0+v)
            path.lineTo(*pn+v)
            path.lineTo(*pn-v)
            
            path.arcTo(xn-radius, yn-radius, 2*radius, 2*radius, startAngle + 180, 180)
            
            path.moveTo(*pn-v)
            path.moveTo(*p0-v)
            path.arcTo(x0-radius, y0-radius, 2*radius, 2*radius, startAngle, 180)
#             return path
        
        [linePath(p0,pn,path, radius, rotation) for p0,pn in zip( self.line[0:-1], self.line[1:])]
        
#         print len(paths)
#         path = paths.pop()
#         while len(paths) > 0:
#             path.intersected(paths.pop())
#         print path
        return path
        
        
        return path
#         paths = [ lineDraw(p0,pn, radius, rotation) for p0, pn in zip( self.line[0:-1], self.line[1:])]
        
#         return paths[0]
    #         path.addEllipse(x0-radius, y0-radius, 2*radius, 2*radius)
            
# #         return path
    
    def paint(self, painter, option, widget):
        painter.setPen(Qt.darkGray)
        painter.setBrush(Qt.darkGray)
        painter.drawPath(self.shape())
        
#         print self.line
#         (x0,y0), (xn,yn) = p0, pn = self.line[0:2]
#         
#         dx, dy = xn-x0, yn-y0
#         rotation = array( [[0,1],[-1,0]])
#         
#         dV = array([dx,dy])
#         mag_dV = linalg.norm(dV)
#         
#         radius = 10
#         
#         v = dot(rotation, dV) * radius / mag_dV
#         
#         p0, pn= array([x0, y0+100]), array([xn, yn+100])
#         
#         painter.setBrush(Qt.NoBrush)
#         startAngle = arctan2(v[0], v[1]) * 180/pi-90; print startAngle
#         painter.drawLine(QPoint(*p0), QPoint(*pn))
# #         painter.drawLine(QPoint(*p0), QPoint(*p0+v))
# #         painter.drawArc(p0[0] - radius, p0[1]-radius, 2*radius, 2*radius, startAngle*16, 180*16)
# 
#         painter.drawPoint(* p0+v)
# #         painter.drawPoint(* p0-v)
# #         painter.drawPoint(* pn+v)
# #         painter.drawPoint(* pn-v)
# #         painter.drawEllipse(* (list(p0-radius) + [2*radius]*2))
# #         painter.end()
        
    
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
        self.centerNode = Node(self, [[-100,-100],[0,-70], [100, -100]])

        scene.addItem(self.centerNode)
        
        self.centerNode.setPos(0,0)
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
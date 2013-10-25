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
            self.graph = weakref.ref(graphWidget)
            self.setFlag(QGraphicsItem.ItemIsMovable)
            self.newPos = QPointF()
            self.setZValue(-1)
        
        def boundingRect(self):
            adjust = 10.0
            return QRectF(self.line[0][0]-adjust, self.line[0][1]-adjust, 2*adjust + self.line[1][0]-self.line[0][0]+100,2*adjust+self.line[1][1]-self.line[0][1]+100)
        
        def shape(self):
            (x0,y0), (xn,yn) = p0, pn = self.line
            dx,dy = xn-x0, yn-y0
            dV = array([dx,dy])
            mag_dV = linalg.norm(dV)
            radius = 10
            rotation = array( [[0,-1],[1,0]])
            
            v = dot(rotation, dV) * radius / mag_dV
            
            startAngle = arctan2(*v) * 180/pi + 90
            
            
            path = QPainterPath()
            path.moveTo(*p0 - v)
            path.addEllipse( x0-radius, y0-radius, 2*radius, 2*radius)
            path.moveTo(*p0+v)
            
            path.lineTo( QPoint(*pn+v))
            
            path.arcTo( xn - radius, yn-radius, 2*radius, 2*radius, startAngle+180, 180)
            
    
            path.lineTo(QPoint(*p0-v))
            
            return path.simplified()
        
        def paint(self, painter, option, widget):
            painter.setPen(QPen(Qt.black))
            painter.setBrush(Qt.darkGray)
            painter.drawPath(self.shape())
        
        
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
            
            self.centerNode = Node(self, [[-100,-100],[0,-70]])
            scene.addItem(self.centerNode)
            
            self.centerNode.setPos(0,0)
            self.scale(0.8,0.8)
            self.setMinimumSize(400,400)
            self.setWindowTitle(self.tr("Elastic Nodes"))
        
        
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        qsrand(QTime(0,0,0).secsTo(QTime.currentTime()))
        
        widget = GraphWidget()
        widget.show()
        
        sys.exit(app.exec_())
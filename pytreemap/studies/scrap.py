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
            self.radius = 8
            
            if graphWidget != None:
                self.graph = weakref.ref(graphWidget)
            
            self.newPos = QPointF()
            self.setCacheMode(self.DeviceCoordinateCache)
            self.setZValue(-1)
        
        
    
        def boundingRect(self):
            adjust = 10.0
            x,y = array(self.line).transpose()
            rect = [min(x)-self.radius, min(y)-self.radius, max(x)-min(x)+2*self.radius, max(y)-min(y)+2*self.radius]
            
            return QRectF(*rect)
        
        def shape(self):
            path = QPainterPath()
            path.setFillRule(Qt.WindingFill)
    
            radius =  self.radius
            rotation = array( [[0,-1],[1,0]])
    
            points = zip(self.line[0:-1], self.line[1:])
            
            for p0, pn in points:
                (x0,y0),(xn,yn) = p0,pn
                dx,dy = array(pn) - array(p0)
                
                dV = array([dx,dy])
                mag_dV = linalg.norm(dV)
                
                v = dot(rotation, dV) * radius / mag_dV
                
                #starting circle
                path.addEllipse(QRectF(x0-radius, y0-radius, 2*radius, 2*radius))
                #rectangular part
                path.moveTo(QPointF(*p0-v))
                path.lineTo(QPointF(*pn-v))
                path.lineTo(QPointF(*pn+v))
                path.lineTo(QPointF(*p0+v))
    
            path.moveTo(QPointF(*pn))
            path.addEllipse(QRectF(xn-radius, yn-radius, 2*radius, 2*radius))
            
            return path.simplified()
    
        
        def paint(self, painter, option, widget):
            painter.setPen(Qt.black)
            painter.setBrush(Qt.darkGray)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.drawPath(self.shape())
        
        def setGraph(self, graph):
            self.graph = weakref.ref(graph)
            
    class GraphWidget(QGraphicsView):
        def __init__(self):
            super(self.__class__, self).__init__()
            
            self.timerId = 0
            
            scene = QGraphicsScene(self)
            scene.setItemIndexMethod(QGraphicsScene.NoIndex)
            scene.setSceneRect(0,0,880,880)
            self.setScene(scene)
            self.setCacheMode(QGraphicsView.CacheBackground)
            self.setRenderHint(QPainter.Antialiasing)
            self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
            self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
            
            self.centerNode = Node(self, [[50,50],[200,100], [500, 100], [700,700]])
            scene.addItem(self.centerNode)
            
            
            self.centerNode.setPos(0,0)
            self.setGeometry(100,100,900,900)
            self.setWindowTitle(self.tr("Elastic Nodes"))
            
        
        
        def addItem(self, item):
            self.item = item
            self.scene().addItem(item)
            item.setGraph(self)
            item.show()
        
        
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        qsrand(QTime(0,0,0).secsTo(QTime.currentTime()))
        
        widget = GraphWidget()
        widget.show()
        
    #     widget.addItem(Node(None,[[200, 200],[400,400],[400,800]]))
        
        sys.exit(app.exec_())
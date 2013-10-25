from PySide.QtCore import *
from PySide.QtGui import *
from numpy import *
import sys

class Example(QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()
        
        self.setGeometry(300,300,500,500)
        self.setWindowTitle('Drawing')
        self.show()
    
    def paintEvent(self, e):
        
#         painter =QPainter(self)
#         
#         p0, pn = (x0,y0), (xn,yn) = [200,200], [400,400]
#         
#         painter.setPen(QPen(Qt.black, 1, Qt.DashLine))
#         painter.setBrush(Qt.NoBrush)
#         painter.drawRect( x0-10,y0-10, xn-x0+20, yn-y0+20)
#         painter.drawLine( x0, y0, xn, yn)
#         
#         painter.setPen( QPen(Qt.darkGray, 1, Qt.SolidLine))
#         radius = 8
#         
#         dx,dy = xn-x0, yn-y0
#         
#         dV = array([dx,dy])
#         mag_dV = linalg.norm(dV)
#         
#         rotation = array( [[0,-1],[1,0]])
#         
#         v = dot(rotation, dV) * radius / mag_dV
#         
#         startAngle = -arctan2(*v) * 180/pi
#         
#         p = p0 + v
#         painter.drawArc( x0-radius, y0-radius, 2*radius, 2*radius,  16*startAngle, 16*(180) )
#         
#         painter.drawLine( QPoint(*p0+v), QPoint(*pn+v))
#         
#         painter.drawArc( xn - radius, yn-radius, 2*radius, 2*radius, 16*(startAngle+180), 16*180)
#         painter.drawLine(QPoint(*p0-v), QPoint(*pn-v))

        path = QPainterPath()
        
        path.moveTo(110,100)
        path.arcTo(90,90,20,20,0,90)
        
        painter = QPainter(self)
        
        painter.setPen(Qt.black)
        painter.drawPath(path)
        
        painter.end()


app = QApplication(sys.argv)

ex = Example()


sys.exit(app.exec_())
from PySide import QtGui, QtCore

import sys
import numpy as np
import colorsys

def randomColor():
    #generates a randomized rgb string color name
    h,s,v = np.random.rand(3)
    r,g,b = colorsys.hsv_to_rgb(h, s*0.6+0.3, v*0.6+0.4)
    return '#%02X%02X%02X' % (r*255, g*255, b*255)

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
    
    def initUI(self):
        
        self.setGeometry(1300,300,500,500)
        self.setWindowTitle('Drawing Pies')
        self.show()
        self.nPies = 4
        self.colors = [QtGui.QColor(randomColor()) for i in range(0,self.nPies)]
        print ['#%02X%02X%02X' %  (color.red(), color.green(), color.blue()) for color in self.colors]
    
    def paintEvent(self,e):
        
        qp = QtGui.QPainter()
        
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.setBrush(QtGui.QColor('#19005A'))
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 3))
        
        x,y = 250,250
        r = 200
        
        startAngle =0;
        arcAngle = 360.0/self.nPies
        
        def putText(qp,x,y,text):
#             qp.setPen(QtGui.QColor(0,0,0))
            metrics = qp.fontMetrics()
            fw,fh = metrics.width(text),metrics.height()
#           
            qp.drawText(x-fw/2,y+fh/4,text)
            
        for index,color in enumerate(self.colors):
            
            qp.setBrush(QtGui.QColor(color))
            
            qp.drawPie(x-r,y-r,2*r,2*r,16*startAngle, 16*arcAngle)
            
            
            
            xd = x + 1.0/2.0*r * np.cos(np.pi/180.0 * (startAngle + arcAngle/2.0))
            yd = y - 1.0/2.0*r * np.sin(np.pi/180.0 * (startAngle + arcAngle/2.0))
#             print startAngle, arcAngle, startAngle + arcAngle/2.0
            print index, round(xd), round(yd)
#             qp.drawPoint(xd,yd)
            putText(qp, xd,yd, str(index))
            
            
            startAngle += arcAngle
            
        
        #draw legend
        x = 460
        y = 10
        height = 20
        width = 40
        for index,color in enumerate(self.colors):
            qp.setPen(QtCore.Qt.NoPen)
            qp.setBrush(color)
            qp.drawRect(x,y,width,height)
            qp.setPen(QtGui.QPen( QtCore.Qt.white, 1))
            putText(qp, x+width/2.0, y+height/2.0, str(index) )
            y = y+height+2
            
        qp.end() 
        
        print '\n'



app = QtGui.QApplication(sys.argv)
ex = Example()
# sys.exit(app.exec_())
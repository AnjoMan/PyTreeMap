from PySide.QtGui import *
from PySide.QtCore import *
import sys

import colorsys
from numpy import *



def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate


@static_var('mods', [0])
def randomColor(level=1):
    def rgb(h,s,v): return '#%02X%02X%02X' % tuple( [ int(round(el*255)) for el in colorsys.hsv_to_rgb(h,s,v)])

    if level == 1:
#         print randomColor.mods
        randomColor.mods = [(randomColor.mods[0] + 0.3)%1, 1]
    elif level > 1:
        randomColor.mods = randomColor.mods[0:level-1] + [(random.rand()-0.5)*2.0/10 * 1/level]
#         randomColor.h += random.rand() * 7.0/10 * 1/self.level**2
#     print randomColor.mods
    return QColor(rgb(sum(randomColor.mods)%1,0.3,0.7))    






class Example(QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(300,300,500,500);
        self.show()
    
    
    def paintEvent(self,e):
        
        x1,x2 = 10,70
        
        painter = QPainter(self)
        painter.setPen(QColor(0,0,0))
        
        
        y = array(range(10,400,30))
        
        for y1,y2 in zip(y, y+30):
            painter.setBrush(randomColor(1))
            print( x1,y1,x2,y2)
            painter.drawRect(x1,y1,x2,y2)
            
            for level,xOffset in enumerate(range(70,700,70)):
                painter.setBrush(randomColor(3))
                painter.drawRect(x1+xOffset, y1, x2+xOffset, y2)
        painter.end()
        


app = QApplication(sys.argv)


ex = Example()


sys.exit(app.exec_())
from PySide.QtCore import *
from PySide.QtGui import *
import sys
from PowerNetwork import *
import colorsys
from numpy import *
from Treemap import layout



def main():
    
    app = QApplication(sys.argv)

    ex = TreemapGraphicsVis()
    
    sys.exit(app.exec_())














def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate

def randomColor(level=1, secondary = None):
    def rgb(h,s,v): return '#%02X%02X%02X' % tuple( [ int(round(el*255)) for el in colorsys.hsv_to_rgb(h,s,v)])

    
    h = 0.32*(1+level)%1
#     secondary = None
    if secondary is not None:
        
        s = (secondary**(1/2)) * 0.4 + 0.2
        v = (secondary**(1/2)) * 0.5 + 0.5
    else:
        s = 0.4
        v = 0.8 
    
    return QColor(rgb(h,s,v))
    



class TreemapGraphicsVis(QGraphicsView):
    border = 10;
    
    def __init__(self, pos=None, faultTree=None, values=[14, 1, 17, 14, 17, 18, 8, 8, 6, 10, 2, 1, 4, 9, 10, 0, 16, 13, 8, 12, 6, 17, 5, 1, 19, 4, 11, 16, 11, 5, 17, 16, 4, 7, 17, 14, 11, 16, 13, 19]):
        super().__init__()
        
        print('init runs')
        if not pos: pos = [50,50,900,900]
        
        (x,y,w,h) = pos
        self.resize(w,h)
        self.move(x,y)
        
        
        self.outlines = []
        self.widgets = []
#         self.elements = []
        
        
        self.scene = QGraphicsScene(self)
        self.setSceneRect(*pos)
            
            
#         if faultTree!=None:
#             self.build(faultTree,[10,10,900,900])
        
        self.build(values)
        
        
        self.setScene(self.scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHint(QPainter.Antialiasing)
        
        self.setWindowTitle('TreemapGraphics')
        self.show()
        self.scale(.9,.9)
    
    def addWidget(self,widget):
        self.widgets.append(widget)
        self.scene.addItem(widget)
    
    def addOutline(self, xa, ya, xb, yb, level):
        self.outlines.append( ((xa,ya,xb,yb),level) )

    def build(self,values):
        pos = self.sceneRect().getRect()
        
        x0,y0,w,h = pos
        
        rectangles, _ = layout(values, [x0,y0,x0+w,y0+h])
        
        for el in rectangles:
            xa,ya,xb,yb = el
            self.addWidget( Rectangle([xa,ya,xb-xa,yb-ya]))
            
class Rectangle(QGraphicsItem,object):
    
    
    def __init__(self, pos):
        super().__init__()
        
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        
        self.pos = QRectF(*pos)
        self.color = QColor(200,100,100)
    
#     def shape(self):
#         try:
#             return self.mShape
#         except:
#             self.mShape = self.defineShape()
#             return self.mShape
#     def defineShape(self):
#         x,y, w,h = self.pos.getRect()
#         x,y,w,h = x+1,y+1,w-2,h-2
#         path = QPainterPath()
#         path.moveTo(x,y)
#         path.addRect(QRectF(x,y,w,h))
#         return path
    def boundingRect(self):
        return QRectF(self.pos)
    
    def paint(self, painter, option, widget):
        mColor = self.color
        painter.setPen(Qt.black)
        painter.setBrush(mColor)
        painter.drawRect(self.pos)
                    

if __name__ == "__main__":
    main()
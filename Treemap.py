
import numpy as np
from collections import defaultdict
import colorsys


from PySide.QtGui import *
from PySide.QtCore import *


def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate
    

def randomColor():
    h,s,v = np.random.rand(3)
#     print h,s,v
    r,g,b = colorsys.hsv_to_rgb(h, s*0.6+0.3, v*0.4+0.5)
    return '#%02X%02X%02X' % (r*255, g*255, b*255)

@static_var('roundingError', 0)
def layColumn(values, pos, quantize=True, minBoxArea = 2):
    xa, ya, xb, yb = pos
    
    dX, dY = xb-xa, yb-ya
    
    if dY < 1.0 or dX < 1.0:
        return [], values, pos
    
    #colLength is the shorter dimension, boxes are lined up along this dimension
    colLength = dY if dY <= dX else dX
    
    #start with an empty list
    a =[]
    aspect = []
    
    def fitValues(values, Y):
        #take a set of values and a column (row) length, and produce the column (row) width and box height (widths)
        try:
            x = sum(values)/Y
        except:
            pass
        ys = np.array(values)/x
        aspect = x/ys# *x/sum(x)
        return x,ys, aspect
    
    #keep the last two box elements
    save = []
    while (len(save) < 1 or save[-1]['aspect'] < 1) and len(values) > 0:
        #take an element out of values and add it to the column
        a += [values.pop()]
        
        #get colWidth, length of each box and aspect ratio of each box
        colWidth, box, aspectRatios = fitValues(a,colLength)
        
        #save average aspect ratio and length of each box.
        save.append( {'aspect': np.average(aspectRatios), 'box':box, 'colWidth': colWidth } )
        
#         #only keep the last two aspect ratio/box combinations
        if len(save) > 2:
            save.pop(0)
    
    
    #check to see which of the closest 2 columns has best aspect ratio
    minAspect, index = min(  (asp, ind) for ind, asp in enumerate(abs(1-np.array([el['aspect'] for el in save]))))
    
    if index < ( len(save) - 1):
        values.append(a.pop())

    boxLengths, colWidth = save[index]['box'], save[index]['colWidth']
    
    
    
    #if values is empty, we need to enforce that colWidth pushes exactly to border
    if len(values)<1:
        colWidth = dX if dY <dX else dY
        
        
    if quantize:
        """ we need to quantize the treemap to integer values in order to draw
            borders between blocks.
            
            When we quantize, we need to manage our rounding errors to ensure 
            that they do not propegate - otherwise we end up with overflowing
            boxes or a large gap at the end.
        """
        
        modValue = colWidth + layColumn.roundingError #incorporate accumulated rounding error into column width
        
        if modValue <2.5: 
            """
                If modValue < 0.5, we get divide-by-zero error and the output
                will not make any sense. This is the hard limit on when we have
                to substitute values with one summary block.
                
                Practically we limit to modValue > 2.5 because below a column
                width of 3, there will be no box between the boundaries.
            """
            while a:
                values.append(a.pop())
            return [], values, pos
        
        layColumn.roundingError += colWidth - np.round(modValue) #update accumulated error to reflect deviation from optimal colWidth
        colWidth = np.round(modValue) #round modified column width
        
        if colWidth > (dY if dY > dX else dX):
            colWidth = dY if dY>dX else dX
            
        boxLengths = np.array(a)/colWidth #recalculate box lengths based on the new column width
#         boxLengths = boxLengths - layColumn.roundingError * colLength / len(boxLengths)
        boxLengths = np.round(boxLengths) #round to integer value
        boxLengths[-1] = boxLengths[-1] + (colLength - sum(boxLengths)) #absorb rounding error into the smallest box in the row to preserve column length
    
    #lay out box dimensions
    if dY <= dX:
        boxPositions = [ [xa    , ya + y, min(xa + colWidth, xb), min(ya+y+dy,      yb)] for y, dy in zip(np.cumsum( [0] + list(boxLengths[0:-1])), boxLengths) ]
        nextBox = [xa + colWidth, ya, xb, yb]
    else:
        boxPositions = [ [xa + x, ya    , min(xa + x + dx,   xb), min(ya + colWidth,yb)] for x, dx in zip(np.cumsum( [0] + list(boxLengths[0:-1])), boxLengths) ]
        nextBox = [xa, ya+colWidth, xb, yb]
    
    
    
    
    """ Here we set a minimum box size below which we don't draw blocks. As blocks
        in the Treemap get small (into the single-pixel dimensions e.g. 4x4),
        the effects of rounding error become large relative to the box area and we
        prefer to replace the smallest boxes with a generic.
        
    """
    
    areas = [(xn-x0)*(yn-y0) for x0,y0,xn,yn in boxPositions]
    if max(areas) < minBoxArea:
        while a:
            values.append(a.pop());
        
        return [], values, pos #returning boxPos = [] indicates that no values were laid out and nextBox should be used as a summary for small insignificant values
# 
    boxPositions.reverse()
    return boxPositions, values, nextBox

# def positionRectangles(pos, ys):
#     x0, y0, xn, yn = pos
#     return [ [x0, y0+y, x, y0+y+dy] for y, dy in zip( np.cumsum([0] + list( ys[0:-1] )), ys)]






#draw outline

@static_var('blocks_summarized',0)
def layout(values, pos, quantize=True, ):
    
    nValues = len(values)
    
    #scale values to fill the given area
    values = np.array(values) * (pos[2]-pos[0])*(pos[3]-pos[1]) /sum([val for val in values if val > 0])
    
    #sort values from smallest to largest (so you can .pop() the biggest value), get indexes
    values, origIndexes = zip( *sorted(zip(list(values), range(len(values)))))
    
    values, origIndexes = list(values), list(origIndexes)
   
    desiredArea = sum(values);
    rectangles = []
    nextBox = pos
    boxPos = pos
    
    col = 0;
    
    
    origIndexes_rect = []
        #track original indexes of values that have been laid out in the treemap
    
    while len(values) > 0 and boxPos:
        boxPos, values, nextBox = layColumn(values, nextBox,quantize=quantize, minBoxArea = 4*4)
            #fit the next x values into a row/column
            
        if nextBox:
            rectangles = boxPos + rectangles
        
        origIndexes_rect = origIndexes[len(origIndexes)-len(boxPos):] + origIndexes_rect
        origIndexes = origIndexes[0:len(origIndexes)-len(boxPos)]
        col += 1
    
    if len(values) > 1 and not boxPos: #we need to do a fill box
        rectangles = [[]]*len(origIndexes) + rectangles  #pad rectangles with empty - indicates these have been replaced
        origIndexes_rect = origIndexes + origIndexes_rect #add indexes of leftover rectangles
        
        rectangles.append(nextBox)
        origIndexes_rect.append(nValues)
    
    elif len(values) == 1: #we don't need a fill box but layColumns quit early and boxPos is empty
        rectangles.insert(0,nextBox)
        origIndexes_rect = origIndexes + origIndexes_rect
        origIndexes = []
    
    origIndexes_rect, rectangles = zip(*sorted( zip(origIndexes_rect, rectangles)))
    
#     layout.blocks_summarized += len(origIndexes)
#     print('<Treemap.layout> blocks summarized: {}'.format(layout.blocks_summarized))
    return list(rectangles), list(origIndexes)
    
    







@static_var('mods', [0])
def randomColor(level=1):
    def rgb(h,s,v): return '#%02X%02X%02X' % tuple( [ int(round(el*255)) for el in colorsys.hsv_to_rgb(h,s,v)])

    if level == 1:
#         print randomColor.mods
        randomColor.mods = [(randomColor.mods[0] + 0.3)%1, 1]
    elif level > 1:
        randomColor.mods = randomColor.mods[0:level-1] + [(random.rand()-0.5)*4.0/10 * 1/level]
#         randomColor.h += random.rand() * 7.0/10 * 1/self.level**2
#     print randomColor.mods
    return QColor(rgb(sum(randomColor.mods)%1,0.3,0.7))     












class TestCanvas(QWidget):
    def __init__(self, pos):
        
        super().__init__()
        self.rectangles = []
        self.setGeometry(*pos)
        
        self.show()
        
    def addRect(self, rect):
        self.rectangles.append(rect)
        
    
    def paintEvent(self,e):
        
        painter = QPainter(self)
        
        for rect in self.rectangles:
            xa,ya,xb,yb = rect
            
            rect = xa,ya,xb-xa,yb-ya
            painter.setBrush(randomColor())
            painter.drawRect(QRect(*rect))





def main():
    import sys
    app=QApplication(sys.argv)
    width, height = 900, 900


    canvas = TestCanvas([100,100,900,900])

    x0, y0, xn, yn = pos = [10,10,800,800]

 
#     values = np.random.rand(20)
    values = [61.604163314943435, 294.6813017301497, 93.649276939196398, 112.70697780452326, 88.953116126775967, 97.039574700870162, 137.10143908004227, 89.092705912171823, 97.275641027366532, 58.075842761050581, 333.70787878589113, 79.082361864220388, 65.173822806601834, 61.620466443905116, 79.0610858923568, 119.15194594331513, 157.76307523648643, 83.495491052375769, 146.8211675408229, 62.277396872459576, 59.428178065922452, 67.902811582920208, -9.3029028577009285, -8.7962074508714068, 14.208160768913103, 101.8804773503449, 73.045427399512732, 64.955629666655113, 83.746037258431556, 197.25455362773596, 67.215787200178852, 64.870088543368524, 61.454496111136791, 68.981997349090875, 65.545621430207575, 87.484672267841347, 98.503136492634326, 192.05389943959915, 60.262705723778026, 60.522842879217364, 64.049680842453768]
    
    values = np.array(values)
    
    rectangles = layout(values, pos)
    
    
    for rect in rectangles:
        print(rect)
        canvas.addRect(rect)
        
    
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


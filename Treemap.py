import Tkinter as Tk
import numpy as np
from collections import defaultdict



def randomColor():
    r,g,b = np.random.rand(3)
    return '#%02X%02X%02X' % (r*255, g*255, b*255)

def layColumn(values, pos):
    
    print len(values)
    xa, ya, xb, yb = pos

    dX, dY = xb-xa, yb-ya
    print dX*dY, sum(values)
    
    #colLength is the shorter dimension, boxes are lined up along this dimension
    colLength = dY if dY <= dX else dX
    #start with an empty list
    a =[]
    
    aspect = []
    
    def fitValues(values, Y):
        #take a set of boxes of 
        x = sum(values)/Y
        ys = np.array(values)/x
        aspect = x/ys
        return x,ys, aspect
    
    #keep the last two box elements
    save = []
    while len(save) < 1 or save[-1]['aspect'] < 1:
        
        if len(values) == 0:
            break
            
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
    
    boxLengths = save[index]['box']
    colWidth = save[index]['colWidth']
    
    #lay out box dimensions
    if dY <= dX:
        boxPositions = [ [xa    , ya + y, xa + colWidth, ya+y+dy      ] for y, dy in zip(np.cumsum( [0] + list(boxLengths[0:-1])), boxLengths) ]
        nextBox = [xa + colWidth, ya, xb, yb]
    else:
        boxPositions = [ [xa + x, ya    , xa + x + dx  , ya + colWidth] for x, dx in zip(np.cumsum( [0] + list(boxLengths[0:-1])), boxLengths) ]
        nextBox = [xa, ya+colWidth, xb, yb]
    
    if abs(dX*dY - sum( [(xn-x0)*(yn-y0) for x0,y0, xn,yn in boxPositions]) - sum(values)) >1:
        import pdb; pdb.set_trace()
    
    print dX*dY - sum( [(xn-x0)*(yn-y0) for x0,y0, xn,yn in boxPositions]), sum(values)
    return boxPositions, values, nextBox

# def positionRectangles(pos, ys):
#     x0, y0, xn, yn = pos
#     return [ [x0, y0+y, x, y0+y+dy] for y, dy in zip( np.cumsum([0] + list( ys[0:-1] )), ys)]


#draw outline


def layout(values, pos):
    
    #scale values to fill the given area
    values = np.array(values) * (pos[2]-pos[0])*(pos[3]-pos[1]) /sum(values)
    #sort values from smallest to largest (so you can .pop() the biggest value)
    values = sorted(list(values))
    
    
    
    rectangles = []
    nextBox = pos
    
    while len(values) > 0:
        boxPos, values, nextBox = layColumn(values,  nextBox)
        rectangles += boxPos
    
    return rectangles


def main():
    master = Tk.Tk()
    master.title("Arranging a treemap")

    width, height = 900, 900


    myCanvas = Tk.Canvas(master, width=width, height=height)
    myCanvas.pack()

    x0, y0, xn, yn = pos = [10,10,890,890]

    myCanvas.create_rectangle(x0-1,y0-1,xn+1,yn+1, fill='#AAAAAA')
    
    X = xn-x0
    Y = yn-y0
    values = np.random.rand(20)
    
    values = np.array(values)
    
    rectangles = layout(values, pos)
    
    
    for xa,ya,xb,yb in rectangles:
        myCanvas.create_rectangle(xa,ya,xb,yb, fill=randomColor())


if __name__ == "__main__":
    main()



import numpy as np
from collections import defaultdict
import colorsys


def randomColor():
    h,s,v = np.random.rand(3)
#     print h,s,v
    r,g,b = colorsys.hsv_to_rgb(h, s*0.6+0.3, v*0.4+0.5)
    return '#%02X%02X%02X' % (r*255, g*255, b*255)

def layColumn(values, pos):
    xa, ya, xb, yb = pos
    
    dX, dY = xb-xa, yb-ya
    
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
    
    #lay out box dimensions
    if dY <= dX:
        boxPositions = [ [xa    , ya + y, xa + colWidth, ya+y+dy      ] for y, dy in zip(np.cumsum( [0] + list(boxLengths[0:-1])), boxLengths) ]
        nextBox = [xa + colWidth, ya, xb, yb]
    else:
        boxPositions = [ [xa + x, ya    , xa + x + dx  , ya + colWidth] for x, dx in zip(np.cumsum( [0] + list(boxLengths[0:-1])), boxLengths) ]
        nextBox = [xa, ya+colWidth, xb, yb]
    
    return boxPositions, values, nextBox

# def positionRectangles(pos, ys):
#     x0, y0, xn, yn = pos
#     return [ [x0, y0+y, x, y0+y+dy] for y, dy in zip( np.cumsum([0] + list( ys[0:-1] )), ys)]


#draw outline


def layout(values, pos):
    
    #filter out negative valuese
    values = [val for val in values if val > 0]
    
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
#     values = np.random.rand(20)
    values = [61.604163314943435, 294.6813017301497, 93.649276939196398, 112.70697780452326, 88.953116126775967, 97.039574700870162, 137.10143908004227, 89.092705912171823, 97.275641027366532, 58.075842761050581, 333.70787878589113, 79.082361864220388, 65.173822806601834, 61.620466443905116, 79.0610858923568, 119.15194594331513, 157.76307523648643, 83.495491052375769, 146.8211675408229, 62.277396872459576, 59.428178065922452, 67.902811582920208, -9.3029028577009285, -8.7962074508714068, 14.208160768913103, 101.8804773503449, 73.045427399512732, 64.955629666655113, 83.746037258431556, 197.25455362773596, 67.215787200178852, 64.870088543368524, 61.454496111136791, 68.981997349090875, 65.545621430207575, 87.484672267841347, 98.503136492634326, 192.05389943959915, 60.262705723778026, 60.522842879217364, 64.049680842453768]
    
    values = np.array(values)
    
    rectangles = layout(values, pos)
    
    
    for xa,ya,xb,yb in rectangles:
        myCanvas.create_rectangle(xa,ya,xb,yb, fill=randomColor())


if __name__ == "__main__":
    main()


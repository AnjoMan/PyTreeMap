import Tkinter as Tk
import os
import random
import scipy.io
import numpy as np

fileName = os.path.join("C:\\","Users","Anton", "Development","Visualization","PyTreeMap", "avgRectangles.txt");




def drawTreeMap(myCanvas, pos, rectangles, sliver=0, colorSeed="#7F7F7F"):

    clamp = lambda x, low, high: min(high, max(low, x))
    colorBase= [clamp(int(x,16), 76, 255-76) for x in [colorSeed[1:3], colorSeed[3:5], colorSeed[5:]]]
    
#         box = box[ [1,0,3,2] ]
    
    r = lambda: random.randint(0,75)
    
    x0,y0,xn,yn = pos
    
    width, height = xn-x0, yn-y0
    
    
    outerCorners = np.transpose(np.vstack( ( rectangles[:,0] + rectangles[:,2], rectangles[:,1]+ rectangles[:,3]) ))
    rectangles[:,0] = rectangles[:,0] / outerCorners[:,0].max()
    rectangles[:,2] = rectangles[:,2] / outerCorners[:,0].max()
    rectangles[:,1] = rectangles[:,1] / outerCorners[:,1].max()
    rectangles[:,3] = rectangles[:,3] / outerCorners[:,1].max()
    
    for box in rectangles:
        x1,y1 = x0 + box[0] * width + sliver, y0 + box[1]*height + sliver
        x2,y2 = x1 + width * box[2] - 2* sliver, y1 + height * box[3]  - 2* sliver
        x1,y1 = clamp(x1, x0+sliver, xn-sliver), clamp(y1, y0+sliver,yn-sliver)
        x2,y2 = clamp(x2, x0+sliver, xn-sliver), clamp(y2, y0+sliver,yn-sliver)
        
        color = ('#%02X%02X%02X' % (r()+colorBase[0],r()+colorBase[1],r()+colorBase[2]))
        myCanvas.create_rectangle(x1,y1,x2,y2, fill=color, width=0)



#end drawTreeMap


layouts = scipy.io.loadmat('treemapLayouts.mat')["treemapLayouts"][0]

masterLayout = layouts[0];
sublayouts = layouts[1:];


xWide, xHigh = 800, 800
space = 10;
sliver = 0;

    
corners = lambda points: [space + points[0]*(xWide-2*space)+sliver, space + points[1]*(xHigh-2*space)+sliver, space + (points[0]+points[2])*(xWide-2*space)-2*sliver, space +(points[1]+points[3])*(xHigh-2*space)-2*sliver]

r = lambda: random.randint(76, 255-76)
color = lambda: ('#%02X%02X%02X' % (r(),r(),r()))


master = Tk.Tk();
myCanvas = Tk.Canvas(master, width=xWide+2*space, height=xHigh+2*space)
myCanvas.pack()

for index,box in enumerate(masterLayout):
    drawTreeMap(myCanvas, corners(box), sublayouts[index], colorSeed=color(), sliver=0)

# n = 9;
# index,box = n, masterLayout[n]
# drawTreeMap(myCanvas, corners(box), sublayouts[index], colorSeed=color(), sliver=0)
Tk.mainloop()



# drawTreeMap(myCanvas, corners([0,0,1,1]), masterLayout)



# print rectangle





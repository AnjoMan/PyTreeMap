import Tkinter as Tk
import numpy as np
import colorsys
master = Tk.Tk()
master.title("Arranging a treemap")

width, height = 900, 900
x0,y0, xn,yn = 10, 10, 890, 890
myCanvas = Tk.Canvas(master, width=width, height=height)
myCanvas.pack()

#decorator to attach values to a function definition
def static_var(varname, value):
    def decorate(func):
        setattr(func,varname,value)
        return func
    return decorate

@static_var("seed", 0)
@static_var("gcr", 0.618033988749895)
def rand(num = 1):
    result = []
    for i in range(0,num):
        rand.seed += 2/(1+np.sqrt(5))
        rand.seed %= 1
        result.append(rand.seed)
    
    return result
    
    


def randomColor():

    r,g,b = np.random.rand(3)
    return '#%02X%02X%02X' % (r*255, g*255, b*255)

def randomHSV():
    
    h,s,v = np.random.rand(3)
    r,g,b = colorsys.hsv_to_rgb(h,s,v)
    
    return '#%02X%02X%02X' % (r*255, g*255, b*255)

def randomRGB():
    r,g,b = np.random.rand(3)
    
    return '#%02X%02X%02X' % (r*255, g*255, b*255)

def hsvColor(i):
    print i
    h,s,v = i, 0.5,0.9
    r,g,b = colorsys.hsv_to_rgb(h,s,v)
    
    return '#%02X%02X%02X' % (r*255, g*255, b*255)



rHeight, rWidth = 015, 50;

for i in range(1,60):
    myCanvas.create_rectangle(x0, y0+ i * rHeight, x0+rWidth, y0+rHeight * (i+1), fill = randomRGB())


for i in range(1,60):
    myCanvas.create_rectangle(x0 + rWidth, y0+ i * rHeight, x0+rWidth*2, y0+rHeight * (i+1), fill = randomHSV())
    
for i in range(1,60):
    myCanvas.create_rectangle(x0 + rWidth*2, y0 + i * rHeight, x0+rWidth*3, y0+rHeight*(i+1), fill = hsvColor(i/60.0))
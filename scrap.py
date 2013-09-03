import Tkinter as Tk
import numpy as np

master = Tk.Tk()
master.title("Arranging a treemap")

width, height = 900, 900

x0,y0,xn,yn = pos = [10,10,890,890]

myCanvas = Tk.Canvas(master, width=width, height=height)
myCanvas.pack()


def randomColor():
    r,g,b = np.random.rand(3)
    return '#%02X%02X%02X' % (r*255, g*255, b*255)



myCanvas.create_rectangle(x0-1,y0-1,xn+1,yn+1, fill=randomColor())

X,Y = xn-x0, yn-y0



# values = np.random.rand(20)

# values = np.array(values)
# values = values * X*Y /sum(values)
values = sorted(values, key=lambda x: 1/x)
a = values[0:3]

x = sum(a)/Y


ys = a/x


posB = [ [x0, y0+y, x, y0+y+dy ] for y, dy in zip( np.cumsum(np.append([0], ys[0:-1])), ys)]

for xa,ya,xb,yb in posB:
    myCanvas.create_rectangle(xa,ya,xb,yb, fill=randomColor())
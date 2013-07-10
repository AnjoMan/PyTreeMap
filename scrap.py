import Tkinter as Tk
import numpy as np
import colorsys












master = Tk.Tk()


myCanvas = Tk.Canvas(master, width=300, height=650)

myCanvas.pack()

for num in range(0,255, 10):
    myCanvas.create_rectangle(10, 10 + num, 100, 10+2*num, fill = '#%02X%02X%02X' % (num,num,num))

import Tkinter as Tk
import numpy as np
import colorsys












master = Tk.Tk()


myCanvas = Tk.Canvas(master, width=300, height=650)

myCanvas.pack()

myCanvas.create_rectangle(10,10,40,100, width=3, fill= '#AA0000')
# myCanvas.create_rectangle(10,10,40,100, width=3)

myCanvas.create_rectangle(40,10,80,120, width=3, fill='#00AA00')

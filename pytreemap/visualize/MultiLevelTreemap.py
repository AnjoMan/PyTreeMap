"""
    written by Anton Lodder 2012-2014
    all rights reserved.
    
    This software is the property of the author and may not be copied,
    sold or redistributed without expressed consent of the author.
"""

if __name__ == '__main__':
    import sys, os, inspect
    try:
        import pytreemap
    except:
        #walk up to 'pytreemap' and add to path.
        realpath = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
        (realpath, filename) = os.path.split(realpath)
        while filename != 'pytreemap':
            (realpath, filename) = os.path.split(realpath)
        sys.path.append(realpath)
        import pytreemap

from PySide.QtCore import *
from PySide.QtGui import *
from PowerNetwork import *
from numpy import *
from Treemap import layout
from VisBuilder import *

from TreemapGraphics import *


def main():
    
    
    file = 'cpfResults_4branches'
    
    
    (faults, faultTree) = getFaults(TreemapFault, CPFfile(file))
    
    
    
    app = QApplication(sys.argv)
    
    ex = TreemapGraphicsVis(pos = [100,100,1100,700],faultTree = faultTree)
    
    sys.exit(app.exec_())
    
    
    
    
    
    
if __name__ == "__main__":
    main()
    
    
    
def MultiLevel(QGraphicsView):
    
    def __init__(self, file = None):
        
        
        super().init()
        
        
        file = 'cpfResults_4branches'
        
        (faults, faultTree) = getFaults(TreemapFault, CPFfile(file))
        
        
        ex = TreemapGraphicsVs(pos = [10,10,700,700], faultTree = faultTree)
        
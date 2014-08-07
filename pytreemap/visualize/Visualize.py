"""
    written by Anton Lodder 2012-2014
    all rights reserved.
    
    This software is the property of the author and may not be copied,
    sold or redistributed without expressed consent of the author.
"""

import scipy.io
import numpy as np
# from mlabwrap import mlab
import colorsys
from collections import defaultdict



from PowerNetwork import *
from Treemap import layout
from FaultTree import *
from TreemapDraw import *
import sys
from PySide import QtGui, QtCore

from VisBuilder import *



## sample files for Tree

file = 'cpfResults_4branch'
# file = 'cpfResults_treemap'

## sample files for Treemap
# file = 'cpfResults_mid'
# file ='cpfResults_med'
file = 'cpfResults_case30_2level'
# file = 'cpfResults_case30_full_3_levels'
# file = 'cpfResults_case30_full_2'

# file = 'cpfResults_case30_1level'


# file = 'cpfResults_case118'
# file = 'cpfResults_case118_full_1level'
# file = 'cpfResults_case118_1level'
# file = 'cpfResults_case118_2level'



depth = 2


print("\n\n\n")


    
# import cProfile
# pr = cProfile.Profile()





mCPFfile = CPFfile(file)

elements = mCPFfile.getElements()













width, height=  1700,800






 


class Visualization(QMainWindow):
    
    def __init__(self, treemap = None, oneline = None):
        super(self.__class__, self).__init__()
        
        
        self.widget = QWidget()
        
        self.oneline = oneline
        self.treemap = treemap
        
        self.treemap.setParent(self.widget)
        self.oneline.setParent(self.widget)
#         
#         hbox = QHBoxLayout()
#         hbox.addWidget(self.treemap)
#         hbox.addWidget(self.oneline)
#         self.widget.setLayout(hbox)
        
        self.treemap.setGeometry(0,0,900,900)
        self.oneline.setGeometry(900,0,900,900)
        self.setCentralWidget(self.widget)
#         self.setLayout(hbox)
        self.setGeometry(20,20,1800,950)
        self.setWindowTitle('Visualize')
        
#         self.treemap.show()
#         self.oneline.show()
        self.show()
        
        log('visualization created')
    
    
    def createView(self, scene):
        
        view = QGraphicsView(scene)
        
        view.setCacheMode(QGraphicsView.CacheBackground)
        view.setRenderHint(QPainter.Antialiasing)
        view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
#         self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
    
        return view

if __name__ == '__main__':
    
    
    
    ## draw a responsive treemap diagram
    
    
    (faults, faultTree) = getFaults(TreeMapFault, mCPFfile, filter=0)
    oneLineList = mCPFfile.Branches + mCPFfile.Buses # order is important here.
    
    app = QtGui.QApplication(sys.argv)
    mOneline = OneLineWidget([0,30,900,900],oneLineList)
    
    mTreemap = None
    mTreemap = TreemapVis(pos = [50,50,900,900],faultTree=faultTree)
    mVis = Visualization( oneline = mOneline, treemap=mTreemap) 
    
    sys.exit(app.exec_())
    
        
        
    ## draw a  tree diagram
    
    
    
#     
#     (faults, faultTree) = getFaults(TreeFault, CPFbranches, loads, baseLoad, filter=0)
#     
#     app = QtGui.QApplication(sys.argv)
#     mTreeVis = TreeVis(faultTree=faultTree, pos=[10,10,1800,1000])
#     sys.exit(app.exec_())
    

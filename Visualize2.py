
# from mlabwrap import mlab



from PowerNetwork import *
from FaultTree import *
# from TreemapDraw import *

from TreemapGraphics import TreemapGraphicsVis, TreemapFault
from VisBuilder import *
import sys
from PySide import QtGui, QtCore


## alternative import:
# from TreemapGraphics import TreemapGraphicsVis,TreemapFault
# from VisBuilder import CPFfile, getFaults
# from PowerNetwork import *

def main():
    ## sample files for Tree

    file = 'cpfResults_4branch'
    # file = 'cpfResults_treemap'
    
    ## sample files for Treemap
    # file = 'cpfResults_mid'
    # file ='cpfResults_med'
    # file = 'cpfResults_case30_2level'
    # file = 'cpfResults_case30_full_3_levels'
    # file = 'cpfResults_case30_full_2'
    
    # file = 'cpfResults_case30_1level'
    
    
    # file = 'cpfResults_case118'
    # file = 'cpfResults_case118_full_1level'
    # file = 'cpfResults_case118_1level'
#     file = 'cpfResults_case118_2level'
    
    
    
    depth = 2
    print("\n\n\n")
    
    
    mCPFfile = CPFfile(file)
    elements = mCPFfile.getElements()
    
    width, height=  1700,800

     
    ## draw a responsive treemap diagram
    
    
    (faults, faultTree) = getFaults(TreemapFault, mCPFfile)
    oneLineList = mCPFfile.Branches + mCPFfile.Buses # order is important here.
    
    app = QtGui.QApplication(sys.argv)
    mOneline = OneLineWidget([0,30,900,900],oneLineList)
    
    mTreemap = None
    mTreemap = TreemapGraphicsVis(pos = [50,50,900,900],faultTree=faultTree)
    mVis = Visualization( oneline = mOneline, treemap=mTreemap) 
    
    sys.exit(app.exec_())
    
        
        
    ## draw a  tree diagram
    
    
    
#     
#     (faults, faultTree) = getFaults(TreeFault, CPFbranches, loads, baseLoad, filter=0)
#     
#     app = QtGui.QApplication(sys.argv)
#     mTreeVis = TreeVis(faultTree=faultTree, pos=[10,10,1800,1000])
#     sys.exit(app.exec_())
    





class Visualization(QMainWindow):
    
    def __init__(self, treemap = None, oneline = None):
        super(self.__class__, self).__init__()
        
        self.oneline = oneline
        self.treemap = treemap
        
        oneline.setParent(self)
        treemap.setParent(self)
        
        
        layout = QHBoxLayout()
        layout.addWidget(self.treemap)
        layout.addWidget(self.oneline)
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.widget = QtGui.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(layout)
        
        self.setGeometry(20,20,1800,950)
        self.setWindowTitle('Visualize')
        
        self.show()
        log('visualization created')


if __name__ == '__main__':
    main()
    
   
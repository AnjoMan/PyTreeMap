
# from mlabwrap import mlab



from PowerNetwork import *
from FaultTree import *
# from TreemapDraw import *
from DetailsWidget import DetailsWidget
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
    
    file = 'cpfResults_case30_1level'
#     file = 'cpfResults_case30_2level'

    file = 'cpfResults_case118_1level'
    
    
    
    depth = 2
    print("\n\n\n")
    
    
    mCPFfile = CPFfile(file)
    elements = mCPFfile.getElements()
    
    width, height=  1700,800

     
    ## draw a responsive treemap diagram
    
    
    (faults, faultTree) = getFaults(TreemapFault, mCPFfile)
    oneLineList = mCPFfile.Branches + mCPFfile.Buses # order is important here.
    
    app = QtGui.QApplication(sys.argv)
    
    mOneline = OneLineWidget(oneLineList, [0,0,900,700])
    mTreemap = TreemapGraphicsVis(pos = [0,0,900,900],faultTree=faultTree)
    mVis = Visualization( oneline = mOneline, treemap=mTreemap) 
    
#     mDetails = DetailsWidget([0,0,500,200])
    
#     mOneline = OneLineWidget(oneLineList, [0,0,900,700], details = mDetails)
#     mTreemap = TreemapGraphicsVis(pos = [0,0,900,900],faultTree=faultTree, details = mDetails)
#     mVis = Visualization( oneline = mOneline, treemap=mTreemap, details = mDetails) 
    
    sys.exit(app.exec_())
    
        
        
    ## draw a  tree diagram
    
    
    
#     
#     (faults, faultTree) = getFaults(TreeFault, CPFbranches, loads, baseLoad, filter=0)
#     
#     app = QtGui.QApplication(sys.argv)
#     mTreeVis = TreeVis(faultTree=faultTree, pos=[10,10,1800,1000])
#     sys.exit(app.exec_())
    





class Visualization(QMainWindow):
    
    def __init__(self, treemap = None, oneline = None, details = None):
        super(self.__class__, self).__init__()
        
        self.oneline = oneline
        self.treemap = treemap
        
        
        oneline.setParent(self)
        treemap.setParent(self)
        
        
        layout = QHBoxLayout()
        layout.addWidget(self.treemap)
        
        if details:
            v = QVBoxLayout()
            v.addWidget(oneline)
            v.addWidget(details)
            layout.addLayout(v)
        elif oneline:
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
    
   
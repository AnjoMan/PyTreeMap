
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
#     file = 'cpfResults_case30_tree'
#     file = 'cpfResults'
    
    
    ## sample files for Treemap
    
#     file = 'cpfResults_case30_2level_branchbus'
#     file = 'cpfResults_case30_1level'
    file = 'cpfResults_case30_2level'
#     file = 'cpfResults_4branches'

#     file = 'cpfResults_case118_1level'
#     file = 'cpfResults_case118_2level'
#     file = 'cpfResults_case118_fixedgeo'
#     file = 'cpfResults'
    
    
    
    depth = 2
    print("\n\n\n")
    
    
    mCPFfile = CPFfile(file)
    elements = mCPFfile.getElements()
    

     
    # draw a responsive treemap diagram
    
    
    (faults, faultTree) = getFaults(TreemapFault, mCPFfile)
    oneLineList = mCPFfile.Branches + mCPFfile.Buses # order is important here.
    
    app = QtGui.QApplication(sys.argv)
#     
    width, height=  1800,800
#     mOneline = OneLineWidget(oneLineList, [0,0,1050,900])
#     mTreemap = TreemapGraphicsVis(pos = [0,0,750,750],faultTree=faultTree)

#     width, height=  900,600
#     mOneline = OneLineWidget(oneLineList, [0,0,550,600])
#     mTreemap = TreemapGraphicsVis(pos = [0,0,350,350],faultTree=faultTree)

#     mVis = Visualization( oneline = mOneline, treemap=mTreemap, pos=(20,20,width,height)) 
    
    mDetails = DetailsWidget([0,0,200,200])
    
    mOneline = OneLineWidget(oneLineList, [0,0,900,700], details = mDetails)
    mTreemap = TreemapGraphicsVis(pos = [0,0,600,600],faultTree=faultTree, details = mDetails)
    mVis = Visualization( oneline = mOneline, treemap=mTreemap, details = mDetails) 
    
    sys.exit(app.exec_())
    
        
#         
#     ## draw a  tree diagram
#     
#     
#     (faults, faultTree) = getFaults(TreeFault, mCPFfile)
# #     (faults, faultTree) = getFaults(TreeFault, CPFbranches, loads, baseLoad, filter=0)
#     
#     app = QtGui.QApplication(sys.argv)
#     mTreeVis = TreeVis(faultTree=faultTree, pos=[10,10,1600,1000])
#     sys.exit(app.exec_())
#     





class Visualization(QMainWindow):
    
    def __init__(self, treemap = None, oneline = None, details = None, pos = (20,20,1800,950)):
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
            
            v.setStretchFactor(oneline, 4)
            v.setStretchFactor(details, 1)
            layout.addLayout(v)
        elif oneline:
            layout.addWidget(self.oneline)
        
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.widget = QtGui.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(layout)
        
        self.setGeometry(*pos)
        self.setWindowTitle('Visualize')
        
        self.show()
        log('visualization created')


if __name__ == '__main__':
    main()
    
   
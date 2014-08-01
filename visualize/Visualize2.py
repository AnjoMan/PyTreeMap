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
        
    


from pytreemap.system.PowerNetwork import OneLineWidget
from pytreemap.visualize.FaultTree import *
# from TreemapDraw import *
from pytreemap.visualize.DetailsWidget import DetailsWidget
from pytreemap.visualize.TreemapGraphics import TreemapGraphicsVis, TreemapFault
from pytreemap.visualize.VisBuilder import JSON_systemFile, MATLAB_systemFile, getFaults, log




import sys
from PySide.QtGui import *
from PySide.QtCore import *



def main():
    import pytreemap.visualize.Visualize2 as Visualize2
    
    print(Visualize2.__file__)
    ## sample files for Tree
#     file = 'cpfResults_case30_tree'
#     file = 'cpfResults'
    
    
    ## sample files for Treemap
    
#     file = 'cpfResults_case30_2level_branchbus'
#     file = 'cpfResults_case30_1level'
    file = os.path.join(os.getcwd(), 'sample_results','cpfResults_case30_2level')
#     file = 'cpfResults_4branches'

#     file = 'cpfResults_case118_1level'
#     file = 'cpfResults_case118_2level'
#     file = 'cpfResults_case118_fixedgeo'
#     file = 'cpfResults'
    
    
    
    depth = 2
    print("\n\n\n")
    
#     mCase = ('case118_geometry.json', 'cpfResults_case118_2level.json')
    mCase =( os.path.join(pytreemap.system.__path__[0],'case30_geometry.json'), os.path.join(pytreemap.system.__path__[0], 'sample_results','cpfResults_case30_2level.json'))
#     mCase = ('case30_geometry.json', 'cpfResults_small.json')
#     mCPFresults = JSON_systemFile(*mCase)
    
    mCPFresults = MATLAB_systemFile(file)
    

     
    # draw a responsive treemap diagram
    
    
    elements = mCPFresults.getElements()
    
    (faults, faultTree) = getFaults(TreemapFault, mCPFresults)
    
    oneLineList = mCPFresults.Branches + mCPFresults.Buses # order is important here.
    
    
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
    mTreemap = TreemapGraphicsVis(pos = [0,0,900,900],faultTree=faultTree, details = mDetails)
    mVis = Visualization( oneline = mOneline, treemap=mTreemap, details = mDetails) 
    
    sys.exit(app.exec_())
    
    
        
#         
#     ## draw a  tree diagram
#     
#     
#     (faults, faultTree) = getFaults(TreeFault, mCPFresults)
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
            
            layout.setStretchFactor(oneline, 1)
            layout.setStretchFactor(v, 2)
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
    
   
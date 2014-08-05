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
    
    
    ## sample files for Treemap
    
    
    
    file = 'cpfResults_case30_2level.mat'
#     file = 'cpfResults_case118_2level'
    
    file = os.path.join(pytreemap.__path__[0], 'sample_results', file) #get absolute file name
    
    
    depth = 2
    print("\n\n\n")
    
#     mCase = ('case118_geometry.json', 'cpfResults_case118_2level.json')
    mCase =( 'case30_geometry.json','cpfResults_case30_2level.json')
#     mCase = ('case30_geometry.json', 'cpfResults_small.json')


    mCase =( os.path.join(pytreemap.system.__path__[0],mCase[0]), os.path.join(pytreemap.__path__[0], 'sample_results',mCase[1]))
    
    
    
    
#     mCPFresults = JSON_systemFile(*mCase)
#     mCPFresults = MATLAB_systemFile(file)
    

     
    # draw a responsive treemap diagram
    
    
#     elements = mCPFresults.getElements()
    
#     (faults, faultTree) = getFaults(TreemapFault, mCPFresults)
    
#     oneLineList = mCPFresults.Branches + mCPFresults.Buses # order is important here.
    
    
    app = QtGui.QApplication(sys.argv)
    
    mVis = ContingencyVisualization(*mCase)
    
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
        super().__init__()
        
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

class ContingencyTreemap(Visualization):
    def __init__(self, system_file, results_file):
        mCPFresults = JSON_systemFile(system_file, results_file)
        
        (faults, faultTree) = getFaults(TreemapFault, mCPFresults)
        
        mDetails = DetailsWidget([0,0,200,200])
        mOneline = OneLineWidget( mCPFresults.Branches + mCPFresults.Buses,[0,0,900,700], details = mDetails)
        mTreemap  = TreemapGraphicsVis(pos = [0,0,900,700],faultTree = faultTree, details = mDetails)
        
        
        
        
        
        super().__init__(treemap=mTreemap, oneline=mOneline, details=mDetails, pos = (20,20,1800,950))
        
        
if __name__ == '__main__':
    main()
    
   
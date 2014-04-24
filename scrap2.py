from VisBuilder import CPFfile
from PowerNetwork import Fault






from PySide.QtCore import *
from PySide.QtGui import *
import sys

def main():
    
    
    
    mFile = CPFfile()
    
    faults = mFile.getFaults(Fault)
    elements = mFile.getElements()
    
    
    
    
    
    
    
    app = QApplication(sys.argv)
    ex = DetailsWidget()
    
    sys.exit(app.exec_())



class DetailsWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.setGeometry(400,300,500,200)
        self.setWindowTitle('Fault Details')
        self.show()


if __name__ == "__main__":
    main()
from VisBuilder import CPFfile
from PowerNetwork import Fault






from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import QWebView
import sys

def main():
    
#     mText = 
        





    
    
    mFile = CPFfile()
    
    faults = mFile.getFaults(Fault)
    elements = mFile.getElements()
    
    
    mFault = faults[2000]
    
    
    
    
    app = QApplication(sys.argv)
    ex = DetailsWidget2(mFault)
    
    sys.exit(app.exec_())

class DetailsWidget2(QWebView):
    
    def __init__(self, fault):
        super().__init__()
        
        

        self.head = "<!DOCTYPE HTML> <head> <style type='text/css'> body{padding:10px;margin:0}h{font-family:sans-serif;font-weight:700;font-size:25px;clear:right;display:block;padding:0;margin-bottom:5px;border-bottom:#000 2px solid}ul{font-family:sans-serif;padding:0;margin:0;list-style-type:none}p{padding:0;margin:0}ul li p{display:inline-block;width:100px;margin-left:5px}.info{float:left;font-family:sans-serif;padding-left:30px}.info>p:first-child{font-weight:700;margin-left:-15px;padding-top:10px}</style> </head>"
        
        
        self.setFault(fault)
        self.setGeometry(400,300,500,200)
        
        self.setWindowTitle('Fault Details')
        self.show()
        
    def setFault(self,fault):
        body = "<body>{}<div style='clear:both'></div></body>".format(fault.html())
        
        
       
        
        self.setHtml(self.head+body)


if __name__ == "__main__":
    main()
from VisBuilder import CPFfile
from PowerNetwork import Fault, Branch, Bus, Transformer, Gen






from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import QWebView
import sys

def main():
    
#     mText = 
        





    
    
    mFile = CPFfile()
    
    faults = mFile.getFaults(Fault)
    elements = mFile.getElements()
    
    mElement = elements[Bus][1]
    mFault = faults[2000]
    
    
    
    
    app = QApplication(sys.argv)
    
    
    ex = DetailsWidget(mFault)
    ex.setContent(elements[Bus][1].html())
    print(elements[Bus][1].html())
    sys.exit(app.exec_())

class DetailsWidget(QWebView):
    body = "<body>{}</body>"
    def __init__(self, pos=None):
        super().__init__()
        
        
#         self.pos = pos or [400,300,500,200]
#         x,y,w,h = self.pos

        self.head = "<!DOCTYPE HTML> <head> <style type='text/css'> body{padding:10px;margin:0}h{font-family:sans-serif;font-weight:700;font-size:25px;clear:right;display:block;padding:0;margin-bottom:5px;border-bottom:#000 2px solid}ul{font-family:sans-serif;padding:0;margin:0;list-style-type:none}p{padding:0;margin:0}ul li p{display:inline-block;width:100px;margin-left:5px}.info{float:left;font-family:sans-serif;padding-left:30px}.info>p:first-child{font-weight:700;margin-left:-15px;padding-top:10px}.el{display:inline-block;clear:right}</style> </head>"
        
        
#         self.resize(w,h)
#         self.setGeometry(400,300,500,200)
        
        self.setWindowTitle('Fault Details')
        self.show()
        
    def setFault(self,fault):
        
        self.setContent(fault.html())
    
    def setElement(self, element):
        self.setContent(element.html())
        
    def setContent(self, html):
        body = "<body>{}</body>".format(html)
        self.setHtml(self.head+body)


if __name__ == "__main__":
    main()
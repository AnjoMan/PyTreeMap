"""
    written by Anton Lodder 2012-2014
    all rights reserved.
    
    This software is the property of the author and may not be copied,
    sold or redistributed without expressed consent of the author.
"""


"""
	 HOWTO:


	 to run this file, make sure that you have a 
	 python distribution installed as well as 
	 Numpy and Scipy packages, and that both python and 
	 the pytreemap library are in your PATH.

	 Then, in a command prompt type

	 >>> python run_oneline.py  [system_file] 


	 e.g.

	 >>> python run_pytreemap.py  case30_geometry.json



"""

import sys
from pytreemap.system.PowerNetwork import OneLineWidget
from pytreemap.visualize.VisBuilder import JSON_systemFile
from PySide.QtGui import QApplication




#get system system_file
file = sys.argv[1] 



#start QApplication service
app = QApplication(sys.argv)

#load system file
mSystem = JSON_systemFile(sys=system_file)

els = mSystem.Transformers + mSystem.Branches + mSystem.Buses + mSystem.Generators
#build visualization
myVis = OneLineWidget(els)

#run
sys.exit(app.exec_())





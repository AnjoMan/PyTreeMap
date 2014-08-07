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

	 >>> python run_pytreemap.py [system geometry file] [results file]


	 e.g.


	 >>> python run_pytreemap.py case30_geometry.json cpfResults_case30_2level.json



"""

import sys
from pytreemap.ContingencyVis import ContingencyTreemap
from PySide.QtGui import QApplication





#get input arguments
system_file, results_file = sys.argv[1], sys.argv[2]




#start QApplication service
app = QApplication(sys.argv)


#build visualization
myVis = ContingencyTreemap(system_file, results_file)

#run
sys.exit(app.exec_())





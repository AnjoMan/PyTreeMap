"""
    written by Anton Lodder 2012-2014
    all rights reserved.
    
    This software is the property of the author and may not be copied,
    sold or redistributed without expressed consent of the author.
"""


"""
	This script will create a treemap visualization with linked oneline diagram
	and text details.






	--------------------
	How to use this file
	--------------------



	to run this file, make sure that you have a 
	python distribution installed as well as 
	Numpy and Scipy packages, and that both python and 
	the pytreemap library are in your PATH.

	Then, in a command prompt type
	>>> python run_pytreemap.py



	To see results from a specific file, use
	>>> python run_pytreemap.py  [results file] 

	e.g.
	>>> python run_pytreemap.py  cpfResults_case30_2level.json




	Note that the above usage requires that the geometry file specified in
	the results file be in the same folder. To override this and specify
	a geometry file explicitly, use
	>>> python run_pytreemap.py [results file] [system file]

	e.g.
	>>> python run_pytreemap.py cpfResults_case30_2level.json case30_geometry.json



"""

import sys
from pytreemap.ContingencyVis import ContingencyTreemap
from PySide.QtGui import QApplication





#get files
results_file = sys.argv[1] if len(sys.argv) > 1 else 'cpfResults_case30_2level.json'
system_file = sys.argv[2] if len(sys.argv) > 2 else None



#start QApplication service
app = QApplication(sys.argv)


#build visualization

myVis = ContingencyTreemap(results_file, system_file)

#run
sys.exit(app.exec_())





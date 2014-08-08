"""
    written by Anton Lodder 2012-2014
    all rights reserved.
    
    This software is the property of the author and may not be copied,
    sold or redistributed without expressed consent of the author.
"""


"""

	This script will produce a tree representation of contingency results







	--------------------
	How to use this file
	--------------------




	to run this file, make sure that you have a 
	python distribution installed as well as 
	Numpy and Scipy packages, and that both python and 
	the pytreemap library are in your PATH.

	Then, in a command prompt type
	>>> python run_tree.py



	to specify a results file, use
	>>> python run_tree.py  [results file]

	e.g.
	>>> python run_tree.py  cpfResults_tree.json



	to specify a custom geometry file, use:
	>>> python run_tree.py [results file] [geometry file]

	e.g.
	>>> python run_tree.py cpfResults_tree.json case30_geometry.json



"""
import sys
from pytreemap.visualize.FaultTree import ContingencyTree
from PySide.QtGui import QApplication


#get files
results_file = sys.argv[1] if len(sys.argv) > 1 else 'cpfResults_tree.json'
system_file = sys.argv[2] if len(sys.argv) > 2 else None


#start QApplication service
app = QApplication(sys.argv)


#build visualizaiton
myVis = ContingencyTree(results_file, system_file)

#run
sys.exit(app.exec_())
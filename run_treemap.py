"""
    written by Anton Lodder 2012-2014
    all rights reserved.
    
    This software is the property of the author and may not be copied,
    sold or redistributed without expressed consent of the author.
"""


"""
	This file will build a treemap visually representing contingency data
	for single and double contingencies. It requires an input file containing
	contingency results; for more information see HOWTO.txt 





	--------------------
	How to run this file
	--------------------


	 to run this file, make sure that you have a 
	 python distribution installed as well as 
	 Numpy and Scipy packages, and that both python and 
	 the pytreemap library are in your PATH.

	 Then, in a command prompt type
	 >>> python run_treemap.py


	 To give a particular results file, use
	 >>> python run_treemap.py  [results file]

	 e.g.

	 >>> python run_pytreemap.py  cpfResults_small.json

"""

import sys
import pytreemap
from pytreemap.visualize.TreemapGraphics import TreemapGraphicsVis, TreemapFault
from pytreemap.visualize.VisBuilder import JSON_systemFile, getFaults
from PySide.QtGui import QApplication
import os



#get results file
results_file= sys.argv[1] if len(sys.argv) > 1 else os.path.join(pytreemap.__path__[0],'sample_results', 'cpfResults_case30_2level.json')




#start QApplication service
app = QApplication(sys.argv)

#load system file
mSystem = JSON_systemFile(res=results_file)

(faults, faultTree) = getFaults(TreemapFault, mSystem)
ex = TreemapGraphicsVis(faultTree=faultTree)

#run
sys.exit(app.exec_())





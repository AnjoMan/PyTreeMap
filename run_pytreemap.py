import sys
from pytreemap.ContingencyVis import ContingencyVisualization as ConVis
from PySide.QtGui import QApplication





#get input arguments
results_file, system_file = sys.argv[1], sys.argv[2]




#start QApplication service
app = QApplication(sys.argv)


#build visualization
myVis = ConVis(system_file, results_file)

#run
sys.exit(app.exec_())





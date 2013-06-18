import scipy.io


# 
# file = scipy.io.loadmat('treemapLayouts.mat');
# 
# 
# 
# layouts = file["treemapLayouts"][0]

layouts = scipy.io.loadmat('treemapLayouts.mat')["treemapLayouts"][0]


myLayout = layouts[0]


for index, line in enumerate(myLayout):
    print line
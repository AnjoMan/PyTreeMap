import scipy.io
import numpy as np
from mlabwrap import mlab



myArray = np.random.rand(20);


r = mlab.treemap(myArray,20,20, nout=1).transpose()
print r
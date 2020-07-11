
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np


x = [1,3,4,1]
y =  [30,34,32,30]
plot = pg.plot()   
plot.plot(x,y) 


## Start Qt event loop unless running in interactive mode or using pyside.
QtGui.QApplication.instance().exec_()

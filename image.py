import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

class ImageWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ImageWidget, self).__init__(parent)

        # Interpret image data as row-major instead of col-major
        pg.setConfigOptions(imageAxisOrder='row-major')

        pg.mkQApp()
        self.win = pg.GraphicsLayoutWidget()
        self.win.setWindowTitle('pyqtgraph example: Image Analysis')

        # A plot1 area (ViewBox + axes) for displaying the image
        self.plot1 = self.win.addPlot()

        # Item for displaying image data
        self.item = pg.ImageItem()
        self.plot1.addItem(self.item)

        # Custom ROI for selecting an image region
        self.ROI = pg.ROI([-8, 14], [6, 5])
        self.ROI.addScaleHandle([0.5, 1], [0.5, 0.5])
        self.ROI.addScaleHandle([0, 0.5], [0.5, 0.5])
        self.plot1.addItem(self.ROI)
        self.ROI.setZValue(10)  # make sure ROI is drawn above image

        # Isocurve drawing
        self.iso = pg.IsocurveItem(level=0.8, pen='g')
        self.iso.setParentItem(self.item)
        self.iso.setZValue(5)

        # Contrast/color control
        self.hist = pg.HistogramLUTItem()
        self.hist.setImageItem(self.item)
        self.win.addItem(self.hist)

        # Draggable line for setting isocurve level
        self.isoLine = pg.InfiniteLine(angle=0, movable=True, pen='g')
        self.hist.vb.addItem(self.isoLine)
        self.hist.vb.setMouseEnabled(y=False) # makes user interaction a little easier
        self.isoLine.setValue(0.8)
        self.isoLine.setZValue(1000) # bring iso line above contrast controls

        # Another plot1 area for displaying ROI data
        self.win.nextRow()
        self.plot2 = self.win.addPlot(colspan=2)
        self.plot2.setMaximumHeight(250)
        self.win.resize(800, 800)
        self.win.show()

        # Generate image self.data
        self.data = np.random.normal(size=(200, 100))
        self.data[20:80, 20:80] += 2.
        self.data = pg.gaussianFilter(self.data, (3, 3))
        self.data += np.random.normal(size=(200, 100)) * 0.1
        self.item.setImage(self.data)
        self.hist.setLevels(self.data.min(), self.data.max())

        # build isocurves from smoothed self.data
        self.iso.setData(pg.gaussianFilter(self.data, (2, 2)))

        # set position and scale of image
        self.item.scale(0.2, 0.2)
        self.item.translate(-50, 0)

        # zoom to fit imageo
        self.plot1.autoRange()  

        self.ROI.sigRegionChanged.connect(self.updatePlot)
        self.updatePlot()

        self.isoLine.sigDragged.connect(self.updateIsocurve)

    # Callbacks for handling user interaction
    def updatePlot(self):
        selected = self.ROI.getArrayRegion(self.data, self.item)
        self.plot2.plot(selected.mean(axis=0), clear=True)

    def updateIsocurve(self):
        self.iso.setLevel(self.isoLine.value())

## Start Qt event loop unless running in interactive mode or using     pyside.
if __name__ == '__main__':

    app = QtGui.QApplication([])
    app.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))

    image_widget = ImageWidget()

    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore,     'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_() 

import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import math
i=-60
x=[]
y=[]
middleX=[]
middleY=[]
middle=-70
#pg.setConfigOption('background', 'b')
#pg.setConfigOption('foreground', 'k')
#win = pg.GraphicsWindow(title="Scatter Plot Symbols")
win = pg.GraphicsLayoutWidget()
qi = pg.QtGui.QImage()
label = pg.QtGui.QLabel(win)
qi.load('sun.png')

label.setPixmap(pg.QtGui.QPixmap.fromImage(qi))
label.setAlignment(QtCore.Qt.AlignCenter)
layout=QVBoxLayout()
layout.addWidget(label,alignment=QtCore.Qt.AlignCenter)
win.setLayout(layout)

win.show()
win.resize(1080,768)
orbitX=[]
orbitY=[]


while i <=60:
    x.append(i)
    y.append(int(math.sqrt(3600-i*i)*(-1)))

    i=i+0.8
#print(x)
i=60
while i >=-60:
    x.append(i)
    y.append((math.sqrt(3600-i*i)))
    i=i-0.8

    #middle orbit

for j in range(-80,81):
    middleX.append(j)
    middleY.append(math.sqrt((1-j*j/6400)*4900))
for j in range(80,-81,-1):
    middleX.append(j)
    middleY.append(math.sqrt((1-j*j/6400)*4900)*(-1))

plot = win.addPlot(title="Solar System")
#Assign wavlue to orbit

for j in range(-100,101):
    orbitX.append(j)
    orbitY.append(math.sqrt((1-j*j/10000)*6400))
for j in range(100,-101,-1):
    orbitX.append(j)
    orbitY.append(math.sqrt((1-j*j/10000)*6400)*(-1))
#plot.plot(orbitX,orbitY)
curve = plot.plot(orbitX,orbitY,pen=pg.mkPen('y', width=2, style=QtCore.Qt.DashLine))  ## add a single curve
curve2=plot.plot(x,y,pen=pg.mkPen('b', width=1,style=QtCore.Qt.DashLine))
curve3=plot.plot(middleX,middleY,pen=pg.mkPen('r', width=1,style=QtCore.Qt.DashLine))
#---------------------------------------
curvePoint = pg.CurvePoint(curve)
curvePoint2=pg.CurvePoint(curve2)
curvePoint3=pg.CurvePoint(curve3)
#---------------------
arrow1 = pg.ArrowItem(angle=90)
arrow1.setParentItem(curvePoint)
text1 = pg.TextItem("test", anchor=(0.5, -1.0))
text1.setParentItem(curvePoint)

#=---------------
arrow2 = pg.ArrowItem(angle=90)
arrow2.setParentItem(curvePoint2)
text2 = pg.TextItem("test", anchor=(0.5, -1.0))
text2.setParentItem(curvePoint2)
#========
arrow3 = pg.ArrowItem(angle=90)
arrow3.setParentItem(curvePoint3)
text3 = pg.TextItem("test", anchor=(0.5, -1.0))
text3.setParentItem(curvePoint3)
index3=0
index = 0
index2=0
center=[0,0]
circle=pg.CircleROI((0,0), size=(5,5),pen={'color':3,'width':5})
circle.setParentItem(curvePoint)
circle2=pg.CircleROI((0,0), size=(5,5),pen={'color':1,'width':3})
circle2.setParentItem(curvePoint2)
circle3=pg.CircleROI((0,0), size=(5,5),pen={'color':"7F00FF",'width':3})
circle3.setParentItem(curvePoint3)

def update():
    global curvePoint,curvePoint2,curvePoint3, index,index2,index3
    index = (index + 1) % len(orbitX)
    index2=(index2+1) % len(x)
    index3=(index3+1) % len(middleX)
    curvePoint.setPos(float(index)/(len(orbitX)-1))
    curvePoint2.setPos(float(index2)/(len(x)-1))
    curvePoint3.setPos(float(index3)/(len(middleX)-1))
   
    text2.setText('[%0.1f, %0.1f]' % (orbitX[index], orbitY[index]))
    text1.setText('[%0.1f, %0.1f]' % (x[index2], y[index2]))
    text3.setText('[%0.1f, %0.1f]' % (middleX[index3],middleY[index3]))

    


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(20)



## Start Qt event loop unless running in interactive mode or using pyside.
QtGui.QApplication.instance().exec_()


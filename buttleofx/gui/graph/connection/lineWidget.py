import sys
from PySide import QtGui, QtCore


class LineWidget(QtGui.QWidget):

    def __init__(self, xIn, yIn, xOut, yOut):
        QtGui.QWidget.__init__(self)
        self.xIn = xIn
        self.yIn = yIn
        self.xOut = xOut
        self.yOut = yOut
        self.initUI()

    def initUI(self):
        self.setGeometry(self.xIn, self.yIn, self.xOut, self.yOut)
        self.show()

    def paintEvent(self, e):
        painter = QtGui.QPainter()
        #painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.begin(self)
        self.drawLines(painter)
        painter.end()

    def drawLines(self, painter):
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(self.xIn, self.yIn, self.xOut, self.yOut)

from PySide import QtGui, QtCore, QtDeclarative


class LineItem(QtDeclarative.QDeclarativeItem):

    def __init__(self, parent=None):
        QtDeclarative.QDeclarativeItem.__init__(self, parent)
        self._x1 = 0
        self._y1 = 0
        self._x2 = 0
        self._y2 = 0

        # Enable paint method calls
        self.setFlag(QtGui.QGraphicsItem.ItemHasNoContents, False)

    def getX1(self):
        return self._x1

    def getY1(self):
        return self._y1

    def getX2(self):
        return self._x2

    def getY2(self):
        return self._y2

    def setX1(self, x1):
        self._x1 = x1

    def setY1(self, y1):
        self._y1 = y1

    def setX2(self, x2):
        self._x2 = x2

    def setY2(self, y2):
        self._y2 = y2

    x1Changed = QtCore.Signal()
    y1Changed = QtCore.Signal()
    x2Changed = QtCore.Signal()
    y2Changed = QtCore.Signal()

    x1 = QtCore.Property(int, getX1, setX1, notify=x1Changed)
    y1 = QtCore.Property(int, getY1, setY1, notify=y1Changed)
    x2 = QtCore.Property(int, getX2, setX2, notify=x2Changed)
    y2 = QtCore.Property(int, getY2, setY2, notify=y2Changed)

    def paint(self, painter, option, widget):
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.drawLine(self._x1, self._y1, self._x2, self._y2)

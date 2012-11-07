import sys
from PySide import QtCore, QtGui, QtDeclarative


class NodeWrapper(QtCore.QObject):

    """
        Class NodeWrapper defined by:
        - name
        - color
        - xCoord
        - yCoord

        Creates a QObject from a given python object Node.
    """

    def __init__(self, element):
        QtCore.QObject.__init__(self)
        self._element = element

    @QtCore.Slot()
    def _getName(self):
        return str(self._element.name)

    @QtCore.Slot(unicode)
    def _setName(self, name):
        self._element.name = name

    @QtCore.Slot()
    def _getColor(self):
        return QtGui.QColor(self._element.r, self._element.g, self._element.b)

    @QtCore.Slot(QtGui.QColor)
    def _setColor(self, r, g, b):
        self._element.r = r
        self._element.g = g
        self._element.b = b

    @QtCore.Slot()
    def _getXCoord(self):
        return self._element.xCoord

    @QtCore.Slot(int)
    def _setXCoord(self, x):
        self._element.xCoord = x

    @QtCore.Slot()
    def _getYCoord(self):
        return self._element.yCoord

    @QtCore.Slot(int)
    def _setYCoord(self, y):
        self._element.yCoord = y

    @QtCore.Slot()
    def _nbInput(self):
        return self._element.nbInput

    changed = QtCore.Signal()
    nodeName = QtCore.Property(unicode, _getName, _setName, notify=changed)
    nodeColor = QtCore.Property(QtGui.QColor, _getColor, _setColor, notify=changed)
    nodeXCoord = QtCore.Property(int, _getXCoord, _setXCoord, notify=changed)
    nodeYCoord = QtCore.Property(int, _getYCoord, _setYCoord, notify=changed)
    nodeNbInput = QtCore.Property(int, _nbInput, notify=changed)

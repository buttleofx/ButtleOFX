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

    @QtCore.Signal
    def changed(self): pass

    # invokable
    #@QtCore.Slot()

    def _getName(self):
        return str(self._element.name)

    def _setName(self, name):
        self._element.name = name

    def _getColor(self):
        return QtGui.QColor(self._element.r, self._element.g, self._element.b)

    def _setColor(self, r, g, b):
        self._element.r = r
        self._element.g = g
        self._element.b = b

    def _getXCoord(self):
        return self._element.xCoord

    def _setXCoord(self, x):
        self._element.xCoord = x

    def _getYCoord(self):
        return self._element.yCoord

    def _setYCoord(self, y):
        self._element.yCoord = y

    def _nbInput(self):
        return self._element.nbInput

    def _setNbInput(self, nbInput):
        self._element.nbInput = nbInput
        self.changed()

    changed = QtCore.Signal()
    nodeName = QtCore.Property(unicode, _getName, _setName, notify=changed)
    nodeColor = QtCore.Property(QtGui.QColor, _getColor, _setColor, notify=changed)
    nodeXCoord = QtCore.Property(float, _getXCoord, _setXCoord, notify=changed)
    nodeYCoord = QtCore.Property(float, _getYCoord, _setYCoord, notify=changed)
    nodeNbInput = QtCore.Property(int, _nbInput, _setNbInput, notify=changed)



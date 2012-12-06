from PySide import QtCore, QtGui


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
        super(NodeWrapper, self).__init__()
        self._element = element

    @QtCore.Signal
    def changed(self):
        pass

    # invokable
    # @QtCore.Slot()

    def getName(self):
        return str(self._element._name)

    def setName(self, name):
        self._element._name = name

    def getColor(self):
        return QtGui.QColor(self._element._r, self._element._g, self._element._b)

    def setColor(self, r, g, b):
        self._element._r = r
        self._element._g = g
        self._element._b = b

    def getXCoord(self):
        return self._element._x

    def setXCoord(self, x):
        self._element._x = x

    def getYCoord(self):
        return self._element._y

    def setYCoord(self, y):
        self._element._y = y

    def getNbInput(self):
        return self._element._nbInput

    def setNbInput(self, nbInput):
        self._element._nbInput = nbInput
        self.changed()

    name = QtCore.Property(unicode, getName, setName, notify=changed)
    color = QtCore.Property(QtGui.QColor, getColor, setColor, notify=changed)
    x = QtCore.Property(float, getXCoord, setXCoord, notify=changed)
    y = QtCore.Property(float, getYCoord, setYCoord, notify=changed)
    nbInput = QtCore.Property(int, getNbInput, setNbInput, notify=changed)

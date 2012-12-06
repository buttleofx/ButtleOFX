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
        return QtGui.QColor( *self._element._color )

    def setColor(self, r, g, b):
        self._element._color = (r, g, b)

    def getXCoord(self):
        return self._element._coord[0]

    def setXCoord(self, x):
        self._element._coord[0] = x

    def getYCoord(self):
        return self._element._coord[1]

    def setYCoord(self, y):
        self._element._coord[1] = y

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

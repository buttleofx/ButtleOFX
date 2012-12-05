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
        self.element = element

    @QtCore.Signal
    def changed(self):
        pass

    # invokable
    # @QtCore.Slot()

    def getName(self):
        return str(self.element.name)

    def setName(self, name):
        self.element.name = name

    def getColor(self):
        return QtGui.QColor(self.element.r, self.element.g, self.element.b)

    def setColor(self, r, g, b):
        self.element.r = r
        self.element.g = g
        self.element.b = b

    def getXCoord(self):
        return self.element.x

    def setXCoord(self, x):
        self.element.x = x

    def getYCoord(self):
        return self.element.y

    def setYCoord(self, y):
        self.element.y = y

    def nbInput(self):
        return self.element.nbInput

    def setNbInput(self, nbInput):
        self.element.nbInput = nbInput
        self.changed()

    name = QtCore.Property(unicode, getName, setName, notify=changed)
    color = QtCore.Property(QtGui.QColor, getColor, setColor, notify=changed)
    x = QtCore.Property(float, getXCoord, setXCoord, notify=changed)
    y = QtCore.Property(float, getYCoord, setYCoord, notify=changed)
    nbInput = QtCore.Property(int, nbInput, setNbInput, notify=changed)

from quickmamba.patterns import Signal

from PySide import QtCore, QtGui


class NodeWrapper(QtCore.QObject):
    """
        Class NodeWrapper defined by:
        - _node = the data of the node
        - _name
        - _type
        - _coord
        - _color
        - _nbInput
        - _image
        - _node : his related node

        Creates a QObject from a given python object Node.
    """

    def __init__(self, node):
        super(NodeWrapper, self).__init__()

        self._node = node

        self._name = node._name
        self._type = node._type
        self._coord = node._coord
        self._color = node._color
        self._nbInput = node._nbInput
        self._image = node._image

        # the links between the nodeWrapper and his node
        self._node.nameChanged.connect(self.setName)
        self._node.typeChanged.connect(self.setType)
        self._node.coordChanged.connect(self.setCoord)
        #self._node.xChanged.connect(self.setXCoord)
        #self._node.yChanged.connect(self.setYCoord)
        self._node.colorChanged.connect(self.setColor)
        self._node.nbInputChanged.connect(self.setNbInput)
        self._node.imageChanged.connect(self.setImage)

    @QtCore.Signal
    def changed(self):
        pass

    @QtCore.Slot()
    def getName(self):
        return str(self._name)

    @QtCore.Slot(str)
    def setName(self, name):
        self._name = name

    @QtCore.Slot()
    def getType(self):
        return str(self._type)

    @QtCore.Slot(str)
    def setType(self, nodeType):
        self._type = nodeType

    @QtCore.Slot()
    def getCoord(self):
        return self._coord

    @QtCore.Slot(int, int)
    def setCoord(self, x, y):
        self._coord = (x, y)

    @QtCore.Slot()
    def getColor(self):
        return QtGui.QColor(*self._color)

    @QtCore.Slot(QtGui.QColor)
    def setColor(self, r, g, b):
        self._color = (r, g, b)

    @QtCore.Slot()
    def getNbInput(self):
        return self._nbInput

    @QtCore.Slot(int)
    def setNbInput(self, nbInput):
        self._nbInput = nbInput
        # self.changed()

    @QtCore.Slot()
    def getImage(self):
        return self._image

    @QtCore.Slot(str)
    def setImage(self, image):
        self._image = image

    @QtCore.Slot(int, int)
    def nodeMoved(self, x, y):
        self._node.setCoord(x, y)

    name = QtCore.Property(str, getName, setName, notify=changed)
    nodeType = QtCore.Property(str, getType, setType, notify=changed)
    coord = QtCore.Property("QVariant", getCoord, setCoord, notify=changed)
    #y = QtCore.Property(int, getYCoord, setYCoord, notify=changed)
    color = QtCore.Property(QtGui.QColor, getColor, setColor, notify=changed)
    nbInput = QtCore.Property(int, getNbInput, setNbInput, notify=changed)
    image = QtCore.Property(str, getImage, setImage, notify=changed)

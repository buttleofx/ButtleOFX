from PySide import QtCore, QtGui
from QuickMamba.quickmamba.patterns.signalEvent import Signal

class NodeWrapper(QtCore.QObject):

    """
        Class NodeWrapper defined by:
        - _id
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
        # the links between the nodeWrapper and his node
        self._node.idChanged.connect(self.setId)
        self._node.nameChanged.connect(self.setName)
        self._node.typeChanged.connect(self.setType)
        self._node.xChanged.connect(self.setXCoord)
        self._node.yChanged.connect(self.setYCoord)
        self._node.colorChanged.connect(self.setColor)
        self._node.nbInputChanged.connect(self.setNbInput)
        self._node.imageChanged.connect(self.setImage)

        self._id = node._id
        self._name = node._name
        self._type = node._type
        self._coord = node._coord
        self._color = node._color
        self._nbInput = node._nbInput
        self._image = node._image

    @QtCore.Signal
    def changed(self):
        pass

    # invokable
    @QtCore.Slot()
    def getId(self):
        return self._id

    @QtCore.Slot(unicode)
    def setId(self, idNode):
        print("id")
        self._id = idNode

    @QtCore.Slot()
    def getName(self):
        print("name")
        return str(self._name)

    @QtCore.Slot()
    def setName(self, name):
        self._name = name

    @QtCore.Slot()
    def getType(self):
        return str(self._type)

    @QtCore.Slot()
    def setType(self, nodeType):
        self._type = nodeType

    @QtCore.Slot()
    def getXCoord(self):
        return self._coord[0]

    @QtCore.Slot(int)
    def setXCoord(self, x):
        self._coord[0] = x

    @QtCore.Slot()
    def getYCoord(self):
        return self._coord[1]

    @QtCore.Slot(int)
    def setYCoord(self, y):
        self._coord[1] = y

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

    nodeId = QtCore.Property(unicode, getId, setId, notify=changed)
    name = QtCore.Property(unicode, getName, setName, notify=changed)
    nodeType = QtCore.Property(unicode, getType, setType, notify=changed)
    x = QtCore.Property(float, getXCoord, setXCoord, notify=changed)
    y = QtCore.Property(float, getYCoord, setYCoord, notify=changed)
    color = QtCore.Property(QtGui.QColor, getColor, setColor, notify=changed)
    nbInput = QtCore.Property(int, getNbInput, setNbInput, notify=changed)
    image = QtCore.Property(unicode, getImage, setImage, notify=changed)
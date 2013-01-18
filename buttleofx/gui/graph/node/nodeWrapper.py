from PySide import QtCore, QtGui

# wrappers
from buttleofx.gui.paramEditor.wrappers import ParamEditorWrapper


class NodeWrapper(QtCore.QObject):
    """
        Class NodeWrapper defined by:
        - _node : the node data

        Creates a QObject from a given python object Node.
    """

    # static variables usefull to display nodes & clips :
    widthNode = 110
    heightEmptyNode = 35
    clipSpacing = 7
    clipSize = 8
    inputSideMargin = 6

    def __init__(self, node, view):
        super(NodeWrapper, self).__init__(view)

        self._node = node
        self._view = view

        self._node.changed.connect(self.emitChanged)

    # We can't connect the two signals because self.changed() is a QML signal.
    # So, we use the function self.emitChanged() to solve the problem

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    ######## getters ########

    def getName(self):
        return str(self._node._name)

    def getType(self):
        return str(self._node._type)

    def getCoord(self):
        return self._node._coord

    def getColor(self):
        return QtGui.QColor(*self._node._color)

    def getNbInput(self):
        return self._node._nbInput

    def getImage(self):
        return self._node._image

    def getParams(self):
        paramEditorWrapper = ParamEditorWrapper(self._view, self._node.getParams())
        return paramEditorWrapper.paramElmts

    ######## setters ########

    def setName(self, name):
        self._node.setName(name)

    def setType(self, nodeType):
        self._node.setType(nodeType)

    def setCoord(self, x, y):
        self._node.setCoord(x, y)

    def setColor(self, r, g, b):
        self._node.setColor(r, g, b)

    def setNbInput(self, nbInput):
        self._node.setNbInput(nbInput)

    def setImage(self, image):
        self._node.setImage(image)

    ######## Slots ########

    name = QtCore.Property(str, getName, setName, notify=changed)
    nodeType = QtCore.Property(str, getType, setType, notify=changed)
    coord = QtCore.Property("QVariant", getCoord, setCoord, notify=changed)
    color = QtCore.Property(QtGui.QColor, getColor, setColor, notify=changed)
    nbInput = QtCore.Property(int, getNbInput, setNbInput, notify=changed)
    image = QtCore.Property(str, getImage, setImage, notify=changed)
    params = QtCore.Property(QtCore.QObject, getParams, constant=True)

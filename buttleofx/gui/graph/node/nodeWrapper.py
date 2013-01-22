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

        print "Gui : nodeWrapper created"

    def __del__(self):
        print "Gui : NodeWrapper deleted"

    # We can't connect the two signals because self.changed() is a QML signal.
    # So, we use the function self.emitChanged() to solve the problem

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    ######## getters ########

    def getName(self):
        return self._node.getName()

    def getNameUser(self):
        return self._node.getNameUser()

    def getType(self):
        return self._node.getType()

    def getCoord(self):
        return QtCore.QPoint(self._node.getCoord()[0], self._node.getCoord()[1])

    def getColor(self):
        return QtGui.QColor(self._node.getColor())

    def getNbInput(self):
        return self._node.getNbInput()

    def getImage(self):
        return self._node.getImage()

    def getParams(self):
        paramEditorWrapper = ParamEditorWrapper(self._view, self._node.getParams())
        return paramEditorWrapper.paramElmts

    ######## setters ########

    def setName(self, name):
        self._node.setName(name)

    def setNameUser(self, nameUser):
        self._node.setNameUser(nameUser)

    def setType(self, nodeType):
        self._node.setType(nodeType)

    # from 2 decimal values
    def setCoord(self, x, y):
        self._node.setCoord(x, y)

    # from a QPoint
    def setCoord(self, point):
        self._node.setCoord(point.x(), point.y())

    # from 3 decimal values
    def setColor(self, r, g, b):
        self._node.setColor(r, g, b)

    # from a QColor
    def setColor(self, color):
        self._node.setColor(color.red(), color.green(), color.blue())

    def setNbInput(self, nbInput):
        self._node.setNbInput(nbInput)

    def setImage(self, image):
        self._node.setImage(image)

    ################################################## DATA EXPOSED TO QML ##################################################

    # params from Buttle
    name = QtCore.Property(str, getName, setName, notify=changed)
    nameUser = QtCore.Property(str, getNameUser, setNameUser, notify=changed)
    nodeType = QtCore.Property(str, getType, setType, notify=changed)
    coord = QtCore.Property(QtCore.QPoint, getCoord, setCoord, notify=changed)
    color = QtCore.Property(QtGui.QColor, getColor, setColor, notify=changed)
    nbInput = QtCore.Property(int, getNbInput, setNbInput, notify=changed)
    image = QtCore.Property(str, getImage, setImage, notify=changed)
    # params from Tuttle
    params = QtCore.Property(QtCore.QObject, getParams, constant=True)

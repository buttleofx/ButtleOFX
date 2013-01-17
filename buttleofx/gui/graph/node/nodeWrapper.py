from PySide import QtCore, QtGui
# core
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands import CmdSetCoord
# quickmamba
from quickmamba.patterns import Signal


class NodeWrapper(QtCore.QObject):
    """
        Class NodeWrapper defined by:
        - _node : the node data

        - The nodeWrapper data :
            - _name
            - _type
            - _coord
            - _color
            - _nbInput
            - _image

        Creates a QObject from a given python object Node.
    """

    def __init__(self, node, view):
        super(NodeWrapper, self).__init__(view)

        self._node = node

        self._name = node._name
        self._type = node._type
        self._coord = node._coord
        self._color = node._color
        self._nbInput = node._nbInput
        self._image = node._image

        # the links between the nodeWrapper and his node
        #self._node.NodeNameChanged.connect(self.nodeNameChanged)
        #self._node.NodeTypeChanged.connect(self.nodeTypeChanged)
        #self._node.NodeCoordChanged.connect(self.nodeCoordChanged)
        #self._node.NodeColorChanged.connect(self.nodeColorChanged)
        #self._node.NodeNbInputChanged.connect(self.nodeNbInputChanged)
        #self._node.NodeImageChanged.connect(self.nodeImageChanged)

        self._node.NodeNameChanged.connect(self.setName)
        self._node.NodeTypeChanged.connect(self.setType)
        self._node.NodeCoordChanged.connect(self.setCoord)
        self._node.NodeColorChanged.connect(self.setColor)
        self._node.NodeNbInputChanged.connect(self.setNbInput)
        self._node.NodeImageChanged.connect(self.setImage)

    @QtCore.Signal
    def changed(self):
        pass

    ######## getters ########

    def getName(self):
        return str(self._name)

    def getType(self):
        return str(self._type)

    def getCoord(self):
        return self._coord

    def getColor(self):
        return QtGui.QColor(*self._color)

    def getNbInput(self):
        return self._nbInput

    def getImage(self):
        return self._image

    ######## setters ########

    def setName(self, name):
        self._name = name

    def setType(self, nodeType):
        self._type = nodeType

    def setCoord(self, x, y):
        print "nodeWrapper.setCoord"
        self._coord = (x, y)
        print "nodeWrapper Coords have changed : " + str(self._coord)

    def setColor(self, r, g, b):
        self._color = (r, g, b)

    def setNbInput(self, nbInput):
        self._nbInput = nbInput

    def setImage(self, image):
        self._image = image

    ######## Slots ########

    @QtCore.Slot(int, int, CommandManager)
    def nodeMoved(self, x, y, cmdManager):
        print "Coordinates before movement :"
        print self._coord
        #self._node.setCoord(x, y)

        cmdMoved = CmdSetCoord(self._node, (x, y))
        cmdManager.push(cmdMoved)
        print "Coordinates after movement :"
        print self._coord

    name = QtCore.Property(str, getName, setName, notify=changed)
    nodeType = QtCore.Property(str, getType, setType, notify=changed)
    coord = QtCore.Property("QVariant", getCoord, setCoord, notify=changed)
    color = QtCore.Property(QtGui.QColor, getColor, setColor, notify=changed)
    nbInput = QtCore.Property(int, getNbInput, setNbInput, notify=changed)
    image = QtCore.Property(str, getImage, setImage, notify=changed)

"""
Obsolete fonctions I haven't yet deleted on the safe side because it's late and maybe I'm making a big mistake.
And if I'm making a big mistake, I apologize in advance Elisa.

    @QtCore.Slot()
    def nodeColorChanged(self):
        self._node.getColor()

    @QtCore.Slot()
    def nodeNbInputChanged(self):
        self._node.getNbInput()

    @QtCore.Slot()
    def nodeNameChanged(self):
        self._node.getName()
    
    @QtCore.Slot()
    def nodeTypeChanged(self):
        self._node.getType()

    @QtCore.Slot()
    def nodeImageChanged(self):
        self._node.getImage()

"""

from PySide import QtCore, QtGui
# core
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands import CmdSetCoord
# wrappers
from buttleofx.gui.paramEditor.wrappers import ParamEditorWrapper
# quickmamba
from quickmamba.patterns import Signal


class NodeWrapper(QtCore.QObject):
    """
        Class NodeWrapper defined by:
        - _node : the node data

        Creates a QObject from a given python object Node.
    """

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
        print "node emitChanged"
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
        return ParamEditorWrapper(self._view, self._node.getParams())

    ######## setters ########

    def setName(self, name):
        self._node._name = name
        self.changed()

    def setType(self, nodeType):
        self._node._type = nodeType
        self.changed()

    def setCoord(self, x, y):
        print "nodeWrapper.setCoord"
        self._node._coord = (x, y)
        print "nodeWrapper Coords have changed : " + str(self._node._coord)
        self.changed()

    def setColor(self, r, g, b):
        self._node._color = (r, g, b)
        self.changed()

    def setNbInput(self, nbInput):
        self._node._nbInput = nbInput
        self.changed()

    def setImage(self, image):
        self._node._image = image
        self.changed()

    ######## Slots ########

    @QtCore.Slot(int, int, CommandManager)
    def nodeMoved(self, x, y, cmdManager):
        print "Coordinates before movement :"
        print self._node._coord
        #self._node.setCoord(x, y)

        cmdMoved = CmdSetCoord(self._node, (x, y))
        cmdManager.push(cmdMoved)
        print "Coordinates after movement :"
        print self._node._coord

    name = QtCore.Property(str, getName, setName, notify=changed)
    nodeType = QtCore.Property(str, getType, setType, notify=changed)
    coord = QtCore.Property("QVariant", getCoord, setCoord, notify=changed)
    color = QtCore.Property(QtGui.QColor, getColor, setColor, notify=changed)
    nbInput = QtCore.Property(int, getNbInput, setNbInput, notify=changed)
    image = QtCore.Property(str, getImage, setImage, notify=changed)

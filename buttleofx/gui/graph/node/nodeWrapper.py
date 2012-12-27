#!/usr/bin/env python
# -*-coding:utf-8-*

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
        self._node.NodeNameChanged.connect(self.nodeNameChanged)
        self._node.NodeTypeChanged.connect(self.nodeTypeChanged)
        self._node.NodeCoordChanged.connect(self.nodeCoordChanged)
        self._node.NodeColorChanged.connect(self.nodeColorChanged)
        self._node.NodeNbInputChanged.connect(self.nodeNbInputChanged)
        self._node.NodeImageChanged.connect(self.nodeImageChanged)

    @QtCore.Signal
    def changed(self):
        pass

    @QtCore.Slot(result="str")
    def getName(self):
        return str(self._name)

    @QtCore.Slot(str)
    def setName(self, name):
        self._name = name

    @QtCore.Slot()
    def nodeNameChanged(self):
        self._node.getName()

    @QtCore.Slot(result="str")
    def getType(self):
        return str(self._type)

    @QtCore.Slot(str)
    def setType(self, nodeType):
        self._type = nodeType

    @QtCore.Slot()
    def nodeTypeChanged(self):
        self._node.getType()

    @QtCore.Slot()
    def getCoord(self):
        return self._coord

    @QtCore.Slot(int, int)
    def setCoord(self, x, y):
        self._coord = (x, y)

    @QtCore.Slot()
    def nodeCoordChanged(self):
        self._node.getCoord()

    @QtCore.Slot(result="QVariant")
    def getColor(self):
        return QtGui.QColor(*self._color)

    @QtCore.Slot(QtGui.QColor)
    def setColor(self, r, g, b):
        self._color = (r, g, b)

    @QtCore.Slot()
    def nodeColorChanged(self):
        self._node.getColor()

    @QtCore.Slot(result="int")
    def getNbInput(self):
        return self._nbInput

    @QtCore.Slot(int)
    def setNbInput(self, nbInput):
        self._nbInput = nbInput
        # self.changed

    @QtCore.Slot()
    def nodeNbInputChanged(self):
        self._node.getNbInput()

    @QtCore.Slot(result="str")
    def getImage(self):
        return self._image

    @QtCore.Slot(str)
    def setImage(self, image):
        self._image = image

    @QtCore.Slot()
    def nodeImageChanged(self):
        self._node.getImage()

    @QtCore.Slot(int, int, CommandManager)
    def nodeMoved(self, x, y, cmdManager):
        print "Coordinates before movement"
        print self._node._coord
        #self._node.setCoord(x, y)

        cmdMoved = CmdSetCoord(self._node, (x, y))
        cmdManager.push(cmdMoved)
        print "Coordinates after movement"
        print self._node._coord
        #cmdManager.undo()

    name = QtCore.Property(str, getName, setName, notify=changed)
    nodeType = QtCore.Property(str, getType, setType, notify=changed)
    coord = QtCore.Property("QVariant", getCoord, setCoord, notify=changed)
    color = QtCore.Property(QtGui.QColor, getColor, setColor, notify=changed)
    nbInput = QtCore.Property(int, getNbInput, setNbInput, notify=changed)
    image = QtCore.Property(str, getImage, setImage, notify=changed)

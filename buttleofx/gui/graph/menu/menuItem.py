from PySide import QtCore


class MenuItem(QtCore.QObject):

    def __init__(self, label, typeItem, listMenuItem):

        self._label = label
        self._type = typeItem
        self._listMenuItem = listMenuItem

    def getLabel(self):
        return self._label

    def getType(self):
        return self._type

    def getListMenuItem(self):
        return self._listMenuItem

    def setLabel(self, label):
        self._label = label

    def setType(self, itemTypeObject):
        self._type = itemTypeObject

    def setListMenuItem(self, listMenuItem):
        self._listMenuItem = listMenuItem

    changed = QtCore.Signal()
    label = QtCore.Property(unicode, getLabel, setLabel, notify=changed)
    itemType = QtCore.Property(QtCore.QObject, getType, setType, notify=changed)
    listMenuItem = QtCore.Property(QtCore.QObject, getListMenuItem, setListMenuItem, notify=changed)

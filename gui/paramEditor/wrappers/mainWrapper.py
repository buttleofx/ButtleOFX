from PySide import QtCore
from qobjectlistmodel import QObjectListModel


class MainWrapper(QtCore.QObject):
    def __init__(self, parent, paramListModel):
        QtCore.QObject.__init__(self)
        self._paramElmts = QObjectListModel(self)
        self._paramElmts.setObjectList(paramListModel)

    def getParamElts(self):
        return self._paramElmts

    modelChanged = QtCore.Signal()
    paramElmts = QtCore.Property("QVariant", getParamElts, notify=modelChanged)

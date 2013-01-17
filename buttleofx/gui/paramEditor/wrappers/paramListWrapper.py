from buttleofx.gui.paramEditor.params import ParamInt
from buttleofx.gui.paramEditor.params import ParamString
from buttleofx.gui.paramEditor.wrappers import IntWrapper
from buttleofx.gui.paramEditor.wrappers import StringWrapper

from quickmamba.models import QObjectListModel

from PySide import QtCore


class ParamListWrapper(QtCore.QObject):
    def __init__(self, parent, paramList):
        super(ParamListWrapper, self).__init__(parent)
        self._paramElmts = QObjectListModel(self)

        mapTypeToWrapper = {
            ParamInt: IntWrapper,
            ParamString: StringWrapper
        }

        paramListModel = [mapTypeToWrapper[paramElt.__class__](paramElt) for paramElt in paramList]
        self._paramElmts.setObjectList(paramListModel)

    def getParamElts(self):
        return self._paramElmts

    modelChanged = QtCore.Signal()
    paramElmts = QtCore.Property("QVariant", getParamElts, notify=modelChanged)

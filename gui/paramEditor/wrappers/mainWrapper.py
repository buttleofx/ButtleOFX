from PySide import QtCore
from QuickMamba import qobjectlistmodel
from gui.paramEditor.paramInt import ParamInt
from gui.paramEditor.paramString import ParamString
from intWrapper import IntWrapper
from stringWrapper import StringWrapper


class MainWrapper(QtCore.QObject):
    def __init__(self, parent, paramList):
        super(MainWrapper, self).__init__(parent)
        #QtCore.QObject.__init__(self)
        self._paramElmts = qobjectlistmodel.QObjectListModel(self)

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

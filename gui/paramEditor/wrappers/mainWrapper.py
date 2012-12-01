from PySide import QtCore
from QuickMamba import qobjectlistmodel
from paramInt import ParamInt
from paramString import ParamString
from wrappers.intWrapper import IntWrapper
from wrappers.stringWrapper import StringWrapper


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

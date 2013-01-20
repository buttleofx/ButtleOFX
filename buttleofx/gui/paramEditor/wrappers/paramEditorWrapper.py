from PySide import QtCore
# core
from buttleofx.core.params import ParamInt, ParamString, ParamBoolean, ParamDouble, ParamDouble2D, ParamDouble3D, ParamChoice3C
# gui
from buttleofx.gui.paramEditor.wrappers import IntWrapper, StringWrapper, BooleanWrapper, DoubleWrapper, Double2DWrapper, Double3DWrapper, Choice3CWrapper
#quickmamba
from quickmamba.models import QObjectListModel


class ParamEditorWrapper(QtCore.QObject):
    def __init__(self, parent, paramList):
        super(ParamEditorWrapper, self).__init__(parent)
        #QtCore.QObject.__init__(self)
        self._paramElmts = QObjectListModel(self)

        mapTypeToWrapper = {
            ParamInt: IntWrapper,
            ParamString: StringWrapper,
            ParamDouble: DoubleWrapper,
            ParamDouble2D: Double2DWrapper,
            ParamDouble3D: Double3DWrapper,
            ParamBoolean: BooleanWrapper,
            ParamChoice3C: Choice3CWrapper
        }

        paramListModel = [mapTypeToWrapper[paramElt.__class__](paramElt) for paramElt in paramList]
        self._paramElmts.setObjectList(paramListModel)

    def getParamElts(self):
        return self._paramElmts

    # @QtCore.Slot(Node)
    def setNodeForParam(self, node):
        self._paramElmts = node._params
        self.modelChanged.emit()

    modelChanged = QtCore.Signal()
    paramElmts = QtCore.Property("QVariant", getParamElts, notify=modelChanged)

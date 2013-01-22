from PySide import QtCore
# core
from buttleofx.core.params import ParamInt, ParamInt2D, ParamString, ParamBoolean, ParamDouble, ParamDouble2D, ParamDouble3D, ParamChoice, ParamPushButton
# gui
from buttleofx.gui.paramEditor.wrappers import IntWrapper, Int2DWrapper, StringWrapper, BooleanWrapper, DoubleWrapper, Double2DWrapper, Double3DWrapper, ChoiceWrapper, PushButtonWrapper
#quickmamba
from quickmamba.models import QObjectListModel


class ParamEditorWrapper(QtCore.QObject):
    def __init__(self, parent, paramList):
        super(ParamEditorWrapper, self).__init__(parent)
        #QtCore.QObject.__init__(self)
        self._paramElmts = QObjectListModel(self)

        mapTypeToWrapper = {
            ParamInt: IntWrapper,
            ParamInt2D: Int2DWrapper,
            ParamString: StringWrapper,
            ParamDouble: DoubleWrapper,
            ParamDouble2D: Double2DWrapper,
            ParamDouble3D: Double3DWrapper,
            ParamBoolean: BooleanWrapper,
            ParamChoice: ChoiceWrapper,
            ParamPushButton: PushButtonWrapper
        }

        paramListModel = [mapTypeToWrapper[paramElt.__class__](paramElt) for paramElt in paramList]
        self._paramElmts.setObjectList(paramListModel)

    def getParamElts(self):
        return self._paramElmts

    def setNodeForParam(self, node):
        self._paramElmts = node._params
        self.modelChanged.emit()

    modelChanged = QtCore.Signal()
    paramElmts = QtCore.Property("QVariant", getParamElts, notify=modelChanged)

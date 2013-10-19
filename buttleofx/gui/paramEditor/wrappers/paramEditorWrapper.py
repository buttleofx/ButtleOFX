from PyQt5 import QtCore
# core
from buttleofx.core.params import ParamInt, ParamInt2D, ParamInt3D, ParamString, ParamBoolean, ParamDouble, ParamDouble2D, ParamDouble3D, ParamChoice, ParamPushButton, ParamRGBA, ParamRGB, ParamGroup, ParamPage
# gui
from buttleofx.gui.paramEditor.wrappers import IntWrapper, Int2DWrapper, Int3DWrapper, StringWrapper, BooleanWrapper, DoubleWrapper, Double2DWrapper, Double3DWrapper, ChoiceWrapper, PushButtonWrapper, RGBAWrapper, RGBWrapper, GroupWrapper, PageWrapper
#quickmamba
from quickmamba.models import QObjectListModel


class ParamEditorWrapper(QtCore.QObject):
    def __init__(self, parent, paramList):
        super(ParamEditorWrapper, self).__init__(parent)

        # the QObjectListModel
        self._paramElmts = QObjectListModel(self)

        # the map : correspondances between core params and wrapper params
        self.mapTypeToWrapper = {
            ParamInt: IntWrapper,
            ParamInt2D: Int2DWrapper,
            ParamInt3D: Int3DWrapper,
            ParamString: StringWrapper,
            ParamDouble: DoubleWrapper,
            ParamDouble2D: Double2DWrapper,
            ParamDouble3D: Double3DWrapper,
            ParamBoolean: BooleanWrapper,
            ParamChoice: ChoiceWrapper,
            ParamPushButton: PushButtonWrapper,
            ParamRGBA: RGBAWrapper,
            ParamRGB: RGBWrapper,
            ParamGroup: GroupWrapper,
            ParamPage: PageWrapper,
        }

        # the list of param wrappers
        self._paramListModel = [self.mapTypeToWrapper[paramElt.__class__](paramElt) for paramElt in paramList]

        # convert wrappers to qObject (for the listView)
        self._paramElmts.setObjectList(self._paramListModel)
        
    def getParamElts(self):
        """
            Returns the list of params, ready for QML (QObjectListModel)
        """
        return self._paramElmts